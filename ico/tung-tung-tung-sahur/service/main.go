package main

import (
	"context"
	"crypto/rand"
	_ "embed"
	"errors"
	"fmt"
	"html/template"
	"net/http"
	"os"
	"sync"
	"time"
)

//go:embed tmpl/base.html
var baseTemplate string

//go:embed tmpl/index.html
var indexTemplate string

//go:embed tmpl/sahur.html
var sahurTemplate string

//go:embed image.png
var tungImage []byte

type Tung struct {
	Tralalero []byte
	Tralala   []byte
}

var tungs = make(map[string][]Tung, 0)
var m = sync.RWMutex{}

var sahurs = make(map[string]*map[string]string)

const base32alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

func randText() string {
	src := make([]byte, 26)
	rand.Read(src)
	for i := range src {
		src[i] = base32alphabet[src[i]%32]
	}
	return string(src)
}

func (t *Tung) tung(wg *sync.WaitGroup) {
	defer wg.Done()
	for i := range t.Tralala {
		if t.Tralala[i] == 0x7b || t.Tralala[i] == 0x7d {
			t.Tralala[i] = 0x20
		}
	}
	for i := range t.Tralalero {
		if t.Tralalero[i] == 0x7b || t.Tralalero[i] == 0x7d {
			t.Tralalero[i] = 0x20
		}
	}
}

func tung_tung_tung_sahur() {
	for range time.Tick(time.Millisecond * 100) {
		m.Lock()

		// Tung tung tung
		var wg sync.WaitGroup
		for _, tung := range tungs {
			for _, tungtung := range tung {
				wg.Add(1)
				go tungtung.tung(&wg)
			}
		}
		wg.Wait()

		// Sahur
		for id, tung := range tungs {
			for _, tungtungtung := range tung {
				if sahur, ok := sahurs[id]; ok {
					(*sahur)[string(tungtungtung.Tralalero)] = string(tungtungtung.Tralala)
				}
			}
			tungs[id] = tungs[id][:0]
		}
		m.Unlock()
	}
}

func index(w http.ResponseWriter, r *http.Request) {
	cookie, err := r.Cookie("tungtungtung")
	if errors.Is(err, http.ErrNoCookie) {
		id := randText()
		cookie = &http.Cookie{
			Name:  "tungtungtung",
			Value: id,
		}
		m.Lock()
		tungs[id] = []Tung{}
		sahurs[id] = &map[string]string{}
		m.Unlock()
	}
	http.SetCookie(w, cookie)
	r.AddCookie(cookie)
	t := template.Must(template.New("foo").Parse(fmt.Sprintf(baseTemplate, indexTemplate)))
	t.Execute(w, r)
}

func tung(w http.ResponseWriter, r *http.Request) {
	id := r.Context().Value("id").(string)

	tung := Tung{}
	tung.Tralalero = []byte(r.FormValue("Tralalero"))
	tung.Tralala = []byte(r.FormValue("Tralala"))

	m.Lock()
	defer m.Unlock()
	tungs[id] = append(tungs[id], tung)
	http.Redirect(w, r, "/", http.StatusFound)
}

func sahur(w http.ResponseWriter, r *http.Request) {
	id := r.Context().Value("id").(string)

	m.RLock()
	defer m.RUnlock()

	sahur := sahurs[id]
	out := ""
	for k, v := range *sahur {
		out += fmt.Sprintf(`<tr><td>%s</td><td>%s</td></tr>`, k, v)
	}
	t := template.Must(template.New("foo").Parse(fmt.Sprintf(baseTemplate, fmt.Sprintf(sahurTemplate, out))))
	t.Execute(w, r)
}

func tung_tung(tung http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie("tungtungtung")
		if errors.Is(err, http.ErrNoCookie) {
			http.Redirect(w, r, "/", http.StatusFound)
			return
		}
		id := cookie.Value
		m.RLock()
		if _, ok := sahurs[id]; !ok {
			http.SetCookie(w, &http.Cookie{Name: "tungtungtung", Expires: time.Now()})
			http.Redirect(w, r, "/", http.StatusFound)
			m.RUnlock()
			return
		}
		m.RUnlock()

		secret := randText()
		ctx := context.WithValue(r.Context(), "id", id)
		ctx = context.WithValue(ctx, "tung", struct {
			Flag   func(string) string
			Secret string
		}{
			Secret: secret,
			Flag: func(s string) string {
				if s == secret {
					return fmt.Sprintf("Flag is %s", os.Getenv("FLAG"))
				}
				return "Tung tung tung sahur!"
			},
		})
		tung.ServeHTTP(w, r.WithContext(ctx))
	})
}

func main() {
	go tung_tung_tung_sahur()

	http.HandleFunc("/", index)
	http.Handle("/tung", tung_tung(http.HandlerFunc(tung)))
	http.Handle("/sahur", tung_tung(http.HandlerFunc(sahur)))
	http.HandleFunc("/tung.png", func(w http.ResponseWriter, r *http.Request) {
		w.Write(tungImage)
	})

	http.ListenAndServe(":8080", nil)
}

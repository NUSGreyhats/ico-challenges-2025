const errorMessage = document.getElementById("error-message");
const successMessage = document.getElementById("success-message");
const checkBtn = document.getElementById("check-btn");
const keyInput = document.getElementById("key-input");
const path = require("path");

var iv = "7729ae2cc35aabd4ca017a9edebc1fa8";
var key = "fc2c33ac5f4ad6989fb20fecb7dbd969461419d68d5248292142eb8821ca8749";
var ct = "623d6edb07f1b4d19ae7c2a5164bd720934a5614ccc0e42410c518f2d7fd3d26";

function hexToBytes(hex) {
  let bytes = [];
  for (let c = 0; c < hex.length; c += 2)
    bytes.push(parseInt(hex.substr(c, 2), 16));
  return bytes;
}

// Convert a byte array to a hex string
function bytesToHex(bytes) {
  let hex = [];
  for (let i = 0; i < bytes.length; i++) {
    let current = bytes[i] < 0 ? bytes[i] + 256 : bytes[i];
    hex.push((current >>> 4).toString(16));
    hex.push((current & 0xf).toString(16));
  }
  return hex.join("");
}

async function decryptAESCBC(encryptedHex, keyHex, ivHex) {
  const ciphertext = hexToUint8Array(encryptedHex);
  const key = hexToUint8Array(keyHex);
  const iv = hexToUint8Array(ivHex);

  const cryptoKey = await window.crypto.subtle.importKey(
    "raw", // format of key
    key, // must be a Uint8Array or ArrayBuffer
    { name: "AES-CBC" },
    false, // not extractable
    ["decrypt"] // allowed usage
  );

  const decryptedBuffer = await window.crypto.subtle.decrypt(
    { name: "AES-CBC", iv: iv },
    cryptoKey,
    ciphertext
  );

  return new TextDecoder().decode(decryptedBuffer);
}

function hexToUint8Array(hex) {
  if (hex.length % 2 !== 0) throw new Error("Invalid hex string");
  const bytes = new Uint8Array(hex.length / 2);
  for (let i = 0; i < hex.length; i += 2) {
    bytes[i / 2] = parseInt(hex.slice(i, i + 2), 16);
  }
  return bytes;
}

keyInput.addEventListener("input", function () {
  this.value = this.value.toUpperCase().replace(/[^A-Z0-9]/g, "");
  if (this.value.trim() === "") {
    checkBtn.disabled = true;
  } else {
    checkBtn.disabled = false;
  }
});

checkBtn.addEventListener("click", async () => {
  errorMessage.innerText = "No Error";
  errorMessage.style.visibility = "hidden";
  successMessage.innerText = "No Result";
  successMessage.style.visibility = "hidden";
  var curkey = keyInput.value.trim();
  if (curkey.length !== 64) {
    errorMessage.innerText = "Wrong Key!";
    errorMessage.style.visibility = "visible";
    setTimeout(() => {
      errorMessage.innerText = "No text";
      errorMessage.style.visibility = "hidden";
    }, 3000);
  } else {
    try {
      var keybytes = hexToBytes(curkey);
      var mykeybytes = hexToBytes(key);
      for (var i = 0; i < 32; i++) {
        if ((keybytes[i] ^ mykeybytes[i]) !== 69) {
          errorMessage.innerText = "Wrong Key!";
          errorMessage.style.visibility = "visible";
          setTimeout(() => {
            errorMessage.innerText = "No text";
            errorMessage.style.visibility = "hidden";
          }, 3000);
          return;
        }
      }
      var newkey = bytesToHex(keybytes);
      decryptAESCBC(ct, newkey, iv)
        .then((pt) => {
          successMessage.innerText = pt;
          successMessage.style.visibility = "visible";
        })
        .catch((err) => {
          errorMessage.innerText = err;
          errorMessage.style.visibility = "visible";
        });
    } catch (error) {
      // errorMessage.innerText = "Wrong Key!";
      errorMessage.innerText = error;
      errorMessage.style.visibility = "visible";
      setTimeout(() => {
        errorMessage.innerText = "No text";
        errorMessage.style.visibility = "hidden";
      }, 3000);
    }
  }
});

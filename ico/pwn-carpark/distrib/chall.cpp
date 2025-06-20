// g++ -g -no-pie chall.cpp -o chall
#include <stdio.h>
#include <vector>

using namespace std;
using ll = long long;

#define CARPARK1_SPACE 10
#define CARPARK2_SPACE 20

void setup(){
    setvbuf(stdout, NULL, _IONBF, 0);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
}

struct Carparks {
    ll carpark1[CARPARK1_SPACE];
    vector<ll> carpark2 = vector<ll>(CARPARK2_SPACE, 0); 
};

int main() {
    setup();
    Carparks cp;
    ll* carpark1 = cp.carpark1;
    vector<ll>& carpark2 = cp.carpark2;
    for (int i = 0; i < CARPARK1_SPACE; i++) {
        carpark1[i] = 0;
    }
    int choice;
    while (true) {
        puts("1. Change carpark1 car");
        puts("2. View carpark1 car");
        puts("3. Change carpark2 car");
        puts("4. View carpark2 car");
        printf("> ");
        scanf("%d", &choice);
        if (choice < 1 || choice > 4) {
            puts("Invalid option!");
            continue;
        }
        int slot;
        puts("Which car?");
        printf("> ");
        scanf("%d", &slot);
        if (choice == 1) {
            if (slot < 0 || slot > CARPARK1_SPACE) {
                puts("Invalid slot!");
                continue;
            }
            ll newval;
            printf("New value > ");
            scanf("%lld", &newval);
            carpark1[slot] = newval;
        } else if (choice == 2) {
            if (slot < 0 || slot > CARPARK1_SPACE) {
                puts("Invalid slot!");
                continue;
            }
            printf("Value of car %d is %lld\n", slot, carpark1[slot]);
        } else if (choice == 3) {
            if (slot < 0 || slot > CARPARK2_SPACE) {
                puts("Invalid slot!");
                continue;
            }
            ll newval;
            printf("New value > ");
            scanf("%lld", &newval);
            carpark2[slot] = newval;
        } else {
            if (slot < 0 || slot > CARPARK2_SPACE) {
                puts("Invalid slot!");
                continue;
            }
            printf("Value of car %d is %lld\n", slot, carpark2[slot]);
        }
    }
}
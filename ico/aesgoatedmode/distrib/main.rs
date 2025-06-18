use aes_gcm::{Aes128Gcm, KeyInit, Nonce};
use aes_gcm::aead::{AeadInPlace, OsRng};
use rand::RngCore;
use std::io::{self, Write};

fn main() {
    // Generate a random AES-128 key (16 bytes)
    let key = Aes128Gcm::generate_key(&mut OsRng);
    let cipher = Aes128Gcm::new(&key);

    println!("AES GOATED MODE Encryption/Decryption");
                    
    let mut buffer = b"ICO{flaghere}".to_vec();
    let mut nonce_bytes = [0u8; 12];
    OsRng.fill_bytes(&mut nonce_bytes);
    let nonce = Nonce::from_slice(&nonce_bytes);
    cipher.encrypt_in_place(nonce, b"", &mut buffer);

    println!("Encrypted flag (hex): {}", hex::encode(&buffer));
    println!("Nonce (hex): {}\n", hex::encode(&nonce_bytes));

    loop {
        print!("Would you like to (e)ncrypt or (d)ecrypt?\n");
        io::stdout().flush().unwrap();


        let mut choice = String::new();
        io::stdin().read_line(&mut choice).unwrap();
        let choice = choice.trim().to_lowercase();

        if choice == "exit" {
            break;
        } else if choice == "e" {
            // === Encrypt Mode ===
            print!("Enter message to encrypt: ");
            io::stdout().flush().unwrap();

            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            let input = input.trim();

            let mut buffer = input.as_bytes().to_vec();

            // Generate random 96-bit nonce
            let mut nonce_bytes = [0u8; 12];
            OsRng.fill_bytes(&mut nonce_bytes);
            let nonce = Nonce::from_slice(&nonce_bytes);

            cipher.encrypt_in_place(nonce, b"", &mut buffer);

            println!("Encrypted (hex): {}", hex::encode(&buffer));
            println!("Nonce (hex): {}\n", hex::encode(&nonce_bytes));

        } else if choice == "d" {
            // === Decrypt Mode ===
            print!("Enter ciphertext (hex): ");
            io::stdout().flush().unwrap();

            let mut ciphertext_hex = String::new();
            io::stdin().read_line(&mut ciphertext_hex).unwrap();
            let ciphertext_hex = ciphertext_hex.trim();

            let mut ciphertext = match hex::decode(ciphertext_hex) {
                Ok(c) => c,
                Err(_) => {
                    println!("Invalid hex input.\n");
                    continue;
                }
            };

            print!("Enter nonce (hex): ");
            io::stdout().flush().unwrap();

            let mut nonce_hex = String::new();
            io::stdin().read_line(&mut nonce_hex).unwrap();
            let nonce_hex = nonce_hex.trim();

            let nonce_bytes = match hex::decode(nonce_hex) {
                Ok(n) if n.len() == 12 => n,
                _ => {
                    println!("Invalid nonce. Must be 12 bytes in hex.\n");
                    continue;
                }
            };

            let nonce = Nonce::from_slice(&nonce_bytes);

            cipher.decrypt_in_place(nonce, b"", &mut ciphertext);
            if String::from_utf8_lossy(&ciphertext).contains("{") || String::from_utf8_lossy(&ciphertext).contains("}") {
                println!("Hehe nice try buddy :>");
                continue;
            }
            println!("Decrypted message (hex): {}\n", hex::encode(&ciphertext));
        } else {
            println!("Invalid choice. Please enter 'e' or 'd'.\n");
        }
    }

    println!("Bye Bye! Hope the goated mode was goated enough for you :)");
}

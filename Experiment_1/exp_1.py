def caesar_encrypt(text, shift):
    result = ""

    for char in text:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            position = (ord(char) - base + shift) % 26
            result += chr(position + base)
        else:
            result += char

    return result


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0

    for char in text:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            shift = ord(key[key_index % len(key)]) - ord('a')
            position = (ord(char) - base + shift) % 26

            result += chr(position + base)
            key_index += 1
        else:
            result += char

    return result


def vigenere_decrypt(text, key):
    result = ""
    key = key.lower()
    key_index = 0

    for char in text:
        if char.isalpha():
            if char.isupper():
                base = ord('A')
            else:
                base = ord('a')

            shift = ord(key[key_index % len(key)]) - ord('a')
            position = (ord(char) - base - shift) % 26

            result += chr(position + base)
            key_index += 1
        else:
            result += char

    return result

while True:

    print("\n===== Classical Cipher Program =====")
    print("1. Caesar Cipher")
    print("2. Vigenere Cipher")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        text = input("Enter plaintext: ")
        shift = int(input("Enter shift: "))

        encrypted = caesar_encrypt(text, shift)
        decrypted = caesar_decrypt(encrypted, shift)

        print("\nEncrypted:", encrypted)
        print("Decrypted:", decrypted)
        print("Verification:", decrypted == text)

    elif choice == "2":

        text = input("Enter plaintext: ")
        key = input("Enter key: ")

        encrypted = vigenere_encrypt(text, key)
        decrypted = vigenere_decrypt(encrypted, key)

        print("\nEncrypted:", encrypted)
        print("Decrypted:", decrypted)
        print("Verification:", decrypted == text)

    elif choice == "3":
        print("Program terminated.")
        break

    else:
        print("Invalid choice.")

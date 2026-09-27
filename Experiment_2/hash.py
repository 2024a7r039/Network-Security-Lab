import hashlib


def generate_hash(data):
    return hashlib.sha256(data).hexdigest()


def text_hash():
    text = input("Enter text: ")
    digest = generate_hash(text.encode())

    print("SHA-256:", digest)


def file_hash():
    path = input("Enter file path: ")

    try:
        with open(path, "rb") as file:
            content = file.read()

        print("File content:")
        print(content.decode("utf-8"))

        print("\nSHA-256:", generate_hash(content))

    except FileNotFoundError:
        print("File not found.")


def append_text():
    path = input("Enter file path: ")

    try:
        with open(path, "rb") as file:
            original = file.read()

        original_hash = generate_hash(original)

        print("\nOriginal content:")
        print(original.decode("utf-8"))

        print("\nOriginal SHA-256:")
        print(original_hash)

        extra = input("\nEnter text to append: ")

        with open(path, "a", encoding="utf-8") as file:
            file.write(extra)

        with open(path, "rb") as file:
            modified = file.read()

        modified_hash = generate_hash(modified)

        print("\nModified content:")
        print(modified.decode("utf-8"))

        print("\nModified SHA-256:")
        print(modified_hash)

        if original_hash != modified_hash:
            print("\nIntegrity Status: MODIFIED")
        else:
            print("\nIntegrity Status: UNCHANGED")

    except FileNotFoundError:
        print("File not found.")


while True:

    print("\n========== SHA-256 MENU ==========")
    print("1. Hash Text")
    print("2. Hash File")
    print("3. Append Text to File")
    print("4. Exit")
    print("==================================")

    choice = input("Enter choice: ")

    if choice == "1":
        text_hash()

    elif choice == "2":
        file_hash()

    elif choice == "3":
        append_text()

    elif choice == "4":
        print("Exiting program...")
        break

    else:
        print("Invalid choice.")

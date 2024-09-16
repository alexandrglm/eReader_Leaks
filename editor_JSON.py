import json
import os

def load_library_from_json(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return []

def save_library_to_json(library, json_file):
    with open(json_file, 'w') as f:
        json.dump(library, f, indent=4)

def edit_book(book):
    print("\nEditing book:")
    for key, value in book.items():
        print(f"{key.capitalize()}: {value}")
        new_value = input(f"NEW {key} ?: ").strip()
        if new_value:
            book[key] = new_value

def main():
    json_file = 'library.json'

    library = load_library_from_json(json_file)

    if not library:
        print(f"There's no books {json_file}.")
        return

    for index, book in enumerate(library, 1):
        print(f"\nBOOK {index} from {len(library)}")
        edit_book(book)

        continue_editing = input("\nContinue? (y/n): ").strip().lower()
        if continue_editing != 'y':
            break

    save_library_to_json(library, json_file)
    print(f"\nCambios guardados en {json_file}.")

if __name__ == '__main__':
    main()


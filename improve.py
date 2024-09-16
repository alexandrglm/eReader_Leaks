import json
import os
import shutil

def load_library_from_json(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return []

def save_library_to_json(library, json_file):
    with open(json_file, 'w') as f:
        json.dump(library, f, indent=4)

def edit_book_info(book):
    print("\nEditando libro:", book['title'])
    book['title'] = input(f"Título [{book['title']}]: ").strip() or book['title']
    book['author'] = input(f"Autor [{book['author']}]: ").strip() or book['author']
    book['publisher'] = input(f"Editorial [{book['publisher']}]: ").strip() or book['publisher']
    book['description'] = input(f"Descripción [{book['description']}]: ").strip() or book['description']
    book['language'] = input(f"Idioma [{book['language']}]: ").strip() or book['language']

def update_cover_image(book, cover_folder):
    cover_path = input(f"Ruta de la nueva portada (dejar en blanco para mantener [{book['cover']}]): ").strip()

    if cover_path and os.path.isfile(cover_path):
        new_filename = f"{book['author']}_{book['title'].replace(' ', '_')}_cover.jpg"
        new_cover_path = os.path.join(cover_folder, new_filename)

        try:
            shutil.copy(cover_path, new_cover_path)
            print(f"Nueva portada copiada a {new_cover_path}")
            book['cover'] = os.path.join('./files/', new_filename)
        except Exception as e:
            print(f"Error al copiar la portada: {e}")
    else:
        print("No se actualizó la portada.")

def regenerate_html(library, output_file):
    with open(output_file, 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Library</title>\n')
        f.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')
        f.write('<style>\n')
        f.write('body { font-family: "Georgia", serif; margin: 20px; }\n')
        f.write('table { width: 100%; border-collapse: collapse; margin-top: 20px; }\n')
        f.write('th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }\n')
        f.write('th { background-color: #f2f2f2; }\n')
        f.write('tr:nth-child(even) { background-color: #f9f9f9; }\n')
        f.write('img { width: 100px; height: auto; }\n')
        f.write('</style>\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Books in My Library</h1>\n')

        f.write('<table>\n')
        f.write('<tr>\n')
        f.write('<th>Cover</th>\n')
        f.write('<th>Title</th>\n')
        f.write('<th>Author</th>\n')
        f.write('<th>Publisher</th>\n')
        f.write('<th>Description</th>\n')
        f.write('<th>Language</th>\n')
        f.write('</tr>\n')

        for book in library:
            f.write('<tr>\n')
            cover_img = book['cover']
            f.write(f'<td><img src="{cover_img}" alt="Cover"></td>\n')
            f.write(f'<td>{book["title"]}</td>\n')
            f.write(f'<td>{book["author"]}</td>\n')
            f.write(f'<td>{book["publisher"]}</td>\n')
            f.write(f'<td>{book["description"]}</td>\n')
            f.write(f'<td>{book["language"]}</td>\n')
            f.write('</tr>\n')

        f.write('</table>\n')
        f.write('</body>\n</html>\n')

def main():
    json_file = 'library.json'
    cover_folder = './files/'
    output_file = 'library.html'

    library = load_library_from_json(json_file)

    if not library:
        print(f"No se encontró el archivo JSON ({json_file}) o está vacío.")
        return

    while True:
        print("\n--- Libros en la Biblioteca ---")
        for idx, book in enumerate(library):
            print(f"{idx + 1}. {book['title']} - {book['author']}")

        choice = input("\nElige un libro para editar (0 para salir): ").strip()

        if choice == '0':
            break

        if choice.isdigit() and 1 <= int(choice) <= len(library):
            selected_book = library[int(choice) - 1]
            edit_book_info(selected_book)
            update_cover_image(selected_book, cover_folder)
        else:
            print("Opción inválida. Intenta nuevamente.")

    save_library_to_json(library, json_file)

    regenerate_html(library, output_file)
    print(f"HTML actualizado: {output_file}")

if __name__ == '__main__':
    main()

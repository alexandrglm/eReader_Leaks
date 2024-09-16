import os
import json
import shutil
import re

def copy_cover_image(src_path, dest_folder, new_filename):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_path = os.path.join(dest_folder, new_filename)
    try:
        shutil.copy(src_path, dest_path)
        print(f"Copied cover image to: {dest_path}")
    except Exception as e:
        print(f"Error copying cover image: {e}")
    return dest_path

def generate_html(library, output_file):
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
        f.write('<h1>Books already read on my eReader</h1>\n')

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
            cover_img = book['cover'].replace("file://", "")
            f.write(f'<td><img src="{cover_img}" alt="Cover"></td>\n')
            f.write(f'<td>{book["title"]}</td>\n')
            f.write(f'<td>{book["author"]}</td>\n')
            f.write(f'<td>{book["publisher"]}</td>\n')
            f.write(f'<td>{book["description"]}</td>\n')
            f.write(f'<td>{book["language"]}</td>\n')
            f.write('</tr>\n')

        f.write('</table>\n')
        f.write('</body>\n</html>\n')

def save_library_to_json(library, json_file):
    with open(json_file, 'w') as f:
        json.dump(library, f, indent=4)

def load_library_from_json(json_file):
    if not os.path.isfile(json_file):
        return []

    with open(json_file, 'r') as f:
        return json.load(f)

def main():
    json_file = 'library.json'
    cover_folder = './files/'
    output_file = 'library.html'
    library = []

    if os.path.isfile(json_file):
        print(f"Archivo JSON encontrado: {json_file}")
        library = load_library_from_json(json_file)

        for i, book in enumerate(library):
            cover_path = book.get('cover', '')
            if cover_path and cover_path.startswith('file://'):
                cover_path = cover_path[7:]
                new_filename = f"{book['title']}_{book['author'].replace(' ', '_')}_{i+1}_cover.jpg"
                new_path = copy_cover_image(cover_path, cover_folder, new_filename)
                book['cover'] = os.path.join(cover_folder, new_filename)

        generate_html(library, output_file)
        print(f'HTML generated: {output_file}')
    else:
        base_path = input("PATH for ./Calibre: ").strip()

        if not os.path.isdir(base_path):
            raise FileNotFoundError(f"PATH {base_path} not valid.")

        for author_folder in os.listdir(base_path):
            author_path = os.path.join(base_path, author_folder)
            if os.path.isdir(author_path):
                for title_folder in os.listdir(author_path):
                    title_path = os.path.join(author_path, title_folder)
                    if os.path.isdir(title_path):
                        metadata_opf_path = os.path.join(title_path, 'metadata.opf')
                        cover_path = os.path.join(title_path, 'cover.jpg')

                        if os.path.isfile(metadata_opf_path):
                            book_metadata = parse_metadata_opf(metadata_opf_path)
                            if os.path.isfile(cover_path):
                                new_filename = f"{author_folder}_{title_folder.split('(')[0].strip()}_cover.jpg"
                                book_metadata['cover'] = copy_cover_image(cover_path, cover_folder, new_filename)
                            else:
                                book_metadata['cover'] = '' 
                            book_metadata['author'] = author_folder
                            book_metadata['title'] = title_folder.split('(')[0].strip() 
                            library.append(book_metadata)

        save_library_to_json(library, json_file)
        generate_html(library, output_file)
        print(f'Archivo JSON generado exitosamente: {json_file}')
        print(f'Archivo HTML generado exitosamente: {output_file}')

if __name__ == '__main__':
    main()

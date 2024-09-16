import os
import json
import shutil

def copy_cover_image(src_path, dest_folder, new_filename):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    dest_path = os.path.join(dest_folder, new_filename)

    try:
        shutil.copy(src_path, dest_path)
        print(f"File copied: {src_path} -> {dest_path}")
    except Exception as e:
        print(f"Error copying cover from {src_path} to {dest_path}: {e}")

    return dest_path

def generate_html(library, output_file):
    with open(output_file, 'w') as f:
        f.write('<!DOCTYPE html>\n<html>\n<head>\n<title>Library</title>\n')
        f.write('<link rel="stylesheet" type="text/css" href="styles.css">\n')
        f.write('<link rel="icon" href="./files/exlibris.svg" type="image/svg+xml">\n')
        f.write('<style>\n')
        f.write('body { font-family: "Georgia", serif; margin: 20px; background: url("./files/exlibris3.png") no-repeat center center fixed; background-size: cover; }\n')
        f.write('table { width: 100%; border-collapse: collapse; margin-top: 20px; }\n')
        f.write('th, td { padding: 10px; text-align: left; border: 1px solid #ddd; }\n')
        f.write('th { background-color: #f2f2f2; }\n')
        f.write('tr:nth-child(even) { background-color: #f9f9f9; }\n')
        f.write('img.cover-img { width: 100px; height: auto; }\n')
        f.write('img.logo { width: 150px; height: auto; margin: 20px; }\n')
        f.write('</style>\n')
        f.write('</head>\n<body>\n')
        f.write('<h1>Books that have already been ex-libris</h1>\n')

        f.write('<div>\n')
        f.write('<h2>Stamps:</h2>\n')
        f.write('<img src="./files/exlibris.svg" class="logo" alt="Logo">\n')
        f.write('<img src="./files/exlibris.png" class="logo" alt="Background Image">\n')
        f.write('</div>\n')

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
            f.write(f'<td><img src="{cover_img}" class="cover-img" alt="Cover"></td>\n')
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

def parse_metadata_opf(metadata_opf_path):
    return {
        'title': 'Unknown Title',
        'author': 'Unknown Author',
        'publisher': 'Unknown Publisher',
        'description': 'No description available',
        'language': 'Unknown Language',
    }

def load_library_from_json(json_file):
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            return json.load(f)
    return None

def find_and_copy_covers(base_path, cover_folder):
    library = []

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
                            new_cover_path = copy_cover_image(cover_path, cover_folder, new_filename)
                            book_metadata['cover'] = os.path.join('./files/', new_filename)
                        else:
                            print(f"No cover found for {title_folder} in {author_folder}")
                            book_metadata['cover'] = ''

                        book_metadata['author'] = author_folder
                        book_metadata['title'] = title_folder.split('(')[0].strip()
                        library.append(book_metadata)

    return library

def main():
    json_file = 'library.json'
    cover_folder = './files/'
    output_file = 'library.html'

    library = load_library_from_json(json_file)

    if library is None:
        base_path = input("PATH for ./Calibre ?: ").strip()

        if not os.path.isdir(base_path):
            print(f"PATH ({base_path}) is not valid.")
            return

        library = find_and_copy_covers(base_path, cover_folder)

        save_library_to_json(library, json_file)
        print(f'JSON file generated: {json_file}')
    else:
        print(f'Previous .JSON found: {json_file}, using it.')

    generate_html(library, output_file)
    print(f'HTML generated: {output_file}')

if __name__ == '__main__':
    main()

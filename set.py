from bs4 import BeautifulSoup

def improve_library_html(input_html, output_html):
    with open(input_html, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "Library set:"

    style_tag = soup.new_tag('style')
    style_tag.string = """
    body {
        font-family: 'Century Schoolbook', serif;
        margin: 20px;
        background-color: #f4f4f4;
    }
    @font-face {
        font-family: 'Century Schoolbook';
        src: url('./files/CS.ttf') format('truetype');
    }
    table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 20px;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    th, td {
        padding: 12px;
        text-align: left;
        border-bottom: 1px solid #ddd;
    }
    th {
        background-color: #333;
        color: white;
        cursor: pointer;
    }
    th.sortable:hover {
        background-color: #555;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    img {
        width: 100px;
        height: auto;
        border-radius: 5px;
    }
    #carousel {
        width: 300px;
        margin: 20px auto;
        position: relative;
        padding: 20px;
        background: url('./files/ereader.png') no-repeat center center;
        background-size: cover;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
    }
    .carousel-images {
        width: 100%;
        height: 400px;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.15);
    }
    .carousel-images img {
        width: 100%;
        height: auto;
        display: none;
        transition: opacity 0.5s ease-in-out;
        opacity: 0;
    }
    .carousel-images img.active {
        display: block;
        opacity: 1;
    }
    #prev, #next {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        border: none;
        padding: 10px;
        cursor: pointer;
        border-radius: 5px;
    }
    #prev { left: 0; }
    #next { right: 0; }
    .back-link {
        display: block;
        margin: 20px auto;
        text-align: center;
        font-size: 18px;
        font-weight: bold;
    }
    .back-link a {
        text-decoration: none;
        color: #333;
        padding: 10px 20px;
        border: 2px solid #333;
        border-radius: 5px;
        transition: background-color 0.3s, color 0.3s;
    }
    .back-link a:hover {
        background-color: #333;
        color: white;
    }
    .carousel-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-top: 10px;
    }
    """

    if not soup.style:
        soup.head.append(style_tag)
    else:
        soup.head.style.string = style_tag.string

    carousel_div = soup.new_tag('div', id='carousel')

    carousel_images_div = soup.new_tag('div', **{'class': 'carousel-images'})
    for img_tag in soup.find_all('img'):
        carousel_img = soup.new_tag('img', src=img_tag['src'])
        carousel_images_div.append(carousel_img)

    carousel_div.append(carousel_images_div)

    prev_button = soup.new_tag('button', id='prev')
    prev_button.string = "Prev."
    next_button = soup.new_tag('button', id='next')
    next_button.string = "Next"

    carousel_div.append(prev_button)
    carousel_div.append(next_button)

    carousel_title = soup.new_tag('div', **{'class': 'carousel-title'})
    carousel_title.string = "exlibris-alexandr"

    soup.body.insert(0, carousel_title)
    soup.body.insert(0, carousel_div)

    back_link_div = soup.new_tag('div', **{'class': 'back-link'})
    back_link = soup.new_tag('a', href='./exlibris.html')
    back_link.string = "Exlibris Editor"
    back_link_div.append(back_link)

    soup.body.append(back_link_div)

    script_tag = soup.new_tag('script')
    script_tag.string = """
    var currentIndex = 0;
    var images = document.querySelectorAll('.carousel-images img');
    images[currentIndex].classList.add('active');

    function showNextImage() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('active');
    }

    function showPrevImage() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        images[currentIndex].classList.add('active');
    }

    document.getElementById('next').addEventListener('click', showNextImage);
    document.getElementById('prev').addEventListener('click', showPrevImage);

    setInterval(showNextImage, 750);

    document.querySelectorAll('th.sortable').forEach(function(header) {
        header.addEventListener('click', function() {
            var table = header.closest('table');
            var tbody = table.querySelector('tbody');
            var rows = Array.from(tbody.querySelectorAll('tr'));
            var index = Array.from(header.parentNode.children).indexOf(header);
            var isAscending = header.classList.contains('asc');

            rows.sort(function(a, b) {
                var aText = a.children[index].innerText;
                var bText = b.children[index].innerText;
                if (isNaN(aText) || isNaN(bText)) {
                    return aText.localeCompare(bText);
                } else {
                    return aText - bText;
                }
            });

            if (isAscending) {
                rows.reverse();
                header.classList.remove('asc');
            } else {
                header.classList.add('asc');
            }

            tbody.innerHTML = '';
            rows.forEach(function(row) {
                tbody.appendChild(row);
            });
        });
    });
    """
    soup.body.append(script_tag)

    with open(output_html, 'w') as file:
        file.write(soup.prettify())

def main():
    input_html = 'library.html'
    output_html = 'Library_set.html'
    improve_library_html(input_html, output_html)
    print(f'Library-set html created: {output_html}')

if __name__ == '__main__':
    main()

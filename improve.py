from bs4 import BeautifulSoup

def improve_library_html(input_html, output_html):
    with open(input_html, 'r') as file:
        soup = BeautifulSoup(file, 'html.parser')

    title_tag = soup.find('title')
    if title_tag:
        title_tag.string = "Enhanced Library with Carousel"

    style_tag = soup.new_tag('style')
    style_tag.string = """
    body {
        font-family: 'Arial', sans-serif;
        margin: 20px;
        background-color: #f4f4f4;
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
    }
    .carousel-images {
        width: 100%;
        height: 400px;
        overflow: hidden;
    }
    .carousel-images img {
        width: 100%;
        height: auto;
        display: none;
    }
    .carousel-images img.active {
        display: block;
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
    prev_button.string = "Anterior"
    next_button = soup.new_tag('button', id='next')
    next_button.string = "Siguiente"

    carousel_div.append(prev_button)
    carousel_div.append(next_button)

    soup.body.insert(0, carousel_div)

    script_tag = soup.new_tag('script')
    script_tag.string = """
    var currentIndex = 0;
    var images = document.querySelectorAll('.carousel-images img');
    images[currentIndex].classList.add('active');

    document.getElementById('next').addEventListener('click', function() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex + 1) % images.length;
        images[currentIndex].classList.add('active');
    });

    document.getElementById('prev').addEventListener('click', function() {
        images[currentIndex].classList.remove('active');
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        images[currentIndex].classList.add('active');
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

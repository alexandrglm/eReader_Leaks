import pdfkit

def convert_html_to_pdf(html_file, pdf_file):
    options = {
        'no-outline': None,
        'enable-local-file-access': None
    }
    try:
        pdfkit.from_file(html_file, pdf_file, options=options)
        print(f"PDF generated: {pdf_file}")
    except Exception as e:
        print(f"Error generating PDF: {e}")

if __name__ == '__main__':
    html_file = 'library.html'
    pdf_file = 'library.pdf'
    convert_html_to_pdf(html_file, pdf_file)

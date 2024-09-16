# eReader exlibris v0.1
## Exlibris generator using Calibre database, of some books that were in my eReader.
![exlibrisVerde](https://github.com/user-attachments/assets/f6e18520-2b2b-4932-bb70-26d0b7cb8540)

## REQUIREMENTS

 - Python 3.x
```
$ pip install pdfkit bs4
```

## TYPICAL USAGE
```
$ python librero.py && python set.py && python exlibris.py
```
1st: Generate library.html / Library-set.html / exlibris.html
2nd: Visualize them on a browser.


### Generate HTML libraries:
```
$ python librero.py # Generates and/or ./library.html
$ python set.py # Generates and/or updates ./Library-set.html
```
### Create an Exlibris PDF list:
```
$ python pdf.py # Generates a PDF with all exlibris data
```
### Create an Exlibris :
```
$ python exlibris.py # Generates and/or updates ./exlibris.html
```
### Edit the JSON:
```
$ python editor_JSON.py # Can edit every JSON line / data
```
### Edit the JSON via HTML interface:
```
$ open ./editor.html # An HTML JSON editor.
```

## Files generated:

1. ./library.html - Basic exlibris list.
2. ./Library-set.html - Advanced exlibris management.
3. ./Library.pdf - PDF with a full data output.

4. ./exlibris.html - SVG/PNG Editor, Exlibris logo creator app.

5. ./library.json - A JSON list with all your exlibris data.
6. ./files/* - Every book cover.


https://github.com/user-attachments/assets/8f34f6dc-960e-4b42-a626-1107a374f60f



_(Development in progress)_


2024 September, 16th.

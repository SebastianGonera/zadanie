
def read_file():
    try:
        with open("tresc_artykulu.txt", 'r', encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("ERROR: Nie odnaleziono pliku tresc_artykulu.txt")
    except Exception:
        print("ERROR: Nieoczekiwany błąd")

def add_to_html(article):
    try:
        with open("szablon.html", 'r') as f:
            html = f.read()
            result = f'{html}\n{article}\n\t</div>\n</body>\n</html>'
            with open("podglad.html", 'w', encoding="utf-8") as f_html:
                f_html.write(result)
    except FileNotFoundError:
        print("ERROR: Nie odnaleziono pliku szablon.html")
    except Exception:
        print("ERROR: Nieoczekiwany błąd")

if __name__ == '__main__':
    artcile = read_file()
    print(artcile)
    add_to_html(artcile)


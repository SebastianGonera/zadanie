import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI


def read_file():
    """
    Funckja odczytuje plik tresc_artykulu.txt i zwraca jego zawartość.
    W przypadku pojawenia się bełdu zostanie wyśwetlony w kosoli dopowedni komunikat.
    :return: string
    """
    try:
        with open("tresc_artykulu.txt", 'r', encoding="utf-8") as f:
            return f.read()

    except FileNotFoundError:
        print("ERROR: Nie odnaleziono pliku tresc_artykulu.txt")

    except Exception as error:
        print(f'ERROR: {error}')


def generate_html():
    """
    Wysyła zapytanie do OpenAI. Nastepnie zawartośc odpowiedzi przekazuje do funkcji add_to_html.
    :return:
    """
    try:
        article = read_file()
        api_key = os.getenv("API_KEY")

        messages = (f'Wygeneruj kod HTML bez CSS i JavaScript. Pomiń tagi: <html>, <head>, <body>.'
                    f' Ustaw nagłówki za pomocą taga <h2> a pozostałe fragmenty tekstu umieść w tagu p. Ostatnią linię tesktu umieść w tagu <p><i>.'
                    f'Zaprponuj miejsca gdzei można umieścić zdjęcie za pomoca znacznika <img>. Dla atrybutu src dodaj następujący tekst'
                    f'"""image_placeholder.jpg""", dodaj również atrybut alt. Tekst: """{article}""" ')

        client = OpenAI(
            api_key=api_key,
        )

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": messages
                        }],
                }
            ],
            max_tokens=1100,
            temperature=0.2
        )

        response_message = response.choices[0].message.content
        add_to_html(response_message)

    except Exception as error:
        print(f'ERROR: {error}')

def add_to_html(article):
    """
    Funckja odczytuje plik szablon.html. Następnie dodaje do niego tekst z parametrem article.
    Zmodyfkiowaną zawartość zapsiuje w pliku podglad.html.
    """
    try:
        with (open("szablon.html", 'r') as f):
            html = BeautifulSoup(f, 'html.parser')
            div_container = html.find('div', class_='container')

            if div_container:
                text = article + "\n"
                div_container.append(BeautifulSoup(text, 'html.parser'))
            else:
                raise ValueError("Nie znaleziono elementu <div class='container'>.")

            with open("podglad.html", 'w', encoding="utf-8") as f_html:
                f_html.write(str(html))
                print("Utworzono plik 'podglad.html'.")

    except FileNotFoundError:
        print("ERROR: Nie odnaleziono pliku szablon.html")

    except ValueError as e:
        print(f"Błąd: {e}")

    except Exception as error:
        print(f'ERROR: {error}')

if __name__ == '__main__':
    load_dotenv()
    generate_html()
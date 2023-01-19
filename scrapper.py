from random import choice
from csv import DictReader
import requests
from bs4 import BeautifulSoup




BASE_URL = "http://quotes.toscrape.com/"

def read_quotes(filename):
    with open(filename, "r") as file:
        csv_reader = DictReader(file)
        return list(csv_reader)



def start_game(quotes):

    quote = choice(quotes)
    remaining_guesses = 4

    print("Here's a quote: ")
    print(quote["text"])
    print(quote["author"])
    guess = " "
    while guess.lower() != quote["author"].lower():
        guess = input(f"Who said this quote? Guesses remaining: {remaining_guesses}\n ")
        if guess.lower() == quote["author"].lower():
            print("YOU GOT IT RIGHT!")
            break
        remaining_guesses -= 1

        print_hint(quote, remaining_guesses)
       

    again = " "
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again? (y/n)\n")
        if again.lower() in ('yes', 'y'):
            print("Okay let's play again!")
            return start_game(quotes)
        else:
            print("Ok, Goodbye!")

def print_hint(quote, remaining_guesses):
    if remaining_guesses == 3:
        res = requests.get(f"{BASE_URL}{quote['bio-link']}")
        soup = BeautifulSoup(res.text, "html.parser")
        birth_date = soup.find(class_="author-born-date").get_text()
        birth_place = soup.find(class_="author-born-location").get_text()
        print(f"Here's a hint: The author was born on {birth_date} {birth_place}")
    elif remaining_guesses == 2:
        first_initial = quote["author"][0]
        print(f"Heres a hint : The author's first name starts with a {first_initial}")
    elif remaining_guesses == 1:
        last_initial = quote["author"].split(" ")[1][0]
        print(f"Heres a hint : The author's last name starts with a {last_initial}")
    else:
        print(f"Sorry you ran out of guesses. The answer was {quote['author']}")
            
quotes = read_quotes("quotes.csv")
start_game(quotes)
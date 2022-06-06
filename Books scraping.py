#! /usr/bin/python3
import sqlite3
import requests
from bs4 import BeautifulSoup

foo= sqlite3.connect("Books_Scrapper.db")
conn = foo.cursor()

# conn.execute('''create table Records(
#                  BookTitle varchar(50),
#                  BookPrice Varchar(50),
#                  Availability Varchar(50),
#                  Rating Varchar(50))
#            ''')


class Book:
    def __init__(self, name, price, avail, rating):
        self.name = name
        self.price = price
        self.availability = avail
        self.rating = "three"

    
    def add_to_database(self):
        "this is used to add the books into a database of books and the code goes here"
        # create database
        conn.execute('''insert into Records VALUES(?,?,?,?)''', (self.name, self.price, self.rating, self.availability,))

        foo.commit()
        print("--[+] adding '%s' to database" % self.name)


def scrape_data(book):
    """ This will be used to populate the books object after extraction """
    book_title = book.find("a").find("img").get("alt").strip()
    price = book.find("p", class_="price_color").text.strip()
    avail_ = book.find("p", class_="instock availability").text.strip()
    rating = book.find("i", class_="icon-star")
    
    bk = Book(book_title, price, avail_, rating)
    bk.add_to_database()


def main():
    """ Loop through the pages and get the books """    
    for index in range(1, 51):
        URL = "http://books.toscrape.com/catalogue/page-%s.html" % index
        page = requests.get(URL, allow_redirects=False, verify=False)
        soup = BeautifulSoup(page.content, "html.parser")
        lists = soup.find_all("article", class_="product_pod")
    
        for book in lists:
            scrape_data(book)


if __name__ == "__main__":
    main()

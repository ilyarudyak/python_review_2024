import requests, bs4
from collections import defaultdict

class BookScraper:
    """
    A class to scrape books from a website https://books.toscrape.com/.

    Exercise: 
    Scrape Book Information from an Online Bookstore
    
    Objective:
    Write a Python script that scrapes book information from an online bookstore's webpage. 
    The script should extract the following details for each book listed on the page:
        - Title
        - Author
        - Price
        - Availability status

    Instructions:
    Choose an online bookstore website that lists books with the above details. 
    Use the requests library to fetch the HTML content of the webpage.
    Use BeautifulSoup to parse the HTML content.
    Extract the required details (title, author, price, and availability status) for each book listed on the page.
    Print the extracted details in a readable format.

    Requirements:
    Handle pagination if the website has multiple pages of book listings.
    Ensure that the script handles potential errors gracefully (e.g., missing data, network issues).
    Use appropriate CSS selectors or HTML tags to locate the required elements.

    Example Output:
    Title: A Light in the Attic
    Author: Shel Silverstein
    Price: £51.77
    Availability: In stock

    Title: Tipping the Velvet
    Author: Sarah Waters
    Price: £53.74
    Availability: In stock

    ...
    """
    
    def __init__(self, url="https://books.toscrape.com/"):
        """
        Initialize the BookScraper object with the URL of the website to scrape.
        """
        self.url = url
        self.page = 1
        self.books = defaultdict(list)

    def scrape_books(self):
        url = self.url
        while url:
            self.scrape_books_from_page()
            self.print_books_from_page()
            url = self.get_next_page(url)

    def get_next_page(self, url):
        """
        Get the URL of the next page to scrape.
        """
        # Download the webpage content
        res = requests.get(url)
        res.encoding = 'utf-8'
        res.raise_for_status()

        # Parse the HTML content to get the next page URL
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Extract the URL of the next page (if available)
        next_page = soup.select(".next a")
        if next_page:
            next_page_url = next_page[0].get("href")
            self.page += 1
            return url.rsplit("/", 1)[0] + "/" + next_page_url
        else:
            return None

    def scrape_books_from_page(self):
        """
        Scrape book information from the website.
        """ 

        # Download the webpage content
        res = requests.get(self.url)
        res.encoding = 'utf-8'  # Ensure the correct encoding
        res.raise_for_status()

        # Parse the HTML content
        soup = bs4.BeautifulSoup(res.text, "html.parser")

        # Extract book details (title, author, price, availability)
        books = soup.select(".product_pod")

        for book in books:  
            title = book.select("h3 a")[0].get("title")
            price = book.select(".price_color")[0].get_text()
            availability = book.select(".instock.availability")[0].get_text().strip()

            book_info = {
                "title": title,
                "price": price,
                "availability": availability
            }

            # Store the book details in a list of dictionaries
            self.books[self.page].append(book_info)
            
        self.books 
        
    def print_books_from_page(self, is_print_all=False):
        """
        Print the book details in a readable format.
        """
        # Print number of books scraped
        print(f"Scraped {len(self.books[self.page])} books from page {self.page}:")
        if is_print_all:
            # Print all book details
            for book in self.books[self.page]:
                print("Title:", book["title"])
                print("Price:", book["price"])
                print("Availability:", book["availability"])
                print()

if __name__ == "__main__":
    scraper = BookScraper()
    scraper.scrape_books()
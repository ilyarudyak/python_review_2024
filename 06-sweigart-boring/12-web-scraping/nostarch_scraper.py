import requests, bs4
from collections import defaultdict
import json
import urllib.parse
import re

class NoStarchScraper:
    """
    A web scraper for the No Starch Press website.

    The goal of this scraper is to extract information 
    about books from the No Starch Press website. 
    Example url: https://nostarch.com/catalog/python

    The scraper will extract the following information:
    - Author
    - Title
    - Publication Year
    - Edition
    - Description

    The scraper will also try to predict a level of the book:
    - Beginner
    - Intermediate
    - Advanced

    The scraper will collect in the list of dictionaries and 
    save it to a json file.
    
    """
    def __init__(self, 
                 url_all_books='https://nostarch.com/catalog/python',
                 url_nostarch='https://nostarch.com',
                 output_file='nostarch_books_python.json'):
        self._url_all_books = url_all_books
        self._url_nostarch = url_nostarch
        self._books = []
        self._output_file = output_file

    def scrape_books(self):
        # Download the webpage content
        response = requests.get(self._url_all_books)
        response.raise_for_status()

        # Parse the HTML content
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # Extract the book information into defaultdict
        books = soup.select('.node.node-product')
        for book in books: 
            self._extract_book_info(book)

    def _extract_book_info(self, book):
        """
        Extract book information from the website.
        """
        # Extract information from the main page: author
        author = self.extract_author(book)

        # Extract information from the main page: title
        title, edition = self.extract_title_and_edition(book)

        # Extract information from the main page: description and year
        year, full_description = self._extract_info_from_book_page(book)

        book_info = {
            'title': title,
            'author': author,
            'year': year,
            'edition': edition,
            'full_description': full_description
        }

        self._books.append(book_info)

    def extract_title_and_edition(self, book):
        raw_title_elements = book.select('header')
        raw_title_element = raw_title_elements[0] if raw_title_elements else None
        raw_title = raw_title_element.get_text().strip() if raw_title_element else None
        title, edition = self._get_edition(raw_title) if raw_title else (None, None)
        return title,edition

    def extract_author(self, book):
        author_elements = book.select('.field-name-field-author .field-item')
        author_element = author_elements[0] if author_elements else None
        author = author_element.get_text().strip() if author_element else None
        return author

    def _extract_info_from_book_page(self, book):
        # Get the URL of the book page
        relative_book_url = book.select('a')[0].get('href')
        if not relative_book_url:
            return None, None
        book_url = urllib.parse.urljoin(self._url_nostarch, relative_book_url)  

        # Download the book page content
        response = requests.get(book_url)
        response.raise_for_status()

        # Parse the HTML content for the book page
        soup = bs4.BeautifulSoup(response.text, 'html.parser')

        # Extract the full description
        full_description_elements = soup.select('.field-name-body .field-item')
        full_description_element = full_description_elements[0] if full_description_elements else None
        full_description = full_description_element.get_text() if full_description_element else None

        # Extract the publication year
        release_date_elements = soup.select('.field-name-released-date')
        release_date_element = release_date_elements[0] if release_date_elements else None
        release_date = release_date_element.get_text() if release_date_element else None
        year = self._extract_year(release_date) if release_date else None

        return year, full_description
    
    def _extract_year(self, release_date):
        """
        Extract the publication year from the release date
        using regex.
        Example release_date: 'June 2021, 600 pp.'
        """
        year = re.search(r'\d{4}', release_date)
        return year.group() if year else None

    def _get_edition(self, raw_title):
        """
        Extract the title and edition from the raw title.
        """
        raw_title_parts = raw_title.split(',')
        if raw_title_parts:
            title = raw_title_parts[0].strip()
            edition = raw_title_parts[1].strip() if len(raw_title_parts) > 1 else None
        else:
            return None, None
        
        return title, edition

    def save_to_json(self):
        """
        Save the book information to a json file.
        """
        print(f'Saving the book information to {self._output_file}...')
        with open(self._output_file, 'w') as file:
            json.dump(self._books, file, indent=2)
        

if __name__ == '__main__':
    scraper = NoStarchScraper()
    print('Scraping books...')
    scraper.scrape_books()
    print(f'Number of books scraped: {len(scraper._books)}')
    scraper.save_to_json()
    print('Done scraping!')
"""
This script reads an example book element from the file 'book_element.html' 
and pretty prints it to the file 'book_element_pretty.html'. 
"""
import bs4

def pretty_print_book_element():
    # Read the book element from the file
    with open('book_element.html') as file:
        book_element = file.read()

    # Parse the book element
    soup = bs4.BeautifulSoup(book_element, 'html.parser')

    # Pretty print the book element to the file
    with open('book_element_pretty.html', 'w') as file:
        file.write(soup.prettify())

if __name__ == '__main__':
    pretty_print_book_element()
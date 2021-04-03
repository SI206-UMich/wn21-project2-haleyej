from bs4 import BeautifulSoup
import requests
import re
import os
import csv 
import unittest


def get_titles_from_search_results(filename):
    """
    Write a function that creates a BeautifulSoup object on "search_results.htm". Parse
    through the object and return a list of tuples containing book titles (as printed on the Goodreads website) 
    and authors in the format given below. Make sure to strip() any newlines from the book titles and author names.

    [('Book title 1', 'Author 1'), ('Book title 2', 'Author 2')...]
    """
    #get file, set up soup objectsand initialize list
    f = open("search_results.htm", "r")
    soup = BeautifulSoup(f, 'html.parser')
    titles = []
    f.close()
    #going through each HTML layer
    #LAYER 1: full page content
    content = soup.find('div', class_ = 'content')
    #LAYER 2: 'search' downward
    maincontainer = content.find('div', class_ = 'mainContentContainer')
    #LAYER 3: the left column of books
    leftcontainer = maincontainer.find('div', class_ = 'leftContainer')
    #LAYER 4: books list
    tablecontainer = leftcontainer.find('table', class_ = 'tableList')
    table = tablecontainer.find('tbody')
    entries = table.find_all('tr')
    #iterate through entires
    for entry in entries:
        title = entry.find("span", itemprop = "name").text
        author = entry.find("a", class_ = "authorName").text
        tup = (title, author)
        titles.append(tup)
    return titles
    


def get_search_links():
    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """
    urls = []
    resp = requests.get("https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc")
    soup = BeautifulSoup(resp.content, 'html.parser')
    div = soup.find_all('div', class_ = "leftContainer")
    for item in div:
        links = item.find_all('a')
        for link in links:
            url = link.get('href', None)
            if re.search(r"\/book\/show\/\S+", str(url)):
                full_url = "https://www.goodreads.com" + url
                urls.append(full_url)
    return urls[:10]




def get_book_summary(book_url):
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """

    resp = requests.get(book_url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    title = soup.find('h1', class_ = 'gr-h1 gr-h1--serif').text.strip()
    author = soup.find('a', class_ = 'authorName').text.strip()
    pages = soup.find('span', itemprop = 'numberOfPages').text.strip()
    page = int(pages[:-6])
    return (title, author, page)


def summarize_best_books(filepath):
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """
    pass


def write_csv(data, filename):
    """
    Write a function that takes in a list of tuples (called data, i.e. the
    one that is returned by get_titles_from_search_results()), writes the data to a 
    csv file, and saves it to the passed filename.

    The first row of the csv should contain "Book Title" and "Author Name", and
    respectively as column headers. For each tuple in data, write a new
    row to the csv, placing each element of the tuple in the correct column.

    When you are done your CSV file should look like this:

    Book title,Author Name
    Book1,Author1
    Book2,Author2
    Book3,Author3
    ......

    This function should not return anything.
    """
    base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, filename)
    with open(full_path, 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = ',')
        csvwriter.writerow(['Book title', 'Author Name'])
        for book in data:
            #parts = book.split(",")
            #print(parts)
            csvwriter.writerow(book)


def extra_credit(filepath):
    """
    EXTRA CREDIT

    Please see the instructions document for more information on how to complete this function.
    You do not have to write test cases for this function.
    """
    pass

class TestCases(unittest.TestCase):

    # call get_search_links() and save it to a static variable: search_urls
    
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        results = get_titles_from_search_results('search_results.htm')

        # check that the number of titles extracted is correct (20 titles)

        self.assertEqual(len(results), 20)

        # check that the variable you saved after calling the function is a list
        self.assertEqual((type(results)), list)

        # check that each item in the list is a tuple
        for result in results:
            self.assertEqual(type(result), tuple)

        # check that the first book and author tuple is correct (open search_results.htm and find it)
        first = ("Harry Potter and the Deathly Hallows (Harry Potter, #7)", "J.K. Rowling")
        self.assertEqual(results[0], first)

        # check that the last title is correct (open search_results.htm and find it)
        last = ("Harry Potter: The Prequel (Harry Potter, #0.5)", "J.K. Rowling")
        self.assertEqual(results[-1], last)

    def test_get_search_links(self):
        # check that TestCases.search_urls is a list

        self.assertTrue(type(get_search_links()),list)

        # check that the length of TestCases.search_urls is correct (10 URLs)

        self.assertEqual(len(get_search_links()), 10)
        # check that each URL in the TestCases.search_urls is a string
        urls = get_search_links()
        for url in urls:
            self.assertTrue(type(url), str)

        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        reg = r"https:\/\/www\.goodreads\.com\/book\/show\/.+"
        for url in urls:
            self.assertIsNotNone(re.search(reg, url))



    def test_get_book_summary(self):
        self.summaries = []
        for url in TestCases.search_urls:
            self.summaries.append(get_book_summary(url))

        # check that the number of book summaries is correct (10)
        self.assertEqual(len(self.summaries), 10)

        # check that each item in the list is a tuple
        for tup in self.summaries:
            self.assertEqual(type(tup), tuple)

        # check that each tuple has 3 elements
        for tup in self.summaries:
            self.assertEqual(len(tup), 3)

        # check that the first two elements in the tuple are string
        for tup in self.summaries:
            self.assertEqual(type(tup[0]), str)
            self.assertEqual(type(tup[1]), str)

        # check that the third element in the tuple, i.e. pages is an int
        for tup in self.summaries:
            self.assertEqual(type(tup[2]), int)

        # check that the first book in the search has 337 pages
        book = self.summaries[0]
        self.assertEqual(book[2], 337)


    def test_summarize_best_books(self):
        # call summarize_best_books and save it to a variable

        # check that we have the right number of best books (20)

            # assert each item in the list of best books is a tuple

            # check that each tuple has a length of 3

        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'

        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'A Beautiful Day in the Neighborhood: The Poetry of Mister Rogers', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        pass


    def test_write_csv(self):
        testData = get_titles_from_search_results('search_results.htm')

        # call write csv on the variable you saved and 'test.csv'
        write_csv(testData, 'test.csv')

        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        with open('test.csv', 'r') as f:
            csv_lines = csv.reader(f)

        # check that there are 21 lines in the csv
            line_count = 0
            for line in csv_lines:
                line_count += 1
            self.assertEqual(line_count, 21)
        # check that the header row is correct
            line_count_2 = 0
            for line in csv_lines:
                if line_count_2 == 0:
                    self.assertEqual(line.strip(), 'Book title,Author Name')

        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
                elif line_count_2 == 1:
                    test_line_1 = ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling')
                    self.assertEqual(line, test_line_1)

        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
                elif line_count_2 == 21:
                    line = ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling')
                    self.assertEqual(csv_lines[-1].strip(), line)
                line_count_2 += 1



if __name__ == '__main__':
    print(extra_credit("extra_credit.htm"))
    unittest.main(verbosity=2)


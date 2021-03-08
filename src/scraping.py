from http_utils import create_https_connection
from bs4 import BeautifulSoup


def scrape_html_doc(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    a_refs = soup.find_all("a")

    for a in a_refs:
        for child in a.children:
            print(child)

import re
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

URL="https://en.wikipedia.org/wiki/Chemical_element"

# </p><p><a href="/wiki/List_of_chemical_elements" title="List of chemical elements">
# 0: "List of chemical elements"
# 1: "Headers"
# 2-...: Items
# ...
# N: Notes
def parse_table(html):
    """ Parses the wikipedia page with the chemical elements to extract the table.
    """

    for table in html.find_all("table", class_="wikitable sortable collapsible"):
        if (table.find("th").get_text().strip() == "List of chemical elements"):
            break
    else:
        raise Exception("Table not found.")

    TABLE = []
    for n, tr in enumerate(table.find_all("tr")):
        ROW = []

        # Remove all citations.
        for c in tr.find_all('sup', {'id': re.compile(r'cite_ref.*')}): c.extract()

        # First row is non-informative.
        if n < 1: continue
        elif n == 1: 
            # Row with column headers.
            COLUMNS = [ i.get_text().strip() for i in tr.find_all("th") ]

        else:
            # Actual rows
            ROW = [ i.get_text().strip() for i in tr.find_all("td") ]

            if len(ROW) == len(COLUMNS):
                TABLE.append(ROW)
            else:
                # The last row does not contain items and has only one column.
                if len(ROW) != 1:
                    raise Exception("Invalid column number.")

    return pd.DataFrame(TABLE, columns=COLUMNS)

def main():
    # Download the content of the page with the chimical elements.
    content = urllib.request.urlopen(URL).read()

    # Parse the page
    html = BeautifulSoup(content, "lxml")

#    print(parsed_html.prettify())

    # Parse the page to pandas table.
    TABLE = parse_table(html)

#     print(TABLE.to_string())

    # Store the pandas table to CSV and JSON.
    TABLE.to_csv("chemical_items.csv", sep=',', encoding='utf-8')
    TABLE.to_json("chemical_items.json", orient='records')

if __name__=="__main__":
    main()

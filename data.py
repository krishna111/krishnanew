from bs4 import BeautifulSoup
import requests
import sys



cik = '0000051143'
type = '10-K'


dateb = '20160101'

# Obtain HTML for search page
base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}"
edgar_resp = requests.get(base_url.format(cik, type, dateb))
edgar_str = edgar_resp.text

# Find the document link
doc_link = ''
soup = BeautifulSoup(edgar_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile2')
rows = table_tag.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        if '2015' in cells[3].text:
            doc_link = 'https://www.sec.gov' + cells[1].a['href']

# Exit if document link couldn't be found
if doc_link == '':
    print("Couldn't find the document link")
    sys.exit()

# Obtain HTML for document page
doc_resp = requests.get(doc_link)
doc_str = doc_resp.text

# Find the XBRL link
xbrl_link = ''
soup = BeautifulSoup(doc_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile', summary='Data Files')
rows = table_tag.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        if 'INS' in cells[3].text:
            xbrl_link = 'https://www.sec.gov' + cells[2].a['href']

# Obtain XBRL text from document
xbrl_resp = requests.get(xbrl_link)
xbrl_str = xbrl_resp.text
soup = BeautifulSoup(xbrl_str, 'lxml')
tag_list = soup.find_all()

# This section of code creates a context table.
# The context table is a dictionary of context names keys that reference dictionary values
# containing date information for each context. For contexts with datetype of 'period' the table
# contains the start and end date. For contexts with datetype of 'instant' the context
# contains the instant date of the context. All entries include a date and dateType value.
# For contexts with datetype of period, the date is equal to the enddate of the context.

contexts = {}

for tag in tag_list:
    if tag.name == 'xbrli:context':

        # This section of code finds the start date of the context if it exists.
        start_date_tag = tag.find(name='xbrli:startdate')
        if start_date_tag == None:
            start_date = None
        else:
            start_date = start_date_tag.text

        # This section of code finds the end date of the context if it exists.
        end_date_tag = tag.find(name='xbrli:enddate')
        if end_date_tag == None:
            end_date = None
        else:
            end_date = end_date_tag.text
            date = end_date_tag.text
            datetype = 'period'

        # This section of code finds the instant date of the context if it exists.
        instant_date_tag = tag.find(name='xbrli:instant')
        if instant_date_tag != None:
            date = instant_date_tag.text
            datetype = 'instant'

        # build a dictionary of date information within a dictionary of context titles
        dtinfo = {'date': date, 'year': date[0:4], 'datetype': datetype, 'startdate': start_date, 'enddate': end_date}
        contexts[tag.attrs['id']] = dtinfo

# Find and print stockholder's equity
i = 0
for tag in tag_list:
    if tag.name == 'us-gaap:stockholdersequity':
        year = contexts[tag.attrs['contextref']]['year']
        print(year + " Stockholder's equity: " + tag.text)
from bs4 import BeautifulSoup
import requests
import sys


def index():
    cik = '0000051143'
    type = '10-K'


dateb = '20160101'

# Obtain HTML for search page
base_url = "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={}&type={}&dateb={}"
edgar_resp = requests.get(base_url.format(cik, type, dateb))
edgar_str = edgar_resp.text

# Find the document link
doc_link = ''
soup = BeautifulSoup(edgar_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile2')
rows = table_tag.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        if '2015' in cells[3].text:
            doc_link = 'https://www.sec.gov' + cells[1].a['href']

# Exit if document link couldn't be found
if doc_link == '':
    print("Couldn't find the document link")
    sys.exit()

# Obtain HTML for document page
doc_resp = requests.get(doc_link)
doc_str = doc_resp.text

# Find the XBRL link
xbrl_link = ''
soup = BeautifulSoup(doc_str, 'html.parser')
table_tag = soup.find('table', class_='tableFile', summary='Data Files')
rows = table_tag.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 3:
        if 'INS' in cells[3].text:
            xbrl_link = 'https://www.sec.gov' + cells[2].a['href']

# Obtain XBRL text from document
xbrl_resp = requests.get(xbrl_link)
xbrl_str = xbrl_resp.text
soup = BeautifulSoup(xbrl_str, 'lxml')
tag_list = soup.find_all()

# This section of code creates a context table.
# The context table is a dictionary of context names keys that reference dictionary values
# containing date information for each context. For contexts with datetype of 'period' the table
# contains the start and end date. For contexts with datetype of 'instant' the context
# contains the instant date of the context. All entries include a date and dateType value.
# For contexts with datetype of period, the date is equal to the enddate of the context.

contexts = {}

for tag in tag_list:
    if tag.name == 'xbrli:context':

        # This section of code finds the start date of the context if it exists.
        start_date_tag = tag.find(name='xbrli:startdate')
        if start_date_tag == None:
            start_date = None
        else:
            start_date = start_date_tag.text

        # This section of code finds the end date of the context if it exists.
        end_date_tag = tag.find(name='xbrli:enddate')
        if end_date_tag == None:
            end_date = None
        else:
            end_date = end_date_tag.text
            date = end_date_tag.text
            datetype = 'period'

        # This section of code finds the instant date of the context if it exists.
        instant_date_tag = tag.find(name='xbrli:instant')
        if instant_date_tag != None:
            date = instant_date_tag.text
            datetype = 'instant'

        # build a dictionary of date information within a dictionary of context titles
        dtinfo = {'date': date, 'year': date[0:4], 'datetype': datetype, 'startdate': start_date, 'enddate': end_date}
        contexts[tag.attrs['id']] = dtinfo

# Find and print stockholder's equity
i = 0
tag_data={}

for tag in tag_list:
    if tag.name == 'us-gaap:stockholdersequity':
        year = contexts[tag.attrs['contextref']]['year']
        tag_data[year]=tag.text

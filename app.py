import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException, Timeout
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import re
import urllib.parse
import csv
import json

def create_session_with_retries():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def extract_emails_and_phones(url, session):
    updateUrl = f"https://web.archive.org/web/timemap/json?url={urllib.parse.quote(url)}&matchType=prefix&output=json"
    try:
        response = session.get(updateUrl, timeout=10)
        responses = json.loads(response.text)[1:]
        for response in responses:
            main_request = f"https://web.archive.org/web/{response[1]}/{url}"
            try:
                main_response = session.get(main_request, timeout=10)
                soup = BeautifulSoup(main_response.content, 'html.parser')
                email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                phone_regex = r'\+?\d[\d -]{8,}\d'
                emails = set(re.findall(email_regex, soup.text))
                phones = set(re.findall(phone_regex, soup.text))
                if emails or phones:
                    return emails, phones
            except (RequestException, Timeout) as e:
                print(f"Error fetching {main_request}: {e}")
                continue
    except (RequestException, Timeout) as e:
        print(f"Error fetching {updateUrl}: {e}")

    return set(), set()

def crawl_archives(urls, output_file):
    with open(output_file, mode='w', newline='') as csv_file:
        fieldnames = ['URL', 'Emails', 'Phones']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

    session = create_session_with_retries()

    for url in urls:
        print(f"Processing {url}")
        emails, phones = extract_emails_and_phones(url, session)
        result = {
            'URL': url,
            'Emails': ', '.join(emails),
            'Phones': ', '.join(phones)
        }

        with open(output_file, mode='a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=['URL', 'Emails', 'Phones'])
            writer.writerow(result)

if __name__ == "__main__":
    with open('urls.txt', 'r') as f:
        urls = [line.strip().replace(',', '') for line in f.readlines()]
    output_file = 'output.csv'
    crawl_archives(urls, output_file)
    print("CSV generated successfully.")

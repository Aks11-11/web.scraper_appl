import requests
from bs4 import BeautifulSoup
import sqlite3

# URL to scrape data from
URL = 'https://example.com'

def create_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def scrape_data():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming the data we want is in a div with class 'item'
    items = soup.find_all('div', class_='item')

    data = []
    for item in items:
        title = item.find('h2').text.strip()
        description = item.find('p').text.strip()
        data.append((title, description))

    store_data(data)

def store_data(data):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.executemany('INSERT INTO data (title, description) VALUES (?, ?)', data)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_db()
    scrape_data()

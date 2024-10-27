import requests
import bs4
from bs4 import BeautifulSoup
import tldextract
import dotenv
from qews import Qews
from bs4.element import Comment
import re
import uuid
import os
import queue
from threading import Thread
from bloom_filter import BloomFilter
import time
from utils import pickle_data, unpickle_data, DATA_DIR

MAX_DOMAINS = 500
MAX_LENGTH = 1000
NUM_WORKERS = 5
WAIT_TIME = 2
DIR_PATH = os.path.dirname(os.path.realpath(__file__)) + '/scraped_documents/'


def scheduler_task(Q, bf):
    pickle_data(Q, 'Q.pkl')
    pickle_data(bf, 'bf.pkl')


def get_page(url):
    response = requests.get(url)
    return response.text


def extract_urls(page):
    soup = BeautifulSoup(page, 'html.parser')
    urls = []
    for link in soup.find_all('a'):
        urls.append(link.get('href'))
    urls = [url for url in urls if url is not None and url.startswith('https://')]
    return urls


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, bs4.element.Comment):
        return False
    if re.match(r"[\s\r\n]+", str(element)):
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    data = u" ".join(t.strip() for t in visible_texts)
    return data


def extract_domain_name(url):
    domain_guess = url.split("/")[2]
    return domain_guess
    

def write_to_file(data, domain):
    file_name = DIR_PATH + domain + str(uuid.uuid4()) + ".txt"
    with open(file_name, 'w') as f:
        f.write(data)


def get_seed_urls():
    seeds = []
    with open('seed_urls.txt', 'r') as f:
        for line in f:
            seeds.append(line.strip())
    return seeds


def initialize():

    #set up bloom filter
    bf_path = DATA_DIR + 'bf.pkl'
    if os.path.exists(bf_path):
        bf = unpickle_data('bf')
    else:
        bf = BloomFilter()

    #initialize seed urls
    Q_path = DATA_DIR + 'Q.pkl'
    if os.path.exists(Q_path):
        Q = unpickle_data('Q')
    else:
        Q = Qews(MAX_DOMAINS, MAX_LENGTH)
        
    #initialize queue ds
    seeds = get_seed_urls()
    
    #populate seed urls
    if os.path.exists(Q_path) and os.path.exists(bf_path):
        return Q, bf
    else:
        for seed in seeds:
            domain = extract_domain_name(seed)
            Q.push(domain, seed)
    return Q, bf


def scrape(Q, bf):
    try:
        url = Q.retrieve()
        if url is None:
            return

        if bf.contains(url):
            return

        page = get_page(url)
        urls = extract_urls(page)
        text = text_from_html(page)
        domain = extract_domain_name(url)
        write_to_file(text, domain)
        bf.add(url)

        for url in urls:
            if url is not None:
                domain = extract_domain_name(url)
                Q.push(domain, url)
    except:
        return

def main():

    Q, bf = initialize()

    while True:
        workers = []
        for i in range(NUM_WORKERS):
            workers.append(Thread(target=scrape, args=(Q, bf)))

        for worker in workers:
            worker.start()

        for worker in workers:
            worker.join()

        time.sleep(WAIT_TIME)


if __name__ == '__main__':
    main()
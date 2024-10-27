# A Simple Web Crawler

This repository contains python code to create a breath first search web crawler that scrapes text from websites and continues the search with urls found.
This webcrawler was created to gather information on a particular topic and create a small knowledge base for later use by a retrieval augmented generation
pipeline. This module is meant to gather less than 1 GB of text data, which is plenty enough for a RAG model. Since the collected data size is small, each scraped page is
stored as a .txt document on the local machine. 

## bloom_filter.py
The bloom filter is implemented to support approximately 1 Million document hashes with a false positive rate of 5%. A bloom filter is a 
probablistic datastructure that is able to check whether an element has been visited or seen with a specifed false positive rate. Since this is 
a simple web crawler with minimal documents, we opt to use this datastructure instead of any optimized DB search. It's also simple enough to implement
with relative ease. This file contains a class that allows one to add an element to the datastructure as well as check whether the datastructure
contains an element. 

## quews.py
This class is a datastructure that manages a seperate queue for urls belonigng to the same website domian. We opt to use a queue in this brief implementation
to manage politeness. We would not like to query from the same domain repeatedly, instead our datastructure randomly pulls a url from a non-empty queue to process.

## scraper.py
This file contains the main method that invokes our quews class, our bloom filter, and a main method that utlized beautifulsoup to parse urls and extract text
from webpages. Our webscraper is threaded. Each worker thread processes one url at a time and saves the content to a .txt file in our data folder on local. Given
that our goal is to gather less than 1 GB of text, threads are enough to speed up our workflow and accomplish the task.

## seed_urls.txt
Have fun! I included asbout 5 seed urls to gather information on Baulder's Gate, for later consumption by a RAG model to answer questions about the game. If you are using
this repository as a starting point to create your own web crawler, consider changing these seed urls.

## Improvements
This is a quick project for fun. In order to improve this design, consider filtering out urls that are too long and may in fact be a spider trasp. Also, if possible you may 
want to process the robot.txt file for each domain to maintain politeness.

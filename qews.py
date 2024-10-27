import os
import sys
import queue
import random
from utils import unpickle_data, pickle_data


class Qews:
    def __init__(self, max_queues, max_length):
        self.max_queues = max_queues
        self.max_length = max_length
        self.n_queues = 0
        self.keys = []
        self.lookup = {}

    def push(self, domain, url):
        if domain not in self.lookup and self.n_queues < self.max_queues:
            self.lookup[domain] = queue.Queue()
            self.n_queues +=1
            self.lookup[domain].put(url)
            return

        if domain in self.lookup and self.lookup[domain].qsize() < self.max_length:
            self.lookup[domain].put(url)
            return

    def retrieve(self):

        try:
            if self.n_queues == 0:
                return None
            idx = random.randint(0, self.n_queues - 1)
            domain = list(self.lookup.keys())[idx]
            url = self.lookup[domain].get()

            if self.lookup[domain].qsize() == 0:
                self.n_queues -= 1
                del self.lookup[domain]
            return url
        except:
            return

if __name__ == "__main__":
    q = Qews(2, 3)
    q.push("google.com", "https://www.google.com")
    q.push("google.com", "https://www.google.com/1")
    q.push("google.com", "https://www.google.com/2")
    q.push("facebook.com", "https://www.facebook.com")
    q.push("facebook.com", "https://www.facebook.com/1")
    q.push("facebook.com", "https://www.facebook.com/2")
    print(len(q.keys))
    print(q.retrieve())
    print(q.retrieve())
    print(q.retrieve())
    print(q.retrieve())
    print(q.retrieve())
    print(q.retrieve())


    
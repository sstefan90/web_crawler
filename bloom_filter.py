import os
import sys
import math
import pickle
'''
Bloom filter for 1MM elements with 0.05 false positive rate
'''

class BloomFilter:
    def __init__(self, n=5*10**6, p=0.05):
        self.n = n
        self.p = p
        self.m = self.get_m(n, p)
        self.k = self.get_k(self.m, n)
        self.bf = [0] * self.m

    def get_m(self, n, p):
        return int(-n * math.log(p) / math.log(2)**2)

    def get_k(self, m, n):
        return int(m / n * math.log(2))

    def add(self, key):
        for i in range(self.k):
            index = hash(key + str(i)) % self.m
            self.bf[index] = 1

    def contains(self, key):
        for i in range(self.k):
            index = hash(key + str(i)) % self.m
            if self.bf[index] == 0:
                return False
        return True

if __name__ == '__main__':
    bf = BloomFilter()
    bf.add("google.com")
    bf.add("facebook.com")
    print(bf.contains("facebook.com"))
    print(bf.contains("twitter.com"))
    print(bf.contains("google.com"))


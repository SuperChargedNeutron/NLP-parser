import os, sys, io

doc_path = os.path.join('docs', 'timferris-harryfinkelstein.txt')

with io.open(doc_path, 'r', encoding='utf-8') as fil:
    lines = fil.read().split('\n')
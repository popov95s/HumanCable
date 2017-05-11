# pip install pyxDamerauLevenshtein
from sys import argv
from pyxdameraulevenshtein import normalized_damerau_levenshtein_distance

sent_file = argv[1]
true_file = argv[2]
with open(sent_file, 'r') as myfile:
   sent_data = myfile.read()
with open(true_file, 'r') as myfile:
   true_data = myfile.read()
print(normalized_damerau_levenshtein_distance(sent_data, true_data))
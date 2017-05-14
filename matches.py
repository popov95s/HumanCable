import sys
# takes in the txt file with sequence
# takes in another txt file with multiple sequences (ideally) and count the number of them.
import re
with open (sys.argv[1], 'r') as myfile:
    true_txt = myfile.read()
with open (sys.argv[2], 'r') as myfile:
    sent_txt = myfile.read()
a = re.compile(true_txt)
matches = re.findall(true_txt, sent_txt)
print(len(matches))

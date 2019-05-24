import random
import hashlib
import time
import math
import datetime
from random import choices
import sys

## Control var for the while
collision_found = False
alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%&$?!*£#@{}[]()=+-><'
## k is the (negative for use in indexing) number of bits (lsb) for which I look for a collision
k, computed_hashes = (0-int(sys.argv[1])), 0
dic = {}

## expected is the theoretical expected number of hashed computed before finding a collision 
expected = 1.25*math.sqrt(2**abs(k))

## This func generates a random string of fixed length
def generate_document():
    return str().join(choices(alphabet, k=7))  

## This func generates the two colliding documents, given the strings they should contain
def file_generator(s1, s2):
    with open('doc1.txt', 'w') as d1, open('doc2.txt', 'w') as d2:
        d1.write(s1)
        d2.write(s2)

## Return the elapsed time in a formatted way
def elapsed(t1, t2):
    return str(datetime.timedelta(seconds=t2-t1))
    
t0 = time.time()

## At every iteration generate a new string/document and look for a collision using a dic
## The keys are the k lsb of the hashe, while the values are the corresponding strings/docs
while(not collision_found):
    doc = generate_document()

    ## hex_digest is the sha1 output in hex format
    hex_digest = hashlib.sha1(bytes(doc, encoding='utf-8')).hexdigest()
    ## bin_digest is the corresponding binary of hex_digest (only the last k bits) 
    bin_digest = bin(int(hex_digest, 16))[k:]
    
    computed_hashes = computed_hashes + 1

    ## Checking if another hash with the same k least sig bits has been previously computed (present in dic)
    if bin_digest in dic.keys() and doc != dic[bin_digest][0]:
        ## print a summary of the collision
        print('Collision found')
        print('doc1:', doc)
        print('doc2:', dic[bin_digest][0])   
        print('sha:', hex_digest)
        print('bin:', bin_digest)
        
        collision_found = True
        
        ## Create the two files
        file_generator(doc, dic[bin_digest][0])
        
    else:
        ## Add a new key and relative str/doc
        dic[bin_digest] = list()
        dic[bin_digest].append(doc)

print('k:', abs(k))
print('elapsed', elapsed(t0, time.time()))
print('expected hashes for collision:', int(expected))
print('generated hashes up to collision:', computed_hashes)

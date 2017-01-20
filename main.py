# Imports
import operator
import json
import ast

# Global Variables
zeros = 0
encod = 'utf-8'

# should be a .txt
def readfile(filename):
  return open(filename, encoding=encod).read()

def writefile(filename, tree, string):
  f = open(filename, 'w', encoding=encod)
  json.dump(tree, f) # dump tree
  f.write(string)
  f.close()

# returns a list with the frequencies of each letter in the string
def frequency(string):
  freq, leng = {}, len(string)
  for i in range(10000):
    if string.count(chr(i)):
      freq[chr(i)] = string.count(chr(i))*1.0/leng
  if string.count('’'):
    freq['’'] = string.count('’')*1.0/leng
  return freq

# returns the second smallest element in a numeric list
def second_smallest(numbers):
  return sorted(numbers,key=float)[1]

# returns a list with the Huffman-encoded ASCII table
def constructHuffmanTree(text, count):
  count = frequency(text)
  aux = dict(count)
  savedCoding = dict()
  for ii in range(len(count) - 2):
    flag = 0
    auxDict = dict()
    dictValues = list(aux.values())
    smallestElementValue = min(dictValues)
    secondSmallestElementValue = sorted(dictValues,key=float)[1]
    for key,value in aux.items():
      if value == smallestElementValue or value == secondSmallestElementValue:
        flag += 1
        if flag == 1:
          node1 = key
          if node1 in savedCoding.keys():
            auxDict['0'] = savedCoding[node1]
          else:
            auxDict['0'] = node1
        elif flag == 2:
          node2 = key
          if node2 in savedCoding.keys():
            auxDict['1'] = savedCoding[node2]
          else:
            auxDict['1'] = node2
          break    
    aux[node1] = aux[node1] + aux[node2]
    newLetter = node1 + node2
    aux[newLetter] = aux[node1]
    savedCoding[newLetter] = auxDict
    del aux[node1]
    del aux[node2]
    del auxDict
    if node1 in savedCoding.keys():
      del savedCoding[node1]
    if node2 in savedCoding.keys():
      del savedCoding[node2]
  finalKeys = list(savedCoding.keys())
  savedCoding['0'] = savedCoding.pop(finalKeys[0])
  savedCoding['1'] = savedCoding.pop(finalKeys[1])
  return savedCoding

# given a tree in this format: {'a':0, 'b':10, 'c':11}
# and words being the string read from the file
def encode(tree,words):
  code = ''
  for let in words:
    if let in tree.keys():
      code = code + str(tree[let])
  return code

def code_to_string(code): 
  compressed = ''
  for i in range(0,len(code),6):
    compressed = compressed + chr(int(code[i:i+6],2) + 40)
  return compressed

#Decoding function
def decode(tree, code):
  node = tree
  text = ''
  for ii in code:
    if type(node[ii]) is dict:
      node = node[ii]
    elif type(node[ii]) is str:
      text += node[ii]
  return text

def string_to_code(text):
  code1 = ''
  for e in text:
    code0 = bin(ord(e)-40)[2:]
    if len(code0) != 6:
      code0 = '0'*(6-len(code0)) + code0
    code1 += code0
  return code1 


##ENCODING

# open file
file = 'text_sample.txt'
original_text = readfile(file)

#Constructing the tree
characterCounter = frequency(original_text)
tree = constructHuffmanTree(original_text, characterCounter)
print(tree)
words = original_text
code = encode(tree,words)

zeros = 6 - len(code)%6
if len(code)%6 != 0:
  code = code + '00000000'[len(code)%6:6]

comp = code_to_string(code)

print("Compresion rate:", len(comp)/len(original_text))

# write in file
extension = 'hff'
ex_filename = 'result' + '.' + extension
tree['999'] = zeros
writefile(ex_filename, tree, comp)

## DECODING
file = 'result.hff'
text2 = readfile(file)

pos = 0
while(1):
  limit = text2.find('}', pos)
  if text2[limit+1] != '"':
    break
  else:
    pos = limit + 1
tree2 = ast.literal_eval(text2[:limit+1])
zeros2 = tree['999']
text2 = text2[limit+1:] # the encoded text

back = string_to_code(text2)
back = back[:(len(back)-zeros2)] # deleting the redundancies

decoded = decode(tree2, back)

f = open('decompressed.txt', 'w', encoding=encod)
f.write(decoded)
f.close()
print(decoded == original_text)
print(len(decoded),len(original_text))
# find the error (if it exists) and print the position, what there is, and what should have been
for i in range(len(original_text)):
  if decoded[i] != original_text[i]:
    print(i,decoded[i],original_text[i])
    break


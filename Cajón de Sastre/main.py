# Imports
import operator
import json
import ast
import math

# Global Variables
zeros = 0
encod = 'utf-8'
num = 7
code1 = 0
stri1 = ''
orig_str = ''

# should be a .txt
def writefile(filename, tree, string):
  f = open(filename, 'w', encoding=encod)
  json.dump(tree, f) # dump tree
  f.write(string)
  f.close()

# returns a list with the frequencies of each letter in the string
def frequency(string):
  freq, leng = {}, len(string)
  for i in set(string):
    if string.count(i):
      freq[i] = string.count(i)*1.0/leng
  return freq

# returns a list with the Huffman-encoded ASCII table
def constructHuffmanTree(text):
  count = frequency(text)
  auxTree = dict.fromkeys(count.keys(), '')
  savedCoding = dict()
  numbers = range(len(count) - 1)
  for ii in numbers:
    flag = 0
    auxDict = dict()
    dictValues = list(count.values())
    smallestElementValue = min(dictValues)
    secondSmallestElementValue = sorted(dictValues,key=float)[1]
    for key,value in count.items():
      if value == smallestElementValue or value == secondSmallestElementValue:
        flag += 1
        if flag == 1:
          node1 = key
          for jj in key:
            auxTree[jj] = '0' + auxTree[jj]
          if node1 in savedCoding.keys() and ii != numbers[-1]:
            auxDict['0'] = savedCoding[node1]
          elif ii != numbers[-1]:
            auxDict['0'] = node1
        elif flag == 2:
          node2 = key
          for jj in key:
            auxTree[jj] = '1' + auxTree[jj]
          if node2 in savedCoding.keys() and ii != numbers[-1]:
            auxDict['1'] = savedCoding[node2]
          elif ii != numbers[-1]:
            auxDict['1'] = node2
          break    
    count[node1] = count[node1] + count[node2]
    newLetter = node1 + node2
    count[newLetter] = count[node1]
    if ii != numbers[-1]:
      savedCoding[newLetter] = auxDict
    del count[node1]
    del count[node2]
    del auxDict
    if node1 in savedCoding.keys() and ii != numbers[-1]:
      del savedCoding[node1]
    if node2 in savedCoding.keys() and ii != numbers[-1]:
      del savedCoding[node2]
  finalKeys = list(savedCoding.keys())
  savedCoding['0'] = savedCoding.pop(finalKeys[0])
  savedCoding['1'] = savedCoding.pop(finalKeys[1])
  return savedCoding, auxTree

# given a tree in this format: {'a':0, 'b':10, 'c':11}
# and words being the string read from the file
def encode(tree,words):
  global zeros, code1, stri1
  code = ''
  for let in words:
    if let in tree.keys():
      code = code + str(tree[let])

  # add redundant zeroes
  zeros = num - len(code)%num
  if len(code)%num != 0:
    code = code + '0000000'[len(code)%num:num]

  code1 = code

  # from binary string to char string
  compressed = ''
  for i in range(0,len(code),num):
    compressed = compressed + chr(int(code[i:i+num],2) + 40)
  stri1 = compressed
  return compressed


##ENCODING
def encoding(file):
  # open file
  original_text = open(file, encoding=encod).read()
  original_text2 = original_text + ' '

  global orig_str
  orig_str = original_text

  #Constructing the tree
  #Returns 2 trees. The first tree is the one we want to introduce in the hff and the second tree is only using in the encoding
  tree, encodingTree = constructHuffmanTree(original_text2) 
  words = original_text2
  comp = encode(encodingTree,words)

  print("Compresion rate:", math.fabs(1 - (len(comp)/len(original_text2)))*100, "%")

  # write in file
  extension = 'hff'
  ex_filename = 'result' + '.' + extension
  tree['999'] = zeros
  print(zeros)
  writefile(ex_filename, tree, comp)


#Decoding function
def decode(text, tree):
  # string to code
  print("Compressed strings equal, ", stri1 == text)
  code = ''
  for e in text:
    auxcode = bin(ord(e)-40)[2:]
    if len(auxcode) != num:
      auxcode = '0'*(num-len(auxcode)) + auxcode
    code += auxcode
    
  print("Codes equal, ", code1 == code)
  code = code[:(len(code)-tree['999'])] # deleting the redundancies
  # code to decompressed string
  node = tree
  text = ''
  for ii in code:
    if isinstance(node[ii], dict):
      node = node[ii]
    elif isinstance(node[ii],str):
      text += node[ii]
      node = tree
      if text != orig_str[:len(text)]:
        print('sth terribly wrong', node[ii])
        break
  return text[:-1]

## DECODING
def decoding(file):
  file = 'result.hff'
  text2 = open(file, encoding=encod).read()
  text2 = 'r' + text2 # to escape newline characters

  cnt = 0
  for i in range(1,len(text2)):
    if text2[i] == '{':
      cnt += 1
    elif text2[i] == '}':
      cnt -= 1
    if cnt == 0:
      tree2 = ast.literal_eval(text2[1:i+1])
      break;

  text2 = text2[i+1:] # the encoded text
  decoded = decode(text2, tree2)

  print("Decompressed text equal, ", orig_str == decoded)

  f = open('decompressed.txt', 'w', encoding=encod)
  f.write(decoded)
  f.close()


def compare(txt, txt2):
  original = open(txt, encoding=encod).read()
  decompressed = open(txt2, encoding=encod).read()
  print(decompressed == original)
  if decompressed != original:
    print(len(decompressed),len(original))

  # find the error (if it exists) and print the position, what there is, and what should have been
  ##for i in range(len(original)):
  ##  if decompressed[i] != original[i]:
  ##    print(i,decompressed[i],original[i])
  ##    break

# MAIN
txt = 'text_sample.txt'
hff = 'result.hff'
txt2 = 'decompressed.txt'
encoding(txt)
decoding(hff)

compare(txt, txt2)

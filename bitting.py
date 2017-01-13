# Imports
import operator
import json
import ast

# Global Variables
zeros = 0
encod = 'latin-1'

# should be a .txt
def readfile(filename):
  return open(filename, encoding=encod).read()

def writefile(filename, string):
  f = open(filename, 'w', encoding=encod)
  f.write(string)
  f.close()

# returns a list with the frequencies of each letter in the string
def frequency(string):
  freq, leng = {}, len(string)
  for i in range(100):
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
  savedCoding = dict.fromkeys(count.keys(), '')
  aux = dict(count)
  for ii in range(len(count) - 1):
    flag = 0
    dictValues = list(aux.values())
    smallestElementValue = min(dictValues)
    secondSmallestElementValue = second_smallest(dictValues)
    for key,value in aux.items():
      if value == smallestElementValue or value == secondSmallestElementValue:
        flag += 1
        if flag == 1:
          node1 = key
          for jj in key:
            savedCoding[jj] = '0' + savedCoding[jj]
        elif flag == 2:
          node2 = key
          for jj in key:
            savedCoding[jj] = '1' + savedCoding[jj]
          break
    aux[node1] = aux[node1] + aux[node2]
    newLetter = node1 + node2
    aux[newLetter] = aux[node1]
    del aux[node1]
    del aux[node2]
  return savedCoding

# given a tree in this format: {'a':0, 'b':10, 'c':11}
# and words being the string read from the file
def encode(tree,words):
  code = ''
  for let in words:
    if let in tree.keys():
      code = code + str(tree[let])
  return code

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

def frombits(bits):
    chars = []
    for b in range(len(bits)//8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
    return ''.join(chars)


file = 'text_sample.txt'
original_text = readfile(file)

#Constructing the tree
characterCounter = frequency(original_text)
tree = constructHuffmanTree(original_text, characterCounter)

words = original_text
code = encode(tree,words)

if len(code)%8 != 0:
  code = code + '0'*(8-(len(code)%8))

tocode = []
for e in code:
  tocode.append(int(e))

comp = frombits(tocode)

extension = 'hff'
ex_filename = 'result' + '.' + extension
writefile(ex_filename, comp)

file = 'result.hff'
text2 = readfile(file)

cnt0 = 0
for i in range(len(text2)):
  if comp[i] != text2[i]:
    # los fallos
    #print(i,comp[i],text2[i])
    cnt0 = cnt0 + 1

back = tobits(text2)

back2 = ''.join(str(e) for e in back)


print(code == back2)
cnt = 0
for i in range(len(code)):
  if back2[i] != code[i]:
    # los fallos
    #print(i,back2[i],code[i])
    cnt = cnt + 1

print(cnt//3, cnt0)

f = open('decompressed.txt', 'w', encoding=encod)
f.write(back2)
f.close()

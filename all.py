## GUI for python2.7

import os
from tkinter import *
from tkinter import filedialog
import operator
import json
import ast

# ~~~~ GLOBAL VARIABLES ~~~~
origin_path = ''
first_ext = ''
zeros = 0
num = 7
b1 = 0
b2 = 0
e1 = 0
e2 = 0

# ~~~~ COMPRESSION FUNCTIONS ~~~~
def readfile(filename):
  return open(filename, encoding='utf-8').read()

def writefile(filename, tree, string):
  f = open(filename, 'w', encoding='utf-8')
  if tree != {}:
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
  aux = dict(count)
  auxTree = dict.fromkeys(count.keys(), '')
  savedCoding = dict()
  numbers = range(len(count) - 1)
  for ii in numbers:
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
    aux[node1] = aux[node1] + aux[node2]
    newLetter = node1 + node2
    aux[newLetter] = aux[node1]
    if ii != numbers[-1]:
      savedCoding[newLetter] = auxDict
    del aux[node1]
    del aux[node2]
    del auxDict
    if node1 in savedCoding.keys() and ii != numbers[-1]:
      del savedCoding[node1]
    if node2 in savedCoding.keys() and ii != numbers[-1]:
      del savedCoding[node2]
  finalKeys = list(savedCoding.keys())
  savedCoding['0'] = savedCoding.pop(finalKeys[0])
  savedCoding['1'] = savedCoding.pop(finalKeys[1])
  return savedCoding, auxTree


# given a tree and words being the string read from the file, returns a binary sequence
def encode(tree,words):
  code = ''
  for let in words:
    if let in tree.keys():
      code = code + str(tree[let])
  return code

def code_to_string(code): 
  compressed = ''
  for i in range(0,len(code),num):
    compressed = compressed + chr(int(code[i:i+num],2) + 40)
  return compressed

#Decoding function
def decode(tree, code):
  node = tree
  text = ''
  for ii in code:
    if ii not in node:
      return text
    elif type(node[ii]) is dict:
      node = node[ii]
    elif type(node[ii]) is str:
      text += node[ii]
      node = tree
  return text

def string_to_code(text):
  code1 = ''
  for e in text:
    code0 = bin(ord(e)-40)[2:]
    if len(code0) != num:
      code0 = '0'*(num-len(code0)) + code0
    code1 += code0
  return code1 


def compression():

  global e1, e2

  origin_data = open(e1.get(), 'r', encoding='utf-8').read()
  destination_path = e2.get()
  origin_data += ' '
  
  #Constructing the tree
  tree, encodingTree = constructHuffmanTree(origin_data)
  code = encode(encodingTree,origin_data)
  zeros = num - len(code)%num
  if len(code)%num != 0:
    code = code + '0000000'[len(code)%num:num]

  compressed = code_to_string(code)
  print("Compresion rate:", len(compressed)/len(origin_data))

  # write in file
  tree['999'] = zeros
  writefile(destination_path, tree, compressed)
  

def decompression():

  origin_data = open(e1.get(), 'r', encoding='utf-8').read()
  destination_path = e2.get()

  text2 = origin_data
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
  zeros2 = tree2['999']
  text2 = text2[i+1:] # the encoded text

  back = string_to_code(text2)
  back = back[:(len(back)-zeros2)] # deleting the redundancies
  decoded = decode(tree2, back)[:-1]

  writefile(destination_path, {}, decoded)

  print(open('text_sample.txt', encoding='utf-8').read() == decoded)

# ~~~~ GUI FUNCTIONS ~~~~
def open_origin_file(entry, entry2):
  
  global origin_path
  global first_ext
  global b1,b2

  options = {}
  options['filetypes'] = [('text files [.txt]', '.txt'),('Huffman-compressed files [.hff]', '.hff')]
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = filedialog.askopenfilename(**options)

  if filename:
    first_ext = filename[-3:]
    entry2.delete(0, END)
    if first_ext == 'txt':
      b1.config(state = 'active')
      b2.config(state = 'disabled')
      entry2.insert(0, filename[:-3] + 'hff')
    elif first_ext == 'hff':
      b1.config(state = 'disabled')
      b2.config(state = 'active')
      entry2.insert(0, filename[:-3] + 'txt')
    origin_path = filename
    entry.delete(0, END)
    entry.insert(0, origin_path)

def open_destination_file(entry):
  
  global first_ext

  options = {}
  if first_ext == 'txt':
    options['defaultextension'] = '.hff'
    options['filetypes'] = [('Huffman-compressed files [.hff]', '.hff')]
  elif first_ext == 'hff':
    options['defaultextension'] = '.txt'
    options['filetypes'] = [('text files [.txt]', '.txt')]                    
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = filedialog.asksaveasfilename(**options)
  
  if filename:
    entry.delete(0, END)
    entry.insert(0, filename)


  # ~~~~~~ GUI ~~~~~~~~
root = Tk()
root.title('Huffman Compressor')
# geometry of the window
# "width x height + hor_pos + ver_pos"
root.geometry("750x150+250+300")

mf = Frame(root)
mf.pack()

f1 = Frame(mf, width=500, height=50)
f1.pack(fill=X) # make all widgets as wide as the parent widget
f2 = Frame(mf, width=500, height=50)
f2.pack()

# sticky: to change the fact that widgets are centered in their cells
# N(north), S(south), E(east), W(west)
Label(f1,text="Select origin file").grid(row=0, column=0, sticky='e')
e1 = Entry(f1, width=75, textvariable=origin_path)
e1.grid(row=0,column=1,padx=2,pady=1,sticky='ew',columnspan=25)

Label(f1,text="Select destination file").grid(row=1, column=0, sticky='e')
e2 = Entry(f1, width=75, textvariable='')
e2.grid(row=1,column=1,padx=2,pady=1,sticky='ew',columnspan=25)

b1 = Button(f2, text="Compress", width=25, command=lambda: compression())
b1.grid(row=2, column=2,sticky='ew', padx=5)
b2 = Button(f2, text="Decompress", width=25, command=lambda: decompression())
b2.grid(row=2, column=3, sticky='ew', padx=5)

Button(f1, text="...", command=lambda: open_origin_file(e1, e2)).grid(row=0, column=27, sticky='ew', padx=8, pady=4)
Button(f1, text="...", command=lambda: open_destination_file(e2)).grid(row=1, column=27, sticky='ew', padx=8, pady=4)

root.mainloop()

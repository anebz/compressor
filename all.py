import os
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import operator
import json
import ast
import math

# ~~~~ GLOBAL VARIABLES ~~~~
origin_path = ''
first_ext = '' # first extension of the origin file
zeros = 0 # redundancies to be added in the code
num = 7 # # bits to be used for encoding
b = [0,0] # global variable for the buttons
e = [0,0] # global variable for the entries
bites = 0
maxbites = 0

# ~~~~ COMPRESSION FUNCTIONS ~~~~
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

# given a tree and words being the string read from the file, returns a compressed string
def encode(tree,words, progress):
  global zeros
  progress.grid(row=2, column=2,sticky='ew', padx=5)
  progress.pack()
  progress["value"] = 0
  maxbytes = 50000
  progress["maximum"] = 5000
  code = ''
  counter = 0
  bites = 0
  for let in words:
    counter += 1
    if let in tree.keys():
      code = code + str(tree[let])
    if counter > len(words)/100 and bites < maxbytes:
      counter = 0
      bites += 500
      progress["value"] = bites
      

  # add redundant zeroes
  zeros = num - len(code)%num
  if len(code)%num != 0:
    code = code + '0000000'[len(code)%num:num]

  # from binary string to char string
  compressed = ''
  for i in range(0,len(code),num):
    compressed = compressed + chr(int(code[i:i+num],2) + 40)
  return compressed

def read_bytes(progress):
  '''simulate reading 500 bytes; update progress bar'''
  global bites, maxbites
  bites += 500
  progress["value"] = bites
  if bites < maxbites:
    # read more bytes after 100 ms
    after(100, read_bytes)

def compression(progress):
  #progress bar
  global bites, maxbites

  
  # get the values from the entries
  origin_data = open(e[0].get(), 'r', encoding='utf-8').read()
  destination_path = e[1].get()
  origin_data += ' '
  
  # Tree generation and encoding
  tree, encodingTree = constructHuffmanTree(origin_data)
  compressed = encode(encodingTree,origin_data, progress)
  print("Compresion rate:", math.fabs(1 - (len(compressed)/len(origin_data)))*100, "%")

  tree['999'] = zeros # save zeros in tree for future use

  # write in file
  f = open(destination_path, 'w', encoding='utf-8')
  json.dump(tree, f) # dump tree
  f.write(compressed)
  f.close()



# ~~~~ DECOMPRESSION FUNCTIONS ~~~~
def decode(text, tree):
  # string to code
  code = ''
  for e in text:
    auxcode = bin(ord(e)-40)[2:]
    if len(auxcode) != num:
      auxcode = '0'*(num-len(auxcode)) + auxcode
    code += auxcode
  code = code[:(len(code)-tree['999'])] # deleting the redundancies

  # code to decompressed string
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
  return text[:-1]
  
def decompression(progress):

  #progress bar
  progress.grid(row=2, column=2,sticky='ew', padx=5)
  progress.pack()

  
  # get the values from the entries
  origin_data = open(e[0].get(), 'r', encoding='utf-8').read()
  destination_path = e[1].get()

  text_from_file = 'r' + origin_data # to escape newline characters

  # extract dict (tree) from the string read from the file
  cnt = 0
  for i in range(1,len(text_from_file)):
    if text_from_file[i] == '{':
      cnt += 1
    elif text_from_file[i] == '}':
      cnt -= 1
    if cnt == 0:
      tree2 = ast.literal_eval(text_from_file[1:i+1])
      break;
  text_from_file = text_from_file[i+1:] # the encoded text

  decoded = decode(text_from_file, tree2)

  f = open(destination_path, 'w', encoding='utf-8')
  f.write(decoded)
  f.close()

  print(open('text_sample.txt', encoding='utf-8').read() == decoded)


# ~~~~ GUI FUNCTIONS ~~~~
def open_origin_file():
  global origin_path
  options = {}
  options['filetypes'] = [('text files [.txt]', '.txt'),('Huffman-compressed files [.hff]', '.hff')]
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = filedialog.askopenfilename(**options)

  if filename: # if filename exists
    first_ext = filename[-3:] # get extension
    e[1].delete(0, END)
    # change button states depending on the extension of the origin file
    if first_ext == 'txt':
      b[0].config(state = 'active')
      b[1].config(state = 'disabled')
      e[1].insert(0, filename[:-3] + 'hff')
    elif first_ext == 'hff':
      b[0].config(state = 'disabled')
      b[1].config(state = 'active')
      e[1].insert(0, filename[:-3] + 'txt')
    origin_path = filename
    e[0].delete(0, END)
    e[0].insert(0, origin_path)

def open_destination_file():
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
    e[0].delete(0, END)
    e[0].insert(0, filename)




  # ~~~~~~ MAIN ~~~~~~~~
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
f3 = Frame(mf, width=500, height=50, pady = 10)
f3.pack()

# sticky: to change the fact that widgets are centered in their cells
# N(north), S(south), E(east), W(west)
Label(f1,text="Select origin file").grid(row=0, column=0, sticky='e')
e[0] = Entry(f1, width=75, textvariable=origin_path) # entry for origin file
e[0].grid(row=0,column=1,padx=2,pady=1,sticky='ew',columnspan=25)

Label(f1,text="Select destination file").grid(row=1, column=0, sticky='e')
e[1] = Entry(f1, width=75, textvariable='') # entry for destination file
e[1].grid(row=1,column=1,padx=2,pady=1,sticky='ew',columnspan=25)

progress = ttk.Progressbar(f3, orient="horizontal", length=700, mode="determinate")

b[0] = Button(f2, text="Compress", width=25, command=lambda: compression(progress)) # compression button
b[0].grid(row=2, column=2,sticky='ew', padx=5)
b[1] = Button(f2, text="Decompress", width=25, command=lambda: decompression(progress)) # decompression button
b[1].grid(row=2, column=3, sticky='ew', padx=5)

Button(f1, text="...", command=lambda: open_origin_file()).grid(row=0, column=27, sticky='ew', padx=8, pady=4)
Button(f1, text="...", command=lambda: open_destination_file()).grid(row=1, column=27, sticky='ew', padx=8, pady=4)

# do this as last thing
root.mainloop() # so that the GUI is always waiting for input

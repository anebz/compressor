## GUI for python2.7

import os
from tkinter import *
from tkinter import filedialog
import operator
import json
import ast

# ~~~~ GLOBAL VARIABLES ~~~~
origin_path = ''
origin_data = ''
destination_path = ''
destination_data = ''
zeros = 0

# ~~~~ COMPRESSION FUNCTIONS ~~~~

# should be a .txt
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
  for i in range(10000):
    if string.count(chr(i)):
      freq[chr(i)] = string.count(chr(i))*1.0/leng
  if string.count('’'):
    freq['’'] = string.count('’')*1.0/leng
  return freq

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

def code_to_string(code):
  global zeros 
  zeros = len(code)%8
  compressed = ''
  if zeros != 0: # not a multiple of 8
    code = code + '0'*zeros # add zeroes, redundancies
  #print(code.find(tree['-'],0))
  for i in range(0,len(code),8):
##    if code[i:i+8] == tree['-']:
##      print('found it')
    compressed = compressed + chr(int(code[i:i+8],2))
  return compressed

#Decoding function
def decode(tree2, code):
  tree = {value:key for key,value in tree2.items()}
  text,add = '',''
  for i in range(len(code)):    
    add += code[i]
    if add in tree.keys():
      text += tree[add]
      add = ''
  return text

# returns the second smallest element in a numeric list
def second_smallest(numbers):
  return sorted(numbers,key=float)[1]

def string_to_code(text):
  code = ''
  for e in text:
    code += "{0:b}".format(ord(e))
  return code


def compression():

  global origin_data #original text
  global destination_path
  
  #Constructing the tree
  characterCounter = frequency(origin_data)
  tree = constructHuffmanTree(origin_data, characterCounter)

  code = encode(tree,origin_data)

  compressed = code_to_string(code)
  print("Compresion rate:", len(compressed)/len(origin_data))

  # write in file
  tree['999'] = zeros
  writefile(destination_path, tree, compressed)
  

def decompression():
    
  global origin_data #original text
  global destination_path


  text2 = origin_data
  tree2 = ast.literal_eval(text2[:text2.find('}')+1])
  zeros2 = tree2['999']

  text2 = text2[text2.find('}'):(len(text2)-zeros2+1)] # the encoded text
  code2 = string_to_code(text2)

  decoded = decode(tree2, code2)


  writefile(destination_path, {}, decoded)

  ##for i in range(len(original_text)):
  ##  if decoded[i] != original_text[i]:
  ##    print(i,decoded[i],original_text[i])
  ##    break

  print ("Compression was good?",origin_data == decoded)


# ~~~~ GUI FUNCTIONS ~~~~
def open_origin_file(path, entry):

  global origin_data
  global origin_path

  options = {}
  options['defaultextension'] = '.txt'
  options['filetypes'] = [('text files', '.txt'),('Huffman-compressed files', '.hff')]
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = filedialog.askopenfilename(**options)

  if filename:
    origin_data = open(filename, 'r', encoding='utf-8').read()
    origin_path = filename
    entry.delete(0, END)
    entry.insert(0, origin_path)


def open_destination_file(path, entry):
  
  global destination_data
  global destination_path

  options = {}
  options['defaultextension'] = '.hff'
  options['filetypes'] = [('text files', '.txt'),('Huffman-compressed files', '.hff')]
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = filedialog.asksaveasfilename(**options)
  
  if filename:
    destination_data = open(filename, 'w', encoding='utf-8')
    destination_path = filename
    entry.insert(0, destination_path)


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
entry1 = Entry(f1, width=75, textvariable=origin_path)
entry1.grid(row=0,column=1,padx=2,pady=1,sticky='ew',columnspan=25)

Label(f1,text="Select destination file").grid(row=1, column=0, sticky='e')
entry2 = Entry(f1, width=75, textvariable=destination_path)
entry2.grid(row=1,column=1,padx=2,pady=1,sticky='ew',columnspan=25)

Button(f1, text="...", command=lambda: open_origin_file(origin_path, entry1)).grid(row=0, column=27, sticky='ew', padx=8, pady=4)
Button(f1, text="...", command=lambda: open_destination_file(destination_path, entry2)).grid(row=1, column=27, sticky='ew', padx=8, pady=4)

Button(f2, text="Compress", width=25, command=lambda: compression()).grid(row=2, column=2,sticky='ew', padx=5)
Button(f2, text="Decompress", width=25, command=lambda: decompression()).grid(row=2, column=3, sticky='ew', padx=5)
# state=DISABLED, 
# main
root.mainloop()
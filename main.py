# Imports
import operator
import pickle

# Global Variables
zeroes = ''

# should be a .txt
def readfile(filename):
  file = open(filename,'r') # 'r' for reading only
  str = file.read() #string with the whole text
  file.close()
  return str

def writefile(filename, string):
  f = open(filename, 'w')
  f.write(string)
  f.close()

# save other relevant information
def write_data(dic):
  dic[999] = zeroes
  with open('important_data.pickle', 'wb') as handle:
    pickle.dump(dic, handle, protocol=pickle.HIGHEST_PROTOCOL)

# read the important information. FILE MUST EXIST
def read_data():
  with open('important_data.pickle', 'rb') as handle:
    return pickle.load(handle)

# returns a list with the frequencies of each letter in the string
def frequency(string):
  freq, leng = {}, len(string)
  for i in range(127):
    if string.count(chr(i)):
      freq[chr(i)] = string.count(chr(i))*1.0/leng
  return freq
  
# given a tree in this format: {0:'a', 10:'b', 11:'c'}
# and words being the string read from the file
def encode(tree,words):
  inv_tree = {value:key for key,value in tree.items()}
  code = ''
  for let in words:
    if let in inv_tree:
      code = code + str(inv_tree[let])
  return code

def code_to_string(code):
  global zeroes 
  zeroes = len(code)%8
  compressed = ''
  if zeroes != 0: # not a multiple of 8
    code = code + '0'*zeroes # add zeroes, redundancies
  for i in range(0,len(code),8):
    compressed = encoded + chr(int(code[i:i+8],2))
  return compressed
 
# returns the second smallest element in a numeric list
def second_smallest(numbers):
  return sorted(numbers,key=float)[1]

# returns a list with the Huffman-encoded ASCII table
##def constructHuffmanTree(text, count):
##  savedCoding = [''] * len(count) # hay que pasarlo a diccionario, mas que a vector
##  aux = count
##  for ii in range(len(count)):
##    dictValues = aux.values()
##    smallestElementValue = min(dictValues)
##    secondSmallestElementValue = second_smallest(dictValues)
##    for key,value in aux:
##      if value == smallestElementValue or value == secondSmallestElementValue:
##        a = 1
##        # Aqui quiero hacer dos cosas. Primero, crear otro dicc llamado aux que tenga los mismos 
##            # elementos que count menos estos dos elementos, que estaran agrupados en un unico elemento
##            # que tenga los dos caracteres del nodo (ejemplo: si tiene a y b, seria un key ab) con value
##            # la suma de los values de cada key, asi hasta solo tener un unico nodo final. 
##            # Tambien mi idea es guardar en savedCoding dependiendo los keys que formen cada nodo la rama de codificacion
##            # '0' o '1', como los apuntes de clase
##
##	
  
# main
if __name__ == "__main__":
  # open file
  file = 'text_sample.txt'
  text = readfile(file)

  #print text
  
##  #Constructing the tree
##  characterCounter = frequency(text)
##  sortedCounter = sorted(characterCounter.items(), key=operator.itemgetter(1))
##  tree = constructHuffmanTree(text, sortedCounter)
  
  # example cases for encoding
  tree = {0:'a', 10:'b', 11:'c'}
  words = 'acbcab' 
  code = encode(tree,words)
  #print code

  compressed = code_to_string(code)

  write_data(tree)
  print read_data()

  # write in file
  extension = 'hff'
  ex_filename = 'result' + '.' + extension
  ex = open('text_sample.txt','r').read() #example to write
  writefile(ex_filename, ex)

  print zeroes

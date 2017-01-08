# Imports
import operator

# should be a .txt
def readfile(filename):
  file = open(filename,'r') # 'r' for reading only
  str = file.read() #string with the whole text
  return str

def writefile(filename, string):
  f = open(filename, 'w')
  f.write(string)
  f.close()

# returns a list with the frequencies of each letter in the string
# returns a list with the frequencies of each letter in the string
def frequency(string):
  freq, leng = {}, len(string)
  for i in range(127):
    if string.count(chr(i)):
      freq[chr(i)] = string.count(chr(i)*1.0/leng)
  return freq
  
# given a tree in this format: {0:'a', 10:'b', 11:'c'}
# and words being the string, read from the file
def encode(tree,words):
  inv_tree = {value:key for key,value in tree.items()}
  code = ''
  for let in words:
    if let in inv_tree:
      code = code + str(inv_tree[let])
  return code

# returns a list with the Huffman-encoded ASCII table
def ConstructHuffmanTree(text, count):
  
  

if __name__ == "__main__":
  # open file
  file = 'text_sample.txt'
  text = openfile(file)
  file.close()
  #print text
  
  #Constructing the tree
  characterCounter = frequency(text)
  sortedCounter = sorted(characterCounter.items(), key=operator.itemgetter(1))
  tree = constructHuffmanTree(text, sortedCounter)
  
  # example cases for encoding
  tree = {0:'a', 10:'b', 11:'c'}
  words = 'acbca' 
  code = encode(tree,words)
  # print code

  # write in file
  extension = 'hff'
  ex_filename = 'result' + '.' + extension
  ex = open('text_sample.txt','r').read() #example to write
  writefile(ex_filename, ex)
  

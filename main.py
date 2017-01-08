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
 
# returns the second smallest element in a numeric list
def second_smallest(numbers):
    m1, m2 = float('inf'), float('inf')
    for x in numbers:
        if x <= m1:
            m1, m2 = x, m1
        elif x < m2:
            m2 = x
    return m2
# returns a list with the Huffman-encoded ASCII table
def ConstructHuffmanTree(text, count):
  savedCoding = [''] * len(count) # hay que pasarlo a diccionario, mas que a vector
  aux = count
  for ii in range(len(count)):
	dictValues = aux.values()
	smallestElementValue = min(dictValues)
	secondSmallestElementValue = second_smallest(dictValues)
	for key,value in aux:
	  if value == smallestElementValue or value == secondSmallestElementValue:
	    # Aqui quiero hacer dos cosas. Primero, crear otro dicc llamado aux que tenga los mismos 
		# elementos que count menos estos dos elementos, que estaran agrupados en un unico elemento
		# que tenga los dos caracteres del nodo (ejemplo: si tiene a y b, seria un key ab) con value
		# la suma de los values de cada key, asi hasta solo tener un unico nodo final. 
		# Tambien mi idea es guardar en savedCoding dependiendo los keys que formen cada nodo la rama de codificacion
		# '0' o '1', como los apuntes de clase

	
  
# main
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
  

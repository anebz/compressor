# should be a .txt
def openfile(filename):
  file = open(filename,'r') # 'r' for reading only
  str = file.read() #string with the whole text
  return str

# given a tree in this format: {0:'a', 10:'b', 11:'c'}
# and words being the string read from the file
def encode(tree,words):
  inv_tree = {v:k for k,v in tree.items()}
  code = ''
  for let in words:
    if let in inv_tree:
      code = code + str(inv_tree[let])
  return code


if __name__ == "__main__":
  file = 'text_sample.txt'
  text = openfile(file)
  #print text
  
  # example cases
  tree = {0:'a', 10:'b', 11:'c'}
  words = 'acbca' 
  code =  encode(tree,words)
  # print code

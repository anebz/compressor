# Imports
import operator
import json
import ast
# Global Variables
zeros = 0

# should be a .txt
def readfile(filename):
  return open(filename, encoding='utf-8').read()

def writefile(filename, tree, string):
  f = open(filename, 'w', encoding='utf-8')
  json.dump(tree, f) # dump tree
  f.write(string)
  f.close()


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

def string_to_code(text):
  code = ''
  for e in text:
    code0 = bin(ord(e))[2:]
    if len(code0) != 8 and e != text[len(text)-1]:
      code0 = '0'*(8-len(code0)) + code0
    code += code0
  return code

## DECODING
file = 'result.hff'
text2 = readfile(file)
limit = text2.find('}')
tree2 = ast.literal_eval(text2[:limit+1])
zeros2 = tree2['999']

text2 = text2[limit+1:] # the encoded text

code2 = string_to_code(text2)
code2 = code2[:(len(code2)-zeros2+1)] # deleting the redundancies

decoded = decode(tree2, code2)

f = open('decompressed.txt', 'w', encoding='utf-8')
f.write(decoded)
f.close()

g = open('a1.txt', encoding='utf-8').read()

print(len(decoded),len(g))

for i in range(len(g)):
  if decoded[i] != g[i]:
    print(i,decoded[i],g[i])
    break



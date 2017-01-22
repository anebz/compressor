tree = {'0': {'0': {'0': {'0': 's', '1': ' '}, '1': {'0': 'r', '1': 'e'}}, '1': {'0': 'L', '1': 'm'}}, '1': {'0': {'0': 'u', '1': 'o'}, '1': {'0': 'p', '1': 'i'}}}
otree = {'p': '10', 'o': '01', 'i': '11', 'L': '10', 's': '000', ' ': '001', 'r': '010', 'e': '011', 'm': '11', 'u': '00'}
def decode(tree, code):
  node = tree
  text = ''
  for ii in code:
    if type(node[ii]) is dict:
      node = node[ii]
    elif type(node[ii]) is str:
      text += node[ii]
      node = tree
  return text

def encode(tree,words):
  code = ''
  for let in words:
    if let in tree.keys():
      code = code + str(tree[let])
  return code


code = '10010100111100111100000011'
ocode = encode(otree,'Lorem ipsum')
print(code)
print(ocode)

print(decode(tree,code))


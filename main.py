
def openfile(filename):

  file = open(filename,'r') # 'r' for reading only
  str = file.read() #string with the whole text
  return str

if __name__ == "__main__":
  text = openfile('text_sample.txt')
  print text

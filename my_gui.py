## GUI for python2.7

import os
from tkFileDialog import askopenfilename, askopenfile, asksaveasfilename
from Tkinter import *

# ~~~~ GLOBAL VARIABLES ~~~~
origin_path = ''
original_data = ''
destination_path = ''
destination_data = ''


# ~~~~ FUNCTIONS ~~~~
def open_origin_file(path, entry):

  global original_data
  global origin_path

  options = {}
  options['defaultextension'] = '.txt'
  options['filetypes'] = [('text files', '.txt')]
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = askopenfilename(**options)

  if filename:
    original_data = open(filename, 'r').read()
    origin_path = filename
    entry.delete(0, END)
    entry.insert(0, origin_path)


def open_destination_file(path, entry):
  
  global destination_data
  global destination_path

  options = {}
  options['defaultextension'] = '.hff'
  options['filetypes'] = [('Huffman-compressed file', '.hff')]
  options['initialdir'] = 'C:\\' + origin_path
  options['title'] = 'Choose file'
  
  filename = asksaveasfilename(**options)
  
  if filename:
    #destination_data = open(filename, 'w').read()
    destination_path = filename
    entry.insert(0, destination_path)

def process_file(content):
  print content


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

Button(f2, text="Compress", width=25, command=lambda: process_file(original_data)).grid(row=2, column=2,sticky='ew', padx=5)
Button(f2, text="Decompress", width=25, state=DISABLED, command=lambda: process_file(original_data)).grid(row=2, column=3, sticky='ew', padx=5)


root.mainloop()

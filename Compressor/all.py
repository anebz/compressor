import os
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
import tkinter as tk
import operator
import json
import ast
import math
import re

# ~~~~ GLOBAL VARIABLES ~~~~
origin_path = ''
destination_path = ''
first_ext = ''  # first extension of the origin file
zeros = 0  # redundancies to be added in the code
num = 7  # # bits to be used for encoding
b = [0, 0]  # global variable for the buttons
e = [0, 0]  # global variable for the entries
foldername = ''
allinfo = ''
files = []
dirs = []
dirpath = ''


# ~~~~ COMPRESSION FUNCTIONS ~~~~
# returns a list with the Huffman-encoded ASCII table
def constructHuffmanTree(text, progress):
	# returns a list with the frequencies of each letter in the string
	def frequencyLZW(string, progress):
		freq, leng = {}, len(string)
		progress["maximum"] += len(set(string)) * 50
		for i in set(re.findall(r'([\s\S][\s\S])', string)):
			progress["value"] += 50
			progress.update()
			if string.count(i):
				freq[i] = string.count(i) * 1.0 / leng
		return freq

	def frequency(string, progress):
		freq, leng = {}, len(string)
		progress["maximum"] += len(set(string)) * 50
		for i in set(string):
			progress["value"] += 50
			progress.update()
			if string.count(i):
				freq[i] = string.count(i) * 1.0 / leng
		return freq

	#count = frequencyLZW(text, progress)
	count = frequency(text, progress)
	auxTree = dict.fromkeys(count.keys(), '')
	savedCoding = dict()
	numbers = range(len(count) - 1)
	progress["maximum"] += len(numbers) * 50
	for ii in numbers:
		progress["value"] += 50
		progress.update()
		flag = 0
		auxDict = dict()
		dictValues = list(count.values())
		smallestElementValue = min(dictValues)
		secondSmallestElementValue = sorted(dictValues, key=float)[1]
		for key, value in count.items():
			if value == smallestElementValue or value == secondSmallestElementValue:
				flag += 1
				if flag == 1:
					node1 = key
					for jj in key:
						auxTree[jj] = '0' + auxTree[jj]
					if node1 in savedCoding.keys() and len(count) > 1:
						auxDict['0'] = savedCoding[node1]
					elif ii != len(count) > 1:
						auxDict['0'] = node1
				elif flag == 2:
					node2 = key
					for jj in key:
						auxTree[jj] = '1' + auxTree[jj]
					if node2 in savedCoding.keys() and len(count) > 1:
						auxDict['1'] = savedCoding[node2]
					elif len(count) > 1:
						auxDict['1'] = node2
					break
		count[node1] = count[node1] + count[node2]
		newLetter = node1 + node2
		count[newLetter] = count[node1]
		del count[node1]
		del count[node2]
		if len(count) > 1:
			savedCoding[newLetter] = auxDict
		else:
			if len(savedCoding) < 2:
				if node1 in savedCoding.keys():
					savedCoding[node2] = auxTree[node2]
				else:
					savedCoding[node1] = auxTree[node1]
		del auxDict
		if node1 in savedCoding.keys() and ii != numbers[-1]:
			del savedCoding[node1]
		if node2 in savedCoding.keys() and ii != numbers[-1]:
			del savedCoding[node2]
	finalKeys = list(savedCoding.keys())
	for jj in range(len(finalKeys)):
		if type(savedCoding[finalKeys[jj]]) is dict:
			savedCoding[auxTree[finalKeys[jj][0]][0]] = savedCoding.pop(finalKeys[jj])
		else:
			savedCoding[auxTree[finalKeys[jj][0]][0]] = finalKeys[jj]
			savedCoding.pop(finalKeys[jj])
	return savedCoding, auxTree


def compression(progress):

	# given a tree and words being the string read from the file, returns a compressed string
	def encode(tree, words, progress):
		# replace each char by its value in the tree (binary string)
		code = ''.join(tree[c] for c in words)

		# add redundant zeroes
		zeros = num - len(code) % num
		if len(code) % num != 0 and zeros != num:
			code = code + '0000000'[len(code) % num:num]
		else:
			zeros = 0

		# from binary string to char string
		compressed = ''.join(chr(int(code[i:i + num], 2) + 40) for i in range(0, len(code), num))

		progress["value"] += 4900
		progress.update()

		return compressed, zeros

	def foldercompression():
		def getallinfo(dirpath): #enhancement: use this iteration to save strings somehow?
			global allinfo
			# go through the folder and all folders and files under it
			for (dirpath, dirnames, filenames) in os.walk(dirpath):
				dirs = dirnames
				files = filenames
				break
			foldername = dirpath[dirpath.rfind('/') + 1:]
			# allinfo: all strings from all files together, now need to create the tree for all files
			for file in files:
				if '.txt' in file:
					allinfo += open(dirpath + '/' + file, 'r', encoding='utf-8').read()
			# recursive if there is a folder below current folder
			for folder in dirs:
				getallinfo(dirpath + '/' + folder)

		def recursive_compression(dirpath, f, encodingTree):
			for (dirpath, dirnames, filenames) in os.walk(dirpath):
				dirs = dirnames
				files = filenames
				break

			f.write('{foldername: ' + dirpath[dirpath.rfind('/') + 1:] + '}')  # name of current folder
			for folder in dirs:  # loop for all folders under current folder
				recursive_compression(dirpath + '/' + folder, f, encodingTree)

			for filename in files:  # loop for all the files
				if '.txt' in filename:
					compressed, zeros = encode(encodingTree, open(dirpath + '/' + filename, 'r', encoding='utf-8').read(), progress)
					f.write('{file' + str(zeros) + ': ' + filename + '}')  # writing filename and zeros at the same time
					f.write(compressed)
			f.write('{}')  # keyword to represent end of folder

		global dirpath
		progress["maximum"] = 5000
		progress["value"] = 0

		# create tree with complete string from all files under all folders
		getallinfo(dirpath)
		tree, encodingTree = constructHuffmanTree(allinfo, progress)

		f = open(destination_path, 'w', encoding='utf-8')
		tree['999'] = 0  # save zeros in tree for future use
		#finalTree = json.dumps(tree).replace(' ', '')  # dump tree
		#finalTree = finalTree.replace('""', '" "')
		#f.write(finalTree)
		json.dump(tree, f)
		# recurisvely compress everything under current folder
		recursive_compression(dirpath, f, encodingTree)
		messagebox.showinfo("Message", "Compression finished")


	# progress bar
	global destination_path
	progress.grid(row=2, column=2, sticky='ew', padx=5)
	progress.pack()
	progress["value"] = 0
	progress.update()
	progress["maximum"] = 5000

	# get the values from the entries
	destination_path = e[1].get()
	if dirpath != '':
		foldercompression()
		return
	origin_data = open(e[0].get(), 'r', encoding='utf-8').read()
	tree, encodingTree = constructHuffmanTree(origin_data, progress)
	compressed, zeros = encode(encodingTree, origin_data, progress)
	#print("Compresion rate:", math.fabs(1 - (len(compressed) / len(origin_data))) * 100, "%")

	tree['999'] = zeros  # save zeros in tree for future use

	f = open(destination_path, 'w', encoding='utf-8')
	#finalTree = json.dumps(tree).replace(' ', '')  # dump tree
	#finalTree = finalTree.replace('""', '" "')
	#f.write(finalTree)
	json.dump(tree, f)
	f.write(compressed)
	f.close()
	progress["value"] += 50
	progress.update()
	messagebox.showinfo("Message", "Compression finished")




# ~~~~ DECOMPRESSION FUNCTIONS ~~~~
def decompression(progress):

	def decode(text, zeros, tree, progress):

		# string to code
		progress["maximum"] = 90500
		code = ''
		cont = 0
		for e in text:
			cont += 1
			if cont > len(text) / 100:
				progress["value"] += 100
				progress.update()
				cont = 0
			auxcode = bin(ord(e) - 40)[2:]
			if len(auxcode) != num:
				auxcode = '0' * (num - len(auxcode)) + auxcode
			code += auxcode
		code = code[:(len(code) - zeros)]  # deleting the redundancies

		# code to decompressed string
		node = tree
		text = ''
		cont = 0
		for ii in code:
			cont += 1
			if cont > len(code) / 800:
				progress["value"] += 100
				progress.update()
				cont = 0
			if ii not in node:
				return text
			elif type(node[ii]) is dict:
				node = node[ii]
			elif type(node[ii]) is str:
				text += node[ii]
				node = tree
		return text

	def folderdecompression(text, dirpath, progress):

		global destination_path, zeros

		if text.startswith('{foldername: '):
			foldername = text[13:text.find('}')] #enhancement: regex
			text = text[text.find('}') + 1:]
			# create folder
			if destination_path[-1] != '/':
				destination_path += '/'
			newdir = destination_path[:destination_path.rfind('/') + 1] + foldername + '/'
			if os.path.exists(newdir):
				messagebox.showinfo("Error", "Folder already exists! Choose another directory")
				return

			# decompress and write file for each file
			os.makedirs(newdir)
			while (text):

				if text.startswith("{}"):
					# go one folder up
					newdir = newdir[:newdir.rfind('/', 0, newdir.rfind('/')) + 1] #TODO regex needed!
					text = text[text.find('}') + 1:]  # shorten text

				#first check foldernames --> list of all foldernames
				if text.startswith("{foldername: "):
					newf = re.findall(r'{foldername:\s([\w\d]+)}', text)[0]
					if newdir[-1] != '/':
						newdir += '/'
					newdir += newf + '/'
					os.makedirs(newdir)
					text = text[text.find('}') + 1:] # shorten text

				if text.startswith("{file"):

					#TODO: regex
					zeros = int(text[text.find('{file') + 5])
					filename = re.findall(r'{file\d:\s([^}]+)}', text)[0]
					text = text[text.find('}') + 1:]  # shorten text

					#TODO: improvable
					idx = 0
					while 1:
						#TODO: need to check with real example
						if text[text.find('{', idx) + 1] == 'f' or text[text.find('{', idx) + 1] == '}':
							decodt = text[:text.find('{', idx)]
							break
						else:
							idx = text.find('{', idx) + 1

					decoded = decode(decodt, zeros, tree2, progress)
					f = open(newdir + filename, 'w', encoding='utf-8')
					f.write(decoded)
					f.close()

					# TODO: improve this
					text = text[text.find(decodt) + len(decodt):]  # shorten text
		return

	global zeros, destination_path

	# progress bar
	progress["value"] = 0
	progress.update()
	# get the values from the entries
	origin_data = open(e[0].get(), 'r', encoding='utf-8').read()
	destination_path = e[1].get()

	text_from_file = 'r' + origin_data  # to escape newline characters

	# extract dict (tree) from the string read from the file
	#cnt = 0
	# USE REGEX (^.*?"999":.*?\})(.*)
	#################### OLD VERSION WORKS!!
	#for i in range(1, len(text_from_file)):
	#	if text_from_file[i] == '{':
	#		cnt += 1
	#	elif text_from_file[i] == '}':
	#		cnt -= 1
	#	if cnt == 0:
	#		tree2 = ast.literal_eval(text_from_file[1:i + 1])
	#		break;
	#text_from_file = text_from_file[i + 1:]  # the encoded text
	################## NEW VERSION, WIP??
	matches = re.search(r'(^.*?"999":.*?\})(.*)',text_from_file)
	tree2 = ast.literal_eval(matches.group(1)[1:])
	text_from_file = matches.group(2)  # the encoded text
	#############################
	if re.match(r'\{foldername:\s(\w+)\}', text_from_file): # 1+ file mode
		folderdecompression(text_from_file, origin_data, progress)

	else:  # single text mode
		zeros = tree2['999']
		decoded = decode(text_from_file, zeros, tree2, progress)

		f = open(destination_path, 'w', encoding='utf-8')
		f.write(decoded)
		f.close()

	progress["value"] = progress["maximum"]
	progress.update()
	messagebox.showinfo("Message", "Decompression finished")


# ~~~~ GUI FUNCTIONS ~~~~
def open_origin_file():
	global origin_path
	options = {}
	options['filetypes'] = [('text files [.txt]', '.txt'), ('Huffman-compressed files [.hff]', '.hff')]
	options['initialdir'] = os.getcwd()
	options['title'] = 'Choose file'

	filename = filedialog.askopenfilename(**options)

	if filename:  # if filename exists
		first_ext = filename[-3:]  # get extension
		e[1].delete(0, END)
		# change button states depending on the extension of the origin file
		if first_ext == 'txt':
			b[0].config(state='active')
			b[1].config(state='disabled')
			e[1].insert(0, filename[:-3] + 'hff')
		elif first_ext == 'hff':
			b[0].config(state='disabled')
			b[1].config(state='active')
			e[1].insert(0, filename[:-3] + 'txt')
		origin_path = filename
		e[0].delete(0, END)
		e[0].insert(0, origin_path)


# open all files under dir
def open_origin_dir():
	global origin_path, foldername, allinfo, dirpath
	dirpath = filedialog.askdirectory()
	files = []

	e[0].delete(0, END)
	e[0].insert(0, dirpath)


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
		e[1].delete(0, END)
		e[1].insert(0, filename)




	# ~~~~~~ MAIN ~~~~~~~~

root = Tk()
root.title('Huffman Compressor')
# geometry of the window
# "width x height + hor_pos + ver_pos"
root.geometry("750x150+250+300")

mf = Frame(root)
mf.pack()

f1 = Frame(mf, width=500, height=50)
f1.pack(fill=X)  # make all widgets as wide as the parent widget
f2 = Frame(mf, width=500, height=50)
f2.pack()
f3 = Frame(mf, width=500, height=50, pady=10)
f3.pack()

# sticky: to change the fact that widgets are centered in their cells
# N(north), S(south), E(east), W(west)
Label(f1, text="Select origin file").grid(row=0, column=0, sticky='e')
e[0] = Entry(f1, width=75, textvariable=origin_path)  # entry for origin file
e[0].grid(row=0, column=1, padx=2, pady=1, sticky='ew', columnspan=25)

Label(f1, text="Select destination file").grid(row=1, column=0, sticky='e')
e[1] = Entry(f1, width=75, textvariable='')  # entry for destination file
e[1].grid(row=1, column=1, padx=2, pady=1, sticky='ew', columnspan=25)

progress = ttk.Progressbar(f3, orient="horizontal", length=700, mode="determinate")

b[0] = Button(f2, text="Compress", width=25, command=lambda: compression(progress))  # compression button
b[0].grid(row=2, column=2, sticky='ew', padx=5)
b[1] = Button(f2, text="Decompress", width=25, command=lambda: decompression(progress))  # decompression button
b[1].grid(row=2, column=3, sticky='ew', padx=5)

Button(f1, text="file", command=lambda: open_origin_file()).grid(row=0, column=27, sticky='ew', padx=8, pady=4)
Button(f1, text="...", command=lambda: open_destination_file()).grid(row=1, column=27, sticky='ew', padx=8, pady=4)
Button(f1, text="dir", command=lambda: open_origin_dir()).grid(row=0, column=35, sticky='ew', padx=8, pady=4)

# do this as last thing
root.mainloop()  # so that the GUI is always waiting for input

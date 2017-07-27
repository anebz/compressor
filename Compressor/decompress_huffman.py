import re
import ast
zeros = 0
num = 7
def decompression(text_from_file):
	def decode(text, tree):
		# string to code
		global zeros
		global num
		code = ''
		cont = 0
		for e in text:
			cont += 1
			if cont > len(text) / 100:
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
				cont = 0
			if ii not in node:
				return text
			elif type(node[ii]) is dict:
				node = node[ii]
			elif type(node[ii]) is str:
				text += node[ii]
				node = tree
		return text

	def folderdecompression(text, dirpath):
		global zeros
		if text.startswith('{foldername: '):
			text = text[:-2]  # delete the last '{}'
			foldername = text[13:text.find('}')]
			# create folder
			newdir = destination_path[:destination_path.rfind('/') + 1] + foldername
			if os.path.exists(newdir):
				messagebox.showinfo("Error", "Folder already exists! Choose another directory")
				return

			# decompress and write file for each file
			os.makedirs(newdir)
			while (1):
				zeros = int(text[text.find('{file') + 5])
				text = text[text.find('{file') + 5:]
				lastpoint = text.find('}')
				filename = text[3:lastpoint]
				text = text[lastpoint + 1:]

				if text.find('{file') != -1:
					decoded = decode(text[:text.find('{file')], tree2)
					f = open(newdir + '/' + filename, 'w', encoding='utf-8')
					f.write(decoded)
				else:
					decoded = decode(text, tree2)
					f = open(newdir + '/' + filename, 'w', encoding='utf-8')
					f.write(decoded)
					f.close()
					break;
		return

	# progress bar
	# get the values from the entries
	text_from_file = 'r' + text_from_file  # to escape newline characters

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
	################## NEW VERSION, WIP
	matches = re.search(r'(^.*?"999":.*?\})(.*)',text_from_file)
	tree = ast.literal_eval(matches.group(1)[1:])
	text_from_file = matches.group(2)  # the encoded text
	#############################

	global zeros
	zeros = tree['999']
	decoded = decode(text_from_file, tree)
	return decoded
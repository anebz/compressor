##import os
### Create a list of directory entries
##dir_name = 'C:\\Users\\anee\\Desktop'
##fList = os.listdir(dir_name)
### The directory entries do not include the full path
### Create a list of file names with full path, eliminating subdirectory entries
##fList1 = [os.path.join(dir_name, f) for f in fList if os.path.isfile(os.path.join(dir_name, f))]
##
##print(fList1)


##import os
##for filename in os.listdir(os.getcwd()):
##  print (filename)
import os
import glob
path = 'C:\\Users\\anee\\Documents\\GitHub\\Huffman-compressor\\Folder'

import os.path
dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
print(dirs)


import os
f = []
d = []
for (dirpath, dirnames, filenames) in os.walk(path):
    f.extend(filenames)
    d.extend(dirnames)
    break
print(d)

##for filename in os.listdir(path):
##  print(filename)
##
##print('\n')
##for filename in glob.glob(os.path.join(path, '*.txt')):
##  print(filename)

import os
import json
import re

zeros = 0

def compression(origin_data):
	# given a tree and words being the string read from the file, returns a compressed string
    def encode(tree, words):
        global zeros
        code = ''.join(tree[c] for c in words)  # replace each char by its value in the tree
        num = 7
        zeros = num - len(code) % num
        if len(code) % num != 0 and zeros != num:
            code = code + '0000000'[len(code) % num:num]
        else:
            zeros = 0
        # from binary string to char string
        compressed = ''.join(chr(int(code[i:i + num], 2) + 40) for i in range(0, len(code), num))
        return compressed
    def constructHuffmanTree(text):
        # returns a list with the frequencies of each letter in the string
        def frequencyLZW(string):
            freq, leng = {}, len(string)
            for i in set(re.findall(r'([\s\S][\s\S])', string)):
                if string.count(i):
                    freq[i] = string.count(i) * 1.0 / leng
            return freq

        def frequency(string):
            freq, leng = {}, len(string)
            for i in set(string):
                if string.count(i):
                    freq[i] = string.count(i) * 1.0 / leng
            return freq

        # count = frequencyLZW(text, progress)
        count = frequency(text)
        auxTree = dict.fromkeys(count.keys(), '')
        savedCoding = dict()
        numbers = range(len(count) - 1)
        for ii in numbers:
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
	# get the values from the entries
    global zeros
    tree, encodingTree = constructHuffmanTree(origin_data)
    compressed = encode(encodingTree, origin_data)
    tree['999'] = zeros  # save zeros in tree for future use
    finalTree = json.dumps(tree).replace(' ', '')  # dump tree
    finalTree = finalTree.replace('""', '" "')  # dump tree
    return finalTree + compressed

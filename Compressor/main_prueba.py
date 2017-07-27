import compress_file
import decompress_huffman
f = open('text_sample.txt', 'r', encoding='utf-8')
texto = f.read()
f.close()
compressed = compress_file.compression(texto)
decompressed = decompress_huffman.decompression(compressed)
print( texto == decompressed )
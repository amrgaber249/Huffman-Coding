import os
import sys
import heapq
import time


class HuffmanNode(object):
    def __init__(self, frequency, char=None):
        self.char = char
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, node):
        if node is None or not isinstance(node, HuffmanNode):
            return -1
        return self.frequency < node.frequency

    def set_children(self, left, right):
        self.left = left
        self.right = right


def string2bits(s=''):
    bits_list=[]
    for x in s:
        decimal = ord(x)
        if decimal >= 160:
            decimal -= 160
        bits_list.append(bin(decimal)[2:].zfill(7))
    return bits_list


def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])


def readfile(file):
    path = os.path.join(sys.path[0], file)
    with open(path, "r") as rfile:
        textfile = rfile.read()
        frequency = {}
        for char in textfile:
            if char not in frequency:
                frequency[char] = 0
            frequency[char] += 1
    return textfile, frequency


def read_encodedfile(file):
    path = os.path.join(sys.path[0], file)
    with open(path, "r") as rfile:
        encoded_tree = rfile.readline()[:-1].split(',')
        remainder = encoded_tree[-1]
        encoded_tree = encoded_tree[:-1]
        frequency = {}
        for i in range(0, len(encoded_tree), 2):
            frequency[chr(int(encoded_tree[i]))] = int(encoded_tree[i+1])
        encoded_msg = rfile.readline()
        msg = ''
        for bits in string2bits(encoded_msg):
            msg += bits
        fix_last_chr = msg[-7:][int(remainder):]
        msg = msg[:-7] + fix_last_chr
    return msg, frequency


def encodeTree(root, current_code=''):
    if root is None:
        return
    if root.char is not None:
        encoded_code[root.char] = current_code
        return
    encodeTree(root.left, current_code + "0")
    encodeTree(root.right, current_code + "1")


def decodeTree(root, current_code=''):
    if root is None:
        return
    if root.char is not None:
        decoded_code[current_code] = root.char
        return
    decodeTree(root.left, current_code + "0")
    decodeTree(root.right, current_code + "1")


def buildTree(frequency, type):
    heap = []
    for key, value in frequency.items():
        heapq.heappush(heap, HuffmanNode(value, key))
    heapq.heapify(heap)
    while(len(heap)) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_frequency = left.frequency + right.frequency
        new_node = HuffmanNode(new_frequency)
        new_node.set_children(left, right)
        heapq.heappush(heap, new_node)
    heap_root = heapq.heappop(heap)
    encodeTree(heap_root) if type == 0 else decodeTree(heap_root)


def ascii_helper(encoded_file):
    bits = ''
    bits_list = []
    for char in encoded_file:
        bits += char
        if len(bits) % 7 == 0:
            decimal = int(bits,2)
            if decimal < 32:
                bits = str(bin(decimal + 160)[2:])
            bits_list.append(bits)
            bits=''
    remainder = 0
    if len(bits)!= 0:
        remainder = 7 - len(bits) % 7
        decimal = int(bits,2)
        if decimal < 32:
            bits = str(bin(decimal+160)[2:])
        bits_list.append(bits.zfill(7))
    ascii_str = bits2string(bits_list)
    return ascii_str, remainder


def compress(path):
    tic = time.time()
    textfile, frequency = readfile(path)
    frequency = {key: value for key, value in sorted(frequency.items(), key=lambda item: item[1])}
    buildTree(frequency, 0)
    print()
    print(' {0:<4} | {1:<8} | {2:<32} '.format('Byte:','Code:','New Codes:'))
    print('_______|__________|____________')
    for key, value in frequency.items():
        hex_code = hex(ord(key))
        bin_code = bin(ord(key))
        print(' {:2}    | {} | {} '.format(hex_code[2:], bin_code[2:].zfill(8), encoded_code[key]))

    with open('encoded.txt', "w") as wfile:
        char_val=''
        for key, value in frequency.items():
            char_val += "{},{},".format(ord(key), value)
        encoded_file = ''
        for char in textfile:
            encoded_file += str(encoded_code[char])
        code_length = len(encoded_file)
        encoded_file, remainder = ascii_helper(encoded_file)
        wfile.write(char_val + str(remainder))
        wfile.write('\n')
        wfile.write(encoded_file)
    compression_ratio = 100 - (os.path.getsize('encoded.txt')/os.path.getsize(path)) * 100
    toc = time.time()
    original_length = len(textfile)
    length_compression_ratio = (code_length / (original_length * 8)) * 100
    print()
    print()
    print('SUCCESSFUL COMPRESSION !!!')
    print('bits compression ratio: {:.2f}%'.format(length_compression_ratio))
    print('file compression ratio: {:.2f}%'.format(compression_ratio))
    print('time elapsed          : {:.4f} sec'.format(toc-tic))
    print()


def decompress(path):
    tic = time.time()
    encoded_msg, frequency = read_encodedfile(path)
    buildTree(frequency,1)
    with open('decoded.txt', "w") as wfile:
        decoded_msg=''
        for bit in encoded_msg:
            decoded_msg += bit
            if decoded_msg in decoded_code.keys():
                wfile.write(decoded_code[decoded_msg])
                decoded_msg = ''
    toc = time.time()
    print()
    print()
    print('SUCCESSFUL DECOMPRESSION !!!')
    print()
    print('time elapsed     : {:.4f} sec'.format(toc-tic))
    print()


while 1:
    print()
    print('###############################')
    print('#        HUFFMAN CODING       #')
    print('###############################')
    print()
    print()
    flag = input('Do you want to \'C\'compress, \'D\'ecompress or \'E\'xit\n>>> ')
    print()
    if flag == 'e' or flag == 'E':
        print('GOODBYE & HAVE A NICE DAY :D')
        print('          ZA WARUDO         ')
        print()
        break
    else:
        file=input("enter file name: ")
        if file not in os.listdir(sys.path[0]):
            print()
            print()
            print("FILE NOT FOUND, TRY AGAIN !!!")
            print()
            print()
            continue
        if flag == 'd' or flag == 'D':
            decoded_code = {}
            decompress(file)
        else:
            encoded_code = {}
            compress(file)



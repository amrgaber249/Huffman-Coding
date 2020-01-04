import heapq, timeit
import pickle, os

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


def compress_folder(path):
    f = 0
    begin_time = timeit.timeit()
    for fname in os.listdir(path):
        begin_time = timeit.timeit()

        bytes, frequency = readFile(path + '/' + fname) #Read File in binary
        heap_root = buildTree(frequency)
        compression_codes = make_newCodes(heap_root) #generate the new codes
        encoded_text = replace_codes(bytes, compression_codes)
        write_compFile(encoded_text, compression_codes, fname, path, f)
        os.remove(path + '/' + fname) #remove the files and keep only the compressed file
        f = 1

    end_time = timeit.timeit()
    print()
    print_stats(end_time-begin_time) #Print elapsed time for each folder
    print()
    print("Successful Compression!")



def readFile(path):
    inputFile = open(path, 'rb') #read binary mode
    bytes = []
    byte = inputFile.read(1)
    while len(byte) > 0:
        bytes.append(byte)
        byte = inputFile.read(1)
    frequency = {}
    for byte in bytes:
        if byte not in frequency:
            frequency[byte] = 0
        frequency[byte] += 1
    return bytes, frequency



def buildTree(frequency):
    heap = []
    for key, value in frequency.items():
        heapq.heappush(heap, HuffmanNode(value, key))
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        new_frequency = left.frequency + right.frequency
        new_node = HuffmanNode(new_frequency)
        new_node.set_children(left, right)
        heapq.heappush(heap, new_node)
    heap_root = heapq.heappop(heap)
    return heap_root

def encodeTree(root, current_code,encoded_code):
    if root: #Not leaf
        if root.char: #leaf Node
            encoded_code[root.char] = current_code
        encodeTree(root.left, current_code + "0",encoded_code)
        encodeTree(root.right, current_code + "1",encoded_code)

def make_newCodes(root):
    nw_codes = dict()
    initial_code = ''
    encodeTree(root, initial_code, nw_codes)
    return nw_codes

def replace_codes(bytes, compression_codes):
    encoded_text = ""
    for char in bytes:
        encoded_text += compression_codes[char]
    return encoded_text


def write_compFile(encoded_text, compression_codes, path,folder_path='', f=0):
    extension = os.path.splitext(path)[1]
    file_name = str(os.path.splitext(path)[0])
    if f == 0: # to decide to overwrite or append
        output_path = folder_path + "/file mad3'ot.roz"
        output = open(output_path, "wb")
    else:
        output_path = folder_path + "/file mad3'ot.roz"
        output = open(output_path, "ab")
    compression_codes = {k:v for k,v in compression_codes.items()}
    compression_codes['file_ext'] = extension
    compression_codes['file_name'] = file_name

    '''This Part is for serializing data ,just security
    and to use in decompression'''
    pickle.dump(compression_codes, output, protocol=pickle.HIGHEST_PROTOCOL)
    b = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i+8]
        b.append(int(byte,2))
    pickle.dump(bytes(b), output, protocol=pickle.HIGHEST_PROTOCOL)
    output.close()

def print_stats(elapsedTime):
    print("Elapsed time:", str(abs(round(elapsedTime, 5))) + " seconds")



#-----------------------------------#
'''Reverse the codes assigned to each character for whole files'''
def reverse_codes(tree, compressed_text):
    decoded_text = ''
    temp = ''
    for ch in compressed_text:
        temp += str(ch)
        if tree.__contains__(temp):
            decoded_text += tree[temp]
            temp = ''
    return decoded_text


def decompress_folder(path):
    startTime = timeit.timeit()
    filename = os.listdir(path)
    input_file = open(path + '/' + filename[0], "rb")
    while 1:
        tree = dict()
        try:
            tree = pickle.load(input_file) #reading using pickle is more effective because u got a copy on disk
        except EOFError:
            break
        tree = dict(tree)
        file_ext = str(tree['file_ext'])
        file_name = str(tree['file_name'])
        del tree['file_ext'] #del the original extension of compresed in the tree
        del tree['file_name']
        output_path = path + '/' + file_name + file_ext

        tree = {str(v): str(k).replace('b\'', '', 1).replace('b\"', '', 1).replace('\'', '', 1) for k, v in
               tree.items()}

        try:
            text = pickle.load(input_file)
        except EOFError:
            break
        compressed_text = ''
        n = len(text)
        for t in text:
            if n == 1:
                compressed_text += '{0:b}'.format(t)
                break
            compressed_text += '{0:08b}'.format(t)
            n -= 1

        # Decoding the text
        decodedText = reverse_codes(tree, compressed_text)
        finishTime = timeit.timeit()
        decodedText = decodedText.replace('\\r', '').split('\\n')
        output_file = open(output_path, 'w+')
        for t in decodedText:
            output_file.write(t)
            output_file.write('\n')
        output_file.close()
        print_stats(finishTime - startTime)
    #os.remove(path + '/' + filename[0]) '''Not working :('''
    input_file.close()
    return


#--------------------------------------------------------------------------#
print("     ","#### HUFFMAN CODING ####")
print()
c = input("Do you want to Compress or Decompress ? ")
if c == 'C' or c == 'c':
    s = input("Enter the path to compress : ")
    try:
        compress_folder(s)
    except NameError:
        print("Invalid path!")
    except FileNotFoundError:
        print("File not Found!")

elif c == 'D' or c == 'd':
    s = input("Enter the path to decompress : ")
    try:
        decompress_folder(s)
    except NameError:
        print("Invalid path!")
    except FileNotFoundError:
        print("File not Found!")

else:
    print("Invalid Option!")
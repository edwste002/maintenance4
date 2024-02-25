import math as mp
import inspect
import os
import json
import sys

key = "test key"
#-------------------- algo

import math as mp
import inspect
import os
import json
import sys

key = "test key"
bits32 = [ i for i in range(32)]
bits32xor = [ str(i % 2) for i in range(32) ]
bits128xor = [ str(i % 2) for i in range(128) ] 

def xor(a,b):
    #print(type(a), type(b))
    if a=='0':
        if b=='0':
            return '0'
        else:
            return '1'
    else:
        if b=='0':
            return '1'
        else:
            return '0'


def get32bitstring(v):
    v = bin(v)[2:]
    b = '0'*(32-len(v)) + v
    return b

def get32bitstringFromBytes(b):
    s = ''
    for i in range(4):
        sb = bin(b[i])[2:]
        sb = '0'*(8-len(sb)) + sb
        s = s + sb
    return s

def get32bitstringFromInteger(i):
    if (i > (2**32 - 1)):
        raise
    sb = bin(i)[2:]
    sb = '0'*(32-len(sb)) + sb
    return sb

def get128bitstringFromBytes(b):
    s = ''
    for i in range(4*4):
        #print('i: ',i)
        sb = str(bin(b[i]))[2:]
        sb = '0'*(8-len(sb)) + sb
        s = s + sb
    return s

def getBytesFromArbitraryInteger(i):
    #processes bytes in order left to right
    sb = bin(i)[2:]
    extra = len(sb) % 8
    sb = '0' * (8 - len(sb)) + sb
    l = []
    for i in range(len(sb)//8):
        l.append(int(sb[i*8:(i*8)+8],2) )
    bs = bytes(l)
    return bs

def getArbitraryIntegerFromBytes(b):
    #goes backwards...careful
    v = 0
    print('<<<<<<<<<<<<<<<<<')
    print(b)
    for i in range(len(b)):
        print('<<<<<<<<<<<<<<<')
        print(b[-1 * 1])
        v = (int(b[-1 * i]) * ( 2 ** (8*i) ) ) + v
    return v

def getArbitraryIntegerFromBytesForTextLength(b):
    #goes backwards...careful
    v = 0
    print('<<<<<<<<<<<<<<<<<')
    for i in range(len(b)):
        print('<<<<<<<<<<<<<<<')
        print(b[-1 * 1])
        v = (int(b[-1 * i]) * ( 2 ** (8*i) ) ) + v
    return v

def get128BytesFromBitstring(b):
    l = []
    for i in range(4*4):
        l.append(b[(i*8):(i*8)+8])
    return bytes(l)

def get128bitstringFromInteger(i):
    sb = bin(i)[2:]
    sb = '0'*(128-len(sb)) + sb
    return sb

def xor_32_bits(a,b):
    return ''.join([ str(xor(a[i],b[i])) for i in range(32) ])

def xor128BitsFromBytes(a,b):
    c = get128bitstringFromBytes(a)
    d = get128bitstringFromBytes(b)
    return ''.join([ str(xor(c[i],d[i])) for i in range(128) ])

def xor128BitsFromBitString(a,b):
     return ''.join([ str(xor(a[i],b[i])) for i in range(128) ])

def TruffleShuffle32bitstring(binaryString):
    xor_bits = xor_32_bits(binaryString, bits32xor)
    return xor_bits

def TruffleShuffle128FromBitstring(bitstring128):
    l = []
    for i in range(4):
        xor_bits = xor_32_bits(bitstring128[( i * 4*8 ) :  (i * 4 * 8) + 4 * 8 ], bits32xor)
        l.append(xor_bits)
    return int(''.join( (l[i] for i in range(4) ) ) , base=2)



derangementSize = [1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496, 1334961, 14684570, 176214841, 2290792932, 32071101049, 481066515734, 7697064251745, 130850092279664, 2355301661033953, 44750731559645106, 895014631192902121, 18795307255050944540, 413496759611120779881, 9510425471055777937262, 228250211305338670494289, 5706255282633466762357224, 148362637348470135821287825, 4005791208408693667174771274, 112162153835443422680893595673, 3252702461227859257745914274516, 97581073836835777732377428235481, 3025013288941909109703700275299910, 96800425246141091510518408809597121, 3194414033122656019847107490716704992, 108610077126170304674801654684367969729, 3801352699415960663618057913952878940514, 136848697178974583890250084902303641858505, 5063401795622059603939253141385234748764684, 192409268233638264949691619372638920453057993, 7503961461111892333037973155532917897669261726]

def getDerangementSize(n):
    return derangementSize[n]

#print([getDerangementSize(i) for i in range(40)])

def recurseDerangement(i,iterlist,n):
    #iterlist needs to be list of whole numbers
    #print('recurse_________',i,iterlist,n)
    length = len(iterlist)
    if length==2:
        if (i==0):
            return [iterlist[1],iterlist[0]]
    if length==3:
        if(i==0):
            return[iterlist[1],iterlist[2],iterlist[0]]
        if(i==1):
            return[iterlist[2],iterlist[0],iterlist[1]]
    dMain = getDerangementSize(length)
    dNext = getDerangementSize(length-1)
    dNexter = getDerangementSize(length-2)
    #print('\tl_',length)
    #print('\i_',i)
    #print('\tdMain_',dMain)
    #print('\tdNext_',dNext)
    #print('\tdNexter_',dNexter)

    dMultiplier = dNext + dNexter

    if i>dMain:
        print('error')
        raise
    #pairs on bottom
    firstPart = i // dMultiplier
    secondPart = i % dMultiplier

    derangement = [i for i in iterlist]
    newiterlist = iterlist[:]
    #figure out out of order
    if secondPart >= dNexter:
        derangement_item = newiterlist[firstPart+1]
        v = newiterlist[0]
        #relabeling
        for i in range(len(newiterlist)):
            if newiterlist[i]==v:
                newiterlist[i]=newiterlist[firstPart+1]
                #print('relabeling')
        newiterlist.pop(0)
        returnediterlist = recurseDerangement(secondPart-dNexter,newiterlist,n-1)
        #unlabeling
        for i in range(len(returnediterlist)):
            if returnediterlist[i]==iterlist[firstPart+1]:
                returnediterlist[i]=v
        #add first item back into list
        returnediterlist.insert(0,derangement_item)
        return returnediterlist
    else:
        derangement_item = [newiterlist[firstPart+1],newiterlist[0]]
        newiterlist.pop(firstPart+1)
        newiterlist.pop(0)
        returnediterlist = recurseDerangement(secondPart,newiterlist,n-2)
        #add pairs back to list
        returnediterlist.insert(0,derangement_item[0])
        returnediterlist.insert(firstPart+1,derangement_item[1])
        return returnediterlist
    
def eee_round(bitsInSelectorFunction128bitsFromBytes, bitsIn32bitsAsBytes, count=0):
    #print('bits:', bitsIn32bitsAsBytes)
    b32 =  get32bitstringFromBytes(bitsIn32bitsAsBytes)
    #print('converted bits',b32)
    b32 = TruffleShuffle32bitstring(b32)
    #print('truffle bits',b32)
    #print('bitsInSelectorFunction128bitsFromBytes: ', bitsInSelectorFunction128bitsFromBytes)
    b128 = get128bitstringFromBytes(bitsInSelectorFunction128bitsFromBytes)
    #print('b128 ', b128)
    b128 = TruffleShuffle128FromBitstring(b128)
    #print('b128 truffle[', b128)
    i128 = (b128 + count) % getDerangementSize(32)
    #print('128 into derangment ', i128)
    #print('eee:\t', b32,  '\t', b128, '\t', i128)
    selected = recurseDerangement( i128, bits32, 32 )
    print('selected:',selected)
    l = [ 0 for i in range(32) ]
    for i in range(32):
        l[selected[i]] = b32[i]
    #print(l)
    #print(len(l))
    b = bytes( [ int( ''.join(l[(i*8):((i*8)+8)]), base = 2) for i in range(4) ] )
    #print(b)
    return b

def reverse_eee_round(bitsInSelectorFunction128bitsFromBytes, bitsIn32bitsAsBytes, count=0):
    #print('bits:', bitsIn32bitsAsBytes)
    b32 =  get32bitstringFromBytes(bitsIn32bitsAsBytes)
    b128 = get128bitstringFromBytes(bitsInSelectorFunction128bitsFromBytes)
    #print('b128 ', b128)
    b128 = TruffleShuffle128FromBitstring(b128)
    #print('b128 truffle[', b128)
    i128 = (b128 + count) % getDerangementSize(32)
    #print('128 into derangment ', i128)
    #print('eee:\t', b32,  '\t', b128, '\t', i128)
    selected = recurseDerangement( i128, bits32, 32 )
    print('selected:',selected)
    
    l = [ 0 for i in range(32) ]
    for i in range(32):
        l[i] = b32[selected[i]]
    
    l = TruffleShuffle32bitstring( get32bitstringFromInteger(int( ''.join(l),base = 2)) )
    b = bytes( [ int( ''.join(l[(i*8):((i*8)+8)]), base = 2) for i in range(4) ] )
    #print(b)
    return b

def get_quick_checksum(data_in):
    v = data_in[0]
    for i in range(len(data_in[0:-4])):
        v = eee_round(data_in[i+0]*(2**(96)) + data_in[i+1]*(2**(64)) + data_in[i+2]*(2**(32)) + data_in[i+3], v )
        v = int(v,base=2)
    return eee_round(data_in[-4]*(2**(96)) + data_in[-3]*(2**(64)) + data_in[-2]*(2**(32)) + data_in[-1], v )


def selectorShuffle( oldSelector, selector128, extra=''):
    # TODO add extra later
    # left shift
    # xor remainder back on back
    oldSelector = oldSelector [4:] + oldSelector[0:4]
    #print(oldSelector)
    oldSelector = xor128BitsFromBytes(oldSelector, selector128)
    #print(oldSelector)
    oldSelector = bytes( int(oldSelector[(i*8):(i+1)*8],2) for i in range(16) )
    oldSelector = oldSelector [4:] + oldSelector[0:4]
    #print(len(oldSelector))
    oldSelector = xor128BitsFromBytes(oldSelector, selector128)
    oldSelector = bytes( int(oldSelector[i*8:(i+1)*8],2) for i in range(16) ) 
    return oldSelector

def decrypt_rounds_for_text_size(oldSelector,predata, data):
    d = predata[0:16] + data[:] + data[0:16]
    #doesn't work with sizes with 0,0,0,0 in their length
    zeroBytesString = bytes([0,0,0,0])
    for i in range(len(data)//4):
        selector128 = d[ (i) * 4 : ((i)*4) + 4*4 ]
        #--TODO extra does nothing ----------------
        oldSelector = selectorShuffle( oldSelector, selector128 )
        
        data32 = d[ ((i)*4) + 4*4 : ((i+1)*4) + 4*4 ]
        
        b = reverse_eee_round( oldSelector, data32  , i )
        d = d[:(i)*4 + 4*4] +  b + d[((i+1)*4) + 4*4:]
        print('----decrypt for text rounds size-->oldselector\t:', oldSelector, 'round\t selector128:',selector128)
        print('\t','data32:',data32, '\toutput:\t', d)
        if b == zeroBytesString:
            print('found zero 32 bit string')
            return oldSelector, getArbitraryIntegerFromBytes(d[16:16 + i * 4])
        
        
    print('size not found')
    raise
    return oldSelector, 0, 0

def encrypt_rounds(oldSelector,predata, data):
    d = predata[0:16] + data[:] + predata[0:16]
    output = bytes()
    for i in range(len(data)//4):
        selector128 = d[ (i) * 4 : ((i)*4) + 4*4 ]
        #--TODO extra does nothing ----------------
        oldSelector = selectorShuffle( oldSelector, selector128 )
                
        data32 = d[ ((i)*4) + 4*4 : ((i+1)*4) + 4*4 ]
        
        b = eee_round( oldSelector, data32  , i )
        
        output = output + b
        print('--->oldselector\t:', oldSelector, 'round\t selector128:',selector128)
        print('\t','data32:',data32, '\toutput:\t', output)
    return oldSelector, output

def decrypt_rounds(oldSelector,predata,data):
    d = predata[0:16] + data[:] + predata[0:16]
    output = bytes()
    for i in range(len(data)//4):
        selector128 = d[ (i) * 4 : ((i)*4) + 4*4 ]
        #--TODO extra does nothing ----------------
        oldSelector = selectorShuffle( oldSelector, selector128 )
        
        data32 = d[ ((i)*4) + 4*4 : ((i+1)*4) + 4*4 ]
        
        b = reverse_eee_round( oldSelector, data32  , i )
        d = d[:(i)*4 + 4*4] +  b + d[((i+1)*4) + 4*4:]
        print('--->oldselector\t:', oldSelector, 'round\t selector128:',selector128)
        #print('\t','data32:',data32, '\toutput:\t', output)
    output = d[16:-16]
    return oldSelector, output

def encrypt_data(data,password):
    #predata needs 16 length to work
    #password first
    #then data
    if len(password)<20:
        print("password too short")
        raise

    oldSelector = bytes([ 0 for i in range(16) ] )
    outputsizetext = bytes([])
    outputtext = bytes([])
    
    oldSelector, notused = encrypt_rounds(oldSelector,password[0:16], password)

    print('-------------------------------------oldSelector: ', oldSelector) 
    
    #TODO - fix size issue...very bad-----------------------------
    #add data size to the front
    szBytes = getBytesFromArbitraryInteger(len(data))
    if len(szBytes)>16:
        print('szOfFile too big')
    szBytes = szBytes + (16 - len(szBytes)) * bytes([0])
    print('szBytes:', szBytes)
    print('length of szBytes:', len(szBytes))

    oldSelector, outputText = encrypt_rounds(oldSelector,password[0:16], szBytes + data)

    #add size check for end of data....
    return outputText

def decrypt_data(data,password):
    #password first
    #then data
    if len(password)<20:
        print("password too short")
        raise
    
    output = bytes()
    oldSelector = bytes([ 0 for i in range(16) ] )
    
    oldSelector, notused = encrypt_rounds(oldSelector,password[0:16], password)

    print('--------------------------------------oldSelector: ', oldSelector) 
    #limits text size by 2**(8*100)
    noSelector, sizeOfText = decrypt_rounds_for_text_size(oldSelector,password[0:16], data[0:100])
    print('\tsizeOfText: ', sizeOfText)
    oldSelector, outputText = decrypt_rounds(oldSelector,password[0:16], data)
    print('outputText: ',outputText)
    return outputText[16:16 + sizeOfText]
#------------------------------------------------------------------------------------------------------------------
#-------------------- old code pieces


def diff(fileList, folder1, folder2):
    for f in fileList:
        with open(str(folder1) + '\\' + f, 'rb') as file1, open(str(folder2) + '\\' + f, 'rb') as file2:
            data1 = file1.read()
            data2 = file2.read()
            #print('-------------')
            #print(data1)
            #print('-------------')
            #print(data2)

        if data1 != data2:
            print(f," Files do not match.")
        else:
            print(f," Files match.")

def array_index(arr, indices):
    if len(indices)==0:
        return arr
    return multiget_rec(arr[indices[0]], indices[1:])


def get_files_directory(startpath,remove_prefix=''):
    #TODO---------------------------------------------------------  text
    #walk file directory making a relative path list of each file
    if not os.path.isdir(startpath):
        print(startpath,remove_prefix,' is not a directory.')
        return False

    listOfFiles = []
    dirpaths = []
    rolling_count = 0

    listOfFiles = []
    rolling_crypted_size_count = 0
    chunksize = 1024*1024
    
    for (dirpath, dirnames, filenames) in os.walk(startpath):
        if not dirpath in dirnames:
            dirpaths.append([len(dirpath.removeprefix(remove_prefix)),dirpath.removeprefix(remove_prefix)])
        for file in filenames:

            sz = os.path.getsize(os.path.join(dirpath, file))
    
            crypted_size = sz + 16

            relativepath = str(os.path.join(dirpath, file))
            relativepath = os.path.relpath(relativepath,remove_prefix)
            
            listOfFiles += [ [len(relativepath),relativepath, rolling_crypted_size_count, crypted_size, sz] ]
            rolling_crypted_size_count += crypted_size
            
    return [listOfFiles,dirpaths]

alphalist=[chr(i) for i in range(256)]

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

def getbinval(v):
    val = alphalist.index(v)
    v = bin(val)[2:]
    b = '0'*(8-len(v)) + v
    return b

def getbytebinval(v):
    v = bin(v)[2:]
    b = '0'*(8-len(v)) + v
    return b

def gettextval(v):
    return alphalist[int("0b"+"".join(v),2)]

def text_decrypt(text,key):
    data = decrypt_data(text,key)
    return data

def text_decrypt_from_bytes_for_header(text,key):
    #TODO---------------------------------------------------------  text
    data = decrypt_data(text,key)
    return data

def text_encrypt(text,key):
    data = encrypt_data(text,key)
    return data

def text_encrypt_from_bytes_for_header(text,key):
    data = encrypt_data(text,key)
    return data

def get_next_directory_list_parsed_entry(z):
    #relative_file_name_length,relativepath, rolling_crypted_size_count, crypted_size, sz
    #print(len(z))
    firstBracket = z.find('[')
    if firstBracket==-1:
        return [-1,-1]
    idx = firstBracket + 1
    idx2 = z[idx:].find(',')
    directory_entry_length = int(z[idx:idx+idx2])
    entry=z[idx+idx2+2:idx+idx2+2+directory_entry_length]

    idx4 = z[idx+idx2+2+directory_entry_length:].find(']')

    return [directory_entry_length,entry],z[idx+idx2+2+directory_entry_length+idx+1:]


def get_next_file_list_parsed_entry(z):
    #relative_file_name_length,relativepath, rolling_crypted_size_count, crypted_size, sz
    #print(len(z))
    firstBracket = z.find('[')
    #print(firstBracket)
    if firstBracket==-1:
        return [-1,-1]
    idx = firstBracket + 1
    #get string
    state = 0
    firstparenth, startint, secondstartint, file, count1, count2 = 0,0,0,'',0,0
    relativepathlength=0
    relativepath_index_end = 0
    sizeend=0
    z = z.replace('\\\\','\\')
    while(state <= 3):
        #file string
        if(state == 0):
            if(z[idx]==','):
                #read file path length and file name
                relativepath_index=idx
                relative_file_name_length=int(z[firstBracket+1:relativepath_index])
                relativepath = z[idx+3:idx+2+relative_file_name_length+1]
                relativepath_index_end = idx+2+relative_file_name_length+1+2
                idx = relativepath_index_end
                state = state + 1
                #print(relative_file_name_length,relativepath)
        elif (state == 1):
            if(z[idx]==','):
                #print(idx,relativepath_index_end,relative_file_name_length)
                
                rolling_crypted_size_count = int(z[relativepath_index_end+1:idx])
                rolling_crypted_size_count_index = idx
                state = state + 1
        elif (state == 2):
            if(z[idx]==','):
                crypted_size_index = idx
                crypted_size = int(z[rolling_crypted_size_count_index+1:idx])
                state = state + 1
        elif (state == 3):
            if(z[idx]==']'):
                sz = int(z[crypted_size_index + 1:idx])
                state = state + 1
        idx = idx + 1

    return [relative_file_name_length,relativepath, rolling_crypted_size_count, crypted_size, sz], z[idx+1:]

def parse_directory_list_string(header):
    #print(header)
    header = header.rstrip('_')
    firstBracket = header.find('[')
    lastBracket = header.rfind(']')
    if firstBracket!=0 and lastBracket!= len(header):
        return []
    header = header[1:-1]
    #print(header)
    #print(len(header))
    z = get_next_directory_list_parsed_entry(header)
    entry,header = z
    l = []
    while entry != -1:
        l.append(entry)
        #print(entry,'entry length-', len(entry[0]))
        #print(l,z,entry,header)
        entry,header = get_next_directory_list_parsed_entry(z)
    return l

def parse_file_list_string(header):

    print(header)
    header = header.rstrip('_')
    firstBracket = header.find('[')
    lastBracket = header.rfind(']')
    if firstBracket!=0 and lastBracket!= len(header):
        return []
    header = header[1:-1]
    #print(header)
    #print(len(header))
    #print(header)
    z = get_next_file_list_parsed_entry(header)
    entry,header = z
    #print(z,header,entry)
    l = []
    while entry != -1:
        l.append(entry)
        #print(l,z,entry,header)
        #print(entry,'entry length-', len(entry[0]))
        entry,header = get_next_file_list_parsed_entry(header)
    return l  
    
def decrypt_file_from_storage(start_pos, filename, crypted_filesize, sz, encrypted_locker_filename, key):
    k = key

    
    #split
    import os
    #print(filename)
    #print(os.path.dirname(filename))
    try:
        os.makedirs(os.path.dirname(filename))
    except FileExistsError:
        print("File already exists",filename)
        pass
    except FileNotFoundError:
        print("File Not Found error",filename)
        pass
    
    with open(encrypted_locker_filename,mode='rb') as f:
        f.seek(start_pos)
        
        with open(filename,mode='wb') as fo:

            for z in range(filechunks):
                #print(z,fileSz)
                
                data = f.read()

                fo.write(data)
        
                
def encrypt_file_for_storage(filename, encrypted_file_handle, key):
    print('encrypting:',filename)
    #TODO---------------------------------------------------------  text
    # need a filesize header on encrypted file to deal with length mismatch
    # pads size to
    

    sz = os.path.getsize(filename)

    bytesread = 0    
    
    lenbinsz = len(bin(sz)[2:])
    lenbinbytesz = len(bin(sz)[2:]) // 8
    paddedbinsz = '0'*((lenbinbytesz*8)-lenbinsz) + (bin(sz)[2:])
    encrypted_file_handle.write(ciphbytes[0])



def list_folder_files(storage_file_name,key):
    #TODO---------------------------------------------------------  text
    header_length, crypt_header_size = get_header_file_sizes(storage_file_name,key)
    with open(storage_file_name,'rb') as storage_file:
        storage_file.seek(len(str(header_length))+len(str(crypt_header_size))+2)
        crypt_header = storage_file.read(crypt_header_size)
        #print('----------list_folder_files------------')
        #print('---crypt_header----------------')
        #print(crypt_header)
        
        listOfFiles = decrypt_header(crypt_header,key)
        #print('------listOfFiles--------------')
        #print(listOfFiles)
    return listOfFiles

def get_header_string_val_from_bytes_in_array(t,i):
    l = []
    while t[i]!=0:
        #print('-----------------------',sf[i])
        #print(type(sf[i]))
        #chr(sf[i])
        #print('33')
        l.append(chr(t[i]))
        i = i + 1
    i = i + 1
    #print(l)
    return int(''.join(l)),i

def get_header(storage_file_name,key):
    #TODO---------------------------------------------------------  text
    #text_decrypt_from_bytes_for_header(text,key)
    with open(storage_file_name,'rb') as storage_file:
        sf = storage_file.read(240)
        text = text_decrypt_from_bytes_for_header(sf,key)
        print('--------------------------sf:',sf)
        print(text)
        #print(type(text))
        index = 0
        file_directory_length,index = get_header_string_val_from_bytes_in_array(text,index)
        file_list_length,index = get_header_string_val_from_bytes_in_array(text,index)
        dirs_list_length,index = get_header_string_val_from_bytes_in_array(text,index)
        print('--------file_list_length:',file_list_length)
        print('--------dirs_list_length:',dirs_list_length)
        print('--------file_directory_length:',file_directory_length)
        print('--------------------------index:',index)
        storage_file.seek(0)
        total_encrypted_header_length = index+file_directory_length
        sf = storage_file.read(total_encrypted_header_length)
        print('--------------------------sf:',sf)
        print('text--------')
        text = text_decrypt_from_bytes_for_header(sf,key)
        print('----------text',text)
        list_of_files_string = ''.join([alphalist[i] for i in text[index+1:index+1+file_list_length]])
        list_of_dirs_string = ''.join([alphalist[i] for i in text[index+1+file_list_length+2:-2]])    #to account for extra brackets
        print(index)
        print('list_of_files_string-----------------',list_of_files_string)
        print('list_of_dirs_string-----------------',list_of_dirs_string)
        list_of_dirs_string = list_of_dirs_string.rstrip('_')
        print(list_of_dirs_string)
        list_of_files = parse_file_list_string(list_of_files_string)
        #TODO fix this later
        #list_of_dirs = parse_directory_list_string(list_of_dirs_string)
        
    return file_list_length,dirs_list_length,file_directory_length,list_of_files,list_of_dirs_string,total_encrypted_header_length

import math as mp
import inspect
import os
import json
import sys

key = "test key"
bits32 = [ i for i in range(32)]
bits32xor = [ str(i % 2) for i in range(32) ]
bits128xor = [ str(i % 2) for i in range(128) ] 

def xor(a,b):
    #print(type(a), type(b))
    if a=='0':
        if b=='0':
            return '0'
        else:
            return '1'
    else:
        if b=='0':
            return '1'
        else:
            return '0'


def get32bitstring(v):
    v = bin(v)[2:]
    b = '0'*(32-len(v)) + v
    return b

def get32bitstringFromBytes(b):
    s = ''
    for i in range(4):
        sb = bin(b[i])[2:]
        sb = '0'*(8-len(sb)) + sb
        s = s + sb
    return s

def get32bitstringFromInteger(i):
    if (i > (2**32 - 1)):
        raise
    sb = bin(i)[2:]
    sb = '0'*(32-len(sb)) + sb
    return sb

def get128bitstringFromBytes(b):
    s = ''
    for i in range(4*4):
        #print('i: ',i)
        sb = str(bin(b[i]))[2:]
        sb = '0'*(8-len(sb)) + sb
        s = s + sb
    return s

def getBytesFromArbitraryInteger(i):
    #processes bytes in order left to right
    sb = bin(i)[2:]
    extra = len(sb) % 8
    sb = '0' * (8 - len(sb)) + sb
    l = []
    for i in range(len(sb)//8):
        l.append(int(sb[i*8:(i*8)+8],2) )
    bs = bytes(l)
    return bs

def getArbitraryIntegerFromBytes(b):
    #goes backwards...careful
    v = 0
    print('<<<<<<<<<<<<<<<<<')
    print(b)
    for i in range(len(b)):
        print('<<<<<<<<<<<<<<<')
        print(b[-1 * 1])
        v = (int(b[-1 * i]) * ( 2 ** (8*i) ) ) + v
    return v

def getArbitraryIntegerFromBytesForTextLength(b):
    #goes backwards...careful
    v = 0
    print('<<<<<<<<<<<<<<<<<')
    for i in range(len(b)):
        print('<<<<<<<<<<<<<<<')
        print(b[-1 * 1])
        v = (int(b[-1 * i]) * ( 2 ** (8*i) ) ) + v
    return v

def get128BytesFromBitstring(b):
    l = []
    for i in range(4*4):
        l.append(b[(i*8):(i*8)+8])
    return bytes(l)

def get128bitstringFromInteger(i):
    sb = bin(i)[2:]
    sb = '0'*(128-len(sb)) + sb
    return sb

def xor_32_bits(a,b):
    return ''.join([ str(xor(a[i],b[i])) for i in range(32) ])

def xor128BitsFromBytes(a,b):
    c = get128bitstringFromBytes(a)
    d = get128bitstringFromBytes(b)
    return ''.join([ str(xor(c[i],d[i])) for i in range(128) ])

def xor128BitsFromBitString(a,b):
     return ''.join([ str(xor(a[i],b[i])) for i in range(128) ])

def TruffleShuffle32bitstring(binaryString):
    xor_bits = xor_32_bits(binaryString, bits32xor)
    return xor_bits

def TruffleShuffle128FromBitstring(bitstring128):
    l = []
    for i in range(4):
        xor_bits = xor_32_bits(bitstring128[( i * 4*8 ) :  (i * 4 * 8) + 4 * 8 ], bits32xor)
        l.append(xor_bits)
    return int(''.join( (l[i] for i in range(4) ) ) , base=2)
#---------------------

def decrypt_folder(new_folder_name,storage_file_name,key):
    #TODO make empty directories
    result = get_header(storage_file_name,key)
    #file_list_length,dirs_list_length,file_directory_length,list_of_files,list_of_dirs,total_encrypted_header_length+1
    file_list_length,dirs_list_length,file_directory_length,list_of_files,list_of_dirs,start_offset=result[0],result[1],result[2],result[3],result[4],result[5]

    for file_tuple in list_of_files:
        #start_pos, filename, filesize, encrypted_locker_filename, key
        
        relative_file_name_length,relativepath, rolling_crypted_size_count, crypted_size, sz = file_tuple[0],file_tuple[1],file_tuple[2],file_tuple[3],file_tuple[4]
        
        #print('--------------------------------',new_folder_name+relativepath,start_offset)
        print('-------------------file tuple----------------------',file_tuple)
        decrypt_file_from_storage(start_offset+rolling_crypted_size_count, new_folder_name+relativepath, crypted_size, sz, storage_file_name, key)
        #for i in range(10):
        #    decrypt_file_from_storage(start_offset+rolling_crypted_size_count-5+i, new_folder_name+relativepath+str(i), crypted_size, storage_file_name, key)
        #break
    
def encrypt_folder(startpath,prefix,storage_file_name,key):
    #TODO---------------------------------------------------------  text
    #need unicode support for filenames
    #print('----encrypt_folder_step------')
    
    file_directory = get_files_directory(startpath,prefix)
    
    #print('file_list-------------',file_directory)
    file_list,dirs = file_directory[0],file_directory[1]
    print(file_list)
    print(dirs)
    relative_file_name_length,relativepath, rolling_crypted_size_count, crypted_size, sz = file_list[0],file_list[1],file_list[2],file_list[3],file_list[4]
    #print('crypted header size-----',len(text_encrypt(str(file_directory),key)),len(str(file_directory)))
    #s = sum((f[2] for f in file_list))
    file_directory_length = len(str(file_directory))
    file_list_length = len(str(file_list))
    dirs_length = len(str(dirs))

    header = str(file_directory_length) + str('\0') + \
            str(file_list_length) + str('\0') + \
            str(dirs_length) + str('\0') +  \
            str(file_directory) + str('\0')

    encrypted_header = text_encrypt_from_bytes_for_header(header,key)
    encrypted_headers_bytes = bytes([ord(s) for s in encrypted_header])
    
    with open(storage_file_name,'wb') as storage_file:
        storage_file.write(encrypted_headers_bytes)
        for current_file_header in file_list:
            #print(current_file_header)
            relative_file_name_length,relativepath, rolling_crypted_size_count, crypted_size, sz = current_file_header[0],current_file_header[1],current_file_header[2],current_file_header[3],current_file_header[4]
            #print('encrypting--------------',os.path.basename(relativepath))
            encrypt_file_for_storage(prefix + '\\' + relativepath, storage_file, key)

import sys
#print(alphalist)
encryptOrDecrypt = input('(e)ncrypt or (d)ecrypt a folder?')
l=['fixed','other','per']

if encryptOrDecrypt=='e':
    folder = input('enter full folder path')
    prefix = input('enter folder prefix')
    binfile = input('bin file')
    key = input('enter key')
    encrypt_folder(folder,prefix,binfile,key)
    #for i in l:
    #   encrypt_folder('F:\\data\\docs\\' + i, 'F:\\data\\docs', 'docs.' + i +'.bin', key)
elif encryptOrDecrypt=='d':
    folder = input('enter folder name')
    binfile = input('bin file')
    key = input('enter key')
    decrypt_folder(folder, binfile, key)



data = bytes([123,123,23,34,34,35,36,37,42,42,42,4,342%256,234234%256,342342%256,342342%256,342342%256,5656534%256,53,34,3,55,654%256,654546%256,654%256])
password = bytes([221,232,242,56,154,24,60,40,46,6,64,156,56,64,6,78,4,6,3,4,142,134])
print('data: ', data)
print(len(data))

print('---encrypt----')
v = encrypt_data(data,password)
print(v)
print('--decrypt------')
print(decrypt_data(v,password))
print('-----------')


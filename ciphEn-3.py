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



#-------------------- old code pieces
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

'''
def decrypt_data(data,password):
    #password first
    #then data
    if len(password)<20:
        print("password too short")
        raise
    extra = len(password) % 4
    output = bytes()
    oldSelector = bytes([ 0 for i in range(16) ] )
    p = password[0:16] + password[:] + password[0:16]
    
    for i in range(len(password)//4):
        
        selector128 = p[ (i) * 4 : ((i)*4) + 4*4 ]
        oldSelector = selectorShuffle( oldSelector, selector128, p[(i*4):((i+1)*4)] )
        data32 = p[ ((i)*4) + 4*4 : ((i+1)*4) + 4*4 ]
        
        print('password selector128:',selector128,'\t','data32:',data32, '\t', output)
        b = eee_round( oldSelector, p  , i )

    extra = len(password) % 4
    d = p[0:16] + data[:] + data[0:16]
    print(len(d))
    for i in range(len(data)//4):

        selector128 = d[ (i) * 4 : ((i)*4) + 4*4 ]
        oldSelector = selectorShuffle( oldSelector, selector128 )
        data32 = d[ ((i)*4) + 4*4 : ((i+1)*4) + 4*4 ]
        
        b = reverse_eee_round( oldSelector, data32  , i )
        
        d = d[:(i)*4 + 4*4] +  b + d[((i+1)*4) + 4*4:]
        output = output + b
        print('data\t selector128:\t',selector128,'\t','data32:\t',data32,'\t new_data:\t',b, '\t', output)
    
    print('hia')
    #add size check for end of data....
    return output[ : (len(data)-extra) ]
'''


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


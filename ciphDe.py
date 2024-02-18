import math as mp
import inspect
import os
import json
import sys

key = "test key"



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
'''
whole_file_size = len(str(directory_string))*2 + 2 + s
    whole_file_size = len(str(whole_file_size)) + whole_file_size + 1
'''
def get_files_directory(startpath):
    if not os.path.isdir(startpath):
        return False

    listOfFiles = []
    rolling_count = 0
    for (dirpath, dirnames, filenames) in os.walk(startpath):
        for file in filenames:
            sz = os.path.getsize(os.path.join(dirpath, file))
            #sz = os.path.getsize(file)
            startpathlength = len(str(os.path.join(startpath)))
            relativepath = str(os.path.join(dirpath, file))[startpathlength:]
            
            #ff = str(os.path.join(startpath)) - str(os.path.join(dirpath, file))
            #listOfFiles += [ [os.path.join(dirpath, file), rolling_count, sz] ]
            listOfFiles += [ [relativepath, rolling_count, sz] ]
            rolling_count += 1 + sz
    return listOfFiles

alphalist=[chr(i) for i in range(256)]

def cycleselect(n):
    #0-14  first (2,2,2 cycles)   n/5     1,n/5    next,n%5
    #15+90  104     u,v    n/6   0-14, 0-5      0-14/5  0-3, 0-4  sorted and ordered backwards
    #second (2,4 cycles) 15+90+40 145
    #third (3,3 cycles) 145-255 110 (last 10 clipped off)
    #(6 cycles)

    cycles4 = [
	[1, 2, 3, 4],
	[1, 2, 4, 3],
	[1, 3, 2, 4],
	[1, 3, 4, 2],
	[1, 4, 2, 3],
	[1, 4, 3, 2]]
               
    if n<15:
        cycles = []
        u,v = divmod(n,5)
        cyclelist = [2,3,4,5,6]
        cycles.append([1,cyclelist.pop(v)])
        cycles.append([cyclelist.pop(0),cyclelist.pop(u)])
        cycles.append([cyclelist.pop(0),cyclelist.pop(0)])
        return cycles
    
    if n<(15+90):
        a = (n-15)
        #0-14, 0-5
        u,v = divmod(a,6)
        cycles = []
        #0-3,0-4
        x,y = divmod(u+1,5)
        #print(u,v)  
        cyclelist = [1,2,3,4,5,6]
        x,y = x if x < y else y,x if x > y else y
        cycles.append([cyclelist.pop(y),cyclelist.pop(x)])
        cc = cycles4[v]
        cycles.append([cyclelist[cc[0]-1],
                       cyclelist[cc[1]-1],
                       cyclelist[cc[2]-1],
                       cyclelist[cc[3]-1]])
        return cycles
    
    if n<(15+90+40):
        cycles = []
        cyclePerm2by2,z = divmod(n-(15+90),10)
        perm1,perm2 = divmod(cyclePerm2by2,2)
        nchoosekchart = [ [1,2,3],[1,3,4],[1,4,5],[1,5,6],
                          [1,2,4],[1,3,5],[1,4,6],
                          [1,2,5],[1,3,6],
                          [1,2,6]
                          ]
                          
        cycles2 = [
            [1, 2, 3],
            [1, 3, 2],
        ]
        xx,yy,zz = nchoosekchart[z]
        cyclelist = [1,2,3,4,5,6]
        if not perm1:
            cycles.append([xx,yy,zz])
        else:
            cycles.append([xx,zz,yy])

        cyclelist.remove(xx)
        cyclelist.remove(yy)
        cyclelist.remove(zz)
        if not perm2:
            cycles.append([cyclelist[0], cyclelist[1], cyclelist[2]])
        else:
            cycles.append([cyclelist[0], cyclelist[2], cyclelist[1]])
        return cycles
    
    z = n - 145
    cycles = []
    #0-4,0-23
    a,b = divmod(z,4*3*2)
    #0-3,0-5
    c,d = divmod(b,3*2)
    #0-2,0-1
    e,f = divmod(d,2)
    cyclelist=[2,3,4,5,6]
    cycle = [1]
    cycle.append(cyclelist.pop(a))
    cycle.append(cyclelist.pop(c))
    cycle.append(cyclelist.pop(e))
    cycle.append(cyclelist.pop(f))
    cycle.append(cyclelist.pop(0))
    cycles.append(cycle)
    return cycles

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='little')

def getbinval(v):
    val = alphalist.index(v)
    v = bin(val)[2:]
    b = '0'*(8-len(v)) + v
    return b

def gettextval(v):
    return alphalist[int("0b"+"".join(v),2)]
    
def cyclemult(vec,cycles):
    b = [ vec[i] for i in range(len(vec))]
    for cycle in cycles:
        b[cycle[1]-1] = vec[cycle[0]-1]
        if len(cycle) > 2:
            for c in range(len(cycle[1:])):
                b[cycle[c+1]-1] = vec[cycle[c]-1]
        b[cycle[0]-1] = vec[cycle[-1]-1]
    return b

def inversecycle(cycles):
    inversecycles = []
    for cycle in cycles:
        inversecycles.append(list(reversed(cycle)))
    return inversecycles

def text_decrypt(text,key):
    if len(text)%3!=0:
        return []
    t = len(text)
    k = len(key)

    if t < 6:
        return []
    if k < 4:
        return []
    m = float(t)/float(k)
    val = (4.0/3.0)*t
    k = key
    while (len(k) < val):
        k = k + key
    k = k + key
    #24 bits so 6 bits or 3 text characters per 4 key text characters
    #expand key out to fit 4:3 ratio
    
    z = []
    kcount = 0
    for a in range(0,len(text),3):
        ba = getbinval(text[a])
        bb = getbinval(text[a+1])
        bc = getbinval(text[a+2])
        kcount = kcount + 4
        cya = inversecycle(cycleselect(alphalist.index(k[kcount])))
        cyb = inversecycle(cycleselect(alphalist.index(k[kcount+1])))
        cyc = inversecycle(cycleselect(alphalist.index(k[kcount+2])))
        cyd = inversecycle(cycleselect(alphalist.index(k[kcount+3])))
        v1, v2, v3, v4 = ba[0:6], ba[6:] + bb[0:4], bb[4:] + bc[0:2], bc[2:]
        resulta = cyclemult(v1,cya)
        resultb = cyclemult(v2,cyb)
        resultc = cyclemult(v3,cyc)
        resultd = cyclemult(v4,cyd)
        text1 = resulta + resultb[0:2]
        text2 = resultb[2:] + resultc[0:4]
        text3 = resultc[4:] + resultd
        z.append(gettextval(text1))
        z.append(gettextval(text2))
        z.append(gettextval(text3))
    return "".join(z)

def text_encrypt(text,key):
    text = text + '_'*(3 - (len(text) % 3))
    t = len(text)
    k = len(key)

    if t < 6:
        return []
    if k < 4:
        return []
    
    m = float(t)/float(k)
    
    val = (4.0/3.0)*t
    
    k = key
    while (len(k) < val):
        k = k + key
    k = k + key
    #24 bits so 6 bits or 3 text characters per 4 key text characters
    #expand key out to fit 4:3 ratio
    
    z = []
    kcount = 0
    for a in range(0,len(text),3):
        #print('-------------------------',a,'--------------------------')
        #6 bits * 4 = 24 bits total
        #8 bits * 3 = 3 letters at a time
        #
        #print(text[a],text[a+1],text[a+2])
        ba = getbinval(text[a])
        bb = getbinval(text[a+1])
        bc = getbinval(text[a+2])

        kcount = kcount + 4

        #print(ba,bb,bc)
        cya = cycleselect(alphalist.index(k[kcount]))
        cyb = cycleselect(alphalist.index(k[kcount+1]))
        cyc = cycleselect(alphalist.index(k[kcount+2]))
        cyd = cycleselect(alphalist.index(k[kcount+3]))

        #print(cya,cyb,cyc,cyd)
        v1, v2, v3, v4 = ba[0:6], ba[6:] + bb[0:4], bb[4:] + bc[0:2], bc[2:]

        #print(v1, v2, v3, v4)
        resulta = cyclemult(v1,cya)
        resultb = cyclemult(v2,cyb)
        resultc = cyclemult(v3,cyc)
        resultd = cyclemult(v4,cyd)

        #print(resulta, resultb, resultc, resultd)
        text1 = resulta + resultb[0:2]
        text2 = resultb[2:] + resultc[0:4]
        text3 = resultc[4:] + resultd

        #print(text1,text2,text3)
        #print('')
        z.append(gettextval(text1))
        z.append(gettextval(text2))
        z.append(gettextval(text3))
    return "".join(z)

def bulk_encrypt_lines(text_lines,key):
    ciph_lines = []
    for t in text_lines:
        ciph=encrypt(t,key)
        ciph_lines.append(ciph)
    return ciph_lines

def bulk_decrypt_lists(list_inputs,key):
    #print(list_inputs)
    cl = []
    tl = []
    for c in list_inputs:
        cl.append("".join(c))
    #print(cl)
    for c in cl:
        #print(c)
        d=decrypt(c,key)
        #print(d)
        tl.append(d)
    #print(tl,cl)
    return tl,cl

def bulk_decrypt_lines(lines,key):
    tl = []
    for c in lines:
        tl.append(decrypt(c,key))
    return tl

def encrypt_file(filename, filenameout, key):
    # need a filesize header on encrypted file to deal with length mismatch
    # pads size to 
    #open(filename,mode='r') as f:
    #    f.read(
    k = key
    if len(k) < 4:
        return []
    sz = os.path.getsize(filename)
    data = None
    chunksize = 240
    bytesread = 0
    filechunks = sz // 240
    chunksize = 240
    m = float(chunksize)/float(len(key))
    
    val = (4.0/3.0)*chunksize
    
    while (len(k) < val):
        k = k + key
    k = k + key
    lenbinsz = len(bin(sz)[2:])
    lenbinbytesz = len(bin(sz)[2:]) // 8
    paddedbinsz = '0'*((lenbinbytesz*8)-lenbinsz) + (bin(sz)[2:])
    with open(filename,mode='rb') as f:
        with open(filenameout,mode='wb') as fo:
            
            intsz = bin(sz)[2:]
            fo.write(bytes(intsz,'utf-8'))
            fo.write(bytes('\n','utf-8'))
            endchunk = False
            while not endchunk:
                
                data = f.read(chunksize)
                if len(data) != 240:
                    endchunk = True
                    padding = bytes('_'*(240-len(data)),'utf-8')
                    data = data + padding

                ciphchunk = []
                #240 bytes
                # zip(data,k)
                # 24 bits each
                # or 3 bytes
                # 1920 bits or 80 sets of 24
                for i in range(80):
                    databytes = data[(i*3):(i*3)+3]
                    keys = k[(i*4):(i*4)+4]

                    #print(databytes,keys)
                    datachunks = ['0'*(8-len(bin(b)[2:])) + bin(b)[2:] for b in databytes]
                    keychunks =  [getbinval(b) for b in keys]

                    #print(datachunks,keychunks)
                    
                    datachunks = [datachunks[0][0:6],
                                  datachunks[0][6:] + datachunks[1][0:4],
                                  datachunks[1][4:] + datachunks[2][0:2],
                                  datachunks[2][2:]]

                    keyCycles = []
                    for ke in keys:
                        keyCycles.append(cycleselect(alphalist.index(ke)))
                    #print(keyCycles)
                    ciphchunks = [ cyclemult(datachunks[iii],keyCycles[iii]) for iii in range(4)]
                    #print(ciphchunks)
                    ciphbinstrings = [ ciphchunks[0] + ciphchunks[1][0:2],
                                       ciphchunks[1][2:] + ciphchunks[2][0:4],
                                       ciphchunks[2][4:] + ciphchunks[3]]

                    #print(ciphbinstrings)
                    ciphbytes = [bitstring_to_bytes("".join(ciphbinstrings[0])),
                                bitstring_to_bytes("".join(ciphbinstrings[1])),
                                bitstring_to_bytes("".join(ciphbinstrings[2]))]
                    #print(ciphbytes)
                                            
                    fo.write(ciphbytes[0])
                    fo.write(ciphbytes[1])
                    fo.write(ciphbytes[2])

def get_next_parsed_entry(z):
    #print(len(z))
    firstBracket = z.find('[')
    #print(firstBracket)
    if firstBracket==-1:
        return [-1,-1]
    idx = firstBracket + 1
    #get string
    state = 0
    firstparenth, startint, secondstartint, file, count1, count2 = 0,0,0,'',0,0
    while(state <= 4):
        #file string
        if(state == 0):
            if(z[idx]=='\''):
                firstparenth = idx
                state = state + 1
        elif (state == 1):
            
            if(z[idx]=='\'') and (z[idx-1]!='\\'):
                #print(file)
                file = z[firstparenth+1:idx].replace('\\\\','\\')
                state = state + 1
        #count 1 int
        elif (state == 2):
            if(z[idx]==','):
                startint = idx
                state = state + 1
        elif (state == 3):
            if(z[idx]==','):
                count1 = int(z[startint+1:idx])
                secondstartint = idx
                state = state + 1
        elif (state == 4):
            if(z[idx]==']'):
                count2 = int(z[secondstartint+1:idx])
                state = state + 1
        idx = idx + 1

    return [file,count1,count2], z[idx+1:] 
    
#shallow only
def decrypt_header(s,key):
    #print('-----decrypt header step-----------')
    #print(type(s))
    #print(s)
    header = text_decrypt(s.decode('utf-8'),key)
    #print(header)
    header = header.rstrip('_')
    firstBracket = header.find('[')
    lastBracket = header.rfind(']')
    if firstBracket!=0 and lastBracket!= len(header):
        return []
    header = header[1:-1]
    #print(header)
    #print(len(header))
    z = get_next_parsed_entry(header)
    entry,header = z
    l = []
    while entry != -1:
        l.append(entry)
        #print(entry,'entry length-', len(entry[0]))
        entry,header = get_next_parsed_entry(header)
    return l

def decrypt_file_from_storage(start_pos, filename, filesize, encrypted_locker_filename, key):
    sz = filesize
    k = key

    if len(k) < 4:
        return []
    data = None
    chunksize = 240
    bytesread = 0
    filechunks = sz // 240
    fileSz = ( sz % 240 )
    if (sz % 240 != 0):
        filechunks = filechunks + 1
    chunksize = 240
    m = float(chunksize)/float(len(key))
    val = (4.0/3.0)*chunksize
    while (len(k) < val):
        k = k + key
    k = k + key
    
    #split
    import os
    #print(filename)
    #print(os.path.dirname(filename))
    try:
        os.makedirs(os.path.dirname(filename))
    except FileExistsError:
        pass
    except FileNotFoundError:
        pass
    
    with open(encrypted_locker_filename,mode='rb') as f:
        f.seek(start_pos)
        
        with open(filename,mode='w+b') as fo:

            for z in range(filechunks):
                #print(z,fileSz)
                
                data = f.read(chunksize)
                #print(data)
                ciphchunk = []
                #240 bytes
                # zip(data,k)
                # 24 bits each
                # or 3 bytes
                # 1920 bits or 80 sets of 24        or 80 sets of 3 bytes
                for i in range(80):
                    databytes = data[(i*3):(i*3)+3]
                    keys = k[(i*4):(i*4)+4]

                    #print(databytes,keys)
                    bindatachunks = ['0'*(8-len(bin(b)[2:])) + bin(b)[2:] for b in databytes]
                    keychunks =  [getbinval(b) for b in keys]

                    #print(bindatachunks)
                    #print(keychunks)

                    #print(bindatachunks,keychunks)
                    
                    bindatachunks = [bindatachunks[0][0:6],
                                  bindatachunks[0][6:] + bindatachunks[1][0:4],
                                  bindatachunks[1][4:] + bindatachunks[2][0:2],
                                  bindatachunks[2][2:]]
                    
                    #    print(i)
                    #    print(z)
                    #    print(filechunks)
                        
                        
                    #print(bindatachunks)
                    
                    keyCycles = []
                    
                    for ke in keys:
                        keyCycles.append(inversecycle(cycleselect(alphalist.index(ke))))
                        
                    #print(keyCycles)
                    #print('filechunks: ',z, 'ciphcount: ', ciphcount,'  ', filechunks,' i: ',i,' 80')
                    ciphchunks = [ cyclemult(bindatachunks[ciphcount],keyCycles[ciphcount]) for ciphcount in range(4)]
                    #print(ciphchunks)
                    ciphbinstrings = [ ciphchunks[0] + ciphchunks[1][0:2],
                                       ciphchunks[1][2:] + ciphchunks[2][0:4],
                                       ciphchunks[2][4:] + ciphchunks[3]]

                    #print(ciphbinstrings)
                    ciphbytes = [bitstring_to_bytes("".join(ciphbinstrings[0])),
                                bitstring_to_bytes("".join(ciphbinstrings[1])),
                                bitstring_to_bytes("".join(ciphbinstrings[2]))]
                    #print(ciphbytes)

                    if z!=filechunks-1:                      
                        fo.write(ciphbytes[0])
                        fo.write(ciphbytes[1])
                        fo.write(ciphbytes[2])
                    else:
                        #32byte block   32,33,34  35 byte file
                        #test this for off by one
                        currentByteBlock = z*240 + i*3
                        #print('------------',i,'-----------------',currentByteBlock)
                        
                        if (currentByteBlock - sz) >= 0:
                            #check that this breaks out of the function
                            break    
                        elif (currentByteBlock+1 - sz) == 0:
                            fo.write(ciphbytes[0])
                        elif (currentByteBlock+2 - sz) == 0:
                            fo.write(ciphbytes[0])
                            fo.write(ciphbytes[1])
                        else:
                            fo.write(ciphbytes[0])
                            fo.write(ciphbytes[1])
                            fo.write(ciphbytes[2])

def encrypt_file_for_storage(filename, encrypted_file_handle, key):
    # need a filesize header on encrypted file to deal with length mismatch
    # pads size to 
    #open(filename,mode='r') as f:
    #    f.read(
    k = key
    if len(k) < 4:
        return []
    sz = os.path.getsize(filename) + 1
    data = None
    chunksize = 240
    fileSz = ( sz % 240 )
    bytesread = 0
    filechunks = sz // 240
    chunksize = 240
    m = float(chunksize)/float(len(key))
    val = (4.0/3.0)*chunksize

    k = key

    if len(k) < 4:
        return []
    data = None
    
    bytesread = 0
    
    if (sz % 240 != 0):
        filechunks = filechunks + 1

    
    while (len(k) < val):
        k = k + key
    k = k + key
    lenbinsz = len(bin(sz)[2:])
    lenbinbytesz = len(bin(sz)[2:]) // 8
    paddedbinsz = '0'*((lenbinbytesz*8)-lenbinsz) + (bin(sz)[2:])
    with open(filename,mode='rb') as f:

        endchunk = False
        while not endchunk:
                
            data = f.read(chunksize)
            if len(data) != 240:
                endchunk = True
                padding = bytes('_'*(240-len(data)),'utf-8')
                data = data + padding

            ciphchunk = []
                #240 bytes
                # zip(data,k)
                # 24 bits each
                # or 3 bytes
                # 1920 bits or 80 sets of 24
            for i in range(80):
                databytes = data[(i*3):(i*3)+3]
                keys = k[(i*4):(i*4)+4]

                #print(databytes,keys)
                datachunks = ['0'*(8-len(bin(b)[2:])) + bin(b)[2:] for b in databytes]
                keychunks =  [getbinval(b) for b in keys]
    
                datachunks = [datachunks[0][0:6],
                                  datachunks[0][6:] + datachunks[1][0:4],
                                  datachunks[1][4:] + datachunks[2][0:2],
                                  datachunks[2][2:]]

                keyCycles = []
                for ke in keys:
                    keyCycles.append(cycleselect(alphalist.index(ke)))
                #print(keyCycles)
                ciphchunks = [ cyclemult(datachunks[iii],keyCycles[iii]) for iii in range(4)]
                #print(ciphchunks)
                ciphbinstrings = [ ciphchunks[0] + ciphchunks[1][0:2],
                                       ciphchunks[1][2:] + ciphchunks[2][0:4],
                                       ciphchunks[2][4:] + ciphchunks[3]]

                #print(ciphbinstrings)
                ciphbytes = [bitstring_to_bytes("".join(ciphbinstrings[0])),
                                bitstring_to_bytes("".join(ciphbinstrings[1])),
                                bitstring_to_bytes("".join(ciphbinstrings[2]))]
                #print(ciphbytes)
                                            
                encrypted_file_handle.write(ciphbytes[0])
                encrypted_file_handle.write(ciphbytes[1])
                encrypted_file_handle.write(ciphbytes[2])
                    
def decrypt_file(filename,filenameout,key):
    sz = os.path.getsize(filename)
    szlength = (sz % 240)
    k = key

    if len(k) < 4:
        return []
    data = None
    chunksize = 240
    bytesread = 0
    filechunks = (sz-szlength) // 240
    chunksize = 240
    m = float(chunksize)/float(len(key))
    val = (4.0/3.0)*chunksize
    while (len(k) < val):
        k = k + key
    k = k + key

    with open(filename,mode='rb') as f:
        with open(filenameout,mode='wb') as fo:

            fileLengthBitBytes = f.read(szlength)
            fileLengthBits = [ chr(int(i)) for i in fileLengthBitBytes ]
            #print(fileLengthBits)
            fileLengthBitString= "".join(fileLengthBits[0:-1])
            fileSz = int(fileLengthBitString,2)
            for z in range(filechunks):
                
                data = f.read(chunksize)
                ciphchunk = []
                #240 bytes
                # zip(data,k)
                # 24 bits each
                # or 3 bytes
                # 1920 bits or 80 sets of 24        or 80 sets of 3 bytes
                for i in range(80):
                    databytes = data[(i*3):(i*3)+3]
                    keys = k[(i*4):(i*4)+4]

                    #print(databytes,keys)
                    bindatachunks = ['0'*(8-len(bin(b)[2:])) + bin(b)[2:] for b in databytes]
                    keychunks =  [getbinval(b) for b in keys]

                    #print(bindatachunks,keychunks)
                    
                    bindatachunks = [bindatachunks[0][0:6],
                                  bindatachunks[0][6:] + bindatachunks[1][0:4],
                                  bindatachunks[1][4:] + bindatachunks[2][0:2],
                                  bindatachunks[2][2:]]
                    #print(bindatachunks)
                    
                    keyCycles = []
                    
                    for ke in keys:
                        keyCycles.append(inversecycle(cycleselect(alphalist.index(ke))))
                        
                    #print(keyCycles)
                    
                    ciphchunks = [ cyclemult(bindatachunks[ciphcount],keyCycles[ciphcount]) for ciphcount in range(4)]
                    #print(ciphchunks)
                    ciphbinstrings = [ ciphchunks[0] + ciphchunks[1][0:2],
                                       ciphchunks[1][2:] + ciphchunks[2][0:4],
                                       ciphchunks[2][4:] + ciphchunks[3]]

                    #print(ciphbinstrings)
                    ciphbytes = [bitstring_to_bytes("".join(ciphbinstrings[0])),
                                bitstring_to_bytes("".join(ciphbinstrings[1])),
                                bitstring_to_bytes("".join(ciphbinstrings[2]))]
                    #print(ciphbytes)

                    if z!=filechunks-1:                      
                        fo.write(ciphbytes[0])
                        fo.write(ciphbytes[1])
                        fo.write(ciphbytes[2])
                    else:
                        #32byte block   32,33,34  35 byte file
                        #test this for off by one
                        currentByteBlock = z*240 + i*3
                        if (currentByteBlock - fileSz) >= 0:
                            #check that this breaks out of the function
                            break    
                        elif (currentByteBlock+1 - fileSz) == 0:
                            fo.write(ciphbytes[0])
                        elif (currentByteBlock+2 - fileSz) == 0:
                            fo.write(ciphbytes[0])
                            fo.write(ciphbytes[1])
                        else:
                            fo.write(ciphbytes[0])
                            fo.write(ciphbytes[1])
                            fo.write(ciphbytes[2])
                            
def get_header_file_sizes(storage_file_name,key):
    with open(storage_file_name,'rb') as storage_file:
        sf = storage_file.read(101).decode('utf-8')
        #print('--------HEADER FILE SIZES---------')
        #print(sf)
        #print('----------------------------------')
        headerzeroindex = sf.find('\0')
        filesizezero = sf[headerzeroindex+1:].find('\0')
        header_length = int(sf[0:headerzeroindex])
        crypt_header_size = int(sf[headerzeroindex+1:headerzeroindex+1+filesizezero])
    return header_length, crypt_header_size

def list_folder_files(storage_file_name,key):
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

def decrypt_folder(new_folder_name,storage_file_name,key):
    header_length, crypt_header_size = get_header_file_sizes(storage_file_name,key)
    listofFiles = list_folder_files(storage_file_name,key)
    start_offset = crypt_header_size + len(str(header_length)+'\0') + len(str(crypt_header_size)+'\0')
    #print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<decrypt<<<<<<<<<<<<<<<<<<<<<<<')

    #print('----------head_length----------------')
    #print(header_length)
    #print('----------crypt_header------------')
    #print(crypt_header_size)
    #print('----------list_folder_files----------')
    #print(listofFiles)

    for filetuple in listofFiles:
        #start_pos, filename, filesize, encrypted_locker_filename, key
        #print('--------------------------------',new_folder_name+filetuple[0],start_offset)
        decrypt_file_from_storage(start_offset+filetuple[1], new_folder_name+filetuple[0], filetuple[2], storage_file_name, key)
    
def encrypt_folder(startpath,storage_file_name,key):
    #print('----encrypt_folder_step------')
    file_list = get_files_directory(startpath)
    #print(file_list)
    header = bytes(text_encrypt(str(file_list),key),'utf-8')
    #print(len(text_encrypt(str(file_list),key)),len(str(file_list)))
    s = sum((f[2] for f in file_list))
    header_length = len(str(file_list))
    cryptheader_length = len(header)
    
#    whole_file_size = len(str(header_length)) + 1 + len(str(cryptheader_length)) + 1 + s + 1
#    whole_file_size = whole_file_size + len(str(crypt_header_size)+'\0')
    
    #print(whole_file_size)
    #print(file_list)
    # output
    # whole_file_size
    # str(file_list)
    # files + '\0'
    # str(file_list again)
    
    #print(file_list)
    #print('---header--length----------')
    #print(header_length)
    #print('------------------------')
    #print(whole_file_size)
    #print('---crypted header-------')
    #print(header,len(header))
    #print('-----------------------')
    
    with open(storage_file_name,'wb') as storage_file:
        storage_file.write(bytes(str(header_length) + str('\0'),'utf-8'))
        storage_file.write(bytes(str(cryptheader_length) + str('\0'),'utf-8'))
        storage_file.write(header)
        for current_file_header in file_list:
            #print(os.path.basename(current_file_header[0]))
            with open(os.path.basename(current_file_header[0]),'w+b') as f:
                #print(os.path.basename(current_file_header[0]))
                encrypt_file_for_storage(startpath + '\\' + current_file_header[0], f, key)
            encrypt_file_for_storage(startpath + '\\' + current_file_header[0], storage_file, key)
            storage_file.write(bytes(str('\0'),'utf-8'))
        storage_file.write(header)

'''
        print('-------------listOfFiles-------------------')
        for i in listOfFiles:
            print(i)
    
    print('----sf---------------------')
    print(sf)
    print(len(sf))
    print('---------------------------')
    print(headerzeroindex)
    print('---------------------------')
    print(filesizezero)
    print('--header_length-------------------------')
    print(header_length)
    print('---crypt_header----------------')
    print(crypt_header)
    print('-----header----------------')
    print(header)
    print('--------headerzeroindex+filesizezero+2+header_length------------')
    print(headerzeroindex+filesizezero+2+header_length,headerzeroindex,filesizezero)
    print('-----------------')
    print(whole_file_size)
    print('---------------------------')
'''
    
#for i in a:
#    print(i)
#    encrypt_file(i,i+'.ciph','randomkeytesta')
#    decrypt_file(i+'.ciph',i+'.ciph.deciph','randomkeytesta')

#print(get_files_directory("abc"))
#encrypt_file('inputtext.txt', "asldfkj.txt", "test key")
#decrypt_file('asldfkj.txt', "asldfkj2.txt", "test key")


#aa = encrypt_folder("test folder","testfolder.fre","test key")
import sys
foldername=input('enter target folder name')
binfile=input('enter bin file name')
key = input('enter key')
decrypt_folder(foldername, binfile, key)

#decrypt_folder("new folder 2","testfolder.fre","test key")
#z = [i[0] for i in get_files_directory('test folder')]
#print(z)
#diff(z,'test folder','new folder 2')
#header_length, crypt_header_size = get_header_file_sizes('testfolder.fre','test key')
#start_offset = crypt_header_size + len(str(header_length)+'\0') + len(str(crypt_header_size)+'\0')
#print(header_length,crypt_header_size,start_offset)
#listofFiles = list_folder_files('testfolder.fre','test key')
#print(listofFiles)
#with open('testfolder.fre','rb') as f:
#    f.seek(start_offset)
#    z=f.read(1570)
#    print(z)
    
#decrypt_file_from_storage(0+start_offset, 'f.py',1571,'testfolder.fre', 'test key')
#decrypt_file_from_storage(1571+start_offset, 'a.py', 451, 'testfolder.fre', 'test key')

#decrypt_file_from_storage(start_pos, filename, filesize, encrypted_locker_filename, key)

#print(list_folder_files("testfolder.fre","test key"))
#print(z)
#a = json.dumps(z)
#b = json.loads(a)
#print(z==b)

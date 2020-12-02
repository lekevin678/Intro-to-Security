import hashlib
import string
import time
import sys

def hash__SHA1(word):
    m = hashlib.sha1(word)
    return m.hexdigest()

def hash__SHA256(word):
    m = hashlib.sha256(word)
    return m.hexdigest()

def hash__SHA3256(word):
    m = hashlib.sha3_256(word)
    return m.hexdigest()

def hash__MD5(word):
    m = hashlib.md5(word)
    return m.hexdigest()

def hash__BLAKE2b(word):
    m = hashlib.blake2b(word)
    return m.hexdigest() 

def bloomSetup(bloomFilter__5, bloomFilter__3, bloomLength , f):
    for i in f:
        plainText = i.rstrip()
        hString = hash__SHA1(plainText) 
        index_SHA1 = int(hString, 16) % bloomLength
        

        hString = hash__SHA256(plainText) 
        index_SHA256 = int(hString, 16) % bloomLength

        hString = hash__SHA3256(plainText) 
        index_SHA3 = int(hString, 16) % bloomLength
        

        hString = hash__MD5(plainText) 
        index_MD5 = int(hString, 16) % bloomLength
        

        hString = hash__BLAKE2b(plainText) 
        index_BLAKE = int(hString, 16) % bloomLength


        bloomFilter__5[index_SHA1] = 1

        bloomFilter__5[index_SHA256] = 1
        bloomFilter__3[index_SHA256] = 1

        bloomFilter__5[index_SHA3] = 1
        bloomFilter__3[index_SHA3] = 1

        bloomFilter__5[index_MD5] = 1
        bloomFilter__3[index_MD5] = 1

        bloomFilter__5[index_BLAKE] = 1

def bloomCheck__5(bloomFilter__5, bloomLength, s):
    hString = hash__SHA1(s) 
    index_SHA1 = int(hString, 16) % bloomLength

    hString = hash__SHA256(s) 
    index_SHA256 = int(hString, 16) % bloomLength

    hString = hash__SHA3256(s) 
    index_SHA3 = int(hString, 16) % bloomLength
        
    hString = hash__MD5(s) 
    index_MD5 = int(hString, 16) % bloomLength
        
    hString = hash__BLAKE2b(s) 
    index_BLAKE = int(hString, 16) % bloomLength

    if(bloomFilter__5[index_SHA1] == 1 and bloomFilter__5[index_SHA256] == 1 and bloomFilter__5[index_SHA3] == 1 and bloomFilter__5[index_MD5] == 1 and bloomFilter__5[index_BLAKE] == 1):
        return 1
    else:
        return 0

def bloomCheck__3(bloomFilter__3, bloomLength, s):
    hString = hash__SHA256(s) 
    index_SHA256 = int(hString, 16) % bloomLength

    hString = hash__SHA3256(s) 
    index_SHA3 = int(hString, 16) % bloomLength
        
    hString = hash__MD5(s) 
    index_MD5 = int(hString, 16) % bloomLength

    if(bloomFilter__3[index_SHA256] == 1 and bloomFilter__3[index_SHA3] == 1 and bloomFilter__3[index_MD5] == 1):
        return 1
    else:
        return 0

dictArg = sys.argv[2]
inputArg = sys.argv[4]
output3Arg = sys.argv[6]
output5Arg = sys.argv[7]

bloomLength = 2364657
bloomFilter__5 = [0] * bloomLength
bloomFilter__3 = [0] * bloomLength

dictionary = open(dictArg, "r+b");
bloomSetup(bloomFilter__5, bloomFilter__3, bloomLength, dictionary)



inputFile = open(inputArg, "r+b")
num = int(inputFile.readline().rstrip())
inputWords = []

for i in range(num):
    inputWords.append(inputFile.readline().rstrip())

out3 = open(output3Arg, "w")
for i in inputWords:
    isBad = bloomCheck__3(bloomFilter__3, bloomLength, i)

    if (isBad == 1):
        out3.write("maybe\n")
    else:
        out3.write("no\n")

out5 = open(output5Arg, "w")
for i in inputWords:
    isBad = bloomCheck__5(bloomFilter__5, bloomLength, i)

    if (isBad == 1):
        out5.write("maybe\n")
    else:
        out5.write("no\n")






#find time for one password
dictionary.seek(0)
test = dictionary.readline().rstrip()

start = time.time()
bloomCheck__3(bloomFilter__3, bloomLength, i)
end = time.time() - start
print("BLOOMCHECK 3 TIME: ", end='')
print(end)


start = time.time()
bloomCheck__5(bloomFilter__5, bloomLength, i)
end = time.time() - start
print("BLOOMCHECK 5 TIME: ", end='')
print(end)

dictionary.close()
inputFile.close()
out5.close()       
out3.close()


    


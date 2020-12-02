from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

import random
import string
import time

class Hash:
    def get_random_string(self, randNum):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(randNum))
        return result_str

    def find_hash(self, s):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(s)
        temp = digest.finalize()
        hexString = ""
        for i in temp:
            hexString = hexString + (i.encode("hex"))
        
        return  hexString[0:3]


class Hash_Weak(Hash):
    randS__Key = ""
    hash__Key = ""

    def runTrials(self, i):
        print("Run (%d)     Key: %s" % (i , self.hash__Key))
            
        trialNum = 0
        foundMatch = False 

        while (foundMatch == False):
            randNum = random.randint(2,100);
            randomWord = self.get_random_string(randNum)
            randomHash = self.find_hash(randomWord)

            if randomWord==self.randS__Key:
                continue

            trialNum += 1

            if randomHash==self.hash__Key:
                print("     *****FOUND MATCH*****")
                print("         Strings:\t%s != %s" % (self.randS__Key, randomWord))
                print("         Hashes:\t%s == %s" % (self.hash__Key, randomHash ))
                print("\n         Number of Trials: %d\n" % trialNum )
                foundMatch = True
            
            else:
                continue

        return trialNum

    def __init__(self):
        randNum = random.randint(2,100);
        self.randS__Key = self.get_random_string(randNum)
        self.hash__Key = self.find_hash(self.randS__Key)
        
class Hash_Strong(Hash):
    hashDict = dict()

    def runTrials(self, i):
        print("Run (%d)" % (i))
            
        trialNum = 0
        foundMatch = False 

        while (foundMatch == False):
            randomNum = random.randint(2,100);
            randomWord = self.get_random_string(randomNum)
            randomHash = self.find_hash(randomWord)

            if randomHash in self.hashDict:
                if self.hashDict[randomHash]==randomWord:
                    continue

                trialNum += 1
                end = time.time()
                print("     *****FOUND MATCH*****")
                print("     Trials: %d" % trialNum )
                foundMatch = True
        
            else:
                trialNum += 1
                self.hashDict[randomHash] = randomWord

        self.hashDict.clear()
        return trialNum



print("HOW MANY TRAILS WILL I TAKE TO BREAK SHA_256 STRONG COLLISION RESISTANCE (ONLY FIRST 24 BITS OF HASH)? \n")
i = 0
strong_average = 0

while(i < 10):
    i += 1
    one = Hash_Strong()
    strong_average += one.runTrials(i)

strong_average = strong_average / i
print("\n\nAVERAGE NUMBER OF TRIALS: %d\n\n" % strong_average)





print("HOW MANY TRAILS WILL I TAKE TO BREAK SHA_256 WEAK COLLISION RESISTANCE (ONLY FIRST 24 BITS OF HASH)? \n")
i = 0
weak_average = 0

while(i < 10):
    i += 1
    one = Hash_Weak()
    weak_average += one.runTrials(i)

weak_average = weak_average / i
print("\n\nAVERAGE NUMBER OF TRIALS: %d" % weak_average)


print("\n\nSTRONG COLLISION RESISTANCE AVERAGE - %d trials" % strong_average)
print("WEAK COLLISION RESISTANCE AVERAGE - %d trials" % weak_average)





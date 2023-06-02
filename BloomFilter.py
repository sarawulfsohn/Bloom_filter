from BitHash import BitHash
from BitVector import BitVector

class BloomFilter(object):
        
        
    # Return the estimated number of bits needed (N in the slides) in a Bloom 
    # Filter that will store numKeys (n in the slides) keys, using numHashes 
    # (d in the slides) hash functions, and that will have a
    # false positive rate of maxFalsePositive (P in the slides).
    # See the slides for the math needed to do this.  
    def __bitsNeeded(self, numKeys, numHashes, maxFP):
        
        # You use Equation B to get the desired phi from P and d
        phi = 1 - maxFP ** (1/numHashes)
        
        # You then use Equation D to get the needed N from d, phi, and n
        N = numHashes / (1 - (phi ** (1/numKeys)))
        
        # N is the value to return from bitsNeeded
        return round(N)     
    
    # Create a Bloom Filter that will store numKeys keys, using 
    # numHashes hash functions, and that will have a false positive 
    # rate of maxFalsePositive.
    # All attributes must be private.
    def __init__(self, numKeys, numHashes, maxFP):      
        self.__numKeys   = numKeys
        self.__numHashes = numHashes
        self.__maxFP     = maxFP
        
        # will need to use __bitsNeeded to figure out how big
        # of a BitVector will be needed        
        self.__numbits = self.__bitsNeeded(numKeys, numHashes, maxFP)    
        
        '''In addition to the BitVector, might you need any other attributes?'''
        self.__bloomFilter = BitVector(size = self.__numbits)
        self.__numBitsSet = 0
        
    
    
    # insert the specified key into the Bloom Filter.
    # Doesn't return anything, since an insert into 
    # a Bloom Filter always succeeds!
    # See the "Bloom Filter details" slide for how insert works.
    def insert(self, key):
        for i in range(self.__numHashes):
            hashh = BitHash(key, i)
            index = hashh % self.__numbits
            if self.__bloomFilter[index] != 1: #if we havent already set that one
                self.__bloomFilter[index] = 1 #set it to true
                self.__numBitsSet += 1        #increment count

    
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    # See the "Bloom Filter details" slide for how find works.
    def find(self, key):
        #– For i = 1 .. d 
        for i in range(self.__numHashes):
            hashh = BitHash(key, i)
            
            #check the bit at position Hi(key) % N
            if self.__bloomFilter[hashh % self.__numbits] != 1:
                return False #as soon as i find a 0 i return false
            
        return True
            
       
       
    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    # This is NOT the same thing as trying to use the Bloom Filter and
    # measuring the proportion of false positives that are actually encountered.   
    def falsePositiveRate(self):
        
        # What is phi in this case? it is the ACTUAL measured current proportion 
        # of bits in the bit vector that are still zero.         
        phi = (self.__numbits - self.__numBitsSet) / self.__numbits
        #(1 - self.__numHashes/self.__numBits)** self.__numKeys # eqtn c
        
        # In other words, you use equation A to give you P from d and phi. 
        P = (1 - phi) ** self.__numHashes
        return P  
    
    # Returns the current number of bits ACTUALLY set in this Bloom Filter
    # WHEN TESTING, MAKE SURE THAT YOUR IMPLEMENTATION DOES NOT CAUSE
    # THIS PARTICULAR METHOD TO RUN SLOWLY.
    def numBitsSet(self):
        return self.__numBitsSet 


       
def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    # create the Bloom Filter 
    B = BloomFilter(numKeys, numHashes, maxFalse)
    
    # read the first numKeys words from the file and insert them 
    # into the Bloom Filter. Close the input file.
    file = open("wordlist.txt", "r")
    count = 0
    
    for line in file:        #for each line
        if count < numKeys:  #while we havent reached total
            B.insert(line)  # insert them into the filter
            count += 1      #increment count of inserted words
    file.close()
    

    # Print out what the PROJECTED false positive rate should 
    # THEORETICALLY be based on the number of bits that ACTUALLY ended up being set
    # in the Bloom Filter. Use the falsePositiveRate method.
    print("projected false positive rate: ", B.falsePositiveRate())

    # Now re-open the file, and re-read the same bunch of the first numKeys 
    # words from the file and count how many are missing from the Bloom Filter, 
    # printing out how many are missing. This should report that 0 words are 
    # missing from the Bloom Filter.
    
    file = open("wordlist.txt", "r")
    count = 0
    missing = 0
    line = file.readline()
    
    
    while count < numKeys: #re-read the first numkeys
        ans = B.find(line)
        if ans == False: missing += 1
        count += 1 #increment count of how many keys have been checked
        line = file.readline() #move to next line
    print ("missing words: ", missing)
    

    # Now read the next numKeys words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.
    
    count = 0
    foundfalse = 0
    line = file.readline() #move to next line
    
    while count < numKeys: #continue reading the next numkey lines
        ans = B.find(line)
        if ans == True: foundfalse += 1
        count += 1 #increment count of how many keys have been checked
        line = file.readline() #move to next line
    print ("falsely found: ", foundfalse)   
    file.close()
    
    # Print out the percentage rate of false positives.
    # THIS NUMBER MUST BE CLOSE TO THE ESTIMATED FALSE POSITIVE RATE ABOVE
    actualPercentage =  foundfalse/numKeys
    print("actual false positive percentage: ", actualPercentage)
   
    
if __name__ == '__main__':
    __main()       
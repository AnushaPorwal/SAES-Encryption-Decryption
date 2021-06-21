import numpy as np

def bitStr2Matrix(msg):
    #input is a 16bit string
    #output is a 2x2 matrix with 4 bits in each position
    
    #input to output positioning:
    #input: a, b, c, d ; where each alphabet is 4 bits long.
    #output: a , c
    #        b , d
    msgMat = [ [np.array([], dtype = np.int64), np.array([], dtype = np.int64)], 
               [np.array([], dtype = np.int64), np.array([], dtype = np.int64)] ]

    for i in range(0, 4):
        msgMat[0][0] = np.append(msgMat[0][0], int(msg[i]))
        msgMat[0][1] = np.append(msgMat[0][1], int(msg[i+8]))
        msgMat[1][0] = np.append(msgMat[1][0], int(msg[i+4]))
        msgMat[1][1] = np.append(msgMat[1][1], int(msg[i+12]))
    
    return msgMat

def matrix2bitstring(ipmatrix):
    #Converting a 2x2 matrix to 16bit output string.
    
    #input to output positioning:
    #input: a , c
    #       b , d
    #output: a, b, c, d ; where each alphabet is 4 bits long.
    
    msgop = ""
    for i in range(0, 2):
        for j in range(0, 2):
            for k in range(0, 4):
                msgop = msgop + str(ipmatrix[j][i][k])
    return msgop

def keyGeneration(key):
    #Function to generate 6 round keys of 8 bit each, from the key of 16 bits
    #input is the 2x2 list of np arrays of 4 numbers each => 4 bits
    #returns a 6x2 list of np arrays with the round keys
    
    #Round Constants
    RCon = [[np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0])],
            [np.array([0, 0, 1, 1]), np.array([0, 0, 0, 0])]]
    
    #Substitution Box
    sBox = [[np.array([1, 0, 0, 1]), np.array([0, 1, 0, 0]), np.array([1, 0, 1, 0]), np.array([1, 0, 1, 1])],
            [np.array([1, 1, 0, 1]), np.array([0, 0, 0, 1]), np.array([1, 0, 0, 0]), np.array([0, 1, 0, 1])],
            [np.array([0, 1, 1, 0]), np.array([0, 0, 1, 0]), np.array([0, 0, 0, 0]), np.array([0, 0, 1, 1])],
            [np.array([1, 1, 0, 0]), np.array([1, 1, 1, 0]), np.array([1, 1, 1, 1]), np.array([0, 1, 1, 1])]]
    
    #each row of word variable is a round key, w0 to w5:
    word = [[np.array([]), np.array([])],
            [np.array([]), np.array([])],
            [np.array([]), np.array([])],
            [np.array([]), np.array([])],
            [np.array([]), np.array([])],
            [np.array([]), np.array([])]]
    
    #word0 is simply k0 and k1:
    word[0][0] = key[0][0]
    word[0][1] = key[1][0]
    
    #word1 is simply k2 and k3:
    word[1][0] = key[0][1]
    word[1][1] = key[1][1]
    
    #start word2:
    #word0 XOR RCon[0] XOR SubNib(RotNib(word1))
    
    #swapped word1, ie RotNib(word1):
    nib = [word[1][1], word[1][0]]
    
    for j in range(len(nib)):
        #for each element, row number is determined by the left most 2 bits of the input element
        # col number is determined by the rightmost 2 bits
        rowStr = "" + str(nib[j][0]) + str(nib[j][1])
        colStr = "" + str(nib[j][2]) + str(nib[j][3])
        #converting the binary bits to decimal integers to access the table:
        row = int(rowStr, 2)
        col = int(colStr, 2)
        #substituting:
        nib[j] = sBox[row][col]
        #XORing the output of SubNib(RotNib(word1)), Rcon[0] and word0 (nibble wise):
        nib[j] = (nib[j] + RCon[0][j] + word[0][j])%2
        word[2][j] = nib[j]
    #end word2
    
    #start word3:
    #XORing word2 and word1 (nibble wise):
    for i in range(0, 2):
        word[3][i] = word[2][i] + word[1][i]
        for j in range(0, len(word[3][i])):
            word[3][i][j] = word[3][i][j]%2
    #end word3
    
    #start word4:
    #word2 XOR RCon[1] XOR SubNib(RotNib(word3))
    
    #swapped word4, ie RotNib(word3):
    nib = [word[3][1], word[3][0]]
    
    for j in range(0, len(nib)):
        #for each element, row number is determined by the left most 2 bits of the input element
        # col number is determined by the rightmost 2 bits
        rowStr = "" + str(nib[j][0]) + str(nib[j][1])
        colStr = "" + str(nib[j][2]) + str(nib[j][3])
        #converting the binary bits to decimal integers to access the table:
        row = int(rowStr, 2)
        col = int(colStr, 2)
        #substituting:
        nib[j] = sBox[row][col]
        #XORing the output of SubNib(RotNib(word3)), Rcon[1] and word2 (nibble wise):
        nib[j] = (nib[j] + RCon[1][j] + word[2][j])%2
        word[4][j] = nib[j]
    #end word4
    
    #start word5:
    #XORing word4 and word3 (nibble wise):
    for i in range(0, 2):
        word[5][i] = word[4][i] + word[3][i]
        for j in range(0, len(word[5][i])):
            word[5][i][j] = word[5][i][j]%2
    #end word5
    
    wordsModified = [[word[0][0], word[1][0], word[2][0], word[3][0], word[4][0], word[5][0]],
                     [word[0][1], word[1][1], word[2][1], word[3][1], word[4][1], word[5][1]]]
         
    return wordsModified


def gf16MatrixMul(X, Y):
    #X and Y have to contain int32 or int64 np arrays
    #output contains int64 np arrays
    
    #Function for matrix multiplication in gf(16)
    #Irreducible polynimial is (1,0,0,1,1)
    #Input: X, Y: two 2x2 lists of np arrays
    # each np array has size 4, each indicating the associated polynomial.
    # Example: [1,1,1,0] => x^3 + x^2 + x (in the same order)
    
    result = [ [np.zeros(4), np.zeros(4)], [np.zeros(4), np.zeros(4)]]
    
    for i in range(0, len(X)):
        for j in range(0, len(Y[0])):
            for k in range(0, len(Y)):
                x = X[i][k]
                y = Y[k][j]
                mul = np.polymul(x, y)
                #mul.astype(np.int64)
                #dividing by the irreducible polynomial, and using the remainder
                quo, rem = np.polydiv(mul, np.array([1, 0, 0, 1, 1]))
                
                remnew = np.array([])
                
                #We want to keep the size of each np array as 4 only, not more not less
                if len(rem) < 4: #If length is less than 4, then we add required number of 0s to the left
                    remnew = np.zeros(4-len(rem))
                    remnew = np.append(remnew, rem)
                elif len(rem) > 4: #if length is more than 4, then we remove 0s from right
                    #there won't be any 1s, because weve already reduced it using our irreducible polynomial.
                    remnew = np.zeros(4)
                    for n in range(0, 4):
                        remnew[3-n] = int(rem[len(rem)-1-n])
                else: #if the size is 4, nothing needs to be done
                    remnew = rem
                
                #need to take mod of the coefficient values, by 2:
                for n in range(0, len(remnew)):
                    remnew[n] = remnew[n]%2
                
                result[i][j] += remnew
            
            #mod 2 again, after the values are added:
            for n in range(0, len(result[i][j])):
                result[i][j][n] = result[i][j][n]%2
    
    resultModified = [ [np.array([], dtype = np.int64), np.array([], dtype = np.int64)], 
                       [np.array([], dtype = np.int64), np.array([], dtype = np.int64)] ]
    
    for i in range(0, 2):
        for j in range(0, 2):
            for k in range(0, 4):
                resultModified[i][j] = np.append(resultModified[i][j], int(result[i][j][k]))
    
    return resultModified

def SBoxSubstitution(state):
    #Function for performing s box substitution
    #Input is a 2x2 list of np arrays. the size of the arrays is 4 (representing the number of bits)
    
    #SBox values:
    sBox = [[np.array([1, 0, 0, 1], dtype=np.int64), np.array([0, 1, 0, 0], dtype=np.int64), np.array([1, 0, 1, 0], dtype=np.int64), np.array([1, 0, 1, 1], dtype=np.int64)],
            [np.array([1, 1, 0, 1], dtype=np.int64), np.array([0, 0, 0, 1], dtype=np.int64), np.array([1, 0, 0, 0], dtype=np.int64), np.array([0, 1, 0, 1], dtype=np.int64)],
            [np.array([0, 1, 1, 0], dtype=np.int64), np.array([0, 0, 1, 0], dtype=np.int64), np.array([0, 0, 0, 0], dtype=np.int64), np.array([0, 0, 1, 1], dtype=np.int64)],
            [np.array([1, 1, 0, 0], dtype=np.int64), np.array([1, 1, 1, 0], dtype=np.int64), np.array([1, 1, 1, 1], dtype=np.int64), np.array([0, 1, 1, 1], dtype=np.int64)]]
    
    newState = [ [np.array([], dtype=np.int64), np.array([], dtype=np.int64)],
                 [np.array([], dtype=np.int64), np.array([], dtype=np.int64)] ]
    for i in range(len(state)):
        for j in range(len(state[0])):
            #for each element, row number is determined by the left most 2 bits of the input element
            # col number is determined by the rightmost 2 bits
            rowStr = "" + str(state[i][j][0]) + str(state[i][j][1])
            colStr = "" + str(state[i][j][2]) + str(state[i][j][3])
            #converting the binary bits to decimal integers to access the table:
            row = int(rowStr, 2)
            col = int(colStr, 2)
            #substituting:
            newState[i][j] = sBox[row][col]
    
    return newState

def InvSBoxSubstitution(state):
    #Function for performing inverse s box substitution
    #Input is a 2x2 list of np arrays. the size of the arrays is 4 (representing the number of bits)
    
    #Inverse SBox values:
    InvSBox = [[np.array([1, 0, 1, 0], dtype=np.int64), np.array([0, 1, 0, 1], dtype=np.int64), np.array([1, 0, 0, 1], dtype=np.int64), np.array([1, 0, 1, 1], dtype=np.int64)],
               [np.array([0, 0, 0, 1], dtype=np.int64), np.array([0, 1, 1, 1], dtype=np.int64), np.array([1, 0, 0, 0], dtype=np.int64), np.array([1, 1, 1, 1], dtype=np.int64)],
               [np.array([0, 1, 1, 0], dtype=np.int64), np.array([0, 0, 0, 0], dtype=np.int64), np.array([0, 0, 1, 0], dtype=np.int64), np.array([0, 0, 1, 1], dtype=np.int64)],
               [np.array([1, 1, 0, 0], dtype=np.int64), np.array([0, 1, 0, 0], dtype=np.int64), np.array([1, 1, 0, 1], dtype=np.int64), np.array([1, 1, 1, 0], dtype=np.int64)]]
    
    newState = [ [np.array([], dtype=np.int64), np.array([], dtype=np.int64)], 
                 [np.array([], dtype=np.int64), np.array([], dtype=np.int64)] ]
    for i in range(len(state)):
        for j in range(len(state[0])):
            #for each element, row number is determined by the left most 2 bits of the input element
            # col number is determined by the rightmost 2 bits
            rowStr = "" + str(state[i][j][0]) + str(state[i][j][1])
            colStr = "" + str(state[i][j][2]) + str(state[i][j][3])
            #converting the binary bits to decimal integers to access the table:
            row = int(rowStr, 2)
            col = int(colStr, 2)
            #Substituting
            newState[i][j] = InvSBox[row][col]
    
    return newState

def addRoundKey(state, roundKey):
    #Function to XOR state with round key
    newState = [[np.array([], dtype = np.int64), np.array([], dtype = np.int64)], 
                [np.array([], dtype = np.int64), np.array([], dtype = np.int64)] ]
    for i in range(0, 2):
        for j in range(0, 2):
            for k in range(0, 4):
                newState[i][j] =  np.append(newState[i][j], (state[i][j][k] +  roundKey[i][j][k])%2)
                
    return newState

def encryption(inputmsg, keystr):
    '''
        input is the plaintext bit string, and the key string
        both are 16bits
    
        They are converted into 2x2 matrices, with 4 bits in each position
        if a, b, c, d are each 4 bits, and abcd is the input string, then matrix looks like:
            |a c|
            |b d|
        output is a 16 bit encrypted ciphertext string
    '''
    
    msg_matrix = bitStr2Matrix(inputmsg)
    keymatrix = bitStr2Matrix(keystr)
    keys = keyGeneration(keymatrix)
    
    #Encryption Process:

    #Step1: Add Round Key 0 & 1:
    subkeys = []
    subkeys.append(keys[0][0:2])
    subkeys.append(keys[1][0:2])
    msg_matrix = addRoundKey(msg_matrix, subkeys)
    #print(msg_matrix)
    
    #Step2: Nibble Substitution:
    msg_matrix = SBoxSubstitution(msg_matrix)
    #print(msg_matrix)

    #Step3: Shift Rows:
    temp = msg_matrix[1][0]
    msg_matrix[1][0] = msg_matrix[1][1]
    msg_matrix[1][1] = temp
    #print(msg_matrix)

    #Step4: Mix Columns:
    constant = [ [np.array([1]), np.array([1, 0, 0])], [np.array([1, 0, 0]), np.array([1])] ]
    msg_matrix = gf16MatrixMul(constant, msg_matrix)
    #print(msg_matrix)

    #Step5: Add Round Key 2 & 3:
    subkeys = []
    subkeys.append(keys[0][2:4])
    subkeys.append(keys[1][2:4])
    msg_matrix = addRoundKey(msg_matrix, subkeys)
    #print(msg_matrix)
    
    #Step6: Nibble Substitution:
    msg_matrix = SBoxSubstitution(msg_matrix)
    #print(msg_matrix)
    
    #Step7: Shift Rows:
    temp = msg_matrix[1][0]
    msg_matrix[1][0] = msg_matrix[1][1]
    msg_matrix[1][1] = temp
    #print(msg_matrix)
    
    #Step8: Add Round Keys 4 & 5:
    subkeys = []
    subkeys.append(keys[0][4:6])
    subkeys.append(keys[1][4:6])
    msg_matrix = addRoundKey(msg_matrix, subkeys)
    #print(cipher)
    
    ciphertext = matrix2bitstring(msg_matrix)    
    
    return ciphertext

def decryption(inputmsg, keystr):
    '''
        input is the ciphertext bit string, and the key string
        both are 16bits
    
        They are converted into 2x2 matrices, with 4 bits in each position
        if a, b, c, d are each 4 bits, and abcd is the input string, then matrix looks like:
            |a c|
            |b d|
        output is 16 bit plaintext string.
    '''
    cip_matrix = bitStr2Matrix(inputmsg)
    keymatrix = bitStr2Matrix(keystr)
    keys = keyGeneration(keymatrix)
    
    #Decryption Process:

    #Step1: Add Round Key 4 & 5:
    subkeys = []
    subkeys.append(keys[0][4:6])
    subkeys.append(keys[1][4:6])
    cip_matrix = addRoundKey(cip_matrix, subkeys)
    #print(cip_matrix)
    
    #Step2: Inverse Shift Rows:
    temp = cip_matrix[1][0]
    cip_matrix[1][0] = cip_matrix[1][1]
    cip_matrix[1][1] = temp
    #print(cip_matrix)
    
    #Step3: Inverse Nibble Substitution:
    cip_matrix = InvSBoxSubstitution(cip_matrix)
    #print(cip_matrix)
   
    #Step4: Add Round Key 2 & 3:
    subkeys = []
    subkeys.append(keys[0][2:4])
    subkeys.append(keys[1][2:4])
    cip_matrix = addRoundKey(cip_matrix, subkeys)
    #print(plain)
    
    #Step5: Inverse Mix Columns:
    constant = [ [np.array([1, 0, 0, 1]), np.array([1, 0])], [np.array([1, 0]), np.array([1, 0, 0, 1])] ]
    cip_matrix = gf16MatrixMul(constant, cip_matrix)   
    #print(plain)
    
    #Step6: Inverse Shift Rows:
    temp = cip_matrix[1][0]
    cip_matrix[1][0] = cip_matrix[1][1]
    cip_matrix[1][1] = temp
    #print(plain)
    
    #Step7: Inverse Nibble Substitution:
    cip_matrix = InvSBoxSubstitution(cip_matrix)
    #print(plain)
    
    #Step8: Add Round Keys 0 & 1:
    subkeys = []
    subkeys.append(keys[0][0:2])
    subkeys.append(keys[1][0:2])
    cip_matrix = addRoundKey(cip_matrix, subkeys)
    #print(plain2)
    
    plaintext = matrix2bitstring(cip_matrix)
    
    return plaintext


def one_round_encryption(inputmsg, keystr):
    '''
        input is the plaintext bit string, and the key string
        both are 16bits
    
        They are converted into 2x2 matrices, with 4 bits in each position
        if a, b, c, d are each 4 bits, and abcd is the input string, then matrix looks like:
            |a c|
            |b d|
        output is a 16 bit encrypted ciphertext string
    '''
    
    msg_matrix = bitStr2Matrix(inputmsg)
    keymatrix = bitStr2Matrix(keystr)
    keys = keyGeneration(keymatrix)
    
    #Encryption Process:

    #Step1: Add Round Key 0 & 1:
    subkeys = []
    subkeys.append(keys[0][0:2])
    subkeys.append(keys[1][0:2])
    msg_matrix = addRoundKey(msg_matrix, subkeys)
    #print(msg_matrix)
    
    #Step2: Nibble Substitution:
    msg_matrix = SBoxSubstitution(msg_matrix)
    #print(msg_matrix)

    #Step3: Shift Rows:
    temp = msg_matrix[1][0]
    msg_matrix[1][0] = msg_matrix[1][1]
    msg_matrix[1][1] = temp
    #print(msg_matrix)

    #Step4: Mix Columns:
    constant = [ [np.array([1]), np.array([1, 0, 0])], [np.array([1, 0, 0]), np.array([1])] ]
    msg_matrix = gf16MatrixMul(constant, msg_matrix)
    #print(msg_matrix)

    #Step5: Add Round Key 2 & 3:
    subkeys = []
    subkeys.append(keys[0][2:4])
    subkeys.append(keys[1][2:4])
    msg_matrix = addRoundKey(msg_matrix, subkeys)
    #print(msg_matrix)
    
    ciphertext = matrix2bitstring(msg_matrix)    
    
    return ciphertext
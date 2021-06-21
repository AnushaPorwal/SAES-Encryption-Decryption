# SAES-Encryption-Decryption

This code is written in Python and uses the numpy library to help in the implementation all helper functions.

### SAESanusha.py contents:
(1) encryption(inputmsg, key): encrypts plaintext inputmsg using key, and returns a 16 bit ciphertext.  
(2) decryption(inputmsg, key): decrypts ciphertext inputmsg using key, and returns a 16 bit plaintext.  
(3) SBoxSubstitution(state): performs s-box substitution on given state.  
(4) InvSBoxSubstitution(state): performs inverse s-box substitution on given state.  
(5) addRoundKey(state, roundkey): returns the XORing of the state and the round key.  
(6) gf16MatrixMult(X, Y): performs matrix multiplication of X and Y in Galois Field 16. The irreducible polynomial used here is (1,0,0,1,1).  
(7) keyGeneration(key): generates 6 round-keys [word0, ..., word5] using a 16bit key.  

### Template for Demo.ipynb contents:
Provides a small template for the demonstration of encryption and decryption.  
The input to both is a 16 bit binary string message (plain or cipher, depending on the function) and a 16 bit binary key string. The output text is also a 16 bit binary string.

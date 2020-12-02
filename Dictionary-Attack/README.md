# Dictionary-Attack

You are given a plaintext and a ciphertext, you know that aes-128-cbc is used to generate the ciphertext from the plaintext, and you also know that the numbers in the IV are all zeros (not the ASCII character ‘0’). Another clue that you have learned is that the key used to encrypt this plaintext is an English word shorter than 16 characters; the word that can be found from a typical English dictionary. Since the word has less than 16 characters (i.e. 128 bits), space characters (hexadecimal value 0x20) are appended to the end of the word to form a key of 128 bits.
Your goal is to write a program to find out this key.

To Compile:
    gcc dict_attack.c -o attack -lssl -lcrypto
To Run:
    ./attack

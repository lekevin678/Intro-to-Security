#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>


void handleErrors(void){
    ERR_print_errors_fp(stderr);
    abort();
}

void encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key, unsigned char *ciphertext){
    EVP_CIPHER_CTX *ctx;

    int len;


    if(!(ctx = EVP_CIPHER_CTX_new())){
        printf("error\n");
    }

    if(1 != EVP_EncryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, 0000000000000000)){
        printf("error\n");
    }

    if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)){
        printf("error\n");
    }

    if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)){
        printf("error\n");
    }

    EVP_CIPHER_CTX_free(ctx);

}

void string2hexString(char* input, char* output){
    int loop;
    int i; 
    
    i=0;
    loop=0;
    
    int temp=0;
    while(input[loop] != '\0')
    {
        temp = (int) input[loop];
        if (temp < 0){
            temp = (128 - abs(temp) ) + 128;

        }
        sprintf((char*)(output+i),"%02x", temp);
        loop+=1;
        i+=2;
    }
    output[i++] = '\0';
}


int main(){
    FILE * stream;
    char * key = NULL;
    ssize_t buffer = 0;
    ssize_t read;

    stream = fopen("words.txt", "r");

    unsigned char *plaintext= "This is a top secret.";
    unsigned char ciphertext[128];

    while ((read = getline(&key, &buffer, stream)) != -1) {   
        strtok(key, "\n");
        int addZero = 16 - strlen(key);
        if (addZero > 0){
            int count = 0;
            while (count < addZero){
                strncat(key, " ", 1); 
                count ++;
            }
        }

        int ciphertext_len;
        encrypt(plaintext, strlen ((char *)plaintext), key, ciphertext);
        
        char hex_str[64+1];
        string2hexString(ciphertext, hex_str);

        char * ciphertextMain = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9";
        
        if (strcmp(hex_str,ciphertextMain) == 0){
            printf("************FOUND KEY**************\n");
            printf("    KEY: '%s'\n", key);
            return 0;
        }

    }
    fclose(stream);

    return 0;
}


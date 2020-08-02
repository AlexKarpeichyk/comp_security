# Defining necessary variables and supporting functions

## alphabet - a list of characters supported by the cipher
alphabet = "abcdefghijklmnopqrstuvwxyz1234567890+-=*/^<>~!?,.;:'\"`_@#$£€₽&%\|()[]{} "
plaintext = ""
ciphertext = ""
cluster_key = ""

def rotate_make_clusters(rot):
    """
    Supporting function for rotating the alphabet and splitting it 
    into 9 clusters of 8 characters each.
    
    Args: 
        param: rot - alphabet rotation index        
    Returns:
        list: collection of produced character clusters
    """
    ## in case the user rotates the alphabet by more than 72
    rot = rot % 72
    ## rotating the existing alphabet 'rot' characters to the left
    alpha = alphabet[rot:] + alphabet[0:rot]
    ## initialize a list for storing clusters of characters
    clusters = []
    
    ## splitting the rotated alphabet into clusters of 8
    for i in range(9):
        ## adding 8 characters of the alphabet to cluster 'i'
        clusters.append(alpha[:8])
        ## removing the first 8 characters from the alphabet to avoid duplication
        alpha = alpha[8:]
        
    return clusters

# Encryption

def encrypt(plain, en_key):
    """
    Function for encrypting the provided plaintext.
    
    Args:
        param_1: plain  - the plaintext
        param_2: en_key - encryption key (aka alphabet rotation index)
    Return:
        tuple: a pair consisting of the ciphertext and part of the decryption key
    """
    
    ## rotating the alphabet and producing clusters
    alpha = rotate_make_clusters(en_key)
    ## initializing string for ciphertext
    ciphertext = ""
    ## initializing string for the first part of the decryption key representing cluster indices
    key = ""
    ## converting plaintext to lowercase
    plain = plain.lower()
    ## encrypting each character in plaintext with a collection of '.'
    for c in plain:
        ## for each cluster 
        for cluster in alpha:
            ## if chracter 'c' is present in the current cluster 
            if c in cluster:
                ## add the index of the cluster to the key string
                key += (str(alpha.index(cluster) + 1)) ### adding 1 to avoid '0's in the key
                                                       ### (because array counts start from 0)
                ## add the a number of '.' to the ciphertext based on the position of character in cluster
                for i in range(cluster.index(c) + 1): ### adding 1 to avoid 0 number of dots
                                                      ### (because array counts start from 0)
                    ciphertext += "."
        ## add a separator '|' between encrypted characters 
        ciphertext += "|" 
    
    return ciphertext, key

# Decryption

def decrypt(cipher, de_key):
    """
    Function for decrypting the provided ciphertext.
    
    Args:
        param_1: cipher - the ciphertext
        param_2: de_key - decryption key (aka a pair consisting of a string of cluster indices 
                                          and alphabet rotation index)
    """
    ## rotating the alphabet and producing clusters
    alpha = rotate_make_clusters(de_key[1]) ### using the second value of the de_key as a rotation index
    ## initializing string for plaintext
    plaintext = ""
    ## variable that will represent the number of '.'s and the position of charcter in a cluster
    cipher_count = -1 ### -1 to compensate for +1 added during encryption
    ## variable for keeping track of cluster index for a character
    key_count = 0
    
    ## decrypting the ciphertext and building plaintext character by character
    for c in cipher:
        ## for each '.' in the ciphertext add 1 to cipher_count
        if c == '.':
            cipher_count += 1
        ## when hit '|', build a charcter and add it to plaintext string
        else:
            ## decrypt a charcter based on the (key_count) and the (cipher_count) using the first value of de_key
            curr = alpha[int(de_key[0][key_count]) - 1][cipher_count]
            ## add decrypted character to plaintext
            plaintext += curr
            ## move to next cluster in the clusters string (de_key[0])
            key_count += 1
            ## restart the number of '.'s and the position of character in a cluster for the next character
            cipher_count = -1
            
    return plaintext

#print(alphabet)
plaintext = input("Type plaintext here: ")
## encryption key
en_key = int(input("Type a number for encryptin key here: "))
## assigning the first output of encrypt() to ciphertext and the second to the clusters string 
ciphertext, cluster_key = encrypt(plaintext, en_key)
print("Ciphertext:", ciphertext)
print("First part of encryption key: ", cluster_key)

choice = input("Type 'd' if you want to decrypt or press Enter to quit: ")
if not choice == "":
    ciphertext = input("Type ciphertext here or copy and paste from above: ")
    ## initializing decryption key
    de_key = (cluster_key, en_key) ### second value must be the same as encryption key (en_key)
    print("Decryption key:", de_key)
    ## assigning decrypted text from decrypt() to plaintext
    plaintext = decrypt(ciphertext, de_key)
    print("Plaintext:", plaintext)

input()



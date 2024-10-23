
data = b'ABCDEFGH' 


print("Початкові дані:", data)


def initial_permutation(data):
   
    permutation_table = [
        58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7
    ]

    
    data_bits = ''.join(f'{byte:08b}' for byte in data)
    
    
    permuted_data = ''.join(data_bits[i-1] for i in permutation_table)
    
    return permuted_data


permuted = initial_permutation(data)
print("Після початкової перестановки:", permuted)

def split_block(block):
   
    L = block[:32]
    
    R = block[32:]
    return L, R


L, R = split_block(permuted)
print("Ліва частина (L):", L)
print("Права частина (R):", R)


def feistel(R, K):
    
    return ''.join(str(int(r) ^ int(k)) for r, k in zip(R, K))


def des_rounds(L, R):
    for round in range(1, 17):
        
        K = '110101' * 8  
        
        
        new_R = feistel(R, K)
        
        
        L, R = R, new_R  
        
        print(f"Після {round}-го раунду:")
        print("L:", L)
        print("R:", R)
    
    return L, R


L, R = des_rounds(L, R)


def swap_parts(L, R):
    
    return R, L


L, R = swap_parts(L, R)
print("Після обміну:")
print("L:", L)
print("R:", R)


inverse_permutation_table = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


def inverse_permutation(L, R):
    
    combined_block = L + R
    
    permuted_block = ''.join(combined_block[i-1] for i in inverse_permutation_table)
    return permuted_block


final_result = inverse_permutation(L, R)
print("Після інверсної перестановки:", final_result)

def des_decryption_rounds(L, R, keys):
    for i in range(len(keys)-1, -1, -1):
        new_L = R
        new_R = ''.join(str(int(l) ^ int(f_bit)) for l, f_bit in zip(L, feistel(R, keys[i])))
        L, R = new_L, new_R
    return L, R

def des_decrypt(cipher_text, keys):
    
    permuted = initial_permutation(cipher_text)
    L, R = split_block(permuted)

    
    L, R = des_decryption_rounds(L, R, keys)

    
    L, R = swap_parts(L, R)

    
    decrypted_block = inverse_permutation(L, R)
    return decrypted_block


keys = ['110101' * 8] * 16  


cipher_text = b'ABCDEFGH'  


decrypted_text = des_decrypt(cipher_text, keys)
print("Розшифрований текст:", decrypted_text)

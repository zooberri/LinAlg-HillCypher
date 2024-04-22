import numpy as np
from sympy import Matrix


def char_to_number(char):
    if char == ' ':
        return 0  
    elif char == '{':
        return 27
    elif char == '}':
        return 28
    else:
        return ord(char) - 96

def number_to_char(number):
    if number == 0:
        return ' '  
    elif number == 27:
        return '{'
    elif number == 28:
        return '}'
    else:
        return chr(number + 96)

def text_to_numbers(text):
    return [char_to_number(char) for char in text.lower()]

def numbers_to_text(numbers):
    return ''.join([number_to_char(num) for num in numbers])


def matrix_mod_multiplication(matrix_key, block):
    return np.remainder(np.dot(matrix_key, block), 29).astype(int)

def create_blocks(text_numbers, matrix_size):
    while len(text_numbers) % matrix_size != 0:
        text_numbers.append(27)  # Padded with '{' which corresponds to 27
    return [text_numbers[i:i+matrix_size] for i in range(0, len(text_numbers), matrix_size)]

def display_matrices(blocks, matrix_size):
    print("Input sentence as numerical matrix (each row is a block):")
    for block in blocks:
        print(np.array(block).reshape(1, matrix_size))

def display_result(key, block, result_block, encode):
    print(f"Key matrix:\n{key}")
    print("Multiplied by:")
    print(f"Block matrix:\n{np.array([block]).T}")
    print("Results in:")
    transformed_matrix = np.array([result_block]).T
    print(f"Transformed matrix:\n{transformed_matrix}")
    
    corresponding_text = numbers_to_text(result_block)
    operation = "encoded" if encode else "decoded"
    print(f"Which corresponds to: {corresponding_text} ({operation})")

# Main function for the Hill cipher encode/decode routine
def hill_cipher(text, encode=True, cipher_key=np.array([[2, 3], [1, 5]]), mode=1): 
    text_numbers = text_to_numbers(text)
    matrix_size = 2 
    blocks = create_blocks(text_numbers, matrix_size)
    if mode == 1:
        display_matrices(blocks, matrix_size)
    
    inverse_cipher_key = Matrix(cipher_key).inv_mod(29).tolist()

    transformed_blocks = []
    for block in blocks:
        if encode:
            if mode == 1:
                print(f"\nEncoding block {block}:")
            result_block = matrix_mod_multiplication(cipher_key, block)
        else:
            if mode == 1:
                print(f"\nDecoding block {block}:")
            result_block = matrix_mod_multiplication(inverse_cipher_key, block)
        if mode == 1:
            display_result(cipher_key if encode else inverse_cipher_key, block, result_block, encode)
        transformed_blocks.extend(result_block)
        
    result_text = numbers_to_text(transformed_blocks).rstrip('{') 
    return result_text

# The main part of the script starts here
mode = input("Select which mode you want to be in: (1: Encode and Decode message) (2: Guessing game) ")

if mode == '1':
    while True:
        sentence = input("\nEnter a sentence (lowercase letters and spaces only): ")
        if sentence == "QUIT":
            break
        print("\n---- Encoding Process ----")
        encoded_sentence = hill_cipher(sentence, encode=True)
        print("\nEncoded sentence:", encoded_sentence)

        print("\n---- Decoding Process ----")
        decoded_sentence = hill_cipher(encoded_sentence, encode=False)
        print("\nDecoded sentence:", decoded_sentence)
elif mode == '2':
    sentence = "cryptography is cool"
    encoded_sentence = hill_cipher(sentence, encode=True, mode=2)
    print("\nThe encoded sentence is:\n", encoded_sentence)
    print("\nTime to guess what the key is\n")
    
    while True:
        num1 = int(input("Enter the first number in the key: "))
        num2 = int(input("Enter the second number in the key: "))
        num3 = int(input("Enter the third number in the key: "))
        num4 = int(input("Enter the fourth number in the key: "))
        guess_key = np.array([[num1, num2], [num3, num4]])
        
        if np.linalg.det(guess_key) % 29 == 0:
            print("Invalid matrix, determinant is not invertible modulo 29.\n")
            continue
        
        decoded_guess = hill_cipher(encoded_sentence, encode=False, cipher_key=guess_key, mode=2)
        print("\nYour key got the following result:\n", decoded_guess)
        
        if decoded_guess == sentence:
            print("\nCongratulations! You've guessed the correct key.")
            break
        else:
            print("\nIncorrect guess. Try again.")
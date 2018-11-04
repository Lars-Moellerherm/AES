import numpy as np
from BitVector import *
from state import state
import re


def split(file):
    name = 1
    filename = ''
    filetype = ''
    for i in file:
        if i == '.':
            name = 0
            continue
        elif name:
            filename += i
        else:
            filetype +=i
    return filename, filetype

def get_path(filename):
    a=list(re.finditer('/',filename))
    idx = a[-1].end()
    return filename[:idx], filename[idx:]

def encryption(text,key):
    rounds = 10;
    key = key_expansion(key)

    text = add_round_key(text,key[0])

    for i in range(rounds-1):

        text = substitute_bytes(text)

        text = shift_rows(text)

        text = mix_column(text)

        text = add_round_key(text,key[i+1])

    text = substitute_bytes(text)

    text = shift_rows(text)

    text = add_round_key(text,key[rounds])

    return text

def decryption(text,key):
    rounds = 10
    key = key_expansion(key)

    text = add_round_key(text,key[-1])

    for i in range(rounds-1):
        text = inverse_shift_rows(text)

        text = inverse_substitute_bytes(text)

        text = add_round_key(text,key[-i-2])

        text = inverse_mix_column(text)

    text = inverse_shift_rows(text)

    text = inverse_substitute_bytes(text)

    text = add_round_key(text,key[0])

    return text

def key_expansion(key):
    RC = get_round_const(10)
    all_keys = []
    all_keys.append(key.deep_copy())
    for i in range(1,11):
        last_key = all_keys[i-1]
        new_key = state([0 for i in range(128)])
        new_key.set_word([last_key.get_word(0)[j] ^ g(last_key.get_word(3),RC[i])[j] for j in range(4)],0)
        for j in range(1,4):
            new_key.set_word([new_key.get_word(j-1)[n]^last_key.get_word(j)[n] for n in range(4)],j)
        all_keys.append(new_key)
    return all_keys

def substitute_bytes(text):
    for i in range(4*4):
        text.set_byte(sub_with_Sbox(text.get_byte(i)),i)
    return text

def inverse_substitute_bytes(text):
    for i in range(4*4):
        text.set_byte(sub_with_inverse_Sbox(text.get_byte(i)),i)
    return text

def shift_rows(text):
    text.set_row(left_byte_shift(text.get_row(1)),1)
    text.set_row(left_byte_shift(left_byte_shift(text.get_row(2))),2)
    text.set_row(left_byte_shift(left_byte_shift(left_byte_shift(text.get_row(3)))),3)
    return text

def inverse_shift_rows(text):
    text.set_row(right_byte_shift(text.get_row(1)),1)
    text.set_row(right_byte_shift(right_byte_shift(text.get_row(2))),2)
    text.set_row(right_byte_shift(right_byte_shift(right_byte_shift(text.get_row(3)))),3)
    return text

def mix_column(text):
    modulus = BitVector(bitstring='100011011')
    two = BitVector(hexstring='02')
    three = BitVector(hexstring='03')
    one = BitVector(hexstring='01')
    for i in range(4):
        word = text.get_word(i)
        new_word = []
        for j in range(4):
            new_word.append(word[j].gf_multiply_modular(two,modulus,8)^word[(j+1)%4].gf_multiply_modular(three,modulus,8)^word[(j+2)%4].gf_multiply_modular(one,modulus,8)^word[(j+3)%4].gf_multiply_modular(one,modulus,8))
        text.set_word(new_word,i)
    return text

def inverse_mix_column(text):
    modulus = BitVector(bitstring='100011011')
    zeroE = BitVector(hexstring='0E')
    zeroB = BitVector(hexstring='0B')
    zeroD = BitVector(hexstring='0D')
    nine = BitVector(hexstring='09')
    for i in range(4):
        word = text.get_word(i)
        new_word = []
        for j in range(4):
            new_word.append(word[j].gf_multiply_modular(zeroE,modulus,8)^word[(j+1)%4].gf_multiply_modular(zeroB,modulus,8)^word[(j+2)%4].gf_multiply_modular(zeroD,modulus,8)^word[(j+3)%4].gf_multiply_modular(nine,modulus,8))
        text.set_word(new_word,i)
    return text

def add_round_key(text,key):
    for i in range(4*4):
        text.set_byte((text.get_byte(i)^key.get_byte(i)),i)
    return text


def left_byte_shift(word):
    new_word = []
    new_word.append(word[1])
    new_word.append(word[2])
    new_word.append(word[3])
    new_word.append(word[0])
    return new_word

def right_byte_shift(word):
    new_word = []
    new_word.append(word[3])
    new_word.append(word[0])
    new_word.append(word[1])
    new_word.append(word[2])
    return new_word

def sub_with_Sbox(byte):
    modulus = BitVector(bitstring='100011011')
    if byte.int_val()!=0:
        byte = byte.gf_MI(modulus,8)
    else:
        byte = BitVector(intVal=0,size=8)
    a = [byte.deep_copy() for i in range(4)]
    c = BitVector(bitstring='01100011')
    byte ^= (a[0]>>4) ^ (a[1]>>5) ^ (a[2]>>6) ^ (a[3]>>7) ^c
    return byte

def sub_with_inverse_Sbox(byte):
    modulus = BitVector(bitstring='100011011')
    d = BitVector(bitstring='00000101')
    b = [byte.deep_copy() for i in range(3)]
    byte = (b[0] >> 2) ^ (b[1] >> 5) ^ (b[2] >> 7) ^ d
    check = byte.gf_MI(modulus,8)
    byte = check if isinstance(check,BitVector) else BitVector(intVal=0,size=8)
    return byte

def g(word,RCi):
    word = left_byte_shift(word)
    word = [sub_with_Sbox(word[i]) for i in range(4)]
    word = [word[i] ^ RCi[i] for i in range(4)]
    return word

def get_round_const(rounds):
    #round 0
    Rcon = [[BitVector(intVal=0, size=8) for i in range(4)] for i in range(rounds+1)]
    Rcon[1][0] = BitVector(intVal=1,size=8)
    modulus = BitVector(bitstring='100011011')
    for i in range(2,rounds+1):
        Rcon[i][0] = BitVector(intVal=2,size=8).gf_multiply_modular(Rcon[i-1][0],modulus,8)
    return Rcon

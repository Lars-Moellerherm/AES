import numpy as np
import random as rnd
from functions import *
from BitVector import *
from state import state
from tqdm import tqdm



file = str(input("file:"))
filename, filekind = split(file)
key = str(input("key (16 ascii symbols):"))
file = filename+'.'+filekind
task = str(input("encryption (enc) or decryption(dec):"))
if task == "dec":
    final_filekind = str(input("In which filetype should it be decrypted:"))


key = BitVector(textstring=key)

try:
    key= state(key)
except ValueError:
    print('key couln`t be read')


try:
    b = BitVector(filename=file)
except IOError:
    print('An Error occured trying to open the file')
text = []

while(b.more_to_read):
    bit_vec = b.read_bits_from_file(128)
    if bit_vec.__len__()!=128:
        missing =128-bit_vec.__len__()
        bit_vec = bit_vec + BitVector(size=missing)
    text.append(state(bit_vec))
b.close_file_object()


state_number_text=len(text)
mistake = 0

if task == 'enc':
    text_enc = []
    for i in tqdm(range(state_number_text)):
        key_round = key.deep_copy()
        text_enc.append(encryption(text[i],key_round))
    
    text_plain = BitVector(size=0)
    for i in range(state_number_text):
        text_plain += text_enc[i].get_plain()
        
    out_filename = 'enc_'+filename+'.bits'
elif task == 'dec':
    text_dec = []
    for i in tqdm(range(state_number_text)):
        key_round = key.deep_copy()
        text_dec.append(decryption(text[i],key_round))
    
    text_plain = BitVector(size=0)
    for i in range(state_number_text):
        text_plain += text_dec[i].get_plain()
        
    out_filename = 'dec_'+filename[4:]+'.'+final_filekind
else:
    print("The task isn't choosen right. choose enc or dec.")
    mistake = 1



if mistake==0:
    FILEOUT = open(out_filename, 'wb')
    text_plain.write_to_file(FILEOUT)
    FILEOUT.close()



# -*- coding: utf-8 -*-
from BitVector import *

class state:
    
    def __init__(self,plain_text):
        self.state_list = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                self.state_list[j][i] = plain_text[32*i+8*j:32*i+8*(j+1)]
                
    def set_state(self,st_list):
        self.state_list = st_list
                
    def get_plain(self):
        text = BitVector(size=0)
        for j in range(4):
            for n in range(4):
                text=text+self.state_list[n][j]
        return text
    
    

    def print_state(self):
        for i in range(4):
            string = ''
            for j in range(4):
                string += str(self.state_list[i][j].get_bitvector_in_hex())
                string += '\t'
            print(string)
        print('\n')
        
    def get_byte(self,number):
        return self.state_list[number%4][int(number/4)]
    
    def set_byte(self,byte,number):
        self.state_list[number%4][int(number/4)]=byte
    
    def get_word(self,number):
        word = [i for i in range(4)]
        for i in range(4):
            word[i]=self.state_list[i][number]
        return word
    
    def set_word(self,word,number):
        for i in range(4):
            self.state_list[i][number]=word[i]
            
    def get_row(self,number):
        row_list = []
        for i in range(4):
            row_list.append(self.state_list[number][i])
        return row_list
        
    def set_row(self,row,number):
        for i in range(4):
            self.state_list[number][i] = row[i]
            
    def deep_copy(self):
        state_copy = state([i for i in range(128)])
        state_copy.set_state(self.state_list)
        return state_copy
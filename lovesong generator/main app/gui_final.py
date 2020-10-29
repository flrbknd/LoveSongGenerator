# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 23:58:32 2020

@author: Flora
"""
import random
from tkinter import *
from tkinter.font import Font
from PIL import ImageTk, Image
from functions_markov import *
import re

###

    
class MainApp():
    
    def __init__(self, master):
        self.master = master
        self.user_input = {}
        self.create_widgets()
        self.bind_widgets()

    
    def num_of_words(self, event=None):
        num = self.num_e.get()
        if num.isdigit() and 1 <= int(num) <=200:
            self.num_q['text'] = f"Number of words: {num}"
        else:
            num = random.randint(20,80)
            self.num_q['text'] = "Invalid choice, so random length is generated."
        self.user_input.update({'num_words': int(num)})
        type_input = Label(self.frame)

        self.num_e.destroy()
        if "first_word" in self.user_input: 
            self.call_textgen()
            
            
    def first_word(self, event=None):
        word = self.first_word_e.get().lower()
        if word in corpus:
            self.first_word_q['text'] = f"Chosen first word: {word}"
        else:
            word = random.choice(['I', 'you', 'this'])
            self.first_word_q['text'] = "Sorry, we don't know this word. A random word is given."
        self.user_input.update({'first_word': word})
        type_input = Label(self.frame)  
        self.first_word_e.destroy()
        if "num_words" in self.user_input:
            self.call_textgen()
            
    def call_textgen(self):
        created_text = generate_text(self.user_input.get("first_word"), self.user_input.get("num_words"))
        created_text = capitalize_text(created_text)
        self.result_message['text'] = created_text + '...'
        


    def create_widgets(self):
        font_setting = 'consolas 12 bold'
        
        #frame
        self.frame = LabelFrame(self.master, padx=100, pady=50, borderwidth = 0, highlightthickness = 0)
        self.frame.pack(padx = 100, pady = 50)
        #num input - text length
        self.num_q = Label(self.frame, text='How many words would you like?', font = font_setting)
        self.num_q.grid(row= 0, column = 0)

        self.num_e = Entry(self.frame)
        self.num_e.grid(row= 0, column = 1)
        #first word inout
        self.first_word_q = Label(self.frame, text='What should be the first word?', font = font_setting)
        self.first_word_e = Entry(self.frame)
        self.first_word_q.grid(row= 1, column = 0)
        self.first_word_e.grid(row= 1, column = 1)
        #image (decoration)
        self.robot_img = ImageTk.PhotoImage(Image.open('../imgs/robot.png'))
        self.robot_img_label = Label(root, image = self.robot_img)
        self.robot_img_label.pack()
        #result
        self.result_message = Message(root, text="", width=700, font = font_setting)
        self.result_message.pack(pady=25)
        
    def bind_widgets(self):
        self.num_e.bind('<Return>', self.num_of_words)
        self.first_word_e.bind('<Return>', self.first_word)
        

        


root = Tk()
app = MainApp(root)
app.master.title('LoveSong Generator')
app.master.iconbitmap('../imgs/heart.ico')
app.master.geometry("800x600")
#app.master['bg'] = 'white'
app.master.mainloop()                           
                           

# -*- coding: utf-8 -*-
"""
Created on Sat Oct 24 18:02:52 2020

@author: Flora
"""
from collections import defaultdict
import random
import re


def load_training_file(txt_file):
    """Loads text file and return as continuous a string"""
    with open(txt_file) as f:
        raw_lyrics = f.read()
        return raw_lyrics
    

def create_corpus(raw_lyrics):
    """Takes input text, cleans it from unneccesary characters and returns corpus"""
    raw_lyrics = raw_lyrics.replace('\n', ' ')
    for char in ['(', ')', '"']:
        raw_lyrics = raw_lyrics.replace(char, '')
    corpus = raw_lyrics.lower().split()
    for word in corpus: 
        if word[0] == '[':
            corpus.remove(word)
    return corpus

def create_map(corpus, degree):
    """Collects all possible continuation after a sequence of words. 
    The number of words in the sequence should be named (degree)"""
    limit = len(corpus)-degree
    final_dict = defaultdict(list)
    for idx in range(limit):
        dict_value = corpus[idx+degree]
        dict_key = []
        d = degree
        while d > 0:
            dict_key.append(corpus[idx+d-1])
            d -= 1
        dict_key.reverse()
        dict_key = ' '.join(dict_key)
        final_dict[dict_key].append(dict_value)
    return final_dict

def choose_word_after(word_sequence, which_map):
    """Chooses one word from all acceptable options based on the corresponding map value"""
    options = which_map.get(word_sequence)
    if not options:
        random.choice(list(which_map.values())) #to check!!
    return random.choice(options)

def generate_text(first_word, text_len):
    """Generates text depending on previous word sequence. 
    Takes into account either previous two or previous three words"""
    n_minus3 = first_word
    n_minus2 = choose_word_after(first_word, map1_1)
    n_minus1 = choose_word_after(f'{n_minus3} {n_minus2}', map2_1)
    text = [n_minus3, n_minus2, n_minus1]
    for idx in range(text_len-3):
        n_word = random.choice([choose_word_after(f'{n_minus3} {n_minus2} {n_minus1}', map3_1),
                                choose_word_after(f'{n_minus2} {n_minus1}', map2_1)])
        text.append(n_word)
        n_minus3 = n_minus2
        n_minus2 = n_minus1
        n_minus1 = n_word
    text_merged = ' '.join(text)
    return text_merged

def one_more(text):
    """If the text generator left an unfinished sentence, 
    this function adds one more word to the generated text."""
    tokens = text.split()
    return choose_word_after(f'{tokens[-3]} {tokens[-2]} {tokens[-1]}', map3_1)

def capitalize_text(text):
    """Capitalizes text according to punctuation and "I" pronouns"""
    punc_filter = re.compile('([.!?]\s*)')
    split_with_punctuation = punc_filter.split(text)
    cap_str = ''.join([i.capitalize() for i in split_with_punctuation])
    final_list = []
    for word in cap_str.split():
        if word in ["i", "i,"]:
            word = word.upper()
        final_list.append(word)
    final_str = ' '.join(final_list)    
    return final_str

###
    

text_root = '../data/lovesongs_full_collection.txt'      
raw_lyrics = load_training_file(text_root)
corpus = create_corpus(raw_lyrics)    
map1_1 = create_map(corpus, 1)
map2_1 = create_map(corpus, 2)
map3_1 = create_map(corpus, 3)


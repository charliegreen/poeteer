import sqlite3
import re

repeat = re.compile("[A-Z']*\\([0-9]+\\)")
whitespace = re.compile("\\s+")

def normalize_whitespace(line):
    tokens = filter(None, whitespace.split(line))
    return ' '.join(tokens)

def get_stress_pattern(p):
    nums = []
    for c in p:
        if c.isdigit():
            nums.append(1 if int(c)>0 else 0)
    return nums

def get_last_syll(p):
    lastSyll = ''
    for s in p.split(' '):
        for c in s:
            if c.isdigit():
                lastSyll = s[:-1]
                break
            else:
                lastSyll += c
    return lastSyll

def create(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute('create table words (word text, rhyme text, sylls integer,'
              ' stress text, partOfSpeech text)')

    with open('cmudict.0.7a.txt', 'r') as f:
        for line in f:
            line = normalize_whitespace(line)

            if not line[0].isalpha() and line[0] != '\'':
                continue
            
            tokens = line.split(' ',1)
            word = tokens[0]
            pronunciation = tokens[1]

            if repeat.match(word):
                word = word[:word.index('(')]

            stress = ''.join(map(str,get_stress_pattern(pronunciation)))
            sylls  = len(stress)
            rhyme  = get_last_syll(pronunciation)
            pos    = "unknown"  # part of speech

            c.execute('insert into words values (?,?,?,?,?)', (word, rhyme, sylls, stress, pos))

    conn.commit()
    return conn

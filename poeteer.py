#!/usr/bin/python

import sqlite3
import re
import random

import create_database

_debug = False

class Rhymeschemes:
    # limerick = [(create_specifier_line("010010010"),	'A'),
    #             (create_specifier_line("010010010"),	'A'),
    #             (create_specifier_line("010010"),	'B'),
    #             (create_specifier_line("010010"),	'B'),
    #             (create_specifier_line("010010010"),	'A')]

    limerick = [("010010010",	'A'),
                ("010010010",	'A'),
                ("010010",	'B'),
                ("010010",	'B'),
                ("010010010",	'A')]

    # def create_specifier_line(stress_pattern):
    #     l = []
    #     for c in stress_pattern:
    #         if c == '0':
    #             l.append(False)
    #         elif c == '1':
    #             l.append(True)
    #         else:
    #             raise Exception("Unknown stress #"+c)
    #     return l

def debug_print(s):
    if _debug:
        print s

def generate(cursor,specifier):
    poem = ""
    rhymes = dict()

    for lineno in xrange(len(specifier)):
        debug_print("Line %d:" % lineno)

        line = ""

        while line == "":
            num_sylls = len(specifier[lineno][0])

            sylli = 0
            while sylli < num_sylls:
                matching = c.execute("SELECT * FROM words WHERE sylls<=? "
                                     "AND ? LIKE stress || '%'", # || is string concatenation??
                                     (num_sylls-sylli,specifier[lineno][0][sylli:])).fetchall()

                debug_print("  [%s|%d]: %d matches" % (line,sylli,len(matching)))
                random.shuffle(matching) # so we get unique poems
            
                for match in matching:
                    # POS not supported, stress already verified
                    mword, mrhyme, mnsylls, _, _ = match

                    if mnsylls == num_sylls-sylli:
                        # we get the last word on this line, so drop the sick rhymes, yo
                        try:
                            if mrhyme != rhymes[specifier[lineno][1]]:
                                continue
                        except KeyError:
                            rhymes[specifier[lineno][1]] = mrhyme
                
                    line  += mword+" "
                    sylli += mnsylls

                    if mnsylls == 0:
                        print "!!WARN!! match has no syllables: "+str(match)

                    break        
                else:
                    # No matches worked. Retry line.
                    sylli = 0
                    line  = ""
                    break

        poem += line[:-1]+"\n"  # remove the last space in the line, and add a newline

    return poem

if __name__ == '__main__':
    print "Initializing database...."
    conn = create_database.create(':memory:')
    print "Done initializing."
    
    c = conn.cursor()

    print generate(c,Rhymeschemes.limerick)

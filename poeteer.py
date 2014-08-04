#!/usr/bin/python

import sqlite3
import re
import random
import sys

import create_database
import poemfile

_debug = True

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

                    # This shouldn't be necessary
                    # if mnsylls == 0:
                    #     print "!!WARN!! match has no syllables: "+str(match)

                    break        
                else:
                    # No matches worked. Retry line.
                    sylli = 0
                    line  = ""
                    break

        poem += line[:-1]+"\n"  # remove the last space in the line, and add a newline

    return poem

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: poeteer.py poemfile"
        exit(1)

    # Get the specifier before initializing the database, since that's so slow,
    # and it's good to just let the user know if they have a bad file
    specifier = poemfile.get_specifier(sys.argv[1])

    print "Initializing database...."
    conn = create_database.create(':memory:')
    print "Done initializing."
    
    c = conn.cursor()

    print generate(c,specifier)

# Creates poem format specifiers from .poemfile files.
# 
# These files follow the format:
# [	STRESS	RHYME
# 	...		]
# For as many lines as desired.
# 
# The STRESS clause should be a string with a length equal to
# the desired number of syllables per line, and should consist
# of characters specifying the stress of that syllable. Currently,
# only 1 and 0 are supported, for stressed and unstressed, respectively.

import re

_whitespace = re.compile("\\s+")
_stress	    = re.compile("^[01]+$")
_rhyme	    = re.compile("[A-Z]")

def get_specifier(filename):
    specifier = []
    lineno = 0

    with open(filename,'r') as f:
        for line in f:
            lineno += 1

            # fix whitespace
            line = ' '.join(filter(None, _whitespace.split(line)))

            if not line or line[0] == '#':
                continue

            stress, rhyme = line.split(' ',1)
            
            if not _stress.match(stress):
                raise Exception("Invalid stress pattern specifier on line %d of %s: %s" %
                                (lineno, filename, stress))
            
            if not _rhyme.match(rhyme):
                raise Exception("Invalid rhyme specifier on line %d of %s: %s" %
                                (lineno, filename, rhyme))

            specifier.append((stress,rhyme))

    return specifier

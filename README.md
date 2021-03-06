poeteer
=======

An automatic poem generator, which generates poems using the [CMU pronouncing dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict?in=C+M+U+Dictionary&stress=-s).

poeteer is the improved counterpart to [sonneteer](http://github.com/charliegreen/sonneteer), which was a project of mine frmo a while ago for generating sonnets. Not only does poeteer take generic files that specify meter and rhyme scheme, it also has significantly higher performance, and routinely generates sonnets twice as fast as sonneteer (this isn't much of a surprise, considering the naivete of sonneteer, but it is a pleasant change).

The files that specify poem formats are called poemfiles, creatively enough, and contain STRESS/RHYME pairs for every line of the poem. The STRESS clause denotes the meter: it should be a string with a length equal to the desired number of syllables per line, and should consist of characters specifying the stress of that syllable. Currently, only 1 and 0 are supported, for stressed and unstressed, respectively. The RHYME clause is a single capital letter, designating which lines rhyme with which, as you'd expect. See the files in `poemfiles/` for examples.

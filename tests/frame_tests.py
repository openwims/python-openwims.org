import sys
sys.path.append("../")

import unittest
from wim.frame import *
from wim.phrase import BasePhrase

FRAMEDATA_PATH = "/Users/benjamin/hg/wim/tests/framedata.txt"

class TestFrames(object):
    
    def test_parse_matches(self):
        with open(FRAMEDATA_PATH, 'rb') as framedata:
            for line in framedata.readlines():
                if line.startswith('#'): continue
                parts = line.split("\t#")
                parts = [part.strip() for part in parts]
                yield self.check_match(*parts)

    def check_match(self, lemma, frame, parse):
        try:
            explorer = BasePhrase(parse)
        except Exception as e:
            print "Error: %s" % str(e)
            print parse
        phrase   = list(explorer.findall('VP'))[0]
        frame    = VerbTemplate(frame, lemma)

        #assert frame.match(phrase)
        return str(phrase), frame.match(phrase)

if __name__ == "__main__":

    counts = {
        'pass': 0,
        'fail': 0,
    }
    
    test = TestFrames()
    for idx,item in enumerate(test.test_parse_matches()):

        if not item[1]:
            counts['fail'] += 1
            break
        else:
            counts['pass'] += 1

    print 
    print "%(pass)i passes, %(fail)i fails" % counts

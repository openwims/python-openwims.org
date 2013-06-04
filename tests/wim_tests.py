import sys
sys.path.append("../")

import unittest
from wim.frame import Knowledge
from wim.analyze import WIMAnalyzer

FRAMEDATA_PATH = "/Users/benjamin/hg/wim/tests/framedata.txt"

class TestFrames(object):
    
    def test_parse_matches(self):
        kb = Knowledge.read()
        for templates in kb.values():
            for template in templates:
                yield self.check_match(template)

    def check_match(self, template):
        
        analyzer = WIMAnalyzer(str(template['parse']))
        wim = analyzer.analyze()
        
        print template['example']
        print wim
        print "="*50
        print
        
        return wim

if __name__ == "__main__":

    counts = {
        'pass': 0,
        'fail': 0,
    }
    
    test = TestFrames()
    for idx,item in enumerate(test.test_parse_matches()):

        if not item:
            counts['fail'] += 1
            break
        else:
            counts['pass'] += 1

    print "=" * 50
    print "=" * 50
    print "%(pass)i passes, %(fail)i fails" % counts

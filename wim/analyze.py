from nltk.corpus import wordnet as wn

from base import WIM
from phrase import BasePhrase
from frame import VerbTemplate

class WIMAnalyzer(object):

    def __init__(self, tree_str):
        self._tree = BasePhrase(tree_str)
        #self._tree = BasePhrase.convert(tree)
        
    def analyze(self):

        def getframeforwim(framemap, ct, wim):
            if id(ct) not in framemap:
                framemap[id(ct)] = wim.addframe(ct.frametype())
                framemap[id(ct)].addproperty("fromtext", ct.text())
            return framemap[id(ct)]

        self._wim = WIM()
        framemap = {}

        if self._tree is None:
            return self._wim
        
        # Temporary
        #for np in self.rootNPs():
        #    assert getframeforwim(framemap, np, self._wim)

        for vp in self.rootVPs():
            assert getframeforwim(framemap, vp, self._wim) #TODO: IS this a bad thing?
            
            matches = []
            for synset in wn.synsets(vp.headtext(), pos=wn.VERB):
                for lemma in synset.lemmas:
                    for frame in lemma.frame_strings:   
                        try:
                            vframe = VerbTemplate(frame, lemma.name)
                            vframe._sense = synset.name
                        except KeyError as e:
                            # Temporary:
                            #print str(e)
                            #print frame
                            #print lemma.name
                            #print synset
                            #print
                            continue
                                                  
                        if (vframe.match(vp)):
                            matches.append(vframe)
                            
            vp._sense = self.disambiguate(vp, matches) 

            if vp._sense is not None:
                for idx, ct in enumerate(vp._sense.constituents):
                    try:
                        # TODO: Move the skip "X" to the WIMFrame object
                        if vp._sense.wimtemplate[idx] == "X": continue
                        getframeforwim(framemap, vp, self._wim).addproperty(vp._sense.wimtemplate[idx], getframeforwim(framemap, ct, self._wim))
                    except IndexError:
                        #print vp._sense.wimtemplate
                        #print [c.node for c in vp._sense.constituents]
                        #print self._tree.text()
                        return
        
        return self._wim
        
    def disambiguate(self, vp, matches):
        """
        Take the first longest match template
        """
        temsize = 0
        longest = None

        for match in matches:
            if (len(match.wimtemplate) > temsize or 
                (len(match.wimtemplate) == temsize and 'SCOPE' in longest.wimtemplate and 'SCOPE' not in match.wimtemplate)):
                temsize = len(match.wimtemplate)
                longest = match
        return longest

    def rootNPs(self):
        """
        @todo: Need another BasePhrase traversal helper method to get
            lowest node that matches a given part of speech.
        """
        for phrase in self._tree.findall("NP"):
            if len(list(phrase.findall("NP"))) == 1:
                yield phrase

    def rootVPs(self):
        """
        @todo: Do a contains method on the phrase for traversal
        """
        for phrase in self._tree.findall("VP"):
            #if len(list(phrase.findall("VP"))) == 1:
            yield phrase
        
if __name__ == '__main__':

    #analyzer = WIMAnalyzer("(S (S (CL (NP (DET (DT the)) (NP (N man)))(VP (V hit)(NP (DET (DT the)) (NP (N building))))))(PUNCT .))")
    #analyzer = WIMAnalyzer("(S (CL (NP (N (PRO (PRP She)))) (VP (V (VBD shipped)) (NP (N (NN everything))) (PP (TO to) (NP (N (NNP Alaska)))))) (PUNCT .))")
    analyzer = WIMAnalyzer("(S (CL (NP (DET The) (N (NN ball))) (VP (V (VBZ is)) (VP (V (VBG falling)) (PP (PREP (IN on)) (NP (DET the) (N (NN table))))))) (PUNCT .))")
    wim = analyzer.analyze()
    
    data = wim.serialize()

    def recursive_dict_print(adict, level=0):
        
        for key, val in adict.items():
            if isinstance(val, dict):
                print "%s%s: " % ('   '*level, key)
                recursive_dict_print(val, level+1)
            else:
                print "%s%s: %s" % ('   '*level, key, val)

    recursive_dict_print(data)

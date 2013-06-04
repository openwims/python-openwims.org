# wim.frame
# Wim: Verb Frame Mapping and Knowledge
#
# Author:  Jesse English <jesse@unboundconcepts.com>
#          Benjamin Bengfort <benjamin@unboundconcepts.com>
# URL:     <http://unboundconcepts.com/projects/wim/>
# Created: Thu Dec 13 09:40:22 2012 -0400 
#
# Copyright (C) 2012 Unbound Concepts
# For license information, see LICENSE.TXT
#
# ID: frame.py [1] benjamin@unboundconepts.com $

"""
Classes for representing knowledge as a Python object and performing verb
frame mapping on sentences to locate frame matches.

@todo: document
"""

__docformat__ = "epytext en"

##########################################################################
## Imports and Package Dependencies
##########################################################################

import os
import json

from nltk.tree import Tree 

##########################################################################
## Module Static Variables
##########################################################################

KNOWLEDGE_PATH = os.environ.get('WIMKB', None)

##########################################################################
## Knowledge
##########################################################################

class Knowledge(object):
    """
    @todo: cleanup
    """
    
    @classmethod
    def read(klass, path=KNOWLEDGE_PATH):
       
        if not path:
            raise Exception("Specify a path to the verbframes.json as $WIMKB")

        with open(path, 'rb') as kbfile:
            data = json.load(kbfile, encoding="utf8")

            kwargs = {}
            for frame in data['frames']:
                for mapping in frame['mappings']:
                    # Update mapping with frame object
                    mapping['frame']   = frame['frame']

                    # Convert string reprs of Trees
                    mapping['verbmap'] = Tree.parse(mapping['verbmap'])

                    if 'parse' in mapping:
                        mapping['parse']   = Tree.parse(mapping['parse']) 

                # Convert kwargs
                kwargs[frame['frame']] = frame['mappings']

        return klass(**kwargs)

    fields = ('frame', 'verbmap', 'wimtemplate', 'example', 'parse')

    def __init__(self, **kwargs):
        self.__data = {}

        for frame, values in kwargs.items():
            for value in values:
                self[frame] = value
    
    def __len__(self):
        return len(self.__data)

    def __iter__(self):
        for frame in self.frames():
            yield frame

    def __setitem__(self, frame, values):
        if isinstance(values, list) and len(values) <= len(self.fields):
            values = dict(map(None, self.fields, values))
        
        if not isinstance(values, dict):
            raise ValueError("Expecting values containing %s" % self.fields)
        
        if frame in self:
            self.__data[frame].append(values)
        else:
            self.__data[frame] = [values,]

    def __getitem__(self, frame):
        return self.__data[frame]

    def __contains__(self, frame):
        return frame in self.__data

    def frames(self):
        return self.__data.keys()

    def items(self):
        return self.__data.items()

    def values(self):
        return self.__data.values()

    def lookup(self, frame, lemma=None):
        """
        @todo: for to be verbs, the lemma doesn't have the attaching "ing"
            so a double ing happens, hence the third replace. Fix this.
        """
        if lemma:
            frame_s   = frame.replace(lemma, "----s")
            frame_ing = frame.replace(lemma, "----ing")
            frame_ing = frame_ing.replace("----inging", "----ing")

        if frame_s in self: return self[frame_s]
        elif frame_ing in self: return self[frame_ing]
        else: raise KeyError("The frame %s or %s is not in knowledge." % (frame_s, frame_ing))

class VerbTemplate(object):
    """
    @todo: Have knowledge store VerbTemplate objects instead of a dict
    """

    knowledge = Knowledge.read()
    
    def __init__(self, frame, lemma):

        fields = self.knowledge.lookup(frame, lemma)[0] # Temporary

        self.frame       = fields['frame']
        self.verbmap     = fields['verbmap']
        self.wimtemplate = fields['wimtemplate'].split(" ")
        self.example     = fields['example']
        self.parse       = fields['parse']
        self.sense       = None

        self.constituents = [] # REMOVE!!! THIS IS SO BAD

    def split_frame(self, frame):
        """
        @todo: fix.
        """
        frame = frame.replace('body part', 'body-part')
        frame = frame.split(" ")
        tmp   = []
        for item in frame:
            tmp.append(item.replace('body-part', 'body part'))
        return tmp

    def match(self, verbphrase):
        
        # Get the constituent bits of the phrase

        self.constituents = phrase = list(verbphrase.constituents(self.verbmap))

        if len(phrase) != len(self.split_frame(self.frame)):
            return False

        # If the constituents don't match the verb map, we're done.
        for constituent in phrase:
            if constituent._bits:
                attrs = constituent._bits.split(',')
                for attr in attrs:
                    if attr == "head": continue
                    fparts = attr.split(":")
                    attr   = fparts[0]
                    if len(fparts) > 1:
                        param = [verbphrase, fparts[1]]
                    else:
                        param = [verbphrase,]

                    # This will raise an exception if not done right
                    attr = getattr(constituent, attr)
                    if callable(attr):
                        if not attr(*param):
                            if self.frame == "Something is ----ing PP": pass
                                #print verbphrase
#                                print "Failed on: %s" % self.frame
#                                print "\tChecking %s with params: %s" % (attr.__name__, param)
#                                print "\t On: %s" % (constituent,)

 #                               print 

#                                for ct in phrase:
#                                    print "%s: %s" % (ct._bits, ct.text())
                            return False

        return True
                
    def addproperties(self, vp, wim):
        for idx, map in enumerate(self.mappedcomponents):
            meaning = self.mappedmeanings[idx]
            if map == "HEAD":
                pass
            elif map == "SUBJECT":
                for rootNP in vp.subject().rootNPs():
                    vp.frame(wim).addproperty(meaning.lower(), rootNP.frame(wim).name())
            elif map == "DIRECTOBJECT":
                for rootNP in vp.directobject().topNPs():
                    vp.frame(wim).addproperty(meaning.lower(), rootNP.frame(wim).name())
            else:
                #print "--WARNING: didn't know how to add property for %s" % map
                pass
        
    def __str__(self):
        return self.frame

if __name__ == "__main__":

    from phrase import BasePhrase

    sentence = BasePhrase("(S (S (CL (NP (DET (DT the)) (NP (N man)))(VP (V hit)(NP (DET (DT the)) (NP (N building))))))(PUNCT .))")
    frame    = VerbFrame("Somebody hit something", "hit")
    phrase   = list(sentence.findall('VP'))[0]

    if frame.match(phrase):
        print "pass"
    else:
        print "fail"

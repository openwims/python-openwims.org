#!/usr/bin/env python

import sys
import time
import importlib
import json

from wim.utils import *
from nltk.tree import Tree
from optparse import make_option
from wim.wookie import WookieTree
from wim.analyze import WIMAnalyzer
from meridian.reader import Sentence
from simpleconsole import ConsoleError, ConsoleProgram

DEFAULT_GRAMMAR = Sentence.grammarfile
DEFAULT_PARSER  = "nltk.parse.ViterbiParser"

class Wimify(ConsoleProgram):
    
    opts = ConsoleProgram.opts + (
        make_option('-g', '--grammar', metavar='PATH', default=DEFAULT_GRAMMAR, dest='grammar', action='store',
            help='Set the path to the grammar to use instead of the default grammar'),
        make_option('-c', '--class', metavar='CLASS', default=DEFAULT_PARSER, dest='parser', action='store',
            help='Set the class of the parser to use- use module dot notation'),
        make_option('-i', '--index', metavar='INT', default=1, dest='index', action='store', type='int',
            help='Set the index for the output of the JSON file'),
    )

    help = 'Parse and analyze a WIM from a sentence on the command line.'
    args = 'SENTENCE'

    version = ('1', '0', '0')

    def handle(self, *args, **opts):
        
        self.verbosity   = int(opts.get('verbosity', 1))
        self.grammarfile = opts.get('grammar', DEFAULT_GRAMMAR)
        self.parserclass = class_from_string(opts.get('parser', DEFAULT_PARSER))

        if len(args) != 1:
            raise ConsoleError("Specificy a sentence surrounded in double quotes to parse and analyze")

        self.output = {
            'index': int(opts.get('index', 1)),
            'text': args[0],
        }

        if self.verbosity > 1:
            print "Parsing..."
        self.parse()

        if self.verbosity > 1:
            print "Analyzing..."
        self.analyze()

        output = "%s\n" % json.dumps(self.output, ensure_ascii=False, indent='    ')
        return output

    def parse(self):
        
        sentence = Sentence(self.output['text'])
        sentence.grammarfile = self.grammarfile
        sentence.parserclass = self.parserclass
        tokens   = sentence.tokens

        start = time.time()

        parse = sentence.parse

        if parse:
            if isinstance(parse, list):
                parse = parse[0]
        else:
            parse = None

        finit = time.time()
        delta = finit - start

        self.output['parse'] = flatten_tree_string(parse)
        self.output['wookie_parse'] = flatten_tree_string(WookieTree.convert(parse).strip())
        self.output['parse_prob'] = parse.prob() if hasattr(parse, 'prob') else 0.0
        self.output['parse_time'] = delta

    def analyze(self):

#        if self.output['parse']:
        if self.output['wookie_parse']:

            start = time.time()
            
#            analyzer = WIMAnalyzer(self.output['parse'])
            analyzer = WIMAnalyzer(self.output['wookie_parse'])
            wim = analyzer.analyze()

            finit = time.time()
            delta = finit - start

            self.output['wim'] = wim.serialize()
            self.output['wim_time'] = delta

        else:
            self.output['wim'] = {}
            self.output['wim_time'] = 0.0

if __name__ == "__main__":
    Wimify().load(sys.argv)

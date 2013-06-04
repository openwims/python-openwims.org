import nltk.tree

"""
Helper methods to convert stanford parses to goatlick ones.

Phases:
    
    1. Change PUNCT (COMMA ,) (PUNCT .) (PUNCT !) (PUNCT ?)
    2. Wrap nouns in generic N (NN, NNS, NNP, NNPS, PRP) 
        * Note Noun Noun Compounds are also supossed to be wrapped in N. 
    3. Wrap verbs in generic V (VB, VBD, VBG, VBN, VBP, VBZ)
    4. Wrap adverbs in generic ADV (RB, RBR, RBS)
    5. Wrap adjectives in generic ADJ (JJ, JJR, JJS)
    6. Change ROOT to S
    7. Change to CL (S, SBAR, SBARQ, SINV, SQ) except FIRST S
    8. Split tag on - (Functional tags) and remove tag[1:]

"""
COMMA = (',',)
ROOTS = ('ROOT', )
PUNCT = ('.', '!', '?')
NOUNS = ('NN', 'NNS', 'NNP', 'NNPS', 'PRP')
VERBS = ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')
CLAUS = ('S', 'SBAR', 'SBARQ', 'SINV', 'SQ') 
ADJTS = ('JJ', 'JJR', 'JJS')
ADVBS = ('RB', 'RBR', 'RBS')

CONVERSIONS = {
    'COMMA': COMMA,
    'PUNCT': PUNCT,
    'CL':    CLAUS,
    'S':     ROOTS,
}

WRAPPINGS = {
    'N': NOUNS,
    'V': VERBS,
    'ADV': ADVBS,
    'ADJ': ADJTS,
}

def stan2goat(tree_or_str):
    
    if isinstance(tree_or_str, basestring):
        tree = nltk.tree.Tree(tree_or_str)
    elif isinstance(tree_or_str, nltk.tree.Tree):
        tree = tree_or_str
    else:
        raise TypeError("Argument is not convertable into an NLTK Tree structure")
    
    def convert(tree):

        if not isinstance(tree, nltk.tree.Tree): return tree
        
        klass = tree.__class__
        node  = tree.node

        # Strip functional tags
        if '-' in node:
            node = node.split('-')[0]

        # Convert the node
        for tag, stags in CONVERSIONS.items():
            if node in stags:
                node = tag
                break

        # Wrap the WRAPPINGS and convert children recursively
        children = []
        for child in tree:
            if isinstance(child, klass):
                wrapped = None
                for tag, stags in WRAPPINGS.items():
                    if child.node in stags:
                        wrapped = klass(tag, [klass(child.node, list(convert(child)))])
                        break
                if wrapped is None:
                    wrapped = convert(child)
                children.append(wrapped)
            else:
                children.append(child)
        
        return klass(node, children)

    # Perform the conversion
    return convert(tree)

if __name__ == "__main__":

    parse = '(ROOT (S (S (NP (NP (DT The) (JJS strongest) (NN rain)) (VP (ADVP (RB ever)) (VBN recorded) (PP (IN in) (NP (NNP India))))) (VP (VP (VBD shut) (PRT (RP down)) (NP (NP (DT the) (JJ financial) (NN hub)) (PP (IN of) (NP (NNP Mumbai))))) (, ,) (VP (VBD snapped) (NP (NN communication) (NNS lines))) (, ,) (VP (VBD closed) (NP (NNS airports))) (CC and) (VP (VBD forced) (NP (NP (NNS thousands)) (PP (IN of) (NP (NNS people)))) (S (VP (TO to) (VP (VP (VB sleep) (PP (IN in) (NP (PRP$ their) (NNS offices)))) (CC or) (VP (VB walk) (NP (NN home)) (PP (IN during) (NP (DT the) (NN night)))))))))) (, ,) (NP (NNS officials)) (VP (VBD said) (NP-TMP (NN today))) (. .)))'
    
    print stan2goat(parse)

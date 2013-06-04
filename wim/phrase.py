# wim.phrase
# Wim: Relative Phrase Explorers
#
# Author:  Jesse English <jesse@unboundconcepts.com>
#          Benjamin Bengfort <benjamin@unboundconcepts.com>
# URL:     <http://unboundconcepts.com/projects/wim/>
# Created: Wed Dec 12 16:45:45 2012 -0400 
#
# Copyright (C) 2012 Unbound Concepts
# For license information, see LICENSE.TXT
#
# ID: tree.py [1] benjamin@unboundconepts.com $

"""
Classes for representing relative and internal phrases within a parse tree
for quick idenitification of relevant syntactic information for comparison
in frames. These phrases must also be relatively explorable so that they
can traverse the entire syntax tree from subtree nodes, and have expanded
helper methods for meaning dependencies and tree extraction.

:todo: See TODOs in the ``BasePhrase`` object.
:todo: Figure out what is going on with ``descendant``
:todo: Document and refactor the frame methods
"""

__docformat__ = "restructuredtext en"

##########################################################################
## Imports and Package Dependencies
##########################################################################

from nltk.tree import Tree, AbstractParentedTree
from nltk.corpus import wordnet as wn

##########################################################################
## Base Phrase Explorer
##########################################################################

class BasePhrase(AbstractParentedTree):
    """
    A base class for all phrases that is of type ``AbstractParentedTree``,
    an abstract class that automatically maintains pointers to parent
    nodes. These parent  pointers are updated whenever any change is made
    to the tree's structure. 

    ..  note:: Subclassing AbstractParentedTree requires two methods:

        - ``_setparent()`` called whenever a new child is added
        - ``_delparent()`` called whenever a child is removed

    The base phrase builds its internal phrases, representing them as a
    subtype of the BasePhrase. These internal phrases then have semantic
    helper methods for identifying the internals of their own phrase type. 

    Phrase types currently defined:

        - ``SentencePhrase`` is used to identify a complete sentence

        - ``NounPhrase`` is used for complete NP identification, including
          selecting the head, and identifying it as somebody or something

        - ``VerbPhrase`` is used for complete VP identification, including
          selecting the head, and idenitifying wim constituents, as well
          as finding indirect and direct objects of the phrase. This 
          expansive object does a lot of semantic work.

        - ``PrepPhrase`` is used for PP identification

        - ``AdjPhrase`` is used for ADJP identification

        - ``TokenPhrase`` is used for nodes that wrap a single token in
          their tree structure, as opposed to a multiple token phrase.

    ..  note:: Each phrase may have at most one parent.

    ..  todo:: Refactor with meta class and override __new__ in order to
        get proper subtype without resorting to ``BasePhrase.build`` in 
        __init__.

    ..  todo:: Add comparison overrides ``__eq__``, ``__gte__``, etc. for 
        comparison
    
    ..  todo:: Add hash method override ``__hash__`` for using in hashable
        types

    ..  todo:: Implement an ``after`` method that finds the element after 
        the parameter that matches a filter.
    
    ..  todo:: Make the ``find`` method recursive
    """

    #/////////////////////////////////////////////////////////////////////
    # Class (Static) Methods
    #/////////////////////////////////////////////////////////////////////

    @classmethod
    def convert(klass, tree):
        """
        Maps the correct subtype to the node in order to correctly add
        helper methods on a per-phrase basis. The node in this case should
        be a string representing the part of speech of the tree.
        
        Typically, this method is called from the constructor, which
        expects a string representation of a tree, or another tree class.

        ..  warning:: This method cannot be used in conjunction with 
            ``Tree.parse``, pass a string into init to parse it.
        """
        classmap = {
            "CL":   ClausePhrase,
            "NP":   NounPhrase,
            "VP":   VerbPhrase,
            "PP":   PrepPhrase,
            "ADJP": AdjPhrase,
            "N":    TokenPhrase,
            "V":    TokenPhrase,
            "ADJ":  TokenPhrase,
            "ADV":  TokenPhrase,
            "CONJ": TokenPhrase,
            "DET":  TokenPhrase,
            "PRO":  TokenPhrase,
            "TO":   TokenPhrase,
            "PREP": TokenPhrase,
        }   

        if isinstance(tree, Tree):
            children = [klass.convert(child) for child in tree]
            if tree.node not in classmap:
                return klass(tree.node, children)
            else:
                return classmap[tree.node](tree.node, children)
        else:
            return tree

    def __init__(self, node_or_str, children=None):
        self._parent = None   
        super(BasePhrase, self).__init__(node_or_str, children)

        for idx, child in enumerate(self):
            # Retype all children with the appropriate phrase type
            if isinstance(child, Tree):
                child._parent = None        # Ensure that super didn't set wrong parent
                self._setparent(child, idx) # Set the child's parent as self

                self[idx] = BasePhrase.convert(child)

        self._bits  = None                  # Temporary object
        self._frame = None                  # Temporary object

    #/////////////////////////////////////////////////////////////////////
    # Properties
    #/////////////////////////////////////////////////////////////////////

    @property
    def parent(self):
        """
        The parent of this tree, or None if it has no parent.

        :note: Overridden to be a property instead of a method.
        """
        return self._parent

    @property
    def root(self):
        """
        The root of this tree- the unique ancestor of this tree whose
        parent is None. If ``self.parent`` is ``None``, then ptree is its 
        own root.
        
        :note: Overriden to be a property instead of a method.
        """
        root = self
        while root.parent() is not None:
            root = root.parent()
        return root

    #/////////////////////////////////////////////////////////////////////
    # Methods
    #/////////////////////////////////////////////////////////////////////

    def parent_index(self):
        """
        The index of this tree in its parent. For example where:
        ``phrase.parent[phrase.parent_index()]`` is phrase.

        ..  note:: ``phrase.parent_index()`` is not necessarily equal to
            ``phrase.parent().index(phrase)`` since the ``index()`` method
            returns the first child that is equal to its argument.

        :rtype: ``int``
        """
        if self._parent is None: return None
        for idx, child in enumerate(self._parent):
            if child is self: return idx
        assert False, "expected to find self in self._parent!"

    def treeposition(self):
        """
        The tree position of this tree, relative to the root of the tree,
        e.g. ``phrase.root[phrase.treeposition]`` is phrase.

        :rtypes: ``int``
        """
        if self.parent is None:
            return ()
        return self.parent().treeposition() + (self.parent_index(),)
                
    def text(self):
        """
        The representation of the phrase as a string of engish words. This
        might seem obvious, but other display mechanisms like str and repr
        do more tree specific display than text display.

        :returns: The string representation of the text.
        :rtype: ``basestring``
        """
        return ' '.join(self.tokens())
        
    def tokens(self):
        """
        The semantics of a phrase are that the leaf nodes contain the
        tokens of the english representation of the phrase. Therefore this
        helper method returns the leaves, or an ordered list of tokens in
        the phrase.

        :returns: An ordered list of tokens in the phrase
        :rtype: ``list(basestring)``
        """
        return self.leaves()

    def token(self, verbphrase, string):
        """
        :todo: put in the right place, and document.
        :todo: How to deal with quotes?
        :todo: Dealing with head tokens correctly
        """
        string = string.strip()
        string = string.strip('"')
        return (string.lower() == self.text().lower() or
            self.head().token(verbphrase, string))

    def siblings(self):
        """
        Return all subtrees that are at the same level as this phrase, or
        said differently, return all children of the parent, less this 
        phrase. 

        :returns: A list of subtrees of the root tree
        :rtype: ``generator``
        """
        if self._parent is not None:
            # The root node will have no siblings
            for child in self._parent:
                if child != self:
                    yield child

    #/////////////////////////////////////////////////////////////////////
    # Phrase Methods (Required in Subclasses)
    #/////////////////////////////////////////////////////////////////////

    def head(self):
        """
        Return the head of the phrase, or more appropriately the subtree
        that represents the head of the phrase. The head is the part of 
        the phrase that classifies it particularly. For instance the head
        of a NounPhrase is a Noun, and of a VerbPhrase, a Verb, etc.

        :returns: The head of the phrase
        :rtype: ``BasePhrase``
        """
        raise NotImplementedError("No head implemented on %s" % self.__class__.__name__)

    #/////////////////////////////////////////////////////////////////////
    # Tree Searching and Traversal
    #/////////////////////////////////////////////////////////////////////

    def find(self, node):
        """
        Finds the FIRST child whose node matches the passed in node as the
        argument to the method. This is similar to phrase.index(obj) but 
        optimized such that string comparisons and tree node comparisons 
        happen in a semantically organized way.

        :param node: A string representation of the node value (e.g. "NP")
        :type node: ``basestring``

        :returns: The first matching child or None
        :rtype: ``BasePhrase`` or ``None``

        :note: This method is NOT recursive (only searches its children)
        :todo: Make find recursive
        """
        for child in self:
            if isinstance(child, basestring):
                if child == node:
                    return child
            elif isinstance(child, Tree):
                if child.node == node:
                    return child
            else: continue
        return None

        
    def findall(self, node):
        """
        Finds ALL children whose node matches the passed in node as the 
        argument to the method. This is simply a specialized filter of
        the ``Tree.subtrees`` method, and the helper is implemented so.

        :param node: A string representation of the node value (e.g. "NP")
        :type node: ``basestring``
    
        :returns: A list of matching subtrees
        :rtype: ``list(BasePhrase)``
        """
        return self.subtrees(filter=lambda t: t.node==node)

    def findparent(self, node):
        """
        Finds the FIRST parent whose node matches the passed in node as
        the first agrument to the method. This method searches from the
        current phrase up towards the root, locating the closest ancestor.

        :param node: A string representation of the node value (e.g. "NP")
        :type node: ``basestring``
        
        :returns: The first matching parent or None if we reach root.
        :rtype: ``BasePhrase`` or ``None``

        :note: This method is recursive (searches all the way to root.)
        """
        if not self.parent: return None
        if self.parent.node == node:
            return self.parent
        return self.parent.findparent(node)

    def pattern_search(self, pattern):
        """
        Takes a pattern, finds an ordered list of subtree elements that
        match the leaves of the supplied pattern, no matter their position
        on the tree. This way you can extract and flatten some constituent
        pattern from a tree, no matter the nesting levels of the parse.

        ..  note:: This is used to match a verb frame in the knowledge 
            with a particular parse tree. This is why the crush bits and
            functional helper functions are inside of this method.

        :todo: Remove the bits part to somewhere sane.

        :param pattern: An ``nltk.tree.Tree`` with leaves to match on.
        :type pattern: ``Tree``

        :returns: A list of possible leaf matches
        :rtype: ``generator``
        """

        def gather_bits(value):
            return value.split("=")[1]

        def crush_bits(value):
            return value.split("=")[0]

        def functional(value):
            return len(value.split("=")) > 1

        idx = 0
        for child in pattern:
            for mychild in self[idx:]:
                idx += 1
                if crush_bits(child.node) == mychild.node: 

                    if functional(child.node):
                        mychild._bits = gather_bits(child.node)

                    if child.height() == 1:
                        yield mychild
                        break
                    else:
                        if functional(child.node):
                            yield mychild
                        for grandchild in mychild.pattern_search(child):
                            yield grandchild


    def descendant(self, subtree):
        """
        :todo: What is the responsibility of this method?

        :todo: No longer necessary, remove.

        ..  note:: This looks like recursive find, but with an object
            instead of a node phrase, is that True?
        """
        for child in self:
            if child == subtree:
                return child
            if isinstance(child, basestring): continue
            gc = child.descendant(subtree)
            if gc is not None:
                return gc
        return None

    #/////////////////////////////////////////////////////////////////////
    # Frame Helpers and Frame Management
    #/////////////////////////////////////////////////////////////////////
            
    def frame(self, wim):
        """
        :todo: document and remove ``self._frame``
        """
        if self._frame == None:
            self._frame = wim.addframe(self.frametype())
            self._frame.addproperty("fromtext", self.text())
        return self._frame
        
    def frametype(self):
        """
        :todo: document
        """
        return self.text()

    #/////////////////////////////////////////////////////////////////////
    # Parent Management
    #/////////////////////////////////////////////////////////////////////

    def _delparent(self, child, index):
        """
        Required from ``AbstractParentedTree`` - same design as 
        ``ParentedTree`` in nltk.
        """
        # Sanity cheks
        assert isinstance(child, BasePhrase)
        assert self[index] is child
        assert child._parent is self

        # Delete child's parent pointer.
        child._parent = None

    def _setparent(self, child, index, dry_run=False):
        """
        Required from ``AbstractParentedTree`` - same design as 
        ``ParentedTree`` in nltk.
        """
        if not isinstance(child, BasePhrase):
            raise TypeError("Can not insert a non-BasePhrase into a Phrase")

        # If child already has a parent, then complain.
        if child._parent is not None:
            raise ValueError("Child phrase already has a parent.")

        # Set child's parent pointer & index. 
        if not dry_run:
            child._parent = self

##########################################################################
## Type Specific Implementations of Phrases
##########################################################################
        
class ClausePhrase(BasePhrase):
    """
    Represents a clause, or more specifically a subtree whose root node
    is the nonterminal "CL" but can be expanded to more specific clause 
    representations like WHCL or indeterminate clauses. (Or better yet,
    subclassed!) 

    Currently there are is no additional functionality needed, but the
    type is still required for better type checking. 

    :todo: Implement subclasses and any required body
    """
    
    def head(self):
        """
        :todo: Document
        """
        return self.find('VP')
     
class PrepPhrase(BasePhrase):
    """
    Represents a prepositional phrase, specifically a subtree whose root
    node is the nonterminal "PP". This phrase performs phrase specific
    work relative to the use of prepositional phrases in semantic structs.
    """

    #/////////////////////////////////////////////////////////////////////
    # Methods
    #/////////////////////////////////////////////////////////////////////
    
    def head(self):
        """
        Searches the subtree for the head of the prepositional phrase, 
        in this case, it lazily selects the first noun phrase that it 
        encounters. 

        :note: For now, assumes the head is the first NP in the PP

        :returns: The ``NounPhrase`` that heads the ``PrepPhrase``
        :rtype: ``NounPhrase``
        """
        phrase = self.find("NP")
        if phrase is not None:
            return phrase
        phrase = self.find("CL")
        if phrase is not None:
            return phrase.head()
        return None

class AdjPhrase(BasePhrase):
    """
    Represents an adjective phrase, specifically a subtree whose root node
    is the nonterminal "ADJP". This phrase performs phrase specific work
    relative to the use of adjective phrases in semantic structures.
    """

    #/////////////////////////////////////////////////////////////////////
    # Methods
    #/////////////////////////////////////////////////////////////////////

    def head(self):
        """
        Searches the subtree for the head of the adjective phrase, in this
        case, it lazily selects the first adjective that it encounters.

        :note: For now, assume head is the first ADJ in the ADJP

        :returns: The ``TokenPhrase`` that heads the ``AdjPhrase``
        :rtype: ``TokenPhrase``
        """
        return self.findall("ADJ")
    
    def check_framemap(self, fmap):
        """
        Checks if the frame map specifies an adjective as this constituent
        otherwise, ensure teh work is passed to the BasePhrase.

        :todo: Replace with functional bits from the frame pattern.

        :param fmap: The string mapping from the wordnet frame.
        :type fmap: ``basestring``

        :rtype: ``bool``
        """
        fmap = fmap.lower()
        if 'adjective' in fmap:
            return True
        return super(AdjPhrase, self).check_framemap(fmap)

    def directobject(self, verbphrase):
        """
        Checks if this particular adjphrase is the direct object of the
        passed in verbphrase.

        :note: Duplication on NounPhrase

        ..  todo:: Document
        ..  todo:: Refactor the selfy checks (subject, direct & indirect
            objects)
        """
        return verbphrase.directobject() == self
                        
class NounPhrase(BasePhrase):
    """
    Represents a noun phrase, specifically a subtree whose root node is
    the nonterminal "NP". This phrase performs phrase specific work 
    relative to the use of noun phrases in semantic structures. 

    Moreover, this phrase also does simple classification of itself using:

        - ``issombody`` to determine if the NP is a person
        - ``issomething`` determines if the NP is a thing
        - ``ispossesive`` determines if the NP is possesive
        - ``isbodypart`` determines if the NP is a body part

    Further helper classification can be implemented on this class or
    subclasses to provide for better knowledge representations. 

    :todo: Document classifiers
    """

    #/////////////////////////////////////////////////////////////////////
    # Classification Methods
    #/////////////////////////////////////////////////////////////////////

    def something(self, *args):
        """
        Nouns are always something!

        :rtype: ``bool``
        """
        return True
    
    def somebody(self, *args):
        """
        Checks Wordnet if the head noun is an animal- making this somebody
        but first performs a quick, easier check to see if the PoS tagger
        already discovered that this was a person.

        :rtype: ``bool``
        """
        head = self.head()
        
        tags = ("NNP", "NNPS", "PRP", "PRO")
        for tag in tags:
            if head.find(tag) is not None:
                return True

        return self.synmatch('animal.n.01')

    def possesive(self, *args):
        """
        Checks if the NounPhrase is possesive by checking if a POS tag
        exits as one of the children of the NounPhrase.

        :rtype: ``bool``
        """
        return len(self.findall("POS")) > 0

    def bodypart(self, *args):
        """
        Checks Wordnet if the head noun is a body part.

        :rtype: ``bool``
        """
        return self.synmatch('body_part.n.01')

    def subject(self, verbphrase):
        """
        Checks if this particular nounphrase is the subject of the passed
        in verbphrase. 

        ..  todo:: Document
        ..  todo:: Refactor the selfy checks (subject, direct & indirect
            objects)
        """
        return verbphrase.subject() == self

    def directobject(self, verbphrase):
        """
        Checks if this particular nounphrase is the direct object of the
        passed in verbphrase.

        :note: Duplication on AdjPhrase

        ..  todo:: Document
        ..  todo:: Refactor the selfy checks (subject, direct & indirect
            objects)
        """
        return verbphrase.directobject() == self

    def indirectobject(self, verbphrase):
        """
        ..  todo:: Document
        ..  todo:: Refactor the selfy checks (subject, direct & indirect
            objects)
        """
        return verbphrase.indirectobject() == self

    #/////////////////////////////////////////////////////////////////////
    # NounPhrase Helper Methods
    #/////////////////////////////////////////////////////////////////////

    def synmatch(self, classifier):
        """
        Helper method that uses Wordnet synsets to check if a classifier
        is similar to the path of the synset for the text of the head of
        the phrase.
        
        :param classifier: The Wordnet Ontological Synset classifier
        :type classifier: ``basestring``

        :rtype: ``bool``
        """
        classifier = wn.synset(classifier)
        for synset in wn.synsets(self.head().text(), pos=wn.NOUN):
            if synset.path_similarity(classifier) >= 0.2:
                return True
        return False
        
    def rootNPs(self):
        """
        Look for all the NPs inside the NounPhrase that do not have
        internal noun phrases. (The lowest NPs inside of it).

        :note: We might need this, so refactor.
        :todo: What does this do?
        """
        for subtree in self.findall("NP"):
            if len(list(self.findall("NP"))) == 1:
                if subtree == self:
                    yield self
                else:
                    yield self.descendant(subtree)
                    
    #For now, just assume all top NPs are those that are not found inside a PP
    def topNPs(self):
        """
        All the root NPs that are not found in PrepPhrases. 

        ..  todo:: May not be necessary or moved to PrepPhrase or just a
            filter

        ..  todo:: What does this do?
        """
        for np in self.rootNPs():
            found = False
            for pp in self.findall("PP"):
                if self.descendant(pp).descendant(np) is not None:
                    found = True
            if not found and np is not self:
                yield np

    #/////////////////////////////////////////////////////////////////////
    # BasePhrase Overrides
    #/////////////////////////////////////////////////////////////////////
        
    def head(self):
        """
        Searches the subtree for the head of the noun phrase, in this case
        it lazily selects the first noun that it encounters.

        :note: For now, assume head is the first N in the NP

        :returns: The ``TokenPhrase`` that heads the ``NounPhrase``
        :rtype: ``TokenPhrase``

        :todo: REDOCUMENT
        """
        noun = self.find("N") or self.find("EX")
        if noun is None:
            phrase = self.find("NP")
            if phrase is not None:
                noun = phrase.head()
            else:
                for pos in ("EX", "DET",):
                    noun = self.find(pos)
                    if noun is not None:
                        break
        return noun
        
    def frametype(self):
        """
        :todo: Document
        """
        h = self.head()
        if h is None:
            return self.text()
        return h.text()

class VerbPhrase(BasePhrase):
    """
    Represents a verb phrase, specifically a subtree whose root node is
    the nonterminal "VP". This phrase performs phrase specific work 
    relative to the use of verb phrases in semantic structures. 

    The Verb Phrase is the star of the show when it comes to semantic
    structures, and performs a lot of work in terms of disambiguation and
    frame analysis. It identifies semantic phrase patterns relative to
    the verb phrase with the following methods:

        - ``subject`` identifies the subject of the verb phrase
        - ``directobject`` identifies the object or predicate nomnitive
        - ``indirectobject`` identifies following PP patterns

    These objects also perform verb type recognition and classification:

        - ``isinfinitive`` identifies infinitive verbs
        - ``isgerund`` identifies verbs ending in -ing

    And the most special work of all, Verb Phrases are matched to verb
    frames in our knowledge, and passed these frames via the
    ``constituents`` method to split the surrounding phrases into its
    constituent parts for matching to the semantic structure of the frame.
    """

    #/////////////////////////////////////////////////////////////////////
    # Methods
    #/////////////////////////////////////////////////////////////////////

    def constituents(self, verbmap):
        """
        The workhorse of frame matching and phrases in general. Attempts
        to split the phrase, including the parent phrase into constituent
        parts via a verb mapping from the knowledge base. These parts are
        then compared to functional frame elements and phrasal inference
        is performed to decide if the verb map matches the sentence 
        structure and therefore a wim can be created from it.

        :param verbmap: an special, functional tree in knowledge syntax
        :type verbmap: ``Tree``

        :returns: A list of the constituents matched by the verbmap
        :rtype: ``list(BasePhrase)``

        ..  note:: Couldn't use sets or return a set because phrases are
            unhashable... 

        :todo: Make phrases hashable in order to use the set method.
        """
        clause = self.findparent('CL')
        # Coudn't use set because phrases are unhashable... 
        #return set(list(clause.pattern_search(verbmap)))

        uniques = []
        for item in clause.pattern_search(verbmap):
            if item not in uniques:
                uniques.append(item)
        return uniques

    #/////////////////////////////////////////////////////////////////////
    # Grammatical Phrase Construction
    #/////////////////////////////////////////////////////////////////////

    def subject(self):
        """
        Searches for the subject of the verb phrase, in this case it 
        simply selects the first sibling noun phrase. 

        :note: For now, assume the subject is the first sibling NP

        :returns: The ``NounPhrase`` that is the subject of the VP
        :rtype: ``NounPhrase``
        """
        for sibling in self.siblings():
            if sibling.node == "NP":
                return self._parent.descendant(sibling)
        return None
        
    def directobject(self, *args):
        """
        Searches for the direct object of the verb phrase, in this case it
        simply selects the NP following the head of the VP. 

        :note: For now, assume the DO is the first NP following the head

        :returns: The ``NounPhrase`` that is the direct object of the VP
        :rtype: ``NounPhrase``

        ..  todo:: VP can be direct objects, so this is both a fetch and a
            type checking -- see removal comment
        """

        # This needs to be removed
        if len(args) > 0:
            return self == args[0].directobject()
        # to here

        headidx = self.index(self.head())
        for child in self[headidx:]:
            if child.node in ("NP", "ADJP", "VP"):
                return child
            elif child.node in ("PP", "CL"):
                return child.head()
        return None
        
    #For now, assume the IDO is the first NP in the first PP following the head
    def indirectobject(self, *args):
        """
        Searches for the indirect object of the verb phrase, in this case
        it simply searches for the NP in the first PP following the head.

        ..  note:: For now, assume the IDO is the first NP in the first PP
            following the head.

        :returns: The ``NounPhrase`` that is the indirect object of the VP
        :rtype: ``NounPhrase``

        :todo: Refactor with an ``after`` method in ``BasePhrase``
        :todo: Redocument Classification methods

        ..  todo:: VP can be indirect objects, so this is both a fetch and
            a type checking-- see the removal comment.
        """

        # This needs to be removed
        if len(args) > 0:
            return self == args[0].indirectobject()
        # to here

        head = self.head()
        headFound = False
        for child in self:
            if child == head:
                headFound = True
                continue
            if headFound and child.node == "PP":
                return child.head()
        
        directobj = self.directobject()
        dobjFound = False
        for child in self:
            if child == directobj:
                dobjFound = True
                continue
            if dobjFound and child.node in ("NP", "ADJP"):
                return child
        return None
        
    #/////////////////////////////////////////////////////////////////////
    # Classifification Methods
    #/////////////////////////////////////////////////////////////////////
    
    def infinitive(self, *args):
        """
        Determines whether or not the verb phrase is infinitive. In this
        case we rely on the part of speech tagger to have correctly
        identified the verb form, so we can simply search for the 'VB' tag
        in the verb phrase.

        :rtype: ``bool``
        """
        return len(list(self.head().findall('VB'))) > 0

    def gerund(self, *args):
        """
        Determines whether or not the verb phrase is a gerund (ends in
        -ing). In this case we rely on the part of speech tagger to have
        correctly identifid the verb form, so we can simply search for the
        'VBG' tag in the verb phrase.

        :rtype: ``bool``
        """
        return len(list(self.head().findall('VBG'))) > 0

    #/////////////////////////////////////////////////////////////////////
    # BasePhrase Overrides
    #/////////////////////////////////////////////////////////////////////

    def head(self):
        """
        Searches the subtree for the head of the verb phrase, in this case
        it lazily selects the first verb that it encounters.

        :note: For now, assume head is the first V in the VP

        :return: The ``TokenPhrase`` that heads the ``VerbPhrase``
        :rtype: ``TokenPhrase``

        ..  note:: The "is raining" example fails with this method, as 
            will verbs with a be verb selected in front of the head.

        :todo: Refactor to handle "to be" verbs
        :todo: Make the findall a recursive find
        """
        v = list(self.findall("V"))[0]
        return self.descendant(v)
        
    def headtext(self):
        """
        Helper method for quickly getting access to the head text.

        :returns: The text of the ``TokenPhrase`` that is the head.
        :rtype: ``basestring``
        """
        return self.head().text()

    def frametype(self):
        """
        :todo: Document
        """
        return self.headtext()

class TokenPhrase(BasePhrase):
    """
    Represents a token phrase, specifically a subtree whose nodes wraps
    only one token as its leaf node, e.g. a linear tree with a straight
    shot down to the token. TokenPhrases are special for frame mapping, 
    but are not constructed necessarily for every TokenPhrase.
    """

    #/////////////////////////////////////////////////////////////////////
    # Methods
    #/////////////////////////////////////////////////////////////////////

    def token(self, verbphrase, string):
        """
        Override of BasePhrase.token to skip checking the head since this
        doesn't have a head.

        :todo: fix, refactor
        """
        string = string.strip()
        string = string.strip('"')
        return self.text().lower() == string.lower()

##########################################################################
## Main Method for Testing and Demonstration
##########################################################################

if __name__ == "__main__":

    phrase  = BasePhrase("(S (CL (NP (DET The) (N (NN man))) (VP (V (VBD hit)) (NP (DET the) (N (NN building))))))")
    vphrase = list(phrase.findall('VP'))[0]
    subject = vphrase.subject()
    directo = vphrase.directobject()

    assert vphrase is not None
    assert subject is not None
    assert directo is not None

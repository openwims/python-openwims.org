from nltk.tree import Tree, AbstractParentedTree, ParentedTree

def score_table(alpha, beta):
    
    SCORE_TABLE = {
        "CL": {
            "VP": 0.9,
            "NP": 0.9,
        }
    }

    if alpha == beta: return 1.0
    
    if alpha in SCORE_TABLE:
        if beta in SCORE_TABLE[alpha]:
            return SCORE_TABLE[alpha][beta]

    if beta in SCORE_TABLE:
        if alpha in SCORE_TABLE[beta]:
            return SCORE_TABLE[beta][alpha]

    return 0.0

class WookieMixin(object):
    """
    Expects to mixin to an nltk.Tree class
    """

    def strip(self):
        """
        Performs Jesse and Ben flatten magic for GoatLick in particular.
        """

        # First check if a conjunction or some other failure node is in
        # the tree's children, if so, we don't perform the node flattening.
        skipnodes = ('CC',)
        stripnode = True
        for skip in skipnodes:
            if skip in [subtree.node for subtree in self if isinstance(subtree, Tree)]:
                stripnode = False
                break
        
        # If we didn't find a skipnode in the children, then for every node
        # that is the same as the current node, replace the child with its
        # own children (e.g. remove the duplication
        
        children = []
        if stripnode:
            for child in self:
                if isinstance(child, Tree) and child.node == self.node:
                    children.extend(list(child))
                else:
                    children.append(child)
        else:
            children = list(self)

        # Return a new tree with the tree's node and recursively flattened children.
        return self.__class__(self.node, [child.strip() for child in children]) 

    def terminals(self):    
        """
        Returns a list of terminals in the tree, one step up from the leaf
        nodes. These are more properly pre-terminals.
        """

        terminals = []
        for child in self:
            if isinstance(child, Tree):
               terminals.extend(child.terminals())
            else:
                terminals.append(self)
        return terminals

    def depth(self):
        """
        Attempts to calculate the depth of this node. Must be a
        ``ParentedTree`` class in order to work. Raises an exception
        otherwise.
        """
        if not isinstance(self, AbstractParentedTree):
            raise TypeError("Cannot travel up tree for type %s - subclass AbstractParentedTree" % type(self))

        if not self.parent():
            return 0
        else:
            return self.parent().depth() + 1

    def ancestors(self):
        node = self
        while node.parent() is not None:
            node = node.parent()
            yield node

    def __tscore(self, other):
        # Assumes that self is shallower
        tscore   = 0.0
        distance = 0
        farthest = None
        
        for ancestor in other.ancestors():
            distance += 1
            nsimscore = score_table(self.node, other.node) * distance * 1.0  # The 1.0 is CONST

            if nsimscore > tscore:
                tscore   = nsimscore
                farthest = ancestor

        if farthest is not None:
            tscore *= self.__tscore(farthest)
        
        return tscore


    def similarity(self, other):
        """
        Returns the similarity score of this tree compared to another tree
        """

        if not isinstance(other, WookieMixin):
            raise TypeError("Cannot compare similarity to type %s" % type(other))

        if self.leaves() != other.leaves():
            return 0.0

        score = 1.0
        for terminals in zip(self.terminals(), other.terminals()):
            if terminals[0].depth() <= terminals[1].depth():
                shallowest = terminals[0]
                deepest    = terminals[1]
            else:
                shallowest = terminals[1]
                deepest    = terminals[0]

            score *= shallowest.__tscore(deepest)

        return score

class WookieTree(Tree, WookieMixin):
    """
    An actual WookieTree with the mixed-in methods.
    """
    pass

class VinedWookieTree(ParentedTree, WookieMixin):
    """
    A wookie tree with vines to parents.
    """

    def __init__(self, node_or_str, children=None):
        self._parent = None
        super(VinedWookieTree, self).__init__(node_or_str, children)

        for idx, child in enumerate(self):
            if isinstance(child, Tree):
                child._parent = None
                self._setparent(child, idx)

if __name__ == "__main__":

    oldtree = Tree("(S (CL (NP (DET (DT the)) (NP (N (NN man)))) (VP (VP (V (VBD hit)) (NP (DET (DT the)) (NP (N (NN building))))) (PP (PREP (IN with)) (NP (DET (DT a)) (NP (N (NN bat))))))))")
#    oldtree  = Tree("(S (S (CL (NP (N he)) (VP (VP (V (VBD went)) (TO to) (NP (DET (DT the)) (NP (N (NN park))))) (CC and) (VP (V (VBD drove)) (NP (N (NN home))))))) (PUNCT .))")
    wooktree = VinedWookieTree(str(oldtree))
    wooktree = wooktree.strip()

    print wooktree.similarity(VinedWookieTree.convert(oldtree))

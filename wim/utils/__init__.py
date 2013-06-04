import importlib
import nltk.tree

def class_from_string(klass):
    parts = klass.split('.')
    name  = parts[-1]
    modn  = '.'.join(parts[:-1])

    module = importlib.import_module(modn)
    return getattr(module, name, None)

def flatten_tree_string(tree_or_str):
    
    if isinstance(tree_or_str, nltk.tree.Tree):
        tree = nltk.tree.Tree.convert(tree_or_str)
    elif isinstance(tree_or_str, basestring):
        tree = nltk.tree.Tree.parse(tree_or_str)
    else:
        raise TypeError("Couldn't create a flattened tree string of type %s" % type(tree_or_str))

    tree = str(tree).replace('\n', ' ')

    while tree.find('  ') > -1:
        tree = tree.replace('  ', ' ')

    return tree

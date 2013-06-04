#!/usr/bin/env python

__docformat__ = "restructuredtext en"

class DefaultDict(dict):
    """
    A version of collections.defaultdict that is implemented in Python.

    ..  warning:: Using the ``collections.defaultdict`` is more optimal
        since it is written in ``C``, but a Python implementation should
        give more flexibility in overriding the object.

    :cvar default_factory: The default iterable to create on key access.
    :type default_factory: ``type``
    """

    default_factory = None

    def __init__(self, default_factory=None, *args, **kwargs):
        default_factory = default_factory or self.default_factory
        if default_factory is not None and not callable(default_factory):
            raise TypeError('The default factory must be callable')
        super(dict, self).__init__(*args, **kwargs)
        self.default_factory = default_factory

    def copy(self):
        return self.__copy__()

    def __missing__(self, key):
        """
        If the ``default_factory`` attribute is ``None``, this raises a
        ``KeyError`` exception with the *key* as argument.

        If ``default_factory`` is not ``None``, it is called without 
        arguments to provide a default value for the given *key*, this
        value is inserted in the dictionary for the *key* and returned.

        If calling ``default_factory`` raises an exception, this
        exception is propagated unchanged.

        This method is called by the ``__getitem__()`` method of the 
        ``dict`` class when the requested key is not found; whatever it
        returns or raises is then returned by ``__getitem__()``.

        ..  note:: Note that ``__missing__()`` is *not* called for any
            operations besides ``__getitem__()``. This means that
            ``get()`` will, like normal dictionaries, return ``None`` as
            the default rather than using ``default_factory``.

        :param key: The key that is missing from the dictionary
        :type key: ``hashable``

        :raises: ``KeyError``
        
        :returns: An instance of the ``default_factory`` type.
        :rtype: type of ``default_factory``
        """
        if self.default_factory is None:
            raise KeyError(key)

        self[key] = value = self.default_factory()
        return value

    def __getitem__(self, key):
        try:
            return super(dict, self).__getitem__(key)
        except KeyError:
            return self.__missing__(key)

    def __reduce__(self):
        """
        Called during pickling.
        """
        args = self.default_factory, # Note the trailing comma, important!
        return type(self), args, None, None, self.items()

    def __copy__(self):
        kwargs = {'default_factory': self.default_factory}
        return type(self)(self, **kwargs)

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__, 
                               self.default_factory,
                               super(dict, self).__repr__())

class BucketDict(DefaultDict):
    """
    A version of collections.defaultdict that specifies an iterable as the
    default factory, then provides expanded methods for dealing with
    objects inside those iterables. The basic idea is that each key can
    specify a bucket, whose contents must be uniquely related to the key 
    and no other key. 

    ..  note:: Please review all dictionary methods as many of them are 
        overriden and may behave unexpectedly.
    """

    default_factory = list

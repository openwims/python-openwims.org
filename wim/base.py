# wim.base 
# Wim: Base WIM objects
#
# Author:  Jesse English <jesse@unboundconcepts.com>
#          Benjamin Bengfort <benjamin@unboundconcepts.com>
# URL      <http://unboundconcepts.com/projects/wim/>
# Created: Mon Dec 10 10:56:12 2012 -0400
#
# Copyright (C) 2012 Unbound Concepts, Inc.
# For license information, see LICENSE.TXT
#
# ID: base.py [1] benjamin@unboundconcepts.com $

"""
Base classes for data objects that represent Weak Inferred Meanings - a
form of Text Representation Meanings that use only weak verb frame mapping
from WordNet to construct meaning representations that find direct objects
indirect objects, and subjects. 

All objects in the base module are required for many aspects of WIM
processings, therefore they are imported in the __init__ module so that
they are always available when importing the wim module.

:todo: Finish documentation
"""

__docformat__ = "restructuredtext en"

class WIM(object):
    """
    The base object for representing a Weak Inferred Meaning. 

    WIMs contain frames which can contain properites or other frames. They
    operate much like a dictionary, since each frame is a key value pair.

    :todo: Refactor into a dictionary model
    :todo: Create frame collections for easier access and validation.

    ..  attribute:: _frames
        An internal dictionary for storing frames, modeled after the
        __dict__ attribute for property access. The key of this dictionary
        is the frame type, and the value is a list of objects that match
        that frame type.
    """

    def __init__(self, frames={}):
        """
        Build a WIM object.

        :param frames: An optional frame dictionary to initialize with.
        """
        self._frames = frames
        
    def addframe(self, ftype):
        """
        :todo: Replace with __setattr__
        :todo: Keep helper method that uses __setattr__
        """
        matches = []
        if ftype in self._frames:
            matches = self._frames[ftype]
        else:
            self._frames[ftype] = matches
        instance = WIMFrame(ftype, len(matches) + 1)
        matches.append(instance)
        return instance

    def serialize(self):
        """
        Serializes the data object into a series of dictionaries that make
        the WIM static (though still mutable) since they won't have any of
        the methods and properties used to manipulate WIMs. This method is
        typically for serializing the WIM into a JSON format. 

        ..  note:: Using simplejson.dump is recommended from this method.

        :returns: dict
        """
        data = {}
        for key, frames in self._frames.items():
            for frame in frames:
                data[frame.name()] = frame.serialize()

        return data

    def frames(self):
        """
        An iterator that yields every single frame that are stored in the
        internal _frames dictionary, looping through the list values. 

        :returns: generator 
        """
        for frames in self._frames.values():
            for frame in frames:
                yield frame
        
    def __str__(self):
        """
        A string representation of the WIM, verbosely outputting every
        frame and property seperated by new lines. These can be big!

        :returns: str
        """
        return self.__unicode__().encode('ascii', 'replace')

    def __unicode__(self):
        """
        A string representation of the WIM, verbosely outputting every
        frame and property seperated by new lines. These can be big! 

        :returns: unicode
        """
        return "\n".join([str(frame) for frame in self.frames()])
        
class WIMFrame(object):

    def __init__(self, instance, num):
        self._instance = instance
        self._num = num
        self._properties = []

    def addproperty(self, property, value):
        self._properties.append(WIMProperty(property, value))
        
    def name(self):
        return "%s-%i" % (self._instance, self._num)

    def serialize(self):
        data = {}
        for prop in self._properties:
            if isinstance(prop._value, WIMFrame):
                data[prop._property] = prop._value.name()
            else:
                data[prop._property] = prop._value
        return data
        
    def __str__(self):
        out = "%s\n" % self.name()
        for prop in self._properties:
            out += "  " + str(prop) + "\n"
        return out
        
class WIMProperty(object):

    def __init__(self, property, value):
        self._property = property
        self._value = value
        
    def __str__(self):
        if isinstance(self._value, WIMFrame):
            value = self._value.name()
        else:
            value = self._value
        return self._property + " - " + value


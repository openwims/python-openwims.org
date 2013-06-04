#!/usr/bin/env python
# -*- coding: utf-8 -*-

UNISTR = u"être"

if __name__ == "__main__":
    
    print "Unicode:          '%s'" % UNISTR
    print "ASCII ignore:     '%s'" % UNISTR.encode('ascii', 'ignore')
    print "ASCII replace:    '%s'" % UNISTR.encode('ascii', 'replace')
    print "ASCII xmlreplace: '%s'" % UNISTR.encode('ascii', 'xmlcharrefreplace')
    print "ASCII bsreplace:  '%s'" % UNISTR.encode('ascii', 'backslashreplace')
    print "UTF8 encode:      '%s'" % UNISTR.encode('utf8', 'ignore')

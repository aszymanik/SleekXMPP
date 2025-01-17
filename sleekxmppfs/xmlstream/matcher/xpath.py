# -*- coding: utf-8 -*-
"""
    sleekxmppfs.xmlstream.matcher.xpath
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Part of SleekXMPP: The Sleek XMPP Library

    :copyright: (c) 2011 Nathanael C. Fritz
    :license: MIT, see LICENSE for more details
"""

from sleekxmppfs.xmlstream.stanzabase import ET, fix_ns
from sleekxmppfs.xmlstream.matcher.base import MatcherBase


class MatchXPath(MatcherBase):

    """
    The XPath matcher selects stanzas whose XML contents matches a given
    XPath expression.

    .. warning::

        Using this matcher may not produce expected behavior when using
        attribute selectors. For Python 2.6 and 3.1, the ElementTree
        :meth:`~xml.etree.ElementTree.Element.find()` method does
        not support the use of attribute selectors. If you need to
        support Python 2.6 or 3.1, it might be more useful to use a
        :class:`~sleekxmppfs.xmlstream.matcher.stanzapath.StanzaPath` matcher.

    If the value of :data:`IGNORE_NS` is set to ``True``, then XPath
    expressions will be matched without using namespaces.
    """

    def __init__(self, criteria):
        self._criteria = fix_ns(criteria)

    def match(self, xml):
        """
        Compare a stanza's XML contents to an XPath expression.

        If the value of :data:`IGNORE_NS` is set to ``True``, then XPath
        expressions will be matched without using namespaces.

        .. warning::

            In Python 2.6 and 3.1 the ElementTree
            :meth:`~xml.etree.ElementTree.Element.find()` method does not
            support attribute selectors in the XPath expression.

        :param xml: The :class:`~sleekxmppfs.xmlstream.stanzabase.ElementBase`
                    stanza to compare against.
        """
        if hasattr(xml, 'xml'):
            xml = xml.xml
        x = ET.Element('x')
        x.append(xml)

        return x.find(self._criteria) is not None

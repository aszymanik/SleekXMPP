"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz,
                       Emmanuel Gil Peyrot <linkmauve@linkmauve.fr>
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0231.stanza import BitsOfBinary
from sleekxmppfs.plugins.xep_0231.bob import XEP_0231


register_plugin(XEP_0231)

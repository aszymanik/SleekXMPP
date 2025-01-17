"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2013 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0095 import stanza
from sleekxmppfs.plugins.xep_0095.stanza import SI
from sleekxmppfs.plugins.xep_0095.stream_initiation import XEP_0095


register_plugin(XEP_0095)

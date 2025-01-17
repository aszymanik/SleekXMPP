"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0221 import stanza
from sleekxmppfs.plugins.xep_0221.stanza import Media, URI
from sleekxmppfs.plugins.xep_0221.media import XEP_0221


register_plugin(XEP_0221)

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2013 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0152 import stanza
from sleekxmppfs.plugins.xep_0152.stanza import Reachability
from sleekxmppfs.plugins.xep_0152.reachability import XEP_0152


register_plugin(XEP_0152)

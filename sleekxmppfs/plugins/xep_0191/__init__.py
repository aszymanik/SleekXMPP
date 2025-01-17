"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0191.stanza import Block, Unblock, BlockList
from sleekxmppfs.plugins.xep_0191.blocking import XEP_0191


register_plugin(XEP_0191)

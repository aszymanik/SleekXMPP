"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2016 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0334.stanza import Store, NoStore, NoPermanentStore, NoCopy
from sleekxmppfs.plugins.xep_0334.hints import XEP_0334

register_plugin(XEP_0334)

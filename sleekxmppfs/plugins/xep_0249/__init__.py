"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2011 Nathanael C. Fritz, Dalek
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0249.stanza import Invite
from sleekxmppfs.plugins.xep_0249.invite import XEP_0249


register_plugin(XEP_0249)


# Retain some backwards compatibility
xep_0249 = XEP_0249

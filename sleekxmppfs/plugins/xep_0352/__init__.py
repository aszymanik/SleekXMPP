"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2016 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0352.stanza import Active, Inactive, ClientStateIndication
from sleekxmppfs.plugins.xep_0352.csi import XEP_0352


register_plugin(XEP_0352)

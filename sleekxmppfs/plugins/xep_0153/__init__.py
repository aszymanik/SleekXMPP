"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0153.stanza import VCardTempUpdate
from sleekxmppfs.plugins.xep_0153.vcard_avatar import XEP_0153


register_plugin(XEP_0153)

"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0054.stanza import VCardTemp
from sleekxmppfs.plugins.xep_0054.vcard_temp import XEP_0054


register_plugin(XEP_0054)

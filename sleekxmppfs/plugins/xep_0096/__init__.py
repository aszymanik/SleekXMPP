"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2013 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0096 import stanza
from sleekxmppfs.plugins.xep_0096.stanza import File
from sleekxmppfs.plugins.xep_0096.file_transfer import XEP_0096


register_plugin(XEP_0096)

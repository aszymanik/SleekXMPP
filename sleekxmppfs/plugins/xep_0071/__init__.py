"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permissio
"""

from sleekxmppfs.plugins.base import register_plugin

from sleekxmppfs.plugins.xep_0071.stanza import XHTML_IM
from sleekxmppfs.plugins.xep_0071.xhtml_im import XEP_0071


register_plugin(XEP_0071)

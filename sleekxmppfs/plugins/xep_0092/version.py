"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2010 Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import logging

import sleekxmppfs
from sleekxmppfs import Iq
from sleekxmppfs.xmlstream import register_stanza_plugin
from sleekxmppfs.xmlstream.handler import Callback
from sleekxmppfs.xmlstream.matcher import StanzaPath
from sleekxmppfs.plugins import BasePlugin
from sleekxmppfs.plugins.xep_0092 import Version, stanza


log = logging.getLogger(__name__)


class XEP_0092(BasePlugin):

    """
    XEP-0092: Software Version
    """

    name = 'xep_0092'
    description = 'XEP-0092: Software Version'
    dependencies = set(['xep_0030'])
    stanza = stanza
    default_config = {
        'software_name': 'SleekXMPP',
        'version': sleekxmppfs.__version__,
        'os': ''
    }

    def plugin_init(self):
        """
        Start the XEP-0092 plugin.
        """
        if 'name' in self.config:
            self.software_name = self.config['name']

        self.xmpp.register_handler(
                Callback('Software Version',
                         StanzaPath('iq@type=get/software_version'),
                         self._handle_version))

        register_stanza_plugin(Iq, Version)

    def plugin_end(self):
        self.xmpp.remove_handler('Software Version')
        self.xmpp['xep_0030'].del_feature(feature='jabber:iq:version')

    def session_bind(self, jid):
        self.xmpp.plugin['xep_0030'].add_feature('jabber:iq:version')

    def _handle_version(self, iq):
        """
        Respond to a software version query.

        Arguments:
            iq -- The Iq stanza containing the software version query.
        """
        iq.reply()
        iq['software_version']['name'] = self.software_name
        iq['software_version']['version'] = self.version
        iq['software_version']['os'] = self.os
        iq.send()

    def get_version(self, jid, ifrom=None, block=True, timeout=None, callback=None):
        """
        Retrieve the software version of a remote agent.

        Arguments:
            jid -- The JID of the entity to query.
        """
        iq = self.xmpp.Iq()
        iq['to'] = jid
        iq['from'] = ifrom
        iq['type'] = 'get'
        iq['query'] = Version.namespace
        return iq.send(block=block, timeout=timeout, callback=callback)

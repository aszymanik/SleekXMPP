"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2011  Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import logging

from sleekxmppfs.jid import JID
from sleekxmppfs.stanza import Iq, StreamFeatures
from sleekxmppfs.features.feature_bind import stanza
from sleekxmppfs.xmlstream import register_stanza_plugin
from sleekxmppfs.plugins import BasePlugin


log = logging.getLogger(__name__)


class FeatureBind(BasePlugin):

    name = 'feature_bind'
    description = 'RFC 6120: Stream Feature: Resource Binding'
    dependencies = set()
    stanza = stanza

    def plugin_init(self):
        self.xmpp.register_feature('bind',
                self._handle_bind_resource,
                restart=False,
                order=10000)

        register_stanza_plugin(Iq, stanza.Bind)
        register_stanza_plugin(StreamFeatures, stanza.Bind)

    def _handle_bind_resource(self, features):
        """
        Handle requesting a specific resource.

        Arguments:
            features -- The stream features stanza.
        """
        log.debug("Requesting resource: %s", self.xmpp.requested_jid.resource)
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq.enable('bind')
        if self.xmpp.requested_jid.resource:
            iq['bind']['resource'] = self.xmpp.requested_jid.resource
        response = iq.send(now=True)

        self.xmpp.boundjid = JID(response['bind']['jid'], cache_lock=True)
        self.xmpp.bound = True
        self.xmpp.event('session_bind', self.xmpp.boundjid, direct=True)
        self.xmpp.session_bind_event.set()

        self.xmpp.features.add('bind')

        log.info("JID set to: %s", self.xmpp.boundjid.full)

        if 'session' not in features['features']:
            log.debug("Established Session")
            self.xmpp.sessionstarted = True
            self.xmpp.session_started_event.set()
            self.xmpp.event('session_start')

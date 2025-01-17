"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2011 Nathanael C. Fritz
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import uuid
import logging
import hashlib
import random
import sys

from sleekxmppfs.jid import JID
from sleekxmppfs.exceptions import IqError, IqTimeout
from sleekxmppfs.stanza import Iq, StreamFeatures
from sleekxmppfs.xmlstream import ElementBase, ET, register_stanza_plugin
from sleekxmppfs.plugins import BasePlugin
from sleekxmppfs.plugins.xep_0078 import stanza


log = logging.getLogger(__name__)


class XEP_0078(BasePlugin):

    """
    XEP-0078 NON-SASL Authentication

    This XEP is OBSOLETE in favor of using SASL, so DO NOT use this plugin
    unless you are forced to use an old XMPP server implementation.
    """

    name = 'xep_0078'
    description = 'XEP-0078: Non-SASL Authentication'
    dependencies = set()
    stanza = stanza
    default_config = {
        'order': 15,
        'force_plain': False,
    }

    def plugin_init(self):
        self.xmpp.register_feature('auth',
                self._handle_auth,
                restart=False,
                order=self.order)

        self.xmpp.add_event_handler('legacy_protocol',
                self._handle_legacy_protocol)

        register_stanza_plugin(Iq, stanza.IqAuth)
        register_stanza_plugin(StreamFeatures, stanza.AuthFeature)

    def plugin_end(self):
        self.xmpp.del_event_handler('legacy_protocol',
                self._handle_legacy_protocol)
        self.xmpp.unregister_feature('auth', self.order)

    def _handle_auth(self, features):
        # If we can or have already authenticated with SASL, do nothing.
        if 'mechanisms' in features['features']:
            return False
        return self.authenticate()

    def _handle_legacy_protocol(self, event):
        self.authenticate()

    def authenticate(self):
        if self.xmpp.authenticated:
            return False

        log.debug("Starting jabber:iq:auth Authentication")

        # Step 1: Request the auth form
        iq = self.xmpp.Iq()
        iq['type'] = 'get'
        iq['to'] = self.xmpp.requested_jid.host
        iq['auth']['username'] = self.xmpp.requested_jid.user

        try:
            resp = iq.send(now=True)
        except IqError as err:
            log.info("Authentication failed: %s", err.iq['error']['condition'])
            self.xmpp.event('failed_auth', direct=True)
            self.xmpp.disconnect()
            return True
        except IqTimeout:
            log.info("Authentication failed: %s", 'timeout')
            self.xmpp.event('failed_auth', direct=True)
            self.xmpp.disconnect()
            return True

        # Step 2: Fill out auth form for either password or digest auth
        iq = self.xmpp.Iq()
        iq['type'] = 'set'
        iq['auth']['username'] = self.xmpp.requested_jid.user

        # A resource is required, so create a random one if necessary
        resource = self.xmpp.requested_jid.resource
        if not resource:
            resource = str(uuid.uuid4())

        iq['auth']['resource'] = resource

        if not 'digest' in resp['auth']['fields'] or self.force_plain:
            log.warning('Authenticating via jabber:iq:auth Plain.')
            iq['auth']['password'] = self.xmpp.password
        else:
            log.debug('Authenticating via jabber:iq:auth Digest')
            if sys.version_info < (3, 0):
                stream_id = bytes(self.xmpp.stream_id)
                password = bytes(self.xmpp.password)
            else:
                stream_id = bytes(self.xmpp.stream_id, encoding='utf-8')
                password = bytes(self.xmpp.password, encoding='utf-8')

            digest = hashlib.sha1(stream_id + password).hexdigest()
            iq['auth']['digest'] = digest

        # Step 3: Send credentials
        try:
            result = iq.send(now=True)
        except IqError as err:
            log.info("Authentication failed")
            self.xmpp.event("failed_auth", direct=True)
            self.xmpp.disconnect()
        except IqTimeout:
            log.info("Authentication failed")
            self.xmpp.event("failed_auth", direct=True)
            self.xmpp.disconnect()

        self.xmpp.features.add('auth')

        self.xmpp.authenticated = True

        self.xmpp.boundjid = JID(self.xmpp.requested_jid,
                resource=resource,
                cache_lock=True)
        self.xmpp.event('session_bind', self.xmpp.boundjid, direct=True)

        log.debug("Established Session")
        self.xmpp.sessionstarted = True
        self.xmpp.session_started_event.set()
        self.xmpp.event('session_start')

        return True

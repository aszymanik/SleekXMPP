"""
    SleekXMPP: The Sleek XMPP Library
    Copyright (C) 2012 Nathanael C. Fritz, Lance J.T. Stout
    This file is part of SleekXMPP.

    See the file LICENSE for copying permission.
"""

import hashlib
import logging
import threading

from sleekxmppfs.stanza import Presence
from sleekxmppfs.exceptions import XMPPError
from sleekxmppfs.xmlstream import register_stanza_plugin
from sleekxmppfs.plugins.base import BasePlugin
from sleekxmppfs.plugins.xep_0153 import stanza, VCardTempUpdate


log = logging.getLogger(__name__)


class XEP_0153(BasePlugin):

    name = 'xep_0153'
    description = 'XEP-0153: vCard-Based Avatars'
    dependencies = set(['xep_0054'])
    stanza = stanza

    def plugin_init(self):
        self._hashes = {}

        self._allow_advertising = threading.Event()

        register_stanza_plugin(Presence, VCardTempUpdate)

        self.xmpp.add_filter('out', self._update_presence)

        self.xmpp.add_event_handler('session_start', self._start)
        self.xmpp.add_event_handler('session_end', self._end)

        self.xmpp.add_event_handler('presence_available', self._recv_presence)
        self.xmpp.add_event_handler('presence_dnd', self._recv_presence)
        self.xmpp.add_event_handler('presence_xa', self._recv_presence)
        self.xmpp.add_event_handler('presence_chat', self._recv_presence)
        self.xmpp.add_event_handler('presence_away', self._recv_presence)

        self.api.register(self._set_hash, 'set_hash', default=True)
        self.api.register(self._get_hash, 'get_hash', default=True)
        self.api.register(self._reset_hash, 'reset_hash', default=True)

    def plugin_end(self):
        self.xmpp.del_filter('out', self._update_presence)
        self.xmpp.del_event_handler('session_start', self._start)
        self.xmpp.del_event_handler('session_end', self._end)
        self.xmpp.del_event_handler('presence_available', self._recv_presence)
        self.xmpp.del_event_handler('presence_dnd', self._recv_presence)
        self.xmpp.del_event_handler('presence_xa', self._recv_presence)
        self.xmpp.del_event_handler('presence_chat', self._recv_presence)
        self.xmpp.del_event_handler('presence_away', self._recv_presence)

    def set_avatar(self, jid=None, avatar=None, mtype=None, block=True,
                   timeout=None, callback=None):
        if jid is None:
            jid = self.xmpp.boundjid.bare

        vcard = self.xmpp['xep_0054'].get_vcard(jid, cached=True)
        vcard = vcard['vcard_temp']
        vcard['PHOTO']['TYPE'] = mtype
        vcard['PHOTO']['BINVAL'] = avatar

        self.xmpp['xep_0054'].publish_vcard(jid=jid, vcard=vcard)

        self.api['reset_hash'](jid)
        self.xmpp.roster[jid].send_last_presence()

    def _start(self, event):
        try:
            vcard = self.xmpp['xep_0054'].get_vcard(self.xmpp.boundjid.bare)
            data = vcard['vcard_temp']['PHOTO']['BINVAL']
            if not data:
                new_hash = ''
            else:
                new_hash = hashlib.sha1(data).hexdigest()
            self.api['set_hash'](self.xmpp.boundjid, args=new_hash)
            self._allow_advertising.set()
        except XMPPError:
            log.debug('Could not retrieve vCard for %s' % self.xmpp.boundjid.bare)

    def _end(self, event):
        self._allow_advertising.clear()

    def _update_presence(self, stanza):
        if not isinstance(stanza, Presence):
            return stanza

        if stanza['type'] not in ('available', 'dnd', 'chat', 'away', 'xa'):
            return stanza

        current_hash = self.api['get_hash'](stanza['from'])
        stanza['vcard_temp_update']['photo'] = current_hash
        return stanza

    def _reset_hash(self, jid, node, ifrom, args):
        own_jid = (jid.bare == self.xmpp.boundjid.bare)
        if self.xmpp.is_component:
            own_jid = (jid.domain == self.xmpp.boundjid.domain)

        self.api['set_hash'](jid, args=None)
        if own_jid:
            self.xmpp.roster[jid].send_last_presence()

        try:
            iq = self.xmpp['xep_0054'].get_vcard(jid=jid.bare, ifrom=ifrom)

            data = iq['vcard_temp']['PHOTO']['BINVAL']
            if not data:
                new_hash = ''
            else:
                new_hash = hashlib.sha1(data).hexdigest()

            self.api['set_hash'](jid, args=new_hash)
        except XMPPError:
            log.debug('Could not retrieve vCard for %s' % jid)

    def _recv_presence(self, pres):
        try:
            if pres['muc']['affiliation']:
                # Don't process vCard avatars for MUC occupants
                # since they all share the same bare JID.
                return
        except: pass    

        if not pres.match('presence/vcard_temp_update'):
            self.api['set_hash'](pres['from'], args=None)
            return

        data = pres['vcard_temp_update']['photo']
        if data is None:
            return
        elif data == '' or data != self.api['get_hash'](pres['from']):
            ifrom = pres['to'] if self.xmpp.is_component else None
            self.api['reset_hash'](pres['from'], ifrom=ifrom)
            self.xmpp.event('vcard_avatar_update', pres)

    # =================================================================

    def _get_hash(self, jid, node, ifrom, args):
        return self._hashes.get(jid.bare, None)

    def _set_hash(self, jid, node, ifrom, args):
        self._hashes[jid.bare] = args

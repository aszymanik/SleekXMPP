# -*- coding: utf-8 -*-
"""
    sleekxmppfs.xmlstream.filesocket
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module is a shim for correcting deficiencies in the file
    socket implementation of Python2.7.

    Part of SleekXMPP: The Sleek XMPP Library

    :copyright: (c) 2011 Nathanael C. Fritz
    :license: MIT, see LICENSE for more details
"""

from socket import _fileobject
import errno
import socket


class FileSocket(_fileobject):

    """Create a file object wrapper for a socket to work around
    issues present in Python 2.7 when using sockets as file objects.

    The parser for :class:`~xml.etree.ElementTree` requires a file, but
    we will be reading from the XMPP connection socket instead.
    """

    def read(self, size=4096):
        """Read data from the socket as if it were a file."""
        if self._sock is None:
            return None
        while True:
            try:
                data = self._sock.recv(size)
                break
            except socket.error as serr:
                if serr.errno != errno.EINTR:
                    raise
        if data is not None:
            return data


class Socket27(socket.socket):

    """A custom socket implementation that uses our own FileSocket class
    to work around issues in Python 2.7 when using sockets as files.
    """

    def makefile(self, mode='r', bufsize=-1):
        """makefile([mode[, bufsize]]) -> file object
        Return a regular file object corresponding to the socket.  The mode
        and bufsize arguments are as for the built-in open() function."""
        return FileSocket(self._sock, mode, bufsize)

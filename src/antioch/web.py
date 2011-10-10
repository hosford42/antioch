# antioch
# Copyright (c) 1999-2011 Phil Christensen
#
#
# See LICENSE for details

"""
Setup the web client interface.
"""

import os

from twisted.internet import reactor
from twisted.application import internet
from twisted.cred import portal, checkers, credentials
from twisted.web import resource, server, wsgi

from antioch import client, session, auth, conf, restful

class NevowService(internet.TCPServer):
	"""
	Provides a service that responds to web requests.
	"""
	def __init__(self, msg_service, db_url, access_log):
		from nevow import guard, appserver
		self.checker = auth.TransactionChecker()
		self.session_store = session.TransactionUserSessionStore(self.checker, db_url)
		self.portal = portal.Portal(session.SessionRealm(self.session_store))
		self.portal.registerChecker(session.SessionChecker(self.session_store))
		self.root = client.RootDelegatePage(self.session_store, msg_service, self.portal)
		self.factory = appserver.NevowSite(self.root, logPath=access_log)
		internet.TCPServer.__init__(self, conf.get('web-port'), self.factory)

class DjangoService(internet.TCPServer):
	"""
	Provides a service that responds to web requests.
	"""
	def __init__(self, msg_service, db_url, access_log):
		self.root = restful.RootResource(msg_service)
		log_path = conf.get('access-log') or None
		self.factory = server.Site(self.root, logPath=log_path)
		internet.TCPServer.__init__(self, conf.get('web-port'), self.factory)


# antioch
# Copyright (c) 1999-2010 Phil Christensen
#
#
# See LICENSE for details

import hashlib

from twisted.protocols import amp

from antioch import transact, parser, json, sql

class UpdateSchema(transact.WorldTransaction):
	arguments = []

class RequestAccount(transact.WorldTransaction):
	arguments = [
		('name', amp.String()),
		('email', amp.String()),
	]

class RegistrationTransactionChild(transact.TransactionChild):
	@UpdateSchema.responder
	def update_schema(self):
		with self.get_exchange() as x:
			try:
				x.pool.runQuery(sql.build_select('player', email='user@example.com'))
			except Exception, e:
				x.rollback()
				x.begin()
				x.pool.runOperation("ALTER TABLE player ADD COLUMN email varchar(255)")
				system = x.get_object(1)
				if('registration-version' not in system):
					system.add_property('registration-version')
				from antioch.modules import registration
				system['registration-version'].value = registration.VERSION
		return {'result':True}
	
	@RequestAccount.responder
	def request_account(self, name, email):
		passwd = hashlib.md5(email).hexdigest()[:8]
		with self.get_exchange() as x:
			hammer = x.get_object('wizard hammer')
			user = hammer.add_user(dict(
				name	= name,
				passwd	= passwd,
			))
			x.pool.runOperation(sql.build_update('player', dict(email=email), dict(avatar_id=user.get_id())))
		return {'result':True}

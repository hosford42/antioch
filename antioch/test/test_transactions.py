# antioch
# Copyright (c) 1999-2017 Phil Christensen
#
# See LICENSE for details

from twisted.trial import unittest
from twisted.internet import defer, error

from antioch import test, conf
from antioch.core import errors, exchange, parser, transact, interface, code

from django.db import connection

class TransactionTestCase(unittest.TestCase):
    def setUp(self):
        test.init_database(self.__class__)
    
    @defer.inlineCallbacks
    def tearDown(self):
        yield transact.shutdown()    
    
    def test_basic_rollback(self):
        try:
            with exchange.ObjectExchange(connection) as x:
                x.instantiate('object', name="Test Object")
                raise RuntimeError()
        except:
            pass
        
        self.failUnlessRaises(errors.NoSuchObjectError, x.get_object, "Test Object")
    
    def test_timeout(self):
        if(transact.job_timeout is None):
            raise unittest.SkipTest("Code timeout disabled.")

        user_id = 2 # Wizard ID
        d = transact.Parse.run(user_id=user_id, sentence='@exec while(True): pass')
        self.assertFailure(d, error.ProcessTerminated)
        return d
    
    def test_parser_rollback(self):
        created = False
        user_id = 2 # Wizard ID
        try:
            with exchange.ObjectExchange(connection) as x:
                caller = x.get_object(user_id)
                parser.parse(caller, '@exec create_object("Test Object")')
                if(x.get_object('Test Object')):
                    created = True
                parser.parse(caller, '@exec nosuchobject()')
        except:
            pass
        
        self.failUnless(created, "'Test Object' not created.")
        self.failUnlessRaises(errors.NoSuchObjectError, x.get_object, "Test Object")
    
    def test_protected_attribute_access(self):
        user_id = 2 # Wizard ID
        with exchange.ObjectExchange(connection) as x:
            wizard = x.get_object(user_id)
            self.assertEqual(wizard._location_id, wizard.get_location().get_id())
        
        with exchange.ObjectExchange(connection, ctx=user_id) as x:
            wizard = x.get_object(user_id)
            eval_verb = x.get_verb(user_id, '@eval')
            
            # since this will raise AttributeError, the model will attempt to find a verb by that name
            self.failUnlessRaises(SyntaxError, code.r_eval, wizard, 'caller._owner_id')
            self.failUnlessRaises(SyntaxError, code.r_eval, wizard, 'caller._origin_id')
            self.failUnlessRaises(SyntaxError, code.r_eval, wizard, 'caller.__dict__')
            self.failUnlessRaises(SyntaxError, code.r_eval, wizard, 'caller.__slots__')
            
            self.failUnlessRaises(errors.NoSuchVerbError, code.r_eval, wizard, 'getattr(caller, "_owner_id")')
            self.failUnlessRaises(errors.NoSuchVerbError, code.r_eval, wizard, 'getattr(caller, "_origin_id")')
            self.failUnlessRaises(errors.NoSuchVerbError, code.r_eval, wizard, 'getattr(caller, "__dict__")')
            self.failUnlessRaises(errors.NoSuchVerbError, code.r_eval, wizard, 'getattr(caller, "__slots__")')

# -*- coding: utf-8 -*-
import os
import time
import unittest
from configparser import ConfigParser

from ukaraozContigFilter.ukaraozContigFilterImpl import ukaraozContigFilter
from ukaraozContigFilter.ukaraozContigFilterServer import MethodContext
from ukaraozContigFilter.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class ukaraozContigFilterTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('ukaraozContigFilter'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'ukaraozContigFilter',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = ukaraozContigFilter(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_ContigFilter_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_run_ukaraozContigFilter_max(self):
        ref = "79/16/1"
        result = self.serviceImpl.run_ukaraozContigFilter_max(self.ctx, {
            'workspace_name': self.wsName,
            'assembly_ref': ref,
            'min_length': 100,
            'max_length': 1000000
        })
        #result = self.serviceImpl.run_{username}ContigFilter_max(self.ctx, params)
        self.assertEqual(result[0]['n_total'], 2)
        self.assertEqual(result[0]['n_remaining'], 1)
        #print(result)
        #self.assertTrue(len(result[0]['report_name']))
        #self.assertTrue(len(result[0]['report_ref']))
        # TODO -- assert some things (later)
        #self.assertTrue(len(result[0]['filtered_assembly_ref']))
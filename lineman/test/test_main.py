import unittest
import tempfile
import os

import lineman.__main__ as main
from lineman.version import __version__

class LineManBaseTest(unittest.TestCase):
    def setUp(self):
        conf_yaml = """
            template_version: test
            cappy_version: lineman.json
            event_assignment_strategy: chronological
            arm_order: [1]
            token: CDAB7D4C027F135CF12D72FF018BFE95
            redcap_url: http://hcvtargetrc.dev/redcap/api/
            subject_id: dm_subjid
            check_mappings:
                - key: dm_subjid
                - match_against: dm_usubjid
        """
        self.temp_conf_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_conf_file.write(conf_yaml)
        self.temp_conf_file.close()

    def tearDown(self):
        os.remove(self.temp_conf_file.name)

class TestHawkEyeInterop(LineManBaseTest):

    def test_log_has_proper__hawk_eye_keys(self):
        config = main.set_config(self.temp_conf_file.name)
        pre_proc = {
            'records': {
            'num_inputed': 0,
            'num_redcap': 0,
            'num_valid': 0,
            'num_invalid': 0,
            'validated': [],
            'not_validated': [],
            'mappings_done': {},
            },
            'subject_event_dict': {}
        }
        post_proc = {
            'source': 'lineman_test',
            'output': {
                'records': {
                    'num_inputed': 0,
                    'num_redcap': 0,
                    'num_valid': 0,
                    'num_invalid': 0,
                    'validated': [],
                    'not_validated': [],
                    'mappings_done': {},
                },
                'subject_event_dict': {}
            },
        }

        self.assertEqual(main.make_hawk_prey(pre_proc), post_proc)

if __name__ == '__main__':
    unittest.main()

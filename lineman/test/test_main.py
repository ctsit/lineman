import unittest

import lineman.__main__ as main
from lineman.version import __version__

class TestHawkEyeInterop(unittest.TestCase):

    def test_proper_keys(self):
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
            'source': 'lineman_%s' % __version__,
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

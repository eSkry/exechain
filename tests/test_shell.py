from exechain.shell import Shell, Print

import unittest



class TestShellTool(unittest.TestCase):
    def setUp(self) -> None:
        pass
    
    def test_bad_command(self):
        self.assertFalse(Shell("cd abdafsdasdfasdfre3gwq3gw4t")._invoke())

    def test_good_command(self):
        self.assertTrue(Shell("pwd")._invoke())


if __name__ == '__main__':
    unittest.main()
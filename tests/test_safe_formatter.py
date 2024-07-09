from exechain.internal import safe_format, SafeFormatter

import unittest


class TestSafeFormatter(unittest.TestCase):
    def setUp(self) -> None:
        pass
    
    def test_two_parameters(self):
        vars = {
            "a": 1,
            "b": "2",
        }
        
        target_string = f"{vars['a']}{vars['b']}{vars['a']}"
        input_string = "{a}{b}{a}"
        tested_string = safe_format(input_string, vars)
        self.assertEqual(target_string, tested_string)
        
    def test_vars_more(self):
        vars = {
            "a": 1,
            "b": "2",
            "c": 4
        }
        
        target_string = f"{vars['b']}{vars['a']}"
        input_string = "{b}{a}"
        tested_string = safe_format(input_string, vars)
        self.assertEqual(target_string, tested_string)
        
    def test_vars_less(self):
        vars = {
            "a": 1,
        }
        
        target_string = f"{{b}}{vars['a']}"
        input_string = "{b}{a}"
        tested_string = safe_format(input_string, vars)
        self.assertEqual(target_string, tested_string)


    
if __name__ == '__main__':
    unittest.main()
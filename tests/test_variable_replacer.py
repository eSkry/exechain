from exechain.exechain_system import exchain_replace_variables

import unittest


class TestVariableReplacer(unittest.TestCase):
    def setUp(self) -> None:
        pass
    
    
    def test_two_parameters(self):
        vars = {
            "a": "1",
            "b": "2",
        }
        
        target_string = "12"
        input_string = "{a}{b}"
        tested_string = exchain_replace_variables(input_string, vars)
        self.assertEqual(target_string, tested_string)
        
    
    def test_one_parameter(self):
        vars= {
           "name": "Jon Doe",
        }
       
        target_string = "Jon Doe"
        input_string = "{name}"
        tested_string = exchain_replace_variables(input_string, vars)
        self.assertEqual(target_string, tested_string)
       
    
    def test_no_parameters(self):
        vars = {}
        
        target_string = "Тесты делать иногда полезно..."
        input_string = target_string
        tested_string = exchain_replace_variables(input_string, target_string)
        self.assertEqual(target_string, tested_string)
    
    
    def test_numbers_as_value(self):
        vars = {
            "a": 1,
            "b": 2,
        }
        
        target_string = "12"
        input_string = "{a}{b}"
        tested_string = exchain_replace_variables(input_string, vars)
        self.assertEqual(target_string, tested_string)
        
    
if __name__ == '__main__':
    unittest.main()
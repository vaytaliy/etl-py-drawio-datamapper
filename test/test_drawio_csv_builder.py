import unittest
from src.utils.drawio_csv_builder import create_target_lineage, gen_lineage_string
from src.utils import constants

lineage_string : str = [ 
    ['complex_attr', constants.RECORD], 
    ['nested_1_attr', 'string'],
    ['nested_1_attr2', 'string'],
    ['nested_1_attr3', 'string'],
    [None, constants.RECORD_END],
    ['flat_attr_1', 'string'],
    ['flat_attr_2', 'string'],
    [constants.TRG_COL_NAME_VAL, constants.TRG_COL_DATATYPE_VAL]
]

class TestCreateTargetLineage(unittest.TestCase):
    
    def test_create_target_lineage_nested_first(self):
        create_target_lineage(lineage_string)
        self.assertEqual(lineage_string[1][2], 'complex_attr', f'Expected complex_attr, got {lineage_string[1][2]}')

    def test_create_target_lineage_nested_second(self):
        create_target_lineage(lineage_string)
        self.assertEqual(lineage_string[2][2], 'complex_attr', f'Expected complex_attr, got {lineage_string[2][2]}')
    
    def test_create_target_lineage_nested_third(self):
        create_target_lineage(lineage_string)
        self.assertEqual(lineage_string[3][2], 'complex_attr', f'Expected complex_attr, got {lineage_string[3][2]}')
    
    def test_create_target_lineage_flat(self):
        create_target_lineage(lineage_string)
        self.assertEqual(lineage_string[4][2], '', f'Expected complex_attr, got {lineage_string[4][2]}')

if __name__ == '__main__':
    unittest.main()
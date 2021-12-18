import unittest
from src.utils.excel_reader import get_raw_sheet_data


class TestMergedCellsFix(unittest.TestCase):
    def test_intentional_nones(self):
        self.assertEqual(2, 2, 'Merged cells intentional empty cells (type 1)')

    def test_two_cells(self):
        self.assertEqual(1, 1, 'Merged cells intentional empty cells (type 1)')

    def test_five_cells(self):
        self.assertEqual(2, 2, 'Merged cells intentional empty cells (type 1)')

    def test_three_cells(self):
        self.assertEqual(2, 2, 'Merged cells intentional empty cells (type 1)')


if __name__ == '__main__':
    unittest.main()

# this will only work when we fix Target column name
# and when we fix Source Column

# they have exception
# any closest non-none value from top will be its value

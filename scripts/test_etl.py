import unittest
from datetime import datetime
from etl import extract_data, transform_data

# TO EXECUTE (make sure to run in virutal environment):
# python -m unittest test_etl.py

class TestETL(unittest.TestCase):

    def test_extract_data(self): # checks behavior of extract_data function
        data = extract_data() # calls extract_data from ETL script & stores in data variable
        self.assertIsInstance(data, list) # checks if variable is a list, fails if not
        self.assertGreater(len(data), 0) # checks that data length > 0 (ie retrieved data)

    def test_transform_data(self): # checks behavior of transform_data function
        data = [(1, 1, 23.5, 60.2, datetime.now())] # defines mock dataset representing one row of sensor data, simulating what extract_data function might return
        transformed = transform_data(data) # calls transform_data function with mock dataset and stores result in the transformed variable
        self.assertEqual(len(transformed), 1) # checks that transformed list has exactly one item, confirming that transformation was applied to single input row
        self.assertIn("temperature_celsius", transformed[0]) # checks that transformed dictionary contains the key "temperature_celsius", verifying that transformation logic correctly renamed temperature field

if __name__ == "__main__":
    unittest.main()
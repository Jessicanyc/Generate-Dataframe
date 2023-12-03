import unittest
from unittest import patch
from generate_data.pyspark_dataframe import PySparkDataFrameFactory 
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType, ArrayType, DataType


class TestGenerateColumn(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSession.builder.master("local[1]").appName("TestGenerateColumn").getOrCreate()

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()

    def test_generate_string_column(self):
        # Test generate_column for StringType
        field_name = 'test_string'
        field_type = StringType
        num_rows = 10
        df = PySparkDataFrameFactory.generate_column(self.spark, field_name, field_type, 'random', None, [None, ' '], 0.2, num_rows)
        
        self.assertEqual(df.count(), num_rows)  # Check if the DataFrame has the correct number of rows
        self.assertTrue(field_name in df.columns)  # Check if the field_name is in the DataFrame columns
        # Additional assertions can be made on the content of the DataFrame

    def test_generate_integer_column_with_range(self):
        # Test generate_column for IntegerType with range
        field_name = 'test_integer'
        field_type = IntegerType
        specific_attr = [0, 100]
        num_rows = 10
        df = PySparkDataFrameFactory.generate_column(self.spark, field_name, field_type, 'range', specific_attr, [], 0.0, num_rows)
        
        self.assertEqual(df.count(), num_rows)
        self.assertIn(field_name, df.columns)

    def test_generate_float_column(self):
        field_name = 'test_float'
        field_type = FloatType
        num_rows = 10
        df = PySparkDataFrameFactory.generate_column(self.spark, field_name, field_type, 'fixed_length', None, [0.000025], 0.2, num_rows)       
        self.assertEqual(df.count(), num_rows)  # Check if the DataFrame has the correct number of rows

    def test_generate_array_float_column(self):
        field_name = 'test_array_float'
        field_type = ArrayType(FloatType())
        generation_type = 'list_of_floats'
        specific_attr = {'length': 3, 'fixed_length': 2}
        corner_cases = [[]]
        corner_case_probability = 0.15
        num_rows = 10

        df = PySparkDataFrameFactory.generate_column(self.spark, field_name, field_type, generation_type, specific_attr, corner_cases, corner_case_probability, num_rows)

        # Assertions
        self.assertEqual(df.count(), num_rows)
        self.assertIn(field_name, df.columns)

        # Additional check: Ensure each entry is a list of floats of the specified length
        for row in df.collect():
            if row[field_name] is not None:
                self.assertEqual(len(row[field_name]), specific_attr['length'])
                for value in row[field_name]:
                    self.assertIsInstance(value, float)

    def test_generate_array_string_column(self):
        field_name = 'test_array_string'
        field_type = ArrayType(StringType())
        generation_type = 'list_of_strings'
        specific_attr = {'length': 4, 'fixed_length': 3}
        corner_cases = [[], None]
        corner_case_probability = 0.2
        num_rows = 10

        df = PySparkDataFrameFactory.generate_column(self.spark, field_name, field_type, generation_type, specific_attr, corner_cases, corner_case_probability, num_rows)

        # Assertions
        self.assertEqual(df.count(), num_rows)
        self.assertIn(field_name, df.columns)

        # Ensure each entry is a list of strings of the specified length
        for row in df.collect():
            if isinstance(row[field_name], list):
                self.assertEqual(len(row[field_name]), specific_attr['length'])
                for value in row[field_name]:
                    self.assertIsInstance(value, str)

    def test_combine_dataframes(self):
        # Create mock DataFrames
        df1 = self.create_mock_dataframe([(1, 'A'), (2, 'B')], ['col1', 'col2'])
        df2 = self.create_mock_dataframe([(3, 100), (4, 200)], ['col3', 'col4'])

        # Combine DataFrames
        combined_df = PySparkDataFrameFactory.combine_dataframes(self.spark, [df1, df2])

        # Assertions
        self.assertEqual(combined_df.count(), 2)
        self.assertListEqual(sorted(combined_df.columns), sorted(['col1', 'col2', 'col3', 'col4']))

    @patch('generate_data.pyspark_dataframe.PySparkDataFrameFactory.combine_dataframes')
    @patch('generate_data.pyspark_dataframe.PySparkDataFrameFactory.c.generate_column')
    def test_create_pyspark_dataframe(self, mock_generate_column, mock_combine_dataframes):
        mock_schema_definition = [
            ('test_string', StringType(), 'random', None, [None, ' '], 0.2),
            ('test_integer', IntegerType(), 'range', [0, 99], [200], 0.2),
        ]
        num_rows = 4

        # Create mock return values for generate_column
        mock_df_string = self.spark.createDataFrame(
            [Row(test_string="A"), Row(test_string="B"), Row(test_string="C"), Row(test_string="D")],
            StructType([StructField("test_string", StringType(), True)])
        )
        mock_df_integer = self.spark.createDataFrame(
            [Row(test_integer=1), Row(test_integer=2), Row(test_integer=3), Row(test_integer=4)],
            StructType([StructField("test_integer", IntegerType(), True)])
        )
        mock_generate_column.side_effect = [mock_df_string, mock_df_integer]

        # Create mock return value for combine_dataframes
        mock_combined_df = self.spark.createDataFrame(
            [Row(test_string="A", test_integer=1), Row(test_string="B", test_integer=2),
             Row(test_string="C", test_integer=3), Row(test_string="D", test_integer=4)],
            StructType([StructField("test_string", StringType(), True), StructField("test_integer", IntegerType(), True)])
        )
        mock_combine_dataframes.return_value = mock_combined_df

        # Call the function to test
        result = PySparkDataFrameFactory.create_pyspark_dataframe(mock_schema_definition, num_rows)

        # Assert DataFrame properties
        self.assertEqual(result.count(), num_rows)
        self.assertListEqual(sorted(result.columns), sorted(['test_string', 'test_integer']))




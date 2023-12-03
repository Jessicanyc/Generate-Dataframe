from generate_data.factory import DataFrameFactory
from generate_data.utils.generate_helper import *
import pandas as pd
import uuid


class PandasDataFrameFactory(DataFrameFactory):


    # Generate Value Based on Type - Common logic for both
    def generate_value_based_on_type(self, field_type, generation_type, specific_attr):
        # Handle UUID generation
        if generation_type == 'uuid':
            return generate_uuid()

        elif field_type in ['StringType', 'ArrayType(StringType())']:
            length = 10  # Default length
            if specific_attr and isinstance(specific_attr, dict) and 'fixed_length' in specific_attr:
                length = specific_attr['fixed_length']
            return generate_random_string(length)
        elif field_type == 'IntegerType':
            min_val, max_val = specific_attr.get('range', (0, 100))
            return random.randint(min_val, max_val)
        elif field_type == 'FloatType':
            precision = specific_attr or 2
            return round(random.uniform(0, 100), precision)
        elif field_type == 'ArrayType(FloatType())':
            length = specific_attr.get('length', 3)
            fixed_length = specific_attr.get('fixed_length', 2)
            return [round(random.uniform(0, 100), fixed_length) for _ in range(length)]
        # Add other types as needed
        return None

    # Determine if corner case should be applied 
    def apply_corner_case(self, corner_cases, corner_case_probability):
        if corner_cases and random.random() < corner_case_probability:
            return random.choice(corner_cases)
        return None

    def generate_column_data(self, field_name, field_type, generation_type, specific_attr, corner_cases, corner_case_probability, num_rows):
        series_data = []
        for _ in range(num_rows):
            value = self.apply_corner_case(corner_cases, corner_case_probability)
            if value is None:
                value = self.generate_value_based_on_type(field_type, generation_type,specific_attr)
            series_data.append(value)
        return pd.Series(series_data, name=field_name)

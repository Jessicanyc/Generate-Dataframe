from generate_data.factory import DataFrameFactory
from generate_data.utils.generate_helper import *
import pandas as pd


class PandasDataFrameFactory(DataFrameFactory):
    def create_pandas_dataframe(self, schema_definition, num_rows):
        
        columns = [self.generate_column_data(*field, num_rows) for field in schema_definition]
        pd_df = pd.concat(columns, axis=1)
        return pd_df

    def generate_column_data(self, field_name, field_type, generation_type, specific_attr, corner_cases, corner_case_probability, num_rows):
        series_data = []
        for _ in range(num_rows):
            if corner_cases and random.random() < corner_case_probability:
                value = random.choice(corner_cases)
            else:
                if field_type == 'StringType':
                    length = 10  # Default length
                    if specific_attr is not None and 'fixed_length' in specific_attr:
                        length = specific_attr['fixed_length']
                    value = generate_random_string(length) if generation_type == 'random' else ''
                elif field_type == 'IntegerType':
                    min_val, max_val = specific_attr if specific_attr else (0, 100)
                    value = random.randint(min_val, max_val)
                elif field_type == 'FloatType':
                    precision = specific_attr if specific_attr else 2
                    value = round(random.uniform(0, 100), precision)
                elif field_type == 'ArrayType(FloatType())':
                    length = specific_attr['length'] if specific_attr and 'length' in specific_attr else 3
                    fixed_length = specific_attr['fixed_length'] if specific_attr and 'fixed_length' in specific_attr else 2
                    value = [round(random.uniform(0, 100), fixed_length) for _ in range(length)]
                elif field_type == 'ArrayType(StringType())':
                    length = specific_attr['length'] if specific_attr and 'length' in specific_attr else 4
                    fixed_length = specific_attr['fixed_length'] if specific_attr and 'fixed_length' in specific_attr else 3
                    value = [generate_random_string(fixed_length) for _ in range(length)]
                else:
                    value = None
            series_data.append(value)

        return pd.Series(series_data, name=field_name)

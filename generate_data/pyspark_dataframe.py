from generate_data.dataframe_factory import DataFrameFactory
from generate_data.utils.generate_helper import *
from pyspark.sql.types import *
import random

class PySparkDataFrameFactory(DataFrameFactory):

    def create_pyspark_dataframe(self, schema_definition, num_rows):
        # Implement logic to create a PySpark DataFrame
        spark = SparkSession.builder.appName("ColumnWiseDataFrameGenerator").getOrCreate()

        column_dfs = []
        for field in schema_definition:
            column_df = self.generate_column(spark, *field, num_rows)
            column_dfs.append(column_df)

        combined_df = self.combine_dataframes(spark, column_dfs)
        return combined_df


    def generate_column(self, spark, field_name, field_type, generation_type, specific_attr, corner_cases, corner_case_probability, num_rows):
        data = []
        corner_case_indices = set()

        if corner_case_probability > 0:
            # Ensure at least one corner case
            corner_case_indices.add(random.randint(0, num_rows - 1))

            # Add more corner cases based on probability
            additional_cases = int(corner_case_probability * num_rows) - 1
            while len(corner_case_indices) < additional_cases + 1:
                corner_case_indices.add(random.randint(0, num_rows - 1))
        for i in range(num_rows):
            if i in corner_case_indices:
                if not corner_cases:
                    continue
                value = random.choice(corner_cases)
            else:
                if field_type in [StringType, IntegerType, FloatType, BooleanType]:
                    value = generate_value_for_field(field_type, generation_type, specific_attr)
                elif isinstance(field_type, ArrayType):
                    length = specific_attr.get('length', 3)
                    fixed_length = specific_attr.get('fixed_length', 2)
                    value = generate_array_value(field_type.elementType, length, fixed_length)
                else:
                    value = None  # Default case for unsupported field types

            data.append(Row(**{field_name: value}))

        # Define explicit schema for the column
        if isinstance(field_type, DataType):
            column_schema = StructType([StructField(field_name, field_type, True)])
        else:
            column_schema = StructType([StructField(field_name, field_type(), True)])
            
        return spark.createDataFrame(data, column_schema)
    
    def combine_dataframes(self, dfs):
        # Add a unique ID column to each DataFrame
        dfs_with_id = [df.withColumn("id", monotonically_increasing_id()) for df in dfs]
        
        # Initialize the combined DataFrame with the first DataFrame in the list
        combined_df = dfs_with_id[0]

        # Join the remaining DataFrames using the unique ID column
        for df in dfs_with_id[1:]:
            combined_df = combined_df.join(df, "id", "outer")

        # Drop the ID column after joining
        combined_df = combined_df.drop("id")

        return combined_df

    
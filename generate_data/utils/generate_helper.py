from pyspark.sql import SparkSession, Row
from pyspark.sql.types import StringType, IntegerType, FloatType
from pyspark.sql.functions import monotonically_increasing_id
import random
import uuid

def generate_random_string(length=10):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))

def generate_uuid():
    return str(uuid.uuid4())

def generate_array_value(element_type, length, fixed_length):
    if element_type == StringType():
        strl = [generate_random_string(fixed_length) for _ in range(length)]
        return strl#[generate_random_string(fixed_length) for _ in range(length)]
    elif element_type == IntegerType():
        return [random.randint(0, 100) for _ in range(length)]
    elif element_type == FloatType():
        return [round(random.uniform(0, 100), fixed_length) for _ in range(length)]
    else:
        return [None for _ in range(length)]  # Default case for unsupported element types

def generate_value_for_field(field_type, generation_type, specific_attr):
    # Generate data based on field type and generation type
    if field_type == StringType:
        return generate_random_string()
    elif field_type == IntegerType:
        if generation_type == "range":
            min_val, max_val = specific_attr
            return random.randint(min_val, max_val)
        else:
            return random.randint(0, 100)
    elif field_type == FloatType:
        return round(random.uniform(0, 100), specific_attr if generation_type == "fixed_length" else 2)
    else:
        return None  # Default case for unsupported field types
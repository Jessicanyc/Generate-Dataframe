import pandas as pd
import random


def generate_random_string(length=10):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))

def generate_string(specific_attr, generation_type):
    length = specific_attr.get('fixed_length', 10) if specific_attr else 10
    return generate_random_string(length) if generation_type == 'random' else ''

def generate_integer(specific_attr,_):
    min_val, max_val = specific_attr if specific_attr else (0, 100)
    return random.randint(min_val, max_val)

def generate_float(specific_attr,_):
    precision = specific_attr if specific_attr else 2
    return round(random.uniform(0, 100), precision)

def generate_array_float(specific_attr, _):
    length = specific_attr.get('length', 3)
    fixed_length = specific_attr.get('fixed_length', 2)
    return [round(random.uniform(0, 100), fixed_length) for _ in range(length)]

def generate_array_string(specific_attr, _):
    length = specific_attr.get('length', 4)
    fixed_length = specific_attr.get('fixed_length', 3)
    return [generate_random_string(fixed_length) for _ in range(length)]

# Mapping of field types to generation functions
generation_functions = {
    'StringType': generate_string,
    'IntegerType': generate_integer,
    'FloatType': generate_float,
    'ArrayType(FloatType())': generate_array_float,
    'ArrayType(StringType())': generate_array_string
}

def generate_column_data(field_name, field_type, generation_type, specific_attr, corner_cases, corner_case_probability, num_rows):
    series_data = []
    for _ in range(num_rows):
        if corner_cases and random.random() < corner_case_probability:
            value = random.choice(corner_cases)
        else:
            generate_func = generation_functions.get(field_type)
            if generate_func:
                value = generate_func(specific_attr, generation_type)
            else:
                value = None
        series_data.append(value)

    return pd.Series(series_data, name=field_name)
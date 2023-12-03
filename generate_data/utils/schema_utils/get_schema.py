import yaml
from pyspark.sql.types import ArrayType

config_file = 'config.yaml' # Replace with your file name


def get_pyspark_type(type_str, element_type_str=None):
    if type_str == "ArrayType":
        element_type = get_pyspark_type(element_type_str)
        return ArrayType(element_type)
    else:
        # Retrieve the PySpark data type class from the globals and instantiate it
        return globals()[type_str]()

def parse_yaml_to_schema(yaml_file):
    with open(yaml_file, 'r') as file:
        schema_data = yaml.safe_load(file)

    schema_definition = []
    for field in schema_data['fields']:
        field_name = field['name']
        field_type_str = field['type']
        element_type_str = field.get('element_type')
        field_type = get_pyspark_type(field_type_str, element_type_str)
        generation = field['generation']
        corner_cases = field.get('corner_cases', [])
        corner_case_probability = field.get('corner_case_probability', 0)

        specific_attr = None
        if 'value_range' in field:
            specific_attr = field['value_range']
        elif 'fixed_length' in field:
            specific_attr = field['fixed_length']
        elif 'list_details' in field:
            specific_attr = field['list_details']

        schema_definition.append((field_name, field_type, generation, specific_attr, corner_cases, corner_case_probability))

    return schema_definition


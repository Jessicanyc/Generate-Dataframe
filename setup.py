from setuptools import setup, find_packages
from os import path

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='generate_dataframe', 
    version='0.1.0',  
    packages=find_packages(),
    description='An intuitive interface designed for generating dataframes with customizable random values, suitable for testing and development in data processing and machine learning environments.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Tiange Huang',  
    author_email='tiangehuangds@gmail.com', 
    url='https://github.com/Jessicanyc/Generate-Dataframe', 
    install_requires=requirements,
    python_requires='>=3.8',  
)
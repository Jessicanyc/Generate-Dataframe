from abc import ABC, abstractmethod
import random

class DataFrameFactory(ABC):
    
    @abstractmethod
    def create_dataframe(self, schema_definition, num_rows):
        pass

    def generate_random_string(length=10):
        return ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(length))
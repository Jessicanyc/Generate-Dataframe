from abc import ABC, abstractmethod

class DataFrameFactory(ABC):
    
    @abstractmethod
    def create_dataframe(self, schema_definition, num_rows):
        pass
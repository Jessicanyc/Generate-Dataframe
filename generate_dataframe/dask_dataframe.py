from generate_dataframe.dataframe_factory import DataFrameFactory
from generate_dataframe.pandas_dataframe import PandasDataFrameFactory as PDFF
import dask.dataframe as dd


class DaskDataFrameFactory(DataFrameFactory):
    def create_dataframe(self, schema_definition, num_rows):
        # Implement logic to create a Dask DataFrame
        pd_df = PDFF.create_pandas_dataframe(schema_definition, num_rows)
        dask_df = dd.from_pandas(pd_df, npartitions=2) 
        return dask_df



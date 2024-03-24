import inspect
import math
from typing import Union
from typing import Any, List, Union
from itertools import compress

import pandas as pd
import dask.dataframe as dd
import psycopg2
import sqlalchemy

from config.log_config import LOGGER
from config.config import Config


class UtilsDB:
    def __init__(self) -> None:
        self.engine = Config.get_info()['db_engine']
        self.dbsession = sqlalchemy.sessionmaker(bind=self.engine)

    def create_specific_model(
        self, class_name: str, model_name: str, schema_name: str, column_data: dict
    ) -> Any:
        """Create specific model inside specific schema.

        Args:
            class_name (str): Name of the class. Must be camel case - e.g.: 'AAPLDaily'.
            model_name (str): Name of the model. Must be snake case - e.g.: 'aapl_daily'.
            schema_name (str): Name of the schema where the model will be hosted.
            column_data (dict): Dictionary containing information on model columns: name, type, if primary key.
                                It must be of the type {'col1': Column(type, ...),
                                                        'col2': Column(type, ...),
                                                        'col3': Column(type, ...),
                                                         ...}

        Returns:
            object: Returns model class.
        """
        # Define the attributes for the class
        model_class = create_dynamic_model(
            class_name, model_name, schema_name, column_data
        )
        table_name = model_class.__tablename__
        schema_name = model_class.__table_args__["schema"]
        insp = sqlalchemy.inspect(self.engine)
        if not insp.has_table(table_name=table_name, schema=schema_name):
            model_class.__table__.create(self.engine)
            LOGGER.info(
                f"Model '{model_name}' created successfully in schema '{schema_name}'."
            )
        return model_class

    def create_new_models(self) -> None:
        """Create all models found in database.models module, in case one of them is missing."""
        model_list = self.__get_all_classes("database.models")
        insp = sqlalchemy.inspect(self.engine)
        for cls in model_list:
            table_name = cls.__tablename__
            schema_name = cls.__table_args__["schema"]
            if not insp.has_table(table_name=table_name, schema=schema_name):
                cls.__table__.create(self.engine)
                LOGGER.info(
                    f"Model '{table_name}' created successfully in schema '{schema_name}'."
                )

    @staticmethod
    def __get_all_classes(model_name: str) -> List[Any]:
        """Get a list with all models defined in the _model_name_ module."""
        all_items = inspect.getmembers(models)
        classes = [
            item[1]
            for item in all_items
            if inspect.isclass(item[1]) and item[1].__module__ == model_name
        ]
        return classes

    def get_model_class_with_name(self, table_name: str) -> object:
        model_list = self.__get_all_classes("database.models")
        for cls in model_list:
            if cls.__tablename__ == table_name:
                objective_cls = cls
        return objective_cls

    def insert_dict_in_db(
        self, data_dict: dict, model: object, batch_size: int = 10_000
    ) -> None:
        """Insert the input dataframe in the corresponding model in DB.

        Args:
            data_dict (dict): Input dictionary of which its information will be stored in the DB.
            model (object): Model class with table characteristics.
            batch_size (int, optional): Maximum rows to be inserted into the DB per iteration. Defaults to 100_000.
        """
        # Remove duplicates
        data_dict = self.remove_duplicate_ids(data_dict)
        list_of_dicts = [dict(zip(data_dict, t)) for t in zip(*data_dict.values())]
        batched_list_of_dicts = self._divide_dict_in_batches(list_of_dicts, batch_size)
        is_data_batched = len(batched_list_of_dicts) > 1
        LOGGER.info(f"Starting data storage in DB for table '{model.__tablename__}'.")
        for idx, dict_batch in enumerate(batched_list_of_dicts):
            try:
                self.dbsession.bulk_insert_mappings(model, dict_batch)
                # Commit the changes to the database for each model
                self.dbsession.commit()
                if is_data_batched:
                    LOGGER.info(
                    f"Batch number {idx + 1} of table '{model.__tablename__}' has been successfully stored in DB."
                    )
                else:
                    LOGGER.info(
                        f"Table '{model.__tablename__}' has been successfully stored in DB."
                    )
            except sqlalchemy.exc.IntegrityError as e:
                LOGGER.warning(
                    f"Duplicated primary key entries. Skipping. Error log: \n {e}"
                )
            except Exception as e:
                LOGGER.error(
                    f"An error occurred when inserting data into database: {e}."
                )
        # Close connection
        self.dbsession.close()

    def remove_duplicate_ids(self, data_dict: dict) -> dict:
        # First, check if all values in the dictionary are of the same length
        len_keys = []
        for k, v in data_dict.items():
            len_key = len(v)
            len_keys.append(len_key)

        # Create an error log if size is not the same across elements in the list
        is_same = True
        for length in len_keys:
            if len_keys[0] != length:
                is_same = False
                break
        
        if is_same:
            LOGGER.info(f"All values in the keys of the dictionary are of the same size: {len_keys[0]}")
            # Create mask so that the dict only contains unique ID's
            mask_list = []
            for idx, identifier in enumerate(data_dict['id']):
                if identifier not in data_dict['id'][:idx]:
                    mask_list.append(True)
                else:
                    mask_list.append(False)

            # Add unique entries in dictionary
            for k, v in data_dict.items():
                data_dict[k] = list(compress(v, mask_list))
        else:
            LOGGER.error(f"Not all values in the keys of the dictionary are of the same size")
        return data_dict

    @staticmethod
    def _divide_dict_in_batches(input_dict: dict, batch_size: int) -> List[List[dict]]:
        """Divide dictionary in smaller pieces for speed improvement."""
        n_chunks = math.ceil(len(input_dict) / batch_size)
        batched_list_of_dicts = []
        starting_row, ending_row = 0, batch_size
        for n in range(n_chunks):
            chunked_dict_list = input_dict[starting_row: ending_row]
            batched_list_of_dicts.append(chunked_dict_list)
            starting_row += batch_size
            ending_row += batch_size
        return batched_list_of_dicts

    @staticmethod
    def get_table(schema: str, table_name: str, engine: str, as_df = False) -> dd.DataFrame:
        """Get dataframe out of a table in the database.

        Args:
            schema (str): Schema of the table.
            table_name (str): Table name.

        Returns:
            dd.DataFrame: Dask dataframe containing the info of the table.
        """
        # Do not forget to grant access to user
        # ALTER ROLE <user> WITH LOGIN;
        # GRANT SELECT ON ALL TABLES IN SCHEMA <schemaname> TO <user>;
        # GRANT USAGE ON SCHEMA <schemaname> TO  <user>;
        sql_text = f" * FROM {schema}.{table_name}" # The SELECT is added in the next line
        sql = sqlalchemy.sql.select(sqlalchemy.sql.text(sql_text))
        try:
            ddf = dd.read_sql(sql = sql, con = engine, index_col = 'id')
            if as_df:
                ddf = ddf.compute()
            message = None
        except UnicodeDecodeError:
            ddf = None
            message = 'Invalid credentials. Try again.'
        except sqlalchemy.exc.OperationalError:
            ddf = None
            message = 'Please, log in with your credentials.'
        except sqlalchemy.exc.ProgrammingError:
            ddf = None
            message = 'You have no rights to the database.'
        return ddf, message

    def filter_table(self, schema, table_name, engine, filtered_col: str, filtered_val: Union[str, List]) -> None:
        ddf = self.get_table(schema, table_name, engine)
        if isinstance(filtered_val, list):
            ddf = ddf.loc[ddf[filtered_col].isin(filtered_val)]
        else:
            ddf = ddf.loc[ddf[filtered_col] == filtered_val]
        return ddf

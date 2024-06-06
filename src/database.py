import os
from sqlalchemy import create_engine, Column, Float, Integer, MetaData, Table
import pandas as pd
from src.exceptions import DatabaseError

class BaseDatabase:
    def __init__(self, db_name):
        self.db_path = os.path.join('data', db_name)
        self.engine, self.metadata = self.create_db(self.db_path)
    
    def create_db(self, db_path):
        """
        Create a SQLite database.
        
        :param db_path: str, path to the database file
        :return: engine, metadata
        """
        try:
            db_dir = os.path.dirname(db_path)
            if not os.path.exists(db_dir):
                os.makedirs(db_dir)
                print(f"Directory {db_dir} created.")
            
            if os.path.exists(db_path):
                os.remove(db_path)
                print(f"Existing database at {db_path} removed.")
            
            engine = create_engine(f'sqlite:///{db_path}')
            metadata = MetaData()
            print(f"New database created at {db_path}.")
            return engine, metadata
        except Exception as e:
            print(f"Error creating database at {db_path}: {e}")
            raise DatabaseError(f"Error creating database at {db_path}: {e}") from e

    def create_table(self, table_name, columns):
        """
        Create a table in the database.
        
        :param table_name: str, name of the table
        :param columns: list of SQLAlchemy Column objects
        :return: table
        """
        try:
            table = Table(table_name, self.metadata, *columns)
            self.metadata.create_all(self.engine)
            print(f"Table '{table_name}' created in the database.")
            return table
        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            raise DatabaseError(f"Error creating table '{table_name}': {e}") from e

    def insert_data(self, table, data_frame):
        """
        Insert data from a DataFrame into a database table.
        
        :param table: SQLAlchemy table
        :param data_frame: DataFrame
        """
        try:
            conn = self.engine.connect()
            data_frame.to_sql(table.name, conn, if_exists='replace', index=False)
            print(f"Data inserted into table '{table.name}'.")
        except Exception as e:
            print(f"Error inserting data into table '{table.name}': {e}")
            raise DatabaseError(f"Error inserting data into table '{table.name}': {e}") from e

class TrainingDatabase(BaseDatabase):
    def create_and_populate_tables(self, train_data, test_data, ideal_data):
        """
        Create and populate tables in the SQLite database.
        
        :param train_data: DataFrame containing training data
        :param test_data: DataFrame containing test data
        :param ideal_data: DataFrame containing ideal functions data
        """
        # Create database and tables
        train_table = self.create_table('training_data', [
            Column('x', Float),
            Column('y1', Float),
            Column('y2', Float),
            Column('y3', Float),
            Column('y4', Float),
        ])
        
        ideal_table = self.create_table('ideal_functions', [
            Column('x', Float),
            *(Column(f'y{i}', Float) for i in range(1, 51))
        ])
        
        test_table = self.create_table('test_data', [
            Column('x', Float),
            Column('y', Float)
        ])
        
        result_table = self.create_table('results', [
            Column('x', Float),
            Column('y', Float),
            Column('delta_y', Float),
            Column('ideal_function', Integer)
        ])
        
        # Insert data into tables
        self.insert_data(train_table, train_data)
        self.insert_data(ideal_table, ideal_data)
        self.insert_data(test_table, test_data)
        print("Source data has been successfully inserted into the database.")

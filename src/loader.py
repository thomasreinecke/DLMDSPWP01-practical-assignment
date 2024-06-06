import pandas as pd
from src.exceptions import DataLoadingError

class BaseLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_csv(self):
        """
        Load a CSV file into a pandas DataFrame and sort by the x-column.
        
        :return: DataFrame
        """
        try:
            df = pd.read_csv(self.file_path)
            df = df.sort_values(by='x')
            print(f"Successfully loaded and sorted {self.file_path}")
            return df
        except FileNotFoundError as e:
            print(f"File not found: {self.file_path}")
            raise DataLoadingError(f"File not found: {self.file_path}") from e
        except pd.errors.EmptyDataError as e:
            print(f"No data: {self.file_path}")
            raise DataLoadingError(f"No data: {self.file_path}") from e
        except Exception as e:
            print(f"Error loading {self.file_path}: {e}")
            raise DataLoadingError(f"Error loading {self.file_path}: {e}") from e

class DataTrainingLoader(BaseLoader):
    def load(self):
        """
        Load the training data CSV file.
        
        :return: DataFrame
        """
        print("Loading training data...")
        return self.load_csv()

class DataTestLoader(BaseLoader):
    def load(self):
        """
        Load the test data CSV file.
        
        :return: DataFrame
        """
        print("Loading test data...")
        return self.load_csv()

class DataIdealLoader(BaseLoader):
    def load(self):
        """
        Load the ideal functions CSV file.
        
        :return: DataFrame
        """
        print("Loading ideal functions...")
        return self.load_csv()

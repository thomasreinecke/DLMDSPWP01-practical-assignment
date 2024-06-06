# src/exceptions.py

class DataLoadingError(Exception):
    """Exception raised for errors in the data loading process."""
    pass

class DatabaseError(Exception):
    """Exception raised for errors in the database operations."""
    pass

class ModelFittingError(Exception):
    """Exception raised for errors in the model fitting process."""
    pass

class EvaluationError(Exception):
    """Exception raised for errors in the evaluation process."""
    pass

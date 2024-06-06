import os
import pytest
from sqlalchemy import inspect
from src.database import TrainingDatabase
from src.exceptions import DatabaseError
from src.loader import DataTrainingLoader, DataTestLoader, DataIdealLoader

def test_create_and_populate_tables():
    train_loader = DataTrainingLoader(os.path.join('data', 'train.csv'))
    train_data = train_loader.load()

    test_loader = DataTestLoader(os.path.join('data', 'test.csv'))
    test_data = test_loader.load()

    ideal_loader = DataIdealLoader(os.path.join('data', 'ideal.csv'))
    ideal_functions = ideal_loader.load()

    db_path = 'data/test_database.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    training_db = TrainingDatabase('test_database.db')
    training_db.create_and_populate_tables(train_data, test_data, ideal_functions)

    engine = training_db.engine
    inspector = inspect(engine)

    assert 'training_data' in inspector.get_table_names()
    assert 'test_data' in inspector.get_table_names()
    assert 'ideal_functions' in inspector.get_table_names()
    assert 'results' in inspector.get_table_names()

    os.remove(db_path)

def test_database_error():
    with pytest.raises(DatabaseError):
        TrainingDatabase('/invalid/path/database.db')

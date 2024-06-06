import os
import pytest
from src.loader import DataTrainingLoader, DataTestLoader, DataIdealLoader
from src.exceptions import DataLoadingError

def test_load_training_data():
    loader = DataTrainingLoader(os.path.join('data', 'train.csv'))
    df = loader.load()
    assert not df.empty
    assert 'x' in df.columns
    assert 'y1' in df.columns
    assert df['x'].is_monotonic_increasing  # Ensure x values are sorted

def test_load_test_data():
    loader = DataTestLoader(os.path.join('data', 'test.csv'))
    df = loader.load()
    assert not df.empty
    assert 'x' in df.columns
    assert 'y' in df.columns
    assert df['x'].is_monotonic_increasing  # Ensure x values are sorted

def test_load_ideal_functions():
    loader = DataIdealLoader(os.path.join('data', 'ideal.csv'))
    df = loader.load()
    assert not df.empty
    assert 'x' in df.columns
    for i in range(1, 51):
        assert f'y{i}' in df.columns
    assert df['x'].is_monotonic_increasing  # Ensure x values are sorted

def test_load_nonexistent_file():
    loader = DataTrainingLoader('nonexistent.csv')
    with pytest.raises(DataLoadingError):
        loader.load()

import os
import pytest
import pandas as pd
from src.analyzer import least_squares_fit, evaluate_test_data
from src.loader import DataTrainingLoader, DataTestLoader, DataIdealLoader
from src.exceptions import ModelFittingError, EvaluationError

@pytest.fixture
def data_setup():
    train_loader = DataTrainingLoader(os.path.join('data', 'train.csv'))
    train_data = train_loader.load()

    test_loader = DataTestLoader(os.path.join('data', 'test.csv'))
    test_data = test_loader.load()

    ideal_loader = DataIdealLoader(os.path.join('data', 'ideal.csv'))
    ideal_functions = ideal_loader.load()

    return train_data, test_data, ideal_functions

def test_least_squares_fit(data_setup):
    train_data, _, ideal_functions = data_setup
    best_fit_indices = least_squares_fit(train_data, ideal_functions)
    assert len(best_fit_indices) == 4

def test_least_squares_fit_error():
    with pytest.raises(ModelFittingError):
        least_squares_fit(pd.DataFrame(), pd.DataFrame())

def test_evaluate_test_data(data_setup):
    train_data, test_data, ideal_functions = data_setup
    best_fit_indices = least_squares_fit(train_data, ideal_functions)
    results = evaluate_test_data(test_data, train_data, ideal_functions, best_fit_indices)
    # It is acceptable if the results are empty
    assert 'x' in results.columns
    assert 'y' in results.columns
    assert 'delta_y' in results.columns
    assert 'ideal_function' in results.columns

def test_evaluate_test_data_error(data_setup):
    _, test_data, ideal_functions = data_setup
    with pytest.raises(EvaluationError):
        evaluate_test_data(test_data, pd.DataFrame(), ideal_functions, [1, 2, 3, 4])

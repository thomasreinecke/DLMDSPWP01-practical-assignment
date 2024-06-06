# src/analyzer.py

import numpy as np
import pandas as pd
import os
from src.exceptions import ModelFittingError, EvaluationError

def least_squares_fit(train_data, ideal_functions):
    """
    Fit ideal functions to training data using Least Squares method.
    
    :param train_data: DataFrame containing training data
    :param ideal_functions: DataFrame containing ideal functions
    :return: list of indices of the best fitting ideal functions
    """
    try:
        y_train = train_data.drop(columns=['x']).values
        y_ideal = ideal_functions.drop(columns=['x']).values

        best_fit_indices = []
        
        # Calculate the least squares errors and find the best fitting ideal functions
        for y_train_column in y_train.T:
            errors = np.sum((y_ideal - y_train_column[:, np.newaxis])**2, axis=0)
            best_fit_index = np.argmin(errors)
            best_fit_indices.append(best_fit_index + 1)  # Adjust index to account for the 'x' column
        
        return best_fit_indices
    except Exception as e:
        print(f"Error in least squares fitting: {e}")
        raise ModelFittingError(f"Error in least squares fitting: {e}") from e



def evaluate_test_data(test_data, train_data, ideal_functions, best_fit_indices):
    """
    Evaluate test data against best fitting ideal functions and write the mapping results to CSV files.
    
    :param test_data: DataFrame containing test data
    :param train_data: DataFrame containing training data
    :param ideal_functions: DataFrame containing ideal functions
    :param best_fit_indices: list of indices of the best fitting ideal functions
    :return: DataFrame containing evaluation results
    """
    try:
        x_test = test_data['x'].values
        y_test = test_data['y'].values
        x_train = train_data['x'].values

        # Calculate the maximum deviation for each training function
        max_deviations = []
        for idx, index in enumerate(best_fit_indices):
            train_y = train_data.iloc[:, idx + 1].values
            ideal_y = ideal_functions.iloc[:, index].values
            max_deviation = np.max(np.abs(train_y - ideal_y))
            max_deviations.append(max_deviation)

        evaluation_results = []

        # Ensure results directory exists
        if not os.path.exists('results'):
            os.makedirs('results')

        # Write a CSV file for each test dataset mapping
        for idx, ideal_func_index in enumerate(best_fit_indices):
            test_column_name = f'test_y{idx + 1}'
            ideal_column_name = f'ideal_y{ideal_func_index}'  # No need to add 1 since the ideal_func_index is already adjusted
            ideal_func = ideal_functions[f'y{ideal_func_index}'].values

            mapping_df_data = []

            # Evaluate each test data point against the ideal functions
            for x, y in zip(x_test, y_test):
                ideal_y_at_x = np.interp(x, x_train, ideal_func)
                deviation = abs(ideal_y_at_x - y)
                
                # Check if the deviation is within the allowed range
                max_allowed_deviation = max_deviations[idx] * np.sqrt(2)
                maps = deviation <= max_allowed_deviation
                mapping_df_data.append((x, y, ideal_y_at_x, deviation if maps else None, maps))

            mapping_df = pd.DataFrame(mapping_df_data, columns=['x', test_column_name, ideal_column_name, 'deviation', 'maps'])
            mapping_df.to_csv(f'results/mapping-y{idx + 1}.csv', index=False)
            print(f"Mapping results with deviations written to results/mapping-y{idx + 1}.csv")

        return pd.DataFrame(evaluation_results, columns=['x', 'y', 'delta_y', 'ideal_function'])
    except Exception as e:
        print(f"Error in evaluating test data: {e}")
        raise EvaluationError(f"Error in evaluating test data: {e}") from e

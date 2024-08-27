import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import streamlit as st

def CMA():

    # Set file path to CMAs and load Excel file
    file_path = r"C:\Users\skosloff\Documents\Mean-Variance Analysis\BR MV Data 2.xlsx"
    retvol = pd.read_excel(file_path, sheet_name='RetVol')  
    corr = pd.read_excel(file_path, sheet_name='Corr')  

    # Format CMAs

    # Retvol
    retvol.drop(retvol.columns[[0, 1, 3]], axis=1, inplace=True) # Drop columns

    retvol.columns = retvol.iloc[1] # Set secpmd row as column headers
    retvol = retvol[2:]  

    # Corr
    corr.drop(corr.columns[[0,1]], axis=1, inplace=True) # Drop columns
    
    corr.columns = corr.iloc[1] # Set secpmd row as column headers
    corr = corr[2:] 

    corr.set_index('Asset', inplace=True) # Set index


    new_order = [ # Reorder corr to match retvol
        'U.S. cash', 
        'U.S. government bonds (all maturities)', 
        'U.S. large cap equities', 
        'Hedge funds (global)', 
        'U.S. credit (all maturities)', 
        'U.S. private equity (buyout)', 
        'U.S. small cap equities', 
        'Global infrastructure equity', 
        'Real estate mezzanine debt', 
        'U.S. core real estate'
    ] 

    corr = corr.reindex(index=new_order, columns=new_order) # Reindex


    # Compute covariance matrix

    expected_returns = retvol['Expected Return (10yr)'].values
    correlations = corr.values
    variances = retvol['Volatility'].values

    expected_returns = np.array(expected_returns, dtype=float) # Convert to float
    std_devs = np.sqrt(np.array(variances, dtype=float))
    correlations = np.array(correlations, dtype=float)

    cov_matrix = np.diag(std_devs) @ corr @ np.diag(std_devs)

    # Define the number of assets
    n_assets = len(expected_returns)

    return expected_returns, cov_matrix, n_assets, std_devs

# Optimize for returns



def returns(expected_returns, cov_matrix, n_assets):

    # Set volatility tolerance
    vol_tol = st.number_input("Enter a portfolio volatility tolerance", min_value=1.0, max_value=50.0, value=10.0, step=0.1) / 100

    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # Weights must sum to 1
        {'type': 'ineq', 'fun': lambda x: 0.10 - x[3]},  # HF allocation must be <= 10%
        {'type': 'ineq', 'fun': lambda x: vol_tol - np.sqrt(np.dot(x.T, np.dot(cov_matrix, x)))}  # Portfolio volatility <= X%
    ]

    # Initial guess
    x0 = np.ones(n_assets) / n_assets

    # Bounds on all weights
    bounds = [(0.01, 0.6) for _ in range(n_assets)]

    # Max iterations
    options = {
        'maxiter': 5000  # Set maximum number of iterations
    }

    # Objective function
    def objective(weights, expected_returns):
        return -np.dot(weights, expected_returns)  # Negative because we maximize

    # Minimize the objective function
    solution = minimize(objective, x0, args=(expected_returns,), method='SLSQP', bounds=bounds, constraints=constraints, tol=1e-6, options=options)

    # Extract optimized weights
    optimized_weights = np.array(solution.x)

    # Calculate the expected return and volatility of the optimized portfolio
    expected_portfolio_return = optimized_weights @ expected_returns
    expected_portfolio_volatility = np.sqrt(optimized_weights.T @ cov_matrix @ optimized_weights)

    return optimized_weights, expected_portfolio_return, expected_portfolio_volatility





# Sharpe Optimizationm

def sharpe(expected_returns, cov_matrix, n_assets):

    risk_free_rate = st.number_input("Enter a risk free rate", min_value=0.00, max_value=10.00, value=4.75, step=0.01) / 100
    
    
    # Objective function
    def objective(weights):
        portfolio_return = weights @ expected_returns
        portfolio_volatility = np.sqrt(weights.T @ cov_matrix @ weights)
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
        return -sharpe_ratio  # Negative Sharpe ratio for maximization

    # Initial guess
    x0 = np.ones(n_assets) / n_assets

    # Define the constraints dictionary
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},     # Weights must sum to 1
        {'type': 'ineq', 'fun': lambda x: 0.10 - x[3]},  # HF allocation must be <= 10%
        {'type': 'ineq', 'fun': lambda x: 0.20 - x[7]},  # "Global Infrastructure" allocation must be <= 40%
        {'type': 'ineq', 'fun': lambda x: 0.2 - np.sqrt(x.T @ cov_matrix @ x)}  # Portfolio volatility <= X%
    ]

    # Bounds on all weights
    bounds = [(0.01, 0.6) for _ in range(n_assets)]

    # Max iterations
    options = {
        'maxiter': 5000  # Set maximum number of iterations
    }

    # Solve the problem using SLSQP method
    solution = minimize(objective, x0, method='SLSQP', bounds=bounds, constraints=constraints, tol=1e-6, options=options)

    # Output the optimized weights
    optimized_weights = solution.x
    print("Optimized Portfolio Weights:", optimized_weights)

    # Calculate the expected return and volatility of the optimized portfolio
    expected_portfolio_return = optimized_weights @ expected_returns
    expected_portfolio_volatility = np.sqrt(optimized_weights.T @ cov_matrix @ optimized_weights)
    sharpe_ratio = (expected_portfolio_return - risk_free_rate) / expected_portfolio_volatility

    return optimized_weights, expected_portfolio_return, expected_portfolio_volatility, sharpe_ratio

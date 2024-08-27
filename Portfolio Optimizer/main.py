import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from app import returns, CMA, sharpe

def main():

    # Returns

    expected_returns, cov_matrix, n_assets = CMA() [0:3]
    std_devs = CMA() [3]

    # Allow users to edit expected returns via Streamlit
    row_labels = [
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
 
    expected_returns = np.round(expected_returns * 100, 2)
    expected_returns = pd.DataFrame(expected_returns, index=row_labels)
    expected_returns = st.data_editor(expected_returns, num_rows="dynamic")
    expected_returns = np.array(expected_returns.values.ravel(), dtype=float) / 100
    
   # Show standard deviations
    #st.data_editor(CMA() [3], num_rows="dynamic")

    # Call the returns function with the correct arguments
    optimized_weights, expected_portfolio_return, expected_portfolio_volatility  = returns(expected_returns, cov_matrix, n_assets)
   


    # Plot the optimized weights
    asset_names = ['Cash', 'Bonds', 'Large Cap Equities', 'Hedge Funds', 'Credit', 'Private Equity', 
                   'Small Cap Equities', 'Global Infrastructure', 'RE Credit', 'Real Estate']

    current_weights = np.array([0.4123, 0.1312, 0.2267, 0.0869, 0.0645, 0.0291, 0.0155, 0.0121, 0.013, 0.0191])

    x_values = np.arange(len(optimized_weights)) * 3

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    bars_curr = plt.bar(x_values - 0.4, current_weights, width=0.8, label='Current Weights', color='blue')
    bars_opt = plt.bar(x_values + 0.6, optimized_weights, width=0.8, label='Optimized Weights', color='orange')

    plt.title('Current vs Optimized Portfolio Weights (Returns)')
    plt.xlabel('Asset Class')
    plt.ylabel('Weight')
    plt.xticks(x_values, asset_names, rotation=45, ha='right')

    # Annotate bars
    for bar, weight in zip(bars_curr, current_weights):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{weight:.2%}', ha='center', va='bottom', fontsize=8)

    for bar, weight in zip(bars_opt, optimized_weights):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{weight:.2%}', ha='center', va='bottom', fontsize=8)

    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)
    

    st.write(f"Portfolio Expected Returns: {expected_portfolio_return:.2%}")
    st.write(f"Portfolio Expected Volatility: {expected_portfolio_volatility:.2%}")

  
    # Sharpe
    # Call the returns function with the correct arguments
    optimized_weights, expected_portfolio_return, expected_portfolio_volatility, sharpe_ratio = sharpe(expected_returns, cov_matrix, n_assets)

    # Plot the optimized weights
    asset_names = ['Cash', 'Bonds', 'Large Cap Equities', 'Hedge Funds', 'Credit', 'Private Equity', 
                   'Small Cap Equities', 'Global Infrastructure', 'RE Credit', 'Real Estate']

    current_weights = np.array([0.4123, 0.1312, 0.2267, 0.0869, 0.0645, 0.0291, 0.0155, 0.0121, 0.013, 0.0191])

    x_values = np.arange(len(optimized_weights)) * 3

    # Plot the bar chart
    plt.figure(figsize=(12, 6))
    bars_curr = plt.bar(x_values - 0.4, current_weights, width=0.8, label='Current Weights', color='blue')
    bars_opt = plt.bar(x_values + 0.6, optimized_weights, width=0.8, label='Optimized Weights', color='orange')

    plt.title('Current vs Optimized Portfolio Weights (Sharpe)')
    plt.xlabel('Asset Class')
    plt.ylabel('Weight')
    plt.xticks(x_values, asset_names, rotation=45, ha='right')

    # Annotate bars
    for bar, weight in zip(bars_curr, current_weights):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{weight:.2%}', ha='center', va='bottom', fontsize=8)

    for bar, weight in zip(bars_opt, optimized_weights):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval, f'{weight:.2%}', ha='center', va='bottom', fontsize=8)

    plt.legend()
    plt.tight_layout()
    st.pyplot(plt)

    st.write(f"Portfolio Expected Returns: {expected_portfolio_return:.2%}")
    st.write(f"Portfolio Expected Volatility: {expected_portfolio_volatility:.2%}")
    st.write(f"Portfolio Sharpe Ratio: {sharpe_ratio:.2%}")


if __name__ == "__main__":
    main()

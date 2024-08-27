# Portfolio Optimization Project

## Overview

This project is a Streamlit-based web application that performs portfolio optimization with two objective functions: (1) maximizing returns keeping volatility under a specified threshold and (2) maximizing Sharpe ratio. It allows users to input various parameters and see how different asset allocations perform in terms of portfolio expected returns and portfolio expected volatility.

## Features

- Optimize portfolio weights for maximum returns given a volatility constraint
- Optimize portfolio weights for maximum Sharpe ratio
- Visualize current vs. optimized portfolio weights
- Allow users to edit expected returns for different asset classes
- Compare performance metrics of optimized portfolios

## Installation

To run this project, you'll need Python installed on your system. Follow these steps to set up the project:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies:

```
pip install numpy pandas matplotlib scipy streamlit openpyxl
```
4. Place the CMA file in the correct directory and modify the filepath of the code to reflect this

## Usage

To run the application:

1. Navigate to the project directory in your terminal.
2. Run the following command:

```
streamlit run main.py
```

3. The application will open in your default web browser.

## Input Parameters

- **Expected returns**: The initial expected returns come from the CMA file. Users can edit the expected returns for each asset class.
- **Portfolio volatility tolerance**: For the returns optimization strategy (1-50%).
- **Risk-free rate**: For the Sharpe ratio optimization strategy (0-10%).

## Outputs

1. **Current vs. Optimized Portfolio Weights**: A bar chart comparing the current asset allocation with the optimized allocation
2. Performance metrics for each optimization strategy:
   - Portfolio Expected Returns
   - Portfolio Expected Volatility
   - Portfolio Sharpe Ratio (for Sharpe optimization only)

## How It Works

The project uses two main optimization strategies:

1. **Maximize Returns**: This strategy aims to maximize the portfolio's expected return while keeping the portfolio volatility below a specified threshold.

2. **Maximize Sharpe Ratio**: This strategy aims to find the portfolio allocation that maximizes the Sharpe ratio, which is a measure of risk-adjusted returns.

Both strategies use quadratic programming to solve the optimization problem, subject to various constraints such as:
- The sum of weights must equal 1
- Specific asset class allocations are capped (e.g., hedge funds <= 10%)
- Minimum and maximum weights for each asset class

All optimization is done using ```scipy.optimize.minimize``` which is a method within the SciPy library for minimizing (or maximizing) objective functions subject to constraints.

## Mathematical Model

The portfolio optimization is based on the following mathematical models:

1. **Expected Portfolio Return**:

   $$\mu_V = \sum_{i=1}^n w_i \mu_i$$

   Where
   - $\mu_V$ is the expected portfolio return
   - $w_i$ is the weight of asset $i$
   - $\mu_i$ is the expected return of asset $i$

      Alternatively, as an inner product:

   $$\mu_V = \vec{w}\vec{\mu}^T$$

   Where
   - $\vec{w}$ is a vector of the portfolio weights and
   - $\vec{\mu}$ is a vector of the expected returns of the various assets in the portfolio

2. **Portfolio Volatility**:

   $$\sigma_V = \sqrt{\sum_{i=1}^n \sum_{j=1}^n w_i w_j \sigma_i \sigma_j \rho_{ij}}$$

   Where
   - $\sigma_V$ is the portfolio volatility
   - $\sigma_i$ is the standard deviation of asset $i$
   - $\rho_{ij}$ is the correlation between assets $i$ and $j$

   Alternatively, as an inner product:

$$\sigma_V = \vec{w}^T C \vec{w}$$

Where
- C is the covariance matrix: $C = D\Sigma D$ where $D$ is a diagonal matrix of the variances and $\Sigma$ is the correlation matrix.

3. **Sharpe Ratio**:

   $$S = \frac{\mu_V - R_f}{\sigma_p}$$

   Where:
   - $S$ is the Sharpe ratio
   - $R_f$ is the risk-free rate

## Files

- `main.py`: The main Streamlit application that handles user input and visualization.
- `app.py`: Contains the core optimization logic and data processing functions.

## Key Functions

1. `CMA()`: Loads and processes the Capital Market Assumptions (CMAs) from an Excel file.
2. `returns(expected_returns, cov_matrix, n_assets)`: Optimizes the portfolio for maximum returns given a volatility constraint.
3. `sharpe(expected_returns, cov_matrix, n_assets)`: Optimizes the portfolio for maximum Sharpe ratio.

## Limitations and Considerations

- The optimization assumes that the Capital Market Assumptions (expected returns, volatilities, and correlations) are accurate.
- The mathematical model assumes returns are normally distributed (they are not) which poses problems for mean-variance optimization in general

## Future Improvements

- Allow users to input volatilites of the assets
- Allow users to add and change constraints easily
- Improve the front-end
- Add sensitivity analysis to show how changes in assumptions affect the optimal portfolio
- Create ability to stress-test the portfolio under market drawdowns
- Create more visualization of correlations (e.g. with a heatmap)
- Create visualization of efficient frontier and comparison of multiple portfolios
- Incorporate Monte Carlo simulation in order to more accurately model expected returns and volatilities
- Add a method which optimizes for minimum volatility portfolio keeping returns above a threshold


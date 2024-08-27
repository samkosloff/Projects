# Portfolio Simulation Project

## Overview

This project is a Streamlit-based web application that simulates the trajectory of a financial portfolio over time. It allows users to input various parameters and visualize how a portfolio might perform under different conditions, including returns, volatility, distributions, and contributions.

## Features

- Simulate portfolio performance over a specified number of years
- Adjust parameters such as starting balance, annual returns, volatility, distributions, and contributions
- Visualize portfolio trajectory with mean and percentile ranges
- View percentile breakdowns for end balances and total distributions

## Installation

To run this project, you'll need Python installed on your system. Follow these steps to set up the project:

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies:

```
pip install numpy pandas matplotlib seaborn streamlit
```

## Usage

To run the application:

1. Navigate to the project directory in your terminal.
2. Run the following command:

```
streamlit run main.py
```

3. The application will open in your default web browser.

## Input Parameters

- **Years to simulate**: The number of years to run the simulation (1-100 years).
- **Year to begin more aggressive giving**: The year when more aggressive distributions start.
- **Amount to increase giving**: The percentage increase in distributions after the specified year.
- **Starting balance**: The initial portfolio balance in billions of dollars.
- **Average yearly return**: The expected annual return as a percentage.
- **Yearly return volatility**: The standard deviation of annual returns as a percentage.
- **Average percentage given away each year**: The expected annual distribution as a percentage.
- **Standard deviation for amount given away**: The variability in annual distributions.
- **Average amount contributed each year**: The expected annual contribution in hundreds of millions of dollars.
- **Standard deviation on contributed amount**: The variability in annual contributions.

## Outputs

1. **Trajectory of Portfolio**: A graph showing the simulated portfolio balance over time, including:
   - Individual simulation runs (light gray lines)
   - Mean balance (blue line)
   - 5th-95th percentile range (blue shaded area)

2. **Percentile Breakdowns**: Two bar charts showing:
   - End Balance Percentiles (25th, 50th, and 90th)
   - Total Distribution Percentiles (25th, 50th, and 90th)

## How It Works (mathematical model)

The portfolio simulation is based on the following mathematical model:

1. **Portfolio Balance**: The balance $B_y$ at year $y$ is calculated as:

   $$B_y = B_{y-1} + (B_{y-1} R_y) - D_y (B_{y-1} + B_{y-1} R_y) + C_y$$

   Where:
   - $B_{y-1}$ is the balance from the previous year
   - $R_y$ is the return in year $y$
   - $D_y$ is the distribution in year $y$
   - $C_y$ is the contribution in year $y$

   The idea here is to iteratively update the balance of the portfolio given some starting amount $B_0$, growing it by the returns and shrinking it by some amount given away.

2. **Returns**: Annual returns are modeled using a normal distribution:

   $$R_y \sim \mathcal{N}(\mu_R, \sigma_R^2)$$

   Where $\mu_R$ is the average annual return and $\sigma_R$ is the annual volatility.

3. **Distributions**: Annual distributions are also modeled using a normal distribution:

   $$D_y \sim \mathcal{N}(\mu_D , \sigma_D^2)$$

   Where $\mu_D$ is the average distribution rate and $\sigma_D$ is the standard deviation of the distribution rate.

4. **Contributions**: Annual contributions are modeled as:

   $$C_y \sim \mathcal{N}(\mu_C, \sigma_C^2)$$

   Where $\mu_C$ is the average annual contribution and $\sigma_C$ is the standard deviation of contributions. This is specified in dollars whereas the other means and variances are done in percentages. 

5. **Aggressive Giving**: After the specified year for more aggressive giving, the distribution model changes to:

   $$D_y \sim \mathcal{N}((\mu_D + \delta), \sigma_D^2)$$

   Where $\delta$ is the increase in the distribution rate.


## Files

- `main.py`: The main Streamlit application that handles user input and visualization.
- `app.py`: Contains the core simulation logic.

## Limitations and Considerations

- This simulation is a simplified model and does not account for all real-world factors that might affect a portfolio.
- The results are based on random sampling and should not be considered as financial advice.
- The model assumes normally distributed returns, distributions, and contributions, which may not always reflect real-world patterns.

## Future Improvements

- Add functionality to simulate recession conditions
- Add more sophisticated investment return models
- Implement different distribution strategies e.g. spread the periods of aggressive giving over multiple periods so there aren't years with such high distribution requirements



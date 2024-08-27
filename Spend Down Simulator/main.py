import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import streamlit as st
from app import simulate

def main():

    itr = 50000 # Number of iterations
    
    # Collect user data
    yrs = st.number_input("Enter number of Years to simulate", min_value=1, max_value=100, step=1) # Duration of simulation
    boost_yr = st.number_input("Enter year in which more aggressive giving begins", min_value=1, max_value=yrs, step=1) # Year to give more aggresively
    boost_amt = st.number_input("Enter amount to increase giving by (percent shift in mean)", min_value=0.00, max_value=80.00, step=0.01) / 100 # Amount by which to give more aggresively
    # Starting balance
    start_bal = st.number_input("Enter a starting balance (billions of dollars) ", min_value=0.0, max_value=100.0, step=0.1 ) * 1e+9

    # Simulation parameters
    ann_ret = st.number_input("Enter an average yearly return ", min_value=0.0, max_value=25.0, step=0.1) / 100
    ann_vol = st.number_input("Enter a yearly return volatility ", min_value=0.0, max_value=25.0, step=0.1) / 100

    ann_dist = st.number_input("Enter an average percentage to be given away each year ", min_value=0.0, max_value = 25.0, step=0.1) / 100
    dist_std_dev = st.number_input("Enter a standard deviation for the amount given away ", min_value=0.0, max_value = 25.0, step=0.1) / 100

    ann_contr = st.number_input("Enter an average amount to be contributed to the portfolio each year (dollar amount - hundreds of millions) ", min_value=0, max_value = 1000, step=100) * 1e+6
    contr_std_dev = st.number_input("Enter a standard deviation on the dollar amount contributed each year (dollar amount - hundreds of millions ", min_value=0, max_value = 500, step=100) * 1e+6

    # Run Simulation
    bal_df, dist_tab_df = simulate(itr, yrs, start_bal, boost_yr, boost_amt, ann_ret, ann_vol, ann_dist, dist_std_dev, ann_contr, contr_std_dev)

   
   
    # Plotting

    # Plot graph of trajectory

    st.markdown(f"## Trajectory of Portfolio Over {yrs} Years")

    plt.figure(figsize=(12, 6))  # Increased figure size for better readability

    # Plot a sample of the simulations
    sample_size = 500  # Number of simulations to plot
    sample_indices = np.random.choice(itr, sample_size, replace=False)
    for i in sample_indices:
        plt.plot(bal_df.columns, bal_df.iloc[i], color='lightgray', alpha=0.5, linewidth=0.5)

    # Plot mean and percentiles
    mean_balance = bal_df.mean(axis=0)
    percentile_5th = bal_df.quantile(0.05, axis=0)
    percentile_95th = bal_df.quantile(0.95, axis=0)

    plt.plot(bal_df.columns, mean_balance, color='blue', linewidth=2, label='Mean Balance')
    plt.fill_between(bal_df.columns, percentile_5th, percentile_95th, color='blue', alpha=0.2, label='5th-95th Percentile')

    # Adding labels, title, and grid
    plt.xlabel('Years', fontsize=12)
    plt.ylabel('Balance ($)', fontsize=12)
    plt.title(f'Simulation of Portfolio Balance over {yrs} Years', fontsize=14)
    plt.grid(True)
    plt.legend()
    scale = 10**(int(np.floor(np.log10(bal_df.mean(axis=0).iloc[-1]))) - 1)
    plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x / scale :.0f}B')) # Puts tick marks on y-axis in tens of billions

    # Display the plot in Streamlit
    st.pyplot(plt)



    # Plot the percentile breakdowns

    st.markdown("## Percentile Breakdowns")

    # Calculate percentiles for end balances
    percentiles = [25, 50, 90]
    percentile_values_end_balance = np.percentile(bal_df.iloc[:, -1], percentiles)

    # Convert values to billions of dollars
    percentile_values_end_balance_billion = percentile_values_end_balance / 1e9

    # Calculate percentiles for total distributions
    percentile_values_distributions = np.percentile(dist_tab_df['Sum'], percentiles)

    # Convert values to billions of dollars
    percentile_values_distributions_billion = percentile_values_distributions / 1e9

    # Plotting the percentiles as a bar chart for end balances and total distributions
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(16, 6))

    # End Balances plot
    bars1 = ax1.bar([str(p) for p in percentiles], percentile_values_end_balance_billion, color='skyblue')
    ax1.set_xlabel('Percentiles')
    ax1.set_ylabel('Percentile Values (Billions $)')
    ax1.set_title('Terminal Portfolio Values for 25th, 50th, and 90th Percentiles')
    ax1.grid(True)

    # Annotate each bar with the value in billions for end balances
    for bar, value in zip(bars1, percentile_values_end_balance_billion):
        yval = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, yval, f'{value:.2f}B', ha='center', va='bottom')

    # Total Distributions plot
    bars2 = ax2.bar([str(p) for p in percentiles], percentile_values_distributions_billion, color='skyblue')
    ax2.set_xlabel('Percentiles')
    ax2.set_ylabel('Percentile Values (Billions $)')
    ax2.set_title('Total Capital Distribution for 25th, 50th, and 90th Percentiles')
    ax2.grid(True)

    # Annotate each bar with the value in billions for total distributions
    for bar, value in zip(bars2, percentile_values_distributions_billion):
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2, yval, f'{value:.2f}B', ha='center', va='bottom')

    # Adjust layout
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)




if __name__ == "__main__":
    main()
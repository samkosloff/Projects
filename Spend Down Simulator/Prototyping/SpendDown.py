import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns


# Number of iterations and years
itr = 50000
yrs = int(input("Enter a number of years to simulate "))

# Distribution parameters
print("Enter all values as percentages (e.g. 10 percent is entered as 10)")
print()
ann_ret = float(input("Enter an average yearly return ")) / 100
ann_vol = float(input("Enter a yearly return volatility ")) / 100

ann_dist = float(input("Enter an average percentage to be given away each year ")) / 100
dist_std_dev = float(input("Enter a standard deviation for the amount given away ")) / 100

ann_contr = float(input("Enter an average amount to be contributed to the portfolio each year (dollar amount - hundreds of millions) ")) * 1e+6
contr_std_dev = float(input("Enter a standard deviation on the dollar amount contributed each year (dollar amount - hundreds of millions) ")) * 1e+6

# Populate returns, distributions, contributions amounts
returns = np.random.normal(loc=ann_ret, scale=ann_vol, size=(itr, yrs))
dist = np.random.normal(loc=ann_dist, scale=dist_std_dev, size=(itr, yrs))
contr = np.random.normal(loc=ann_contr, scale=contr_std_dev, size=(itr, yrs))



# Initialize balance matrix
bal = np.zeros((itr, yrs))
bal[:, 0] = float(input("Enter a starting balance (billions of dollars) ")) * 1e+9

# Initialize distribution tab matrix
dist_tab = np.zeros((itr, yrs))

# Simulate Y years
for y in range(1, yrs):
    prev_bal = bal[:, y-1]
    
    if y <= 15:
        # First 25 years
        bal[:, y] = prev_bal + (prev_bal * returns[:, y]) - dist[:, y] * (prev_bal + prev_bal * returns[:, y]) + contr[:, y]
    else:
        # Last 25 years
        bal[:, y] = prev_bal + (prev_bal * returns[:, y]) - (dist[:, y] + 0.3) * (prev_bal + prev_bal * returns[:, y]) + contr[:, y] # Shifting distribution of amt given away up
    
    # Calculate distributions
    dist_tab[:, y] = prev_bal * dist[:, y]

# Convert balance and dist_tab to DataFrames if needed for further processing
bal_df = pd.DataFrame(bal)
dist_tab_df = pd.DataFrame(dist_tab)

# Record sum of all distributions given
dist_tab_df['Sum'] = dist_tab_df.sum(axis=1)




# Plotting
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
plt.title('Simulation of Portfolio Balance over 50 Years', fontsize=14)
plt.grid(True)
plt.legend()

# Display the plot
plt.show()



# Calculate and print percentiles for end balances
percentiles = [25, 50, 90]
percentile_values_end_balance = np.percentile(bal_df.iloc[:, -1], percentiles)

# Convert values to billions of dollars
percentile_values_end_balance_billion = percentile_values_end_balance / 1e9

# Calculate and print percentiles for total distributions
percentile_values_distributions = np.percentile(dist_tab_df['Sum'], percentiles)

# Convert values to billions of dollars
percentile_values_distributions_billion = percentile_values_distributions / 1e9

# Plotting the percentiles as a bar chart for end balances and total distributions
fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(16, 6))

# End Balances plot
bars1 = ax1.bar([str(p) for p in percentiles], percentile_values_end_balance_billion, color='skyblue')
ax1.set_xlabel('Percentiles')
ax1.set_ylabel('Percentile Values')
ax1.set_title('End Balance Percentiles for 25th, 50th, and 90th Percentiles')
ax1.grid(True)

# Annotate each bar with the value in billions for end balances
for bar, value in zip(bars1, percentile_values_end_balance_billion):
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, yval, f'{value:.2f}B', ha='center', va='bottom')

# Total Distributions plot
bars2 = ax2.bar([str(p) for p in percentiles], percentile_values_distributions_billion, color='skyblue')
ax2.set_xlabel('Percentiles')
ax2.set_ylabel('Percentile Values')
ax2.set_title('Total Distribution Percentiles for 25th, 50th, and 90th Percentiles')
ax2.grid(True)

# Annotate each bar with the value in billions for total distributions
for bar, value in zip(bars2, percentile_values_distributions_billion):
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width() / 2, yval, f'{value:.2f}B', ha='center', va='bottom')

# Show the plot
plt.tight_layout()
plt.show()
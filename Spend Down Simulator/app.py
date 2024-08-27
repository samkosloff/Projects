import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import streamlit as st


# Simulation

def simulate(itr, yrs, start_bal, boost_yr, boost_amt, ann_ret, ann_vol, ann_dist, dist_std_dev, ann_contr, contr_std_dev):
    
    # Populate returns, distributions, contributions amounts with samples from normal distribution
    returns = np.random.normal(loc=ann_ret, scale=ann_vol, size=(itr, yrs))
    dist = np.random.normal(loc=ann_dist, scale=dist_std_dev, size=(itr, yrs))
    contr = np.random.normal(loc=ann_contr, scale=contr_std_dev, size=(itr, yrs))

    # Initialize balance matrix
    bal = np.zeros((itr, yrs))
    bal[:, 0] = start_bal

    # Initialize distribution tab matrix
    dist_tab = np.zeros((itr, yrs))

    # Simulate Y years
    for y in range(1, yrs):
        prev_bal = bal[:, y-1]
        
        if y <= boost_yr:
            # First X years
            bal[:, y] = prev_bal + (prev_bal * returns[:, y]) - dist[:, y] * (prev_bal + prev_bal * returns[:, y]) + contr[:, y]
        else:
            # Last Y years
            dist[:, y] = dist[:, y] + boost_amt
            bal[:, y] = prev_bal + (prev_bal * returns[:, y]) - dist[:, y] * (prev_bal + prev_bal * returns[:, y]) + contr[:, y] # Shifting distribution of amt given away up
        
        # Calculate distributions
        dist_tab[:, y] = prev_bal * dist[:, y]

    # Convert bal and dist_tab to Dataframes
    bal_df = pd.DataFrame(bal)
    dist_tab_df = pd.DataFrame(dist_tab)

    # Record sum of all distributions given
    dist_tab_df['Sum'] = dist_tab_df.sum(axis=1)

    return bal_df, dist_tab_df
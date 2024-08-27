import pandas as pd
import numpy as np
import xlwings as xw
from datetime import datetime, timedelta

def connect_excel():
    # Define the path to your Excel file
    excel_file_path = r"C:\Users\skosloff\OneDrive - MSD Partners (Legacy)\OptionsTool.xlsx"

    workbook = xw.Book(excel_file_path)

    # Select the specific sheet
    sheet1 = workbook.sheets["Sheet1"]
    sheet2 = workbook.sheets["Sheet2"]

    return(sheet1, sheet2)

# Calculates payoff at expiry of %OTM call given some % move in the underlying
# Note that moves in the underlying and %OTM are input as positive numbers
def OTMcall_T(S_0, move_und, OTM, prem):
    E = S_0 * (1 + OTM) # Strike as %OTM of S_0
    S_T = S_0 * (1 + move_und) # Underlying price at expiry as % move in spot price
    return max(0, (S_T - E) / prem)


# Calculates payoff at expiry of %OTM call given some % move in the underlying
# Note that moves in the underlying and %OTM are input as positive numbers
def OTMput_T(S_0, move_und, OTM, prem):
    E = S_0 * (1 - OTM) # Strike as %OTM of S_0
    S_T = S_0 * (1 - move_und) # Underlying price at expiry as % move in spot price
    return max(0, (E - S_T) / prem)

def put_spread_T(S_0, move_und, X, Y, prem_spread):
    # Converting into %OTM amounts
    X = (100 - float(X)) / 100 
    Y = (100 - float(Y)) / 100
    
    strike_buy = S_0 * (1 - X) # Strike price of X% OTM put
    S_T = S_0 * (1 - move_und) # Price of underlying at expiry after % move
    
    return max(0, (strike_buy - S_T) / prem_spread)

# Define a function which finds the option with the closest strike price to x
def closest_strike(x, chain):
    # Extract strike prices from the option strings and convert to float
    strike_prices = [float(item[0].split()[3][1:]) for item in chain]
    
    # Find the index of the strike price with the minimum absolute difference from x
    closest_index = min(range(len(strike_prices)), key=lambda i: abs(x - strike_prices[i]))
    
    return closest_index

def populate_chains(sheet1, sheet2):
    # Define variable with ticker from Excel
    ticker = sheet1.range('B4').value
    
    # Get term and date
    term = int(sheet1.range('D4').value.split(" ")[0])
    date = (datetime.now() + timedelta(days=term)).strftime('%Y-%m-%d')
    
    # Populate Excel sheet with call option ask prices
    sheet2.range('B2').value = f'=@BQL("filter(filter(options(\'{ticker}\'), EXPIRE_DT=={date}), put_call==\'Call\')","SECURITY_DES().value, PX_ASK().value, EXPIRE_DT().value","mode=cached")'
    
    # Populate Excel sheet with put option prices
    sheet2.range('J2').value = f'=@BQL("filter(filter(options(\'{ticker}\'), EXPIRE_DT=={date}), put_call==\'Put\')","SECURITY_DES().value, PX_ASK().value, EXPIRE_DT().value","mode=cached")'


def populate_premia(sheet1, sheet2):
    # Load option chain from Excel sheet
    call_chain = sheet2.range('C3:D200').value
    call_chain = [sublist for sublist in call_chain if None not in sublist]
    
    # Given spot price
    S_0 = float(sheet1.range('C4').value)
    
    # Define table column and row headers
    percent_moves = np.array([float(value) for value in sheet1.range('I7:L7').value])
    percent_OTMs = np.array([float(value) for value in sheet1.range('H8:H12').value])
    OTMs = (S_0 * (1 + percent_OTMs)).astype(int) # Array of strike prices in dollars
    
    # Get premia from Excel via Bloomberg
    call_prems = [f"{call_chain[closest_strike(strike, call_chain)][1]:.2f}" for strike in OTMs]
    call_prems = [float(prem) for prem in call_prems]
    
    put_chain = sheet2.range('K3:L200').value
    put_chain = [sublist for sublist in put_chain if None not in sublist]
    
    put_prems = [f"{put_chain[closest_strike(strike, put_chain)][1]:.2f}" for strike in OTMs]
    put_prems = [float(prem) for prem in put_prems]

    # Calculate spread premia
    spread_pairs = sheet1.range('H29:H33').value
    spread_prems = []
    for pair in spread_pairs:
        X, Y = map(float, pair.split('-'))
        X_OTM = (100 - X) / 100
        Y_OTM = (100 - Y) / 100
        prem_X = float(f"{put_chain[closest_strike(S_0 * (1 - X_OTM), put_chain)][1]:.2f}")
        prem_Y = float(f"{put_chain[closest_strike(S_0 * (1 - Y_OTM), put_chain)][1]:.2f}")
        spread_prems.append(prem_X - prem_Y)
    
    # Put premia in Excel
    sheet1.range('G8').value = np.array(call_prems).reshape(-1, 1)
    sheet1.range('G19').value = np.array(put_prems).reshape(-1, 1)
    sheet1.range('G29').value = np.array(spread_prems).reshape(-1, 1)


def populate_call_table(sheet1):
    # Given spot price
    S_0 = float(sheet1.range('C4').value)
    
    # Create empty dataframe with moves in underlying as columns
    percent_moves = np.array([float(value) for value in sheet1.range('I7:L7').value])
    percent_OTMs = np.array([float(value) for value in sheet1.range('H8:H12').value])
    OTMcall_table = pd.DataFrame(index=percent_OTMs, columns=percent_moves)
    
    # Update the dataframe with the new titles for columns and rows
    OTMcall_table.columns.name = 'Moves in Underlying'
    OTMcall_table.index.name = '% OTM'
    
    # Get premia from Excel
    call_prems = [float(prem) for prem in sheet1.range('G8:G12').value]
    
    for i in OTMcall_table.index:
        for j in OTMcall_table.columns:
            OTMcall_table.at[i, j] = OTMcall_T(S_0, j, i, call_prems[np.where(OTMcall_table.index == i)[0][0]])
    
    # Load call table into Excel sheet
    sheet1.range('I8:L12').value = OTMcall_table.values
    
    # Update dollar amount moves in underlying in Excel sheet
    sheet1.range('I6:L6').value = float(sheet1.range('C4').value) * ( 1 + percent_moves)


def populate_put_table(sheet1):
    # Given spot price
    S_0 = float(sheet1.range('C4').value)
    
    # Create empty dataframe with moves in underlying as columns
    percent_OTMs = np.array([float(value) for value in sheet1.range('H19:H23').value])
    percent_moves = np.array([float(value) for value in sheet1.range('I18:L18').value])
    
    OTMput_table = pd.DataFrame(index=percent_OTMs, columns=percent_moves)
    
    # Update the dataframe with the new titles for columns and rows
    OTMput_table.columns.name = 'Moves in Underlying'
    OTMput_table.index.name = '% OTM'
    
    # Get premia from Excel
    put_prems = [float(prem) for prem in sheet1.range('G19:G23').value]
    
    for i in OTMput_table.index:
        for j in OTMput_table.columns:
            OTMput_table.at[i, j] = OTMput_T(S_0, j, i, put_prems[np.where(OTMput_table.index == i)[0][0]])
    
    # Load call table into Excel sheet
    sheet1.range('I19:L23').value = OTMput_table.values
    
    # Update dollar amount moves in underlying in Excel sheet
    sheet1.range('I17:L17').value = float(sheet1.range('C4').value) * ( 1 - percent_moves)


def populate_spread_table(sheet1):
    # Given spot price
    S_0 = float(sheet1.range('C4').value)
    
    # Create empty dataframe with moves in underlying as columns
    XY = sheet1.range('H29:H33').value
    percent_moves = np.array([float(value) for value in sheet1.range('I18:L18').value])
    
    spread_table = pd.DataFrame(index=XY, columns=percent_moves)
    
    # Get spread premia from Excel
    spread_prems = [float(prem) for prem in sheet1.range('G29:G33').value]
    
    for i, pair in enumerate(spread_table.index):
        X, Y = pair.split('-')
        for j in spread_table.columns:
            spread_table.at[pair, j] = put_spread_T(S_0, j, X, Y, spread_prems[i])
        
    # Load spread table into Excel sheet
    sheet1.range('I29:L33').value = spread_table.values

    # Update dollar amount moves in underlying in Excel sheet
    sheet1.range('I27:L27').value = float(sheet1.range('C4').value) * (1 - percent_moves)



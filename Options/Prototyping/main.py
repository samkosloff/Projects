from app import *

def main():
    # Connect to Excel
    sheet1, sheet2 = connect_excel()

    # Populate option chains
    populate_chains(sheet1, sheet2)

    # Populate option premia
    populate_premia(sheet1, sheet2)

    # Populate tables
    populate_call_table(sheet1)
    populate_put_table(sheet1)
    populate_spread_table(sheet1)

if __name__ == "__main__":
    main()
def money_made(num_shares, purchase_share_price, current_share_price):
    """
    num_shares is the number of shares of a stock that we purchased.
    purchase_share_price is the price of each of those shares.
    current_share_price is the current share price.
    Return the amount of money we have earned on the stock.
    """
    return num_shares * (current_share_price - purchase_share_price)

if __name__ == '__main__':
    
    # Test the function
    print(money_made(10, 5, 10))  # 50
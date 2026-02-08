"""
Stock Volatility Classifier
Uses Alpha Vantage API to fetch stock data and classify volatility
"""

import os
import sys
import requests


def get_stock_data(symbol):
    """
    Fetch stock data from Alpha Vantage API
    
    Args:
        symbol: Stock ticker symbol (e.g., 'AAPL')
    
    Returns:
        dict: JSON response from API
    """
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    
    if not api_key:
        print("Error: ALPHA_VANTAGE_API_KEY environment variable not set")
        print("Please set it using: export ALPHA_VANTAGE_API_KEY='your_api_key'")
        sys.exit(1)
    
    # Alpha Vantage API endpoint for daily time series
    url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': api_key,
        'outputsize': 'compact'  # Returns latest 100 data points
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        sys.exit(1)


def calculate_percentage_change(price1, price2):
    """
    Calculate percentage change between two prices
    
    Args:
        price1: Earlier price (float)
        price2: Later price (float)
    
    Returns:
        float: Percentage change
    """
    return ((price2 - price1) / price1) * 100


def classify_volatility(percentage_change):
    """
    Classify stock volatility based on percentage change
    
    Args:
        percentage_change: Daily percentage change (float)
    
    Returns:
        str: Volatility classification
    """
    abs_change = abs(percentage_change)
    
    if abs_change < 1:
        return "Stable"
    elif abs_change <= 3:
        return "Moderate"
    else:
        return "Volatile"


def generate_summary(avg_abs_change, most_volatile_change, volatility_level):
    """
    Generate a plain-English summary of stock volatility
    
    Args:
        avg_abs_change: Average absolute percentage change (float)
        most_volatile_change: Largest percentage change (float)
        volatility_level: Overall volatility classification (str)
    
    Returns:
        str: Summary sentence
    """
    direction = "gains" if most_volatile_change > 0 else "losses"
    
    if volatility_level == "Stable":
        return f"This stock has been relatively stable over the past 5 trading days, with an average daily movement of {avg_abs_change:.2f}% and minimal price swings."
    elif volatility_level == "Moderate":
        return f"This stock has shown moderate volatility, averaging {avg_abs_change:.2f}% daily movement with the largest single-day change being {abs(most_volatile_change):.2f}% in {direction}."
    else:
        return f"This stock has been highly volatile, with an average daily movement of {avg_abs_change:.2f}% and a significant single-day swing of {abs(most_volatile_change):.2f}% in {direction}."


def main():
    """Main function to run the stock volatility classifier"""
    
    # Get stock symbol from user
    symbol = input("Enter stock symbol (e.g., AAPL, TSLA): ").upper().strip()
    
    if not symbol:
        print("Error: Stock symbol cannot be empty")
        sys.exit(1)
    
    print(f"\nFetching data for {symbol}...")
    
    # Fetch stock data
    data = get_stock_data(symbol)
    
    # Check for API errors
    if 'Error Message' in data:
        print(f"Error: {data['Error Message']}")
        sys.exit(1)
    
    if 'Note' in data:
        print(f"API Limit: {data['Note']}")
        sys.exit(1)
    
    # Extract time series data
    time_series_key = 'Time Series (Daily)'
    if time_series_key not in data:
        print("Error: Unexpected API response format")
        print("Response:", data)
        sys.exit(1)
    
    time_series = data[time_series_key]
    
    # Get the 5 most recent trading days (need 6 to calculate 5 changes)
    dates = sorted(time_series.keys(), reverse=True)
    
    if len(dates) < 6:
        print("Error: Not enough data (need at least 6 days)")
        sys.exit(1)
    
    # Get last 6 days to calculate 5 daily changes
    last_6_dates = dates[:6]
    
    # Calculate daily changes and store data
    daily_data = []
    percentage_changes = []
    
    for i in range(5):
        current_date = last_6_dates[i]
        previous_date = last_6_dates[i + 1]
        
        current_close = float(time_series[current_date]['4. close'])
        previous_close = float(time_series[previous_date]['4. close'])
        
        pct_change = calculate_percentage_change(previous_close, current_close)
        percentage_changes.append(pct_change)
        
        daily_data.append({
            'date': current_date,
            'close': current_close,
            'change': pct_change
        })
    
    # Calculate average absolute daily percentage change
    avg_abs_change = sum(abs(change) for change in percentage_changes) / len(percentage_changes)
    
    # Find most volatile day
    most_volatile_idx = max(range(len(percentage_changes)), key=lambda i: abs(percentage_changes[i]))
    most_volatile_day = daily_data[most_volatile_idx]
    
    # Get most recent data
    most_recent = daily_data[0]
    
    # Classify overall volatility based on average
    overall_volatility = classify_volatility(avg_abs_change)
    
    # Display results
    print("\n" + "="*80)
    print("STOCK VOLATILITY ANALYSIS")
    print("="*80)
    print(f"Stock Symbol: {symbol}")
    print(f"Analysis Period: {daily_data[-1]['date']} to {daily_data[0]['date']}")
    print(f"\nCurrent Price: ${most_recent['close']:.2f}")
    print(f"Average Absolute Daily Change: {avg_abs_change:.2f}%")
    print(f"Overall Volatility Level: {overall_volatility}")
    print("\n" + "-"*80)
    print("5-DAY TRADING HISTORY")
    print("-"*80)
    print(f"{'Date':<12} {'Closing Price':>15} {'Daily Change':>15} {'Status':>15}")
    print("-"*80)
    
    for day in daily_data:
        change_str = f"{day['change']:+.2f}%"
        volatility_status = classify_volatility(day['change'])
        
        # Highlight most volatile day
        if day['date'] == most_volatile_day['date']:
            volatility_status += " *"
        
        print(f"{day['date']:<12} ${day['close']:>14.2f} {change_str:>15} {volatility_status:>15}")
    
    print("-"*80)
    print(f"\nMost Volatile Day: {most_volatile_day['date']} ({most_volatile_day['change']:+.2f}%)")
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(generate_summary(avg_abs_change, most_volatile_day['change'], overall_volatility))
    print("="*80)


if __name__ == "__main__":
    main()

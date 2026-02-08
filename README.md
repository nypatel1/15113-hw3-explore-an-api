This assignment uses the Alpha Vantage API to fetch real-time stock market data. The API is accessed using Python's requests library to make GET requests to the Alpha Vantage endpoint. Key parameters passed to the API include the function, the stock symbol (AAPL, TSLA, etc.), and the api key for authentication. The API returns data in JSON format, containing a time series object with dates as keys and daily OHLC (Open, High, Low, Close) prices plus volume as nested dictionaries. The script extracts the closing prices from this JSON response and performs calculations to determine volatility metrics.

Obtaining an Alpha Vantage API Key:
1. Visit https://www.alphavantage.co/support/#api-key
2. Sign up for a free API key
3. Set the API key as an environment variable

This project was developed with Claude Sonnet 4.5 


Initial Prompt: "I want to build a Stock Volatility Classifier that uses a public stock market API to fetch recent stock price data for a user-specified symbol, calculates the daily percentage change, and classifies the stock's volatility level. I want to use Alpha Vantage as the stock api."

Feature Enhancement Prompt: "Add these features: Fetch closing prices for the last 5 trading days instead of only the most recent day. Calculate the daily percentage changes and the average absolute daily percentage change. Identify and print the most volatile day (largest % change). Display a simple console table showing the date, closing price, daily % change, and add a short plain-English summary sentence describing the stock's recent volatility."

These prompts guided the core functionality and user experience design of the application.

Additional prompts were used to better understand how using the API worked.

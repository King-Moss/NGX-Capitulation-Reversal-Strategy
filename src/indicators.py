import pandas as pd

def compute_indicators(df):
    df = df.copy()
    df["Return_5D"]   = df["Close"].pct_change(periods=5)
    df["Avg_Vol_20D"] = df["Volume"].rolling(window=20).mean()
    df["MA_50"]       = df["Close"].rolling(window=50).mean()
    return df

def compute_all_indicators(all_stocks):
    return {ticker: compute_indicators(df) for ticker, df in all_stocks.items()}

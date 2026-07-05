def generate_signals(df, return_threshold=-0.10, volume_multiplier=1.5):
    df = df.copy()
    cond1 = df["Return_5D"] <= return_threshold
    cond2 = df["Volume"]    >= volume_multiplier * df["Avg_Vol_20D"]
    df["Signal"] = (cond1 & cond2).astype(int)
    return df

def generate_all_signals(all_stocks, return_threshold=-0.10, volume_multiplier=1.5):
    return {ticker: generate_signals(df, return_threshold, volume_multiplier)
            for ticker, df in all_stocks.items()}

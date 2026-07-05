import pandas as pd
import os

def parse_price(val):
    if pd.isna(val):
        return None
    try:
        return float(str(val).replace(",", "").strip())
    except:
        return None

def parse_volume(vol_str):
    if pd.isna(vol_str) or vol_str == "-":
        return None
    vol_str = str(vol_str).strip().replace(",", "")
    if "B" in vol_str:
        return float(vol_str.replace("B", "")) * 1_000_000_000
    elif "M" in vol_str:
        return float(vol_str.replace("M", "")) * 1_000_000
    elif "K" in vol_str:
        return float(vol_str.replace("K", "")) * 1_000
    else:
        try:
            return float(vol_str)
        except:
            return None

def load_stock(filepath):
    df = pd.read_csv(filepath)
    df = df.rename(columns={"Price": "Close", "Change %": "Change_Pct", "Vol.": "Volume"})
    df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y")
    for col in ["Close", "Open", "High", "Low"]:
        df[col] = df[col].apply(parse_price)
    df["Volume"] = df["Volume"].apply(parse_volume)
    df["Change_Pct"] = df["Change_Pct"].str.replace("%", "").str.strip().astype(float)
    df = df.sort_values("Date").reset_index(drop=True)
    df = df.drop_duplicates(subset="Date")
    ticker = os.path.basename(filepath).replace(" Stock Price History.csv", "").strip()
    df["Ticker"] = ticker
    return df

def load_all_stocks(folder_path):
    all_stocks = {}
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder_path, filename)
            try:
                df = load_stock(filepath)
                ticker = df["Ticker"].iloc[0]
                all_stocks[ticker] = df
            except Exception as e:
                print(f"FAILED: {filename} — {e}")
    return all_stocks

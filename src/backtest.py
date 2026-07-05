import pandas as pd

def run_backtest(all_stocks, profit_target=0.10, stop_loss_pct=0.03,
                 stop_loss_days=20, buy_variable=0.01375, buy_fixed=4,
                 sell_variable=0.01675, sell_fixed=4, position_size=100_000):
    trade_log = []
    for ticker, df in all_stocks.items():
        signal_dates = df[df["Signal"] == 1].index.tolist()
        for sig_idx in signal_dates:
            entry_idx = sig_idx + 1
            if entry_idx >= len(df):
                continue
            entry_row   = df.iloc[entry_idx]
            entry_price = entry_row["Open"]
            entry_date  = entry_row["Date"]
            if pd.isna(entry_price) or entry_price <= 0:
                continue
            stop_price   = entry_price * (1 - stop_loss_pct)
            target_price = entry_price * (1 + profit_target)
            shares       = position_size / entry_price
            buy_cost     = (position_size * buy_variable) + buy_fixed
            exit_price = exit_date = exit_reason = None
            for day in range(1, stop_loss_days + 1):
                monitor_idx = entry_idx + day
                if monitor_idx >= len(df):
                    last = df.iloc[-1]
                    exit_price, exit_date, exit_reason = last["Close"], last["Date"], "End of Data"
                    break
                row = df.iloc[monitor_idx]
                if row["Close"] >= target_price:
                    exit_price, exit_date, exit_reason = target_price, row["Date"], "Profit Target"
                    break
                if row["Close"] <= stop_price:
                    exit_price, exit_date, exit_reason = stop_price, row["Date"], "Stop Loss"
                    break
                if day == stop_loss_days:
                    exit_price, exit_date, exit_reason = row["Close"], row["Date"], "Time Stop"
                    break
            if not exit_price or exit_price <= 0:
                continue
            sale_value   = shares * exit_price
            sell_cost    = (sale_value * sell_variable) + sell_fixed
            net_pnl      = (sale_value - position_size) - buy_cost - sell_cost
            net_return   = net_pnl / position_size
            gross_return = (exit_price - entry_price) / entry_price
            trade_log.append({
                "Ticker"      : ticker,
                "Entry_Date"  : entry_date,
                "Exit_Date"   : exit_date,
                "Entry_Price" : round(entry_price, 4),
                "Exit_Price"  : round(exit_price, 4),
                "Gross_Return": round(gross_return * 100, 2),
                "Net_Return"  : round(net_return * 100, 2),
                "Net_PnL_NGN" : round(net_pnl, 2),
                "Days_Held"   : (exit_date - entry_date).days,
                "Exit_Reason" : exit_reason,
            })
    return pd.DataFrame(trade_log).sort_values("Entry_Date").reset_index(drop=True)

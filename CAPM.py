import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

tickers = {
    'Reliance': 'RELIANCE.NS',     # Target Stock
    'Nifty50': '^NSEI',            # Market Benchmark
    'HDFC Bank': 'HDFCBANK.NS',    # Peer 1: Top Banking Stock
    'Infosys': 'INFY.NS'           # Peer 2: Top IT Stock
}
start_date = '2023-01-01'
end_date = '2025-01-01'

data = pd.DataFrame()

for name, ticker in tickers.items():
    # Download the data
    df = yf.download(ticker, start=start_date, end=end_date, progress=False)
    
    # Check which column exists to avoid errors
    if 'Adj Close' in df.columns:
        data[name] = df['Adj Close']
    elif 'Close' in df.columns:
        data[name] = df['Close']
    else:
        # Fallback for complex multi-level columns
        data[name] = df.iloc[:, 0]

# Drop any missing rows (holidays etc.)
data.dropna(inplace=True)

# Formula: (Today / Yesterday) - 1
returns = data.pct_change().dropna()

# Equation: Reliance_Return = Alpha + (Beta * Nifty_Return)

# X = The Independent Variable (Market Moves)
X = returns['Nifty50']
# Y = The Dependent Variable (Reliance Moves)
Y = returns['Reliance']

# Add a constant (Alpha) to the model
X_sm = sm.add_constant(X)

# Fit the model (Ordinary Least Squares)
model = sm.OLS(Y, X_sm).fit()

# Extract Alpha and Beta
alpha = model.params['const']
beta = model.params['Nifty50']
r_squared = model.rsquared

# Setup the figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot A: Scatter Plot with Regression Line
sns.regplot(x='Nifty50', y='Reliance', data=returns, ax=ax1, 
            scatter_kws={'alpha':0.5, 'color':'blue'}, 
            line_kws={'color':'red', 'label':f'Beta = {beta:.2f}'})
ax1.set_title(f"CAPM Regression: Reliance vs Nifty 50")
ax1.set_xlabel("Market Returns (Nifty 50)")
ax1.set_ylabel("Stock Returns (Reliance)")
ax1.legend()
ax1.grid(True, alpha=0.3)

# Plot B: Correlation Heatmap
corr_matrix = returns.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax2, vmin=-1, vmax=1)
ax2.set_title("Correlation Matrix (Peers & Market)")

plt.tight_layout()
plt.show()


print(f"{'='*30}")
print(f"CAPM ANALYSIS REPORT: Reliance")
print(f"{'='*30}")
print(f"Beta (Sensitivity):      {beta:.4f}")
print(f"Alpha (Extra Return):    {alpha:.5f} (Trading days)")
print(f"R-Squared (Fit):         {r_squared:.4f}")
print("-" * 30)
print("INTERPRETATION:")

# Beta Interpretation
if beta > 1:
    print(f"• High Volatility: Reliance is {beta:.2f}x more volatile than the market.")
elif beta < 1:
    print(f"• Low Volatility: Reliance is more stable than the market (Beta {beta:.2f}).")
else:
    print(f"• Market Mover: Reliance moves exactly with the market.")

# Alpha Interpretation
if alpha > 0:
    print("• Outperformance: The stock generates positive returns purely on its own skill.")
else:
    print("• Underperformance: The stock drags slightly behind what the market predicts.")
    
# Peer Correlation Check
print("-" * 30)
print("PEER CORRELATIONS:")
print(f"• Correlation with HDFC Bank:  {returns['Reliance'].corr(returns['HDFC Bank']):.2f}")
print(f"• Correlation with Infosys:    {returns['Reliance'].corr(returns['Infosys']):.2f}")
print(f"{'='*30}")
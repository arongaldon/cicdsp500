"""
DCA investment on S&P 500

Webapp to provide the user with the estimated quantity of euros
given last 2 years of historical data and the DCA amounts to invest.

DISCLAIMER:
This is NOT a buy or investment recommendation,
just a development and CI/CD practice.

Aron Galdon Gines 2024
"""

from flask import Flask, render_template, request
import pandas as pd
import yfinance as yf

app = Flask(__name__)

def get_sp500_data() -> pd.DataFrame:
    """Retrieve historical S&P 500 data."""
    sp500_ticker = yf.Ticker('^GSPC')
    hist = sp500_ticker.history(period='2y')
    return hist

def calculate_result(initial: float, monthly: float, years: int) -> float:
    """Calculate the result of DCA investment."""
    hist = get_sp500_data()
    hist.reset_index(drop=True, inplace=True)

    months = years * 12

    print(f"[i] cost    total_shares")
    total = initial
    for i in range(1, months + 1):
        cost = hist.loc[i, 'Close']
        total += monthly
        total_shares = total / cost
        print(f"[{i}] {cost:.2f} {total_shares:.2f}")

    print(f"Final cost per share: {cost:.2f}")
    return total_shares * cost

@app.route('/', methods=['GET', 'POST'])
def sp500() -> None:
    """Request details from the user and show the result."""
    if request.method == 'POST':
        result_euros = calculate_result(float(request.form['inversion_inicial'])
                                      , float(request.form['contribucion_mensual'])
                                      , int(request.form['periodo_inversion']))
        str_result = f"{result_euros:.2f} €"
        return render_template('results.html', valor_final=str_result)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(port=80)

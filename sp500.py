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

class InvestmentCalculator:
    """Class with all calculate methods required to populate a results page."""
    def __init__(self, initial: float, monthly: float, years: int):
        self.initial = initial
        self.monthly = monthly
        self.years = years

    def get_sp500_data(self) -> pd.DataFrame:
        """Retrieve historical S&P 500 data."""
        sp500_ticker = yf.Ticker('^GSPC')
        hist = sp500_ticker.history(period='2y')
        return hist

    def calculate_contributed(self) -> float:
        """Calculate the total money contributed by the investor."""
        months = self.years * 12
        return self.initial + self.monthly * months

    def calculate_total(self) -> float:
        """Calculate the result of DCA investment."""
        hist = self.get_sp500_data()
        if hist.empty:
            return 0.0

        hist.reset_index(drop=True, inplace=True)

        months = self.years * 12

        print('[i] cost    total_shares')
        total = self.initial
        for i in range(1, months + 1):
            cost = hist.loc[i, 'Close']
            total += self.monthly
            total_shares = total / cost
            print(f"[{i}] {cost:.2f} {total_shares:.2f}")

        print(f"Final cost per share: {cost:.2f}")
        return total_shares * cost

    def calculate_retained(self) -> float:
        """Calculate the total money retained by the government."""
        return 1

    def calculate_net_profit(self) -> float:
        """Calculate the total net profit after tax."""
        return 2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def sp500() -> None:
    """Request details from the user and show the result."""
    if request.method == 'POST':
        initial = float(request.form['initial'])
        monthly = float(request.form['monthly'])
        years = int(request.form['years'])
        calculator = InvestmentCalculator(initial, monthly, years)
        contributed = calculator.calculate_contributed()
        total = calculator.calculate_total()
        retained = calculator.calculate_retained()
        net_profit = calculator.calculate_net_profit()
        return render_template('results.html'
                               , years=years
                               , contributed=f"{contributed:.2f} €"
                               , total=f"{total:.2f} €"
                               , retained=f"{retained:.2f} €"
                               , net_profit=f"{net_profit:.2f} €")
    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

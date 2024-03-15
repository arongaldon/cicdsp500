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

        # Calculate the average monthly return of the S&P 500
        hist['Monthly_Return'] = hist['Close'].pct_change().fillna(0)
        monthly_return_avg = hist['Monthly_Return'].mean()

        total = self.initial
        for _ in range(self.years * 12):
            total *= (1 + monthly_return_avg)
            total += self.monthly

        return round(total, 2)

    def calculate_retained(self, profit: float) -> float:
        """Calculate the total money retained by the government."""
        ranges = [(6000, 0.19), (50000, 0.21), (200000, 0.23), (300000, 0.27), (float('inf'), 0.28)]

        pending = profit
        retained = 0.0
        for limit, percentage in ranges:
            if profit < limit:
                retained += pending * percentage
                break
            retained += limit * percentage
            pending -= limit

        return retained

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
        profit = total - contributed
        retained = calculator.calculate_retained(profit)
        net_profit = profit - retained
        return render_template('results.html'
                               , years=years
                               , contributed=f"{contributed:,.2f} €"
                               , total=f"{total:,.2f} €"
                               , retained=f"{retained:,.2f} €"
                               , net_profit=f"{net_profit:,.2f} €")
    return render_template('form.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

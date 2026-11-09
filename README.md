# Option-Pricing-Simulator

A Python simulator that uses NumPy and Matplotlib to explore European option pricing through Black–Scholes calculations and Monte Carlo simulation.

The simulator calculates theoretical call and put prices, compares analytical and simulated results, and investigates how volatility and the number of simulations affect option value and numerical uncertainty.

This project focuses on mathematical modelling, statistical analysis and numerical validation. It uses simulated data rather than live market data and is not designed to predict share prices or provide investment advice.

---

## Features

- **European Option Pricing**
  - Black–Scholes analytical pricing for calls and puts
  - Monte Carlo pricing using risk-neutral geometric Brownian motion
  - Discounting of future option payoffs to present value
- Numerical Validation
  - Comparison of Monte Carlo estimates against Black–Scholes prices
  - Absolute pricing error and standard error
  - Approximate 95% confidence intervals
  - Basic checks for put–call parity, price bounds and volatility sensitivity
- Customisable Inputs
  - Current share price
  - Strike price
  - Time to expiry
  - Risk-free interest rate
  - Annual volatility
  - Number of simulations
  - Random seed for reproducible results
- Visualisations
  - Simulated risk-neutral share-price paths
  - Monte Carlo call-price convergence
  - Distribution of discounted call payoffs
  - Call and put prices across different volatility levels
- Performance Measurement
  - Timing of Monte Carlo payoff generation and summary calculations
  - Comparison of numerical accuracy across simulation sample sizes

---

## User Interface

The simulator runs as a Python application with two outputs:

- A console summary displaying model inputs, analytical prices, simulated prices, confidence intervals and calculation time.
- A Matplotlib window containing four graphs for analysing simulation behaviour and pricing sensitivity.

Inputs are adjusted directly in the configuration section at the top of the Python script.

---

## How to Run

1) Clone or download this repository.

2) Ensure Python is installed.

3) Install the required packages in your terminal or Command Prompt:

   python -m pip install numpy matplotlib

4) Open the Python script in your preferred editor or IDE.

5) Adjust the input values at the top of the script if required.

6) Run the script to display the pricing results and graphs.

The default configuration uses:

- Current share price: 100
- Strike price: 100
- Time to expiry: 1 year
- Risk-free interest rate: 4%
- Annual volatility: 20%
- Monte Carlo simulations: 100,000
- Random seed: 42

Prices are expressed in the same currency units as the underlying share price.

---

## Model Assumptions and Limitations

- European options can only be exercised at expiry.
- The underlying asset pays no dividends.
- Interest rates and volatility remain constant.
- Share prices follow geometric Brownian motion without price jumps.
- Simulations use risk-neutral probabilities for pricing, not real-world price forecasts.
- Transaction costs, bid–ask spreads and practical trading constraints are not modelled.
- Confidence intervals measure Monte Carlo sampling uncertainty, not uncertainty caused by incorrect assumptions or inputs.
- Agreement between Monte Carlo and Black–Scholes demonstrates consistency under their shared assumptions, not accuracy against real market prices.

---

## Skills Demonstrated

- Financial Modelling: European option payoffs, Black–Scholes pricing and risk-neutral valuation
- Numerical Methods: Monte Carlo simulation and convergence analysis
- Statistical Analysis: standard errors, confidence intervals and sampling uncertainty
- Scientific Programming: modular Python functions, vectorised NumPy calculations and reproducible random sampling
- Software Validation: input validation and checks against analytical pricing relationships
- Data Visualisation: Matplotlib plots for simulated paths, payoff distributions and parameter sensitivity
- Performance Analysis: investigation of the relationship between simulation size, accuracy and computational cost

---

## Future Improvements

- Antithetic sampling to reduce Monte Carlo variance
- Repeated experiments across multiple random seeds to measure typical pricing error
- CSV export of pricing results and convergence data
- Option Greeks, including delta, gamma and vega
- Delta-hedging simulations with transaction costs
- Support for dividend-paying assets
- Comparison with binomial-tree pricing
- Market-data integration and implied-volatility analysis
- Automated tests covering additional inputs and edge cases
- Interactive controls for changing model parameters

---

## Author

Imaad Javaid  
[Imaad.Javaid@outlook.com](mailto:Imaad.Javaid@outlook.com)

[LinkedIn](https://linkedin.com/in/imaad-javaid-854941369)  
[GitHub](https://github.com/IJF1)

---

*This project extends my physics and simulation portfolio into quantitative finance, applying mathematical modelling, probability and Python to financial pricing problems.*

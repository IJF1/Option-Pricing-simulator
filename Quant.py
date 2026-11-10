import math
import time

import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# INPUTS — change these to experiment
# ============================================================

SPOT_PRICE = 100.0          # Current share price
STRIKE_PRICE = 100.0        # Option exercise price
TIME_TO_EXPIRY = 1.0        # Years
RISK_FREE_RATE = 0.04       # 4% per year, continuously compounded
VOLATILITY = 0.20          # 20% annual volatility
NUMBER_OF_SIMULATIONS = 100_000
RANDOM_SEED = 42

# Model assumptions:
# European options, constant volatility and interest rate,
# no dividends, and geometric Brownian motion.
# Simulations use the risk-neutral rate, not a return forecast.


def normal_cdf(x):
    """Cumulative distribution function of a standard normal."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def validate_inputs(spot, strike, expiry, rate, volatility):
    values = [spot, strike, expiry, rate, volatility]

    if not all(math.isfinite(value) for value in values):
        raise ValueError("All inputs must be finite numbers.")

    if spot <= 0 or strike <= 0:
        raise ValueError("Spot and strike prices must be positive.")

    if expiry <= 0 or volatility <= 0:
        raise ValueError("Expiry and volatility must be positive.")


def black_scholes(spot, strike, expiry, rate, volatility):
    """Return European call and put prices with no dividends."""
    validate_inputs(spot, strike, expiry, rate, volatility)

    d1 = (
        math.log(spot / strike)
        + (rate + 0.5 * volatility**2) * expiry
    ) / (volatility * math.sqrt(expiry))

    d2 = d1 - volatility * math.sqrt(expiry)
    discounted_strike = strike * math.exp(-rate * expiry)

    call = (
        spot * normal_cdf(d1)
        - discounted_strike * normal_cdf(d2)
    )

    put = (
        discounted_strike * normal_cdf(-d2)
        - spot * normal_cdf(-d1)
    )

    return call, put


def monte_carlo_payoffs(
    spot, strike, expiry, rate, volatility, simulations, rng
):
    """Generate independent, discounted call and put payoffs."""
    validate_inputs(spot, strike, expiry, rate, volatility)

    if simulations < 2:
        raise ValueError("Use at least two simulations.")

    z = rng.standard_normal(simulations)

    terminal_prices = spot * np.exp(
        (rate - 0.5 * volatility**2) * expiry
        + volatility * math.sqrt(expiry) * z
    )

    discount_factor = math.exp(-rate * expiry)

    call_payoffs = (
        np.maximum(terminal_prices - strike, 0.0)
        * discount_factor
    )

    put_payoffs = (
        np.maximum(strike - terminal_prices, 0.0)
        * discount_factor
    )

    return call_payoffs, put_payoffs


def estimate_price(payoffs):
    """Return mean, standard error and approximate 95% interval."""
    price = float(np.mean(payoffs))

    standard_error = float(
        np.std(payoffs, ddof=1) / math.sqrt(len(payoffs))
    )

    margin = 1.96 * standard_error

    return price, standard_error, price - margin, price + margin


def simulate_price_paths(
    spot, expiry, rate, volatility, steps, paths, rng
):
    """Simulate share-price paths using exact GBM increments."""
    dt = expiry / steps
    z = rng.standard_normal((steps, paths))

    log_returns = (
        (rate - 0.5 * volatility**2) * dt
        + volatility * math.sqrt(dt) * z
    )

    prices = np.empty((steps + 1, paths))
    prices[0] = spot
    prices[1:] = spot * np.exp(np.cumsum(log_returns, axis=0))

    return np.linspace(0.0, expiry, steps + 1), prices


def run_checks():
    """Basic checks for pricing identities and expected behaviour."""
    spot, strike, expiry, rate, volatility = 100, 105, 1, 0.04, 0.2

    call, put = black_scholes(
        spot, strike, expiry, rate, volatility
    )

    parity_target = spot - strike * math.exp(-rate * expiry)

    assert math.isclose(
        call - put, parity_target, abs_tol=1e-10
    ), "Put-call parity failed."

    assert call >= max(0.0, parity_target)
    assert put >= max(0.0, -parity_target)

    higher_vol_call, higher_vol_put = black_scholes(
        spot, strike, expiry, rate, 0.3
    )

    assert higher_vol_call > call
    assert higher_vol_put > put


def main():
    run_checks()

    if NUMBER_OF_SIMULATIONS < 100:
        raise ValueError("Use at least 100 simulations for the plots.")

    # Separate random streams keep pricing and path plots reproducible.
    seeds = np.random.SeedSequence(RANDOM_SEED).spawn(2)
    pricing_rng = np.random.default_rng(seeds[0])
    path_rng = np.random.default_rng(seeds[1])

    bs_call, bs_put = black_scholes(
        SPOT_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRY,
        RISK_FREE_RATE,
        VOLATILITY,
    )

    start = time.perf_counter()

    call_payoffs, put_payoffs = monte_carlo_payoffs(
        SPOT_PRICE,
        STRIKE_PRICE,
        TIME_TO_EXPIRY,
        RISK_FREE_RATE,
        VOLATILITY,
        NUMBER_OF_SIMULATIONS,
        pricing_rng,
    )

    call_result = estimate_price(call_payoffs)
    put_result = estimate_price(put_payoffs)

    elapsed = time.perf_counter() - start

    print("\nEUROPEAN OPTION PRICING SIMULATOR")
    print("=" * 62)
    print(f"Share price:         {SPOT_PRICE:.2f}")
    print(f"Strike price:        {STRIKE_PRICE:.2f}")
    print(f"Expiry:              {TIME_TO_EXPIRY:.2f} years")
    print(f"Risk-free rate:      {RISK_FREE_RATE:.1%}")
    print(f"Volatility:          {VOLATILITY:.1%}")
    print(f"Simulations:         {NUMBER_OF_SIMULATIONS:,}")
    print("Basic pricing checks: passed")
    print("-" * 62)

    print(
        f"{'Option':<10}"
        f"{'Black-Scholes':>16}"
        f"{'Monte Carlo':>16}"
        f"{'Abs. error':>14}"
    )

    for name, benchmark, result in [
        ("Call", bs_call, call_result),
        ("Put", bs_put, put_result),
    ]:
        price, standard_error, lower, upper = result

        print(
            f"{name:<10}"
            f"{benchmark:>16.4f}"
            f"{price:>16.4f}"
            f"{abs(price - benchmark):>14.4f}"
        )

        print(
            f"  Approx. 95% CI: [{lower:.4f}, {upper:.4f}]"
            f" | Standard error: {standard_error:.4f}"
        )

    print(f"\nMonte Carlo calculation time: {elapsed:.4f} seconds")
    print("Prices are in the same currency units as the share price.")
    print("Confidence intervals describe sampling error only.")
    print("They do not account for incorrect model assumptions.")

    # Use nested samples to examine convergence.
    sample_counts = np.unique(
        np.geomspace(100, NUMBER_OF_SIMULATIONS, 35).astype(int)
    )

    results = np.array([
        estimate_price(call_payoffs[:n])
        for n in sample_counts
    ])

    times, paths = simulate_price_paths(
        SPOT_PRICE,
        TIME_TO_EXPIRY,
        RISK_FREE_RATE,
        VOLATILITY,
        steps=252,
        paths=30,
        rng=path_rng,
    )

    volatilities = np.linspace(0.05, 0.80, 100)

    sensitivity = np.array([
        black_scholes(
            SPOT_PRICE,
            STRIKE_PRICE,
            TIME_TO_EXPIRY,
            RISK_FREE_RATE,
            vol,
        )
        for vol in volatilities
    ])

    fig, axes = plt.subplots(2, 2, figsize=(13, 9))

    ax = axes[0, 0]
    ax.plot(times, paths, linewidth=0.8, alpha=0.6)
    ax.set_title("Simulated share prices: risk-neutral model")
    ax.set_xlabel("Time (years)")
    ax.set_ylabel("Share price")

    ax = axes[0, 1]
    ax.plot(
        sample_counts,
        results[:, 0],
        color="tab:blue",
        label="Monte Carlo estimate",
    )
    ax.fill_between(
        sample_counts,
        results[:, 2],
        results[:, 3],
        color="tab:blue",
        alpha=0.2,
        label="Approx. 95% confidence interval",
    )
    ax.axhline(
        bs_call,
        color="black",
        linestyle="--",
        label="Black-Scholes",
    )
    ax.set_xscale("log")
    ax.set_title("Call-price convergence")
    ax.set_xlabel("Number of simulations")
    ax.set_ylabel("Option price")
    ax.legend()

    ax = axes[1, 0]
    ax.hist(call_payoffs, bins=70, color="tab:green", alpha=0.8)
    ax.set_title("Distribution of discounted call payoffs")
    ax.set_xlabel("Discounted payoff")
    ax.set_ylabel("Frequency")

    ax = axes[1, 1]
    ax.plot(
        volatilities * 100,
        sensitivity[:, 0],
        label="Call",
    )
    ax.plot(
        volatilities * 100,
        sensitivity[:, 1],
        label="Put",
    )
    ax.axvline(
        VOLATILITY * 100,
        color="grey",
        linestyle=":",
        label="Selected volatility",
    )
    ax.set_title("Option-price sensitivity to volatility")
    ax.set_xlabel("Annual volatility (%)")
    ax.set_ylabel("Black-Scholes price")
    ax.legend()

    for ax in axes.flat:
        ax.grid(True, alpha=0.25)

    fig.suptitle(
        "Option Pricing and Monte Carlo Analysis",
        fontsize=16,
    )
    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

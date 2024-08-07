# risk-over-time

Understanding how time scales affect investment risk.

## Motivation

Often, more volatile investments have greater expected value than safer investments. Suppose we have two investment choices: a risky investment $R$ and a safe investment $S$. The expected yearly return of $R$ may be greater than that of $S$, but the standard deviation is greater as well. Comparing the expected value of the two investments is trivial. However, we may also want to know the probability that our investment yields at least some amount $A$. Then the probability of $R>A$ and $S>A$ changes over time. This gives us a notion of how investment risk depends on time, and we can evaluate what degree of risk is appropriate based on how much time we plan to hold an investment.

## Methods

We can model investment growth as a geometric Brownian motion where the yearly growth has some expected value and some standard deviation.

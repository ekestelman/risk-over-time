# risk-over-time

Understanding how time scales affect investment risk.

## Motivation

Sometimes more volatile investments have greater expected value than safer investments. Suppose we have two investment choices: a risky investment $R$ and a safe investment $S$. The expected yearly return of $R$ may be greater than that of $S$, but the standard deviation is greater as well. On short time scales, we might prefer the safer investment: despite the lower expected returns, we have more certainty in how our investment will perform. On longer time scales, however, the short term volatility of a riskier investment may not concern us as much: while the true returns may deviate greatly from the expected value in the short term, we might expect the returns to tend towards the expected value in the long term.

But what is short term and what is long term? How much greater should the expected value of $R$ be to justify the risk? Or how low must the standard deviation of $S$ be to justify the opportunity cost?

To aid our choice, we might consider the following questions:

1) What is the probability that $R$ outperforms $S$ at time $t$?

2) What is the probability that either strategy outperforms some benchmark $B$?

A note on question 1: if the expected value $E[R] > E[S]$, then $P(R>S)$ will usually be greater than $0.5$ for any $t$. That is, it is insufficient to simply choose the strategy that is more likely to perform better. This would be almost equivalent to choosing the strategy with the higher expected value, and this gives no regard to risk tolerance.

## Methods

We can model investment growth using geometric Brownian motion where the yearly growth has some expected value and some standard deviation.

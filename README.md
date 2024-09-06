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

## A note on parameters

The program prompts the user for the mean and standard deviation of each investment under consideration. However, the program currently treats these inputs as $`\mu^*`$ and $`\sigma^*`$ respectively.

$\mu^*$ is defined as the median of the lognormal distribution.

$`\sigma^*`$ is defined such that the interval $`[\mu^*/\sigma^*,\mu^*\cdot\sigma^*]`$ contains 68% of the probability.

## Screenshots

### PDF

The graph below shows the probability density function of our two investment options after a 10 year period.

![](https://github.com/ekestelman/risk-over-time/blob/main/SVGs/risk_pdf.svg)

In this plot, the histogram shows the distribution of simulated results (produced using a Monte Carlo simulation, given yearly returns modeled by a lognormal random variable).

The solid curves depict the theoretical PDF. Overlaying the two plots serves as validation. The dashed vertical line is a benchmark, in this case depicting a constant yearly return of 8.25%.

### CDF

Below is the complement of the cumulative density function for the two investments.

![](https://github.com/ekestelman/risk-over-time/blob/main/SVGs/risk_cdf.svg)

This tells us the probability of our investment yielding at least $x$ after some established time (in this case, 10 years). This plot uses the the simulation results, which is why it may appear bumpy.

Although it may not be noticeable in the image, the two CDFs intersect exactly once.

Again the dashed vertical line is the benchmark. 

### P(A>B)

The graph below shows the probability of investment A outperforming investment B as a function of time.

![](https://github.com/ekestelman/risk-over-time/blob/main/SVGs/risk_a_gt_b.svg)

Again this plot uses the simulation results, which is why it does not increase smoothly.

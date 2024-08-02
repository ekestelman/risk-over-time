import numpy as np
import matplotlib.pyplot as plt
import time
from strats_module import *#Two_Strats

# TODO clargs to output compuation time

if __name__ == "__main__":
  # TODO another graph can show the ROI for each strat rather than just win rate
  # TODO multiplot to show effect of diff mu, sigma (or plots with diff axes)
  years = 30
  principle = 1000
  strat1 = Strat(.1, .15, years=years, principle=principle)
  strat1.print_summary()
  strat2 = Strat(.09, .1, years=years, principle=principle)
  strat2.print_summary()
  compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
  # TODO Add function analogous to compare/summary for benchmark.
  # Can yearly_plot() still accept sigma=0 strat as argument?
  # TODO exp graph with shaded area of x% confidence interval
  benchmark = 1.07
  benchmark = benchmark**years * principle
  #yearly_plot(strat1, strat2, 30, 2)
  strat1.dstr_over_time(years=15, normalize=True)  # TODO test different years set earlier or as arg
  # XXX Using years different from previoulsy set years will mess up other graphs.
  #plt.hist(strat1.roi_dstr, 50, histtype="step") #density=True/False
  #plt.hist(strat2.roi_dstr, 50, histtype="step") #density=True/False
  strats = [strat1.roi_dstr, strat2.roi_dstr]
  #plt.hist(strats, 40, density=True)
  # More bins if years is higher to accomodate more spread.
  # Factor of ~20 makes bars fit curve more accurately but looks messy.
  # Consider interactive plot: toggle curve, nbins.
  # Consider excluding outlying results, consider log plot for long time scales.
  plt.hist(strats, 15 * int(strat1.years**0.5), density=True)
  # TODO chance of being above/below a benchmark for each strat?
  # e.g., better chance that strat 2 > 5% but better chance that strat 1 > 15%.
  # ^CDF plot may basically demonstrate this.
  #x = np.linspace(min(strats[0])/principle, max(strats[0])/principle, 1000)
  #mu, sigma = strat1.mu * years, strat1.sigma * years
  #pdf = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) \
  #      / (x * sigma * (2 * np.pi)**0.5)
  #plt.plot(x*principle, pdf)
  x = np.linspace(min(strats[0]), max(strats[0]), 1000)
  mu, sigma = strat1.mu * strat1.years, strat1.sigma * strat1.years**0.5
  pdf = np.exp(-(np.log(x/principle) - mu)**2 / (2 * sigma**2)) \
        / (x/principle * sigma * (2 * np.pi)**0.5) / principle
  plt.plot(x, pdf)
  plt.plot(*strat2.pdf())
  # Funny output if dereference is omitted
  # TODO make ymax a bit greater than the highest point of either PDF.
  plt.vlines(benchmark, 0, 2*max(pdf), color="black", linestyles="--")
  plt.show()








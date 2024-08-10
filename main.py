import numpy as np
import matplotlib.pyplot as plt
import time
from strats_module import *#Two_Strats

# TODO clargs to output compuation time
# TODO seperate class or methods for computing results analytically instead of
# numerically. Can compare using numerical integration (Monte Carlo to
# integrate over curves). This is probably faster than numerically computing
# curves and then sampling (try testing comp times). Then numerical approach
# can be kept (or separated) just as validation.
# TODO Prompt user for main args, prompt for desired graph(s), loop until exited
# (store objects to avoid recomputation? --won't work currently for yearly plot,
# may not matter much for analytical calculation.)

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
  benchmark = 1.0825
  # TODO include growing benchmark in quantile plot
  benchmark = benchmark**years * principle
  #yearly_plot(strat1, strat2, 30, 2)
  strat1.dstr_over_time(years=15, normalize=True)
  # TODO test different years set earlier or as arg
  # XXX PDF/CDF comparison is messed up if dstr_over_time is only run on one
  # strat (because recalc for input years will only apply to one strat).
  # XXX Using years different from previoulsy set years will mess up other graphs.
  strat1.recalc(years) # Reset strat1 to original years.
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
  #for elm in strats:  # Numerically computed CDF
  #  plt.plot(elm.cum_dstr())
  # TODO show points of intersection on CDF plot? (Consider the interpretation
  # of this statistic.)
  inverse = True
  plt.plot(*strat1.cum_dstr(inverse))  # Maybe strats = [strat1, strat2]
  plt.plot(*strat2.cum_dstr(inverse))
  plt.xlabel("Amount")
  # Math print for ylabel?
  if inverse:
    plt.ylabel("P(>x)")
  else:
    plt.ylabel("P(<x)")
  plt.vlines(benchmark, 0, 1, color="black", linestyles="--")
  plt.show()








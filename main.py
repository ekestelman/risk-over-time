import numpy as np
import matplotlib.pyplot as plt
import time
from strats_module import *#Two_Strats

# TODO clargs to output compuation time

if __name__ == "__main__":
  # TODO another graph can show the ROI for each strat rather than just win rate
  # TODO multiplot to show effect of diff mu, sigma (or plots with diff axes)
  years = 20
  principle = 1000
  strat1 = Strat(.1, .15, years=years, principle=principle)
  strat1.print_summary()
  strat2 = Strat(.09, .1, years=years, principle=principle)
  strat2.print_summary()
  compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
  #yearly_plot(strat1, strat2, 30, 2)
  #plt.hist(strat1.roi_dstr, 50, histtype="step") #density=True/False
  #plt.hist(strat2.roi_dstr, 50, histtype="step") #density=True/False
  strats = [strat1.roi_dstr, strat2.roi_dstr]
  plt.hist(strats, 40, density=True)
  # TODO chance of being above/below a benchmark for each strat?
  # e.g., better chance that strat 2 > 5% but better chance that strat 1 > 15%.
  # ^CDF plot may basically demonstrate this.
  #x = np.linspace(min(strats[0])/principle, max(strats[0])/principle, 1000)
  #mu, sigma = strat1.mu * years, strat1.sigma * years
  #pdf = np.exp(-(np.log(x) - mu)**2 / (2 * sigma**2)) \
  #      / (x * sigma * (2 * np.pi)**0.5)
  #plt.plot(x*principle, pdf)
  x = np.linspace(min(strats[0]), max(strats[0]), 1000)
  mu, sigma = strat1.mu * years, strat1.sigma * years**0.5
  pdf = np.exp(-(np.log(x/principle) - mu)**2 / (2 * sigma**2)) \
        / (x/principle * sigma * (2 * np.pi)**0.5) / principle
  plt.plot(x, pdf)
  plt.show()








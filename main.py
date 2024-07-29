import numpy as np
import matplotlib.pyplot as plt
import time
from strats_module import *#Two_Strats

# TODO clargs to output compuation time

'''
class Two_Strats:
  def __init__(self, mu, sigma, alt_mu, alt_sigma=0, years=1, principle=1e3, \
               trials=10000):
    self.mu = mu
    self.sigma = sigma
    self.alt_mu = alt_mu
    self.alt_sigma = alt_sigma
    self.years = years
    self.principle = principle
    self.trials = trials

def roi_dstr(years, mu, sigma, trials=10000, principle=1e3):
# Distribution of possible returns on investment.
# TODO trials should be int

  start = time.time()
  
  if sigma:
    results = [None for _ in range(trials)]
    for i in range(trials):
      balance = principle
      for j in range(years):
        balance *= np.random.lognormal(mu, sigma)
      results[i] = balance
  else:
    results = principle * np.exp(mu*years)
  
  stop = time.time()
  #print("main loop", stop-start)

  return results

def summarize(results):
  summary = {
             "mean" : np.mean(results),
             "std_biased" : np.std(results),
             "std_unbiased" : np.std(results, ddof=1),
             }
  
  trials = len(results)

  summary["sem"] = summary["std_unbiased"] / trials ** 0.5  # std error on mean
  
  for x in summary:
    summary[x] = round(summary[x], 2)
  
  print("Mean:", summary["mean"], "+/-", summary["sem"])
  print("Sample standard deviation:", summary["std_unbiased"])
  return summary

def win_rate(results, alt_results, alt_sigma):

  trials = len(results)
  win = 0
  
  start = time.time()
  
  if alt_sigma:
    for i in range(trials):
      if results[i] > alt_results[i]:
        win += 1
  else:
    for i in range(trials):
      if results[i] > alt_results:
        win += 1
  
  end = time.time()
  #print("win loop", end - start)
  
  win /= trials
  win_sem = np.std(int(win*trials)*[1]+int((1-win)*trials)*[0], ddof=1) / \
            trials ** 0.5
  # Is there any significance to sample std dev? (i.e., not SEM)
  # XXX validate use of this statistic
  win_sem = round(win_sem, int(np.log10(trials)))
  
  #print(win, "+/-", round(win_sem,int(np.log10(trials))))
  return win, win_sem

def compare(years, summary=False):
  #years = 5
  principle = 1e3
  mu = 0.095
  sigma = 0.15
  # exp(0.0488) ~ 1.05
  # exp(0.0677) ~ 1.07
  # exp(0.0793) ~ 1.0825
  alt_mu = 0.05
  alt_sigma = 0.01
  alt_results = roi_dstr(years, alt_mu, alt_sigma)
  results = roi_dstr(years, mu, sigma)
  trials = len(results)
  win, win_sem = win_rate(results, alt_results, alt_sigma)
  if summary:
    print("Strat A")
    summarize(results)
    print("\nStrat B")
    if alt_sigma:
      summarize(alt_results)
    else:
      print(principle * np.exp(alt_mu*years))
      # TODO better handling of principle arg
      # TODO consider defining mu differently (APY vs APR)
    print("\nP(A>B): ", win, "+/-", \
          round(win_sem,int(np.log10(trials))))
  return win, win_sem

def yearly_plot(stop, step, start=0):
  # TODO allow different start to be set
  years = np.arange(step, stop+step, step)
  win = [None for _ in years]
  win_sem = [None for _ in years]
  for i in range(len(years)):
    win[i], win_sem[i] = compare(years[i])
  plt.errorbar(years, win, win_sem) 
  plt.show()
  '''

if __name__ == "__main__":
  # TODO another graph can show the ROI for each strat rather than just win rate
  # TODO multiplot to show effect of diff mu, sigma (or plots with diff axes)
  #yearly_plot(30, 2)
  #compare(1, summary=True)
  #test_strat = Two_Strats(.1, .15, .05)
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








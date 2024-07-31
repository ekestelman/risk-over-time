import numpy as np
import matplotlib.pyplot as plt
import time

# TODO clargs to output compuation time

def roi_dstr(years, mu, sigma, trials=10000, principle=1e3):
# Distribution of possible returns on investment.
# TODO trials should be int

  start = time.time()
  
  # XXX sigma is not replaceable with self.sigma since it also stands in for 
  # alt_sigma.
  if sigma:
    results = [None for _ in range(trials)]
    for i in range(trials):
      balance = principle
      for j in range(years):
        balance *= np.random.lognormal(mu, sigma)
      results[i] = balance
  else:
    results = [principle * np.exp(mu*years)]
  
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
  
  return summary

def print_summary(summary):
  for x in summary:
    summary[x] = round(summary[x], 2)
  
  print("Mean:", summary["mean"], "+/-", summary["sem"])
  print("Sample standard deviation:", summary["std_unbiased"])

def win_rate(results, alt_results):#, alt_sigma):

  trials = len(results)
  win = 0
  
  start = time.time()
  
  if len(alt_results) > 1:
    for i in range(trials):
      if results[i] > alt_results[i]:
        win += 1
  else:
    for i in range(trials):
      if results[i] > alt_results[0]:
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

#def compare(years, summary=False):
def compare(results, alt_results, summary=False):#years, summary=False):
  ##years = 5
  #principle = 1e3
  #mu = 0.095
  #sigma = 0.15
  ## exp(0.0488) ~ 1.05
  ## exp(0.0677) ~ 1.07
  ## exp(0.0793) ~ 1.0825
  #alt_mu = 0.05
  #alt_sigma = 0.01
  #alt_results = roi_dstr(years, alt_mu, alt_sigma)
  #results = roi_dstr(years, mu, sigma)
  trials = len(results)
  win, win_sem = win_rate(results, alt_results)#, alt_sigma)
  if summary:
    print("Strat A")
    summarize(results)
    print("\nStrat B")
    if len(alt_results)>1:  # TODO what happens if we summarize len 1 results?
      summarize(alt_results)
    else:
      print(principle * np.exp(alt_mu*years))
      # TODO better handling of principle arg
      # TODO consider defining mu differently (APY vs APR)
    print("\nP(A>B): ", win, "+/-", \
          round(win_sem,int(np.log10(trials))))
  return win, win_sem

def yearly_plot(strat1, strat2, stop, step, start=0):
  # TODO allow different start to be set
  years = np.arange(step, stop+step, step)
  win = [None for _ in years]
  win_sem = [None for _ in years]
  for i in range(len(years)):
    strat1.recalc(years[i])
    strat2.recalc(years[i])
    win[i], win_sem[i] = compare(strat1.roi_dstr, strat2.roi_dstr)
    # compare now takes results, not years. years needs to pass through strat obj
    # needs to make new strat object on each loop, or alter existing strat results
  plt.errorbar(years, win, win_sem) 
  plt.show()
  
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
    self.results = roi_dstr(self.years, self.mu, self.sigma, self.trials, \
                            self.principle)
    self.alt_results = roi_dstr(self.years, self.alt_mu, self.alt_sigma, \
                                self.trials, self.principle)
    self.summary = summarize(self.results)
    if alt_sigma:
      self.alt_summary = summarize(self.alt_results)

class Strat:
  def __init__(self, mu, sigma=0, years=1, principle=1e3, trials=10000):
    self.mu = mu
    self.sigma = sigma
    self.years = years
    self.principle = principle
    self.trials = trials
    # TODO Below could be extracted to recalc (or calc) method.
    self.roi_dstr = roi_dstr(years, mu, sigma, trials, principle)
    self.summary = summarize(self.roi_dstr)
    # ^Should this be a method?

  def print_summary(self):
    print_summary(self.summary)

  def recalc(self, years): # Use years=self.years if we extract roi_dstr?
    self.years = years
    self.roi_dstr = roi_dstr(years, self.mu, self.sigma, self.trials, \
                             self.principle)
    self.summary = summarize(self.roi_dstr)

  def pdf(self):
    x = np.linspace(min(self.roi_dstr), max(self.roi_dstr), 1000)
    years, principle = self.years, self.principle
    mu, sigma = self.mu * years, self.sigma * years**0.5
    # Theoretical PDF, not fit to simulated data.
    pdf = np.exp(-(np.log(x/principle) - mu)**2 / (2 * sigma**2)) / \
          (x/principle * sigma * (2 * np.pi)**0.5) / principle
    return x, pdf  # Return x and pdf for easy plotting.
    # Funny output if dereference is omitted when plotting.
    # Clearer to have one function return x and another return pdf?

if __name__ == "__main__":
  # TODO another graph can show the ROI for each strat rather than just win rate
  # TODO multiplot to show effect of diff mu, sigma (or plots with diff axes)
  pass








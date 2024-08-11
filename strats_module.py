import numpy as np
import matplotlib.pyplot as plt
import time

def roi_dstr(years, mu, sigma, trials=10000, principle=1e3):
# Distribution of possible returns on investment.
# TODO trials should be int

  # XXX sigma is not replaceable with self.sigma since it also stands in for 
  # alt_sigma.
  # ^Relevant for older Two_Strats class, not for current Strats class?
  if sigma:
    results = [None for _ in range(trials)]
    for i in range(trials):
      balance = principle
      for j in range(years):
        balance *= np.random.lognormal(mu, sigma)
      results[i] = balance
  else:
    results = [principle * np.exp(mu*years)]
  
  return results

# XXX Get rid of this, integrate it into print_summary()
def summarize(results):
  summary = {
             "mean" : np.mean(results),
             "std_biased" : np.std(results),
             "std_unbiased" : np.std(results, ddof=1),
             }
  
  trials = len(results)

  summary["sem"] = summary["std_unbiased"] / trials ** 0.5  # std error on mean
  # Worth having a SEM function? Scipy has it.
  
  return summary

# XXX No use having this outside class method
def print_summary(summary):
  for x in summary:
    summary[x] = round(summary[x], 2)
  
  print("Mean:", summary["mean"], "+/-", summary["sem"])
  print("Sample standard deviation:", summary["std_unbiased"])
  # std may not be a very useful statistic for a lognormal distribution, may
  # not provide the same intuition as in normal.

def win_rate(results, alt_results):

  trials = len(results)
  win = 0
  
  if len(alt_results) > 1:
    for i in range(trials):
      if results[i] > alt_results[i]:
        win += 1
  else:
    for i in range(trials):
      if results[i] > alt_results[0]:
        win += 1
  
  win /= trials
  win_sem = np.std(int(win*trials)*[1]+int((1-win)*trials)*[0], ddof=1) / \
            trials ** 0.5
  # Is there any significance to sample std dev? (i.e., not SEM)
  # Validate use of this statistic
  # SEM is for uncertainty on the ratio, good for when ratio is based on
  # random sampling. Std dev may still mean something when ratio is computed
  # analytically?
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
    print("---Strat A---")
    print_summary(summarize(results))
    print("\n---Strat B---")
    print_summary(summarize(alt_results))
    # What happens if we summarize len 1 results?
    # ^Output is coherent but has +/- nan for std dev of list with len 1.
    # FIXME nonfatal runtime error from nan std dev
    # TODO Improved handling of sigma=0 strats should be handled by
    # print_summary.
    # XXX this works pretty well for sigma=0 on strat2 but other graphsi
    # are wonky
    # alt_result is strat2.roi_dstr. What does this return when sigma=0?
    # (Returns what we want)
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
  
class Two_Strats:  # From previous draft---not in use.
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
  # TODO method to plot pdf, cdf, etc. along with another strat object passed
  # as arg
  def __init__(self, mu, sigma=0, years=1, principle=1e3, trials=10000):
    self.mu = mu
    self.sigma = sigma
    self.years = years
    self.principle = principle
    self.trials = trials
    # TODO Below could be extracted to recalc (or calc) method.
    # Can roi_dstr be optional in init? Want to initialize object before
    # deciding years
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
    # Can use pdf from scipy.
    x = np.linspace(min(self.roi_dstr), max(self.roi_dstr), 1000)
    years, principle = self.years, self.principle
    mu, sigma = self.mu * years, self.sigma * years**0.5
    # Theoretical PDF, not fit to simulated data.
    pdf = np.exp(-(np.log(x/principle) - mu)**2 / (2 * sigma**2)) / \
          (x/principle * sigma * (2 * np.pi)**0.5) / principle
    return x, pdf  # Return x and pdf for easy plotting.
    # Funny output if dereference is omitted when plotting.
    # Clearer to have one function return x and another return pdf?

  def cdf(self):
    # cdf from scipy? Or implement cdf (analytical)
    # Can produce cdf analytically or numerically
    pass

  def cum_dstr(self, inverse=False):
    # Numerical version of cdf()
    # Cumulative version of roi_dstr
    # Probability of yielding at least x.
    # Use reverse kwarg to give probability of yielding at least some amount.
    # Any use in reversing sort order for other calculations?
    self.roi_dstr.sort() # Check scope.
    # Should we do this earlier?
    x = np.linspace(0, self.roi_dstr[-1], 1000) # max(roi_dstr) if sorted
    # XXX this max makes graphs uneven
    y = [0 for _ in x]
    i = 0
    j = 0
    for i in range(len(x)):
      y[i] = y[i-1]             # 0 on first iter
      while self.roi_dstr[j] < x[i]:
        y[i] += 1
        j += 1
    y = [elm / self.trials for elm in y]
    if inverse:
      y = [1 - elm for elm in y]
    #print(self.years)
    return x, y
    # Funny output if dereference is omitted when plotting.
    #plt.plot(x,y)
    #plt.show()

  def dstr_over_time(self, years=0, normalize=False):
    if not years:
      years = self.years   # Better way to set default?
    # Default year range to years attribute, option to set different range.
    interval = 0.9  # Get the middle 50% of results.
    interval /= 2   # For later arithmetic.
    mid = []
    high = []
    low = []
    curves = [low, mid, high]
    # TODO way to skip years like in yearly_plot
    step = 1
    # FIXME use similar soln to yearly_plot for years messing up in plot if
    # step > 1. Even better: more generalized yearly plot (sub)function.
    #for i in range(step, years, step): # Causes other problems (loop should not start at step or jump.
    # Do functions work as expected if years=0?
    # Faster to start loop at 1 (0 is trivially).
    for i in range(years+1):
      self.recalc(i)
      dstr = self.roi_dstr
      mid.append(np.median(dstr))
      low.append(np.quantile(dstr, 0.5 + interval))
      high.append(np.quantile(dstr, 0.5 - interval))
      # Confirm that curves list is behaving as expected
    for elm in curves:
      # Use nested list comprehension?
      if normalize:
        elm = [_ / self.principle for _ in elm]
        # Confirm the elements are changing as expected
      plt.plot(elm)
    #for i in range(3):
    #  if normalize:
    #    curves[i] = [_ / self.principle for _ in curves[i]]
    #  plt.plot(curves[i])
    #plt.plot(mid)
    #plt.plot(high)
    #plt.plot(low)
    plt.show()

if __name__ == "__main__":
  # TODO another graph can show the ROI for each strat rather than just win rate
  # TODO multiplot to show effect of diff mu, sigma (or plots with diff axes)
  pass








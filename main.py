import numpy as np
import matplotlib.pyplot as plt
import time

# TODO clargs to output compuation time

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
  win_sem = np.std(int(win*trials)*[1]+int((1-win)*trials)*[0]) / trials ** 0.5
  
  print(win, "+/-", round(win_sem,int(np.log10(trials))))

def compare(years):
  #years = 5
  mu = 0.1
  sigma = 0.15
  # exp(0.0488) ~ 1.05
  # exp(0.0677) ~ 1.07
  # exp(0.0793) ~ 1.0825
  alt_mu = 0.05
  alt_sigma = 0
  alt_results = roi_dstr(years, alt_mu, alt_sigma)
  results = roi_dstr(years, mu, sigma)
  summarize(results)
  win_rate(results, alt_results, alt_sigma)

if __name__ == "__main__":
  compare(5)









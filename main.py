import numpy as np
import matplotlib.pyplot as plt
import time

# TODO clargs to output compuation time

years = 5
principle = 1e3
mu = 0.1
sigma = 0.15
trials = 10000
results = [None for _ in range(trials)]

#alt_mu = .0488  # 5% APY
alt_mu = .0793  # 8.25% APY
alt_mu = mu
alt_sigma = 0

start = time.time()

if alt_sigma:
  alt_results = [None for _ in range(trials)]
  for i in range(trials):
    alt_balance = principle
    for j in range(years):
      alt_balance *= np.random.lognormal(alt_mu, alt_sigma)
    alt_results[i] = alt_balance
else:
  alt_results = principle * np.exp(alt_mu*years)# for _ in range(trials)]

stop = time.time()
print("alt loop", stop-start)

start = time.time()

for i in range(trials):
  balance = principle
  for j in range(years):
    balance *= np.random.lognormal(mu, sigma)
  results[i] = balance

stop = time.time()
print("main loop", stop-start)

summary = {
           "mean" : np.mean(results),
           "std_biased" : np.std(results),
           "std_unbiased" : np.std(results, ddof=1),
           }

summary["sem"] = summary["std_unbiased"] / trials ** 0.5  # std error on mean

for x in summary:
  summary[x] = round(summary[x], 2)

print("Mean:", summary["mean"], "+/-", summary["sem"])
print("Sample standard deviation:", summary["std_unbiased"])

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
print("win loop", end - start)

win /= trials
win_sem = np.std(int(win*trials)*[1]+int((1-win)*trials)*[0]) / trials ** 0.5

print(win, "+/-", round(win_sem,int(np.log10(trials))))











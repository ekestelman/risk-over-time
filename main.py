import numpy as np
import matplotlib.pyplot as plt
import time
from scipy.stats import lognorm
from strats_module import *#Two_Strats # * reimports modules?

# TODO clargs to output compuation time
# TODO seperate class or methods for computing results analytically instead of
# numerically. Can compare using numerical integration (Monte Carlo to
# integrate over curves). This is probably faster than numerically computing
# curves and then sampling (try testing comp times). Then numerical approach
# can be kept (or separated) just as validation.
# TODO Prompt user for main args, prompt for desired graph(s), loop until exited
# (store objects to avoid recomputation? --won't work currently for yearly plot,
# may not matter much for analytical calculation.)
# TODO Inputs like: I want minimum p chance of a amount/r rate in t time (output
# best strat) or p chance of a amount (output time for each strat) or a amount in
# t time (output chance).

if __name__ == "__main__":
  # TODO another graph can show the ROI for each strat rather than just win rate
  # TODO multiplot to show effect of diff mu, sigma (or plots with diff axes)
  # Consider click library for inputs
  # TODO print default if no entry
  # TODO show strat parameters on graphs
  years = int(input("Years (int): ") or 10)
  principle = int(input("Principle (int): ") or 1)
  params1 = (input("Mean and standard deviation (space separated): ") or
             "0.18 0.19").split()
  params2 = (input("Mean and standard deviation (space separated): ") or
             "0.13 0.15").split()
  params1 = [float(x) for x in params1]
  params2 = [float(x) for x in params2]
  params1[0] = get_mu(*params1)
  params1[1] = get_sig(*params1)
  params2[0] = get_mu(*params2)
  params2[1] = get_sig(*params2)
  # FIXME mu and sigma are set for log of the lognormal, not the lognormal itself
  # Additional validation: compute mu, sigma of distribution
  # TODO Default to skipping params2? Use 0 0 to skip? Or X?
  benchmark = float(input("Choose benchmark APY: ") or 0.0825)
  # Need a way to opt out of benchmark (input None? 0 should be a valid entry)
  # More standard inputs. Previously 1.0825 is not consistent with other inputs.
  # Will this be treated as APY or APR?
  show = input("What do you want to display?\n" +
               "a) Compare expected value and standard deviation\n" +
               "b) Show growth confidence interval over time\n" +
               "c) Show PDF after time t\n" +
               "d) Show CDF after time t\n" +
               "e) Chance of strat A outperforming strat B over time\n" +
               "> ") or "abcde"
  # TODO we can display analyses in order that they are written?
  # TODO initialize strat objects, promt user for mean and std dev (then ask
  # what to display). See when calculations are performed in objects.
  # save computations.
  #strat1 = Strat(.1, .15, years=years, principle=principle)
  strat1 = Strat(*params1, years=years, principle=principle)
  #strat1.print_summary()
  #strat2 = Strat(.09, .1, years=years, principle=principle)
  strat2 = Strat(*params2, years=years, principle=principle)
  #strat2.print_summary()
  labelA = "$\mu=$"+str(strat1.mu)+", $\sigma=$"+str(strat1.sigma) #"Strat A"
  labelB = "$\mu=$"+str(strat2.mu)+", $\sigma=$"+str(strat2.sigma) #"Strat B"
  if 'a' in show:
    compare(strat1.roi_dstr, strat2.roi_dstr, summary=True)
  # TODO Add function analogous to compare/summary for benchmark.
  # TODO Show yearly mean for verification?
  # Can yearly_plot() still accept sigma=0 strat as argument?
  # TODO exp graph with shaded area of x% confidence interval
  # TODO include growing benchmark in quantile plot
  benchmark = (1+benchmark)**years * principle
  # 1 + benchmark is more consistent with other inputs.
  if 'e' in show:
    yearly_plot(strat1, strat2, 30, 2)
    strat1.recalc(years)
    strat2.recalc(years)
    # Need to recalc after any plot that performs recalc over different years
    # And/or move this later
  # Prompt user for time frame? Make bigger, can zoom anyway?
  # Slow with numerical method...
  # Prompt user for confidence interval? Interactive plot?
  if 'b' in show:
    strat1.dstr_over_time(years=15, normalize=True)
  # Not the best name for this method... quantiles_over_time?
  # TODO Side by side or overlayed plot of both strats? Benchmark?
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
  if 'c' in show:
    plt.hist(strats, 15 * int(strat1.years**0.5), density=True, label=[labelA, labelB])
    # TODO better labels for hist/pdf
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
    plt.plot(x, pdf, label=labelA)
    sp_pdf = lognorm.pdf(x/principle, sigma, scale=np.exp(mu))
    #plt.plot(x, sp_pdf)
    tot_diff = 0
    for i in range(len(pdf)):
      diff = pdf[i] - sp_pdf[i]
      tot_diff += abs(diff)
      #print(pdf[i]); print(sp_pdf[i], diff)
    print(tot_diff)
    #plt.plot(x, lognorm.pdf(x/principle, sigma, scale=np.exp(mu)))
    plt.plot(*strat2.pdf(), label=labelB)
    # Funny output if dereference is omitted
    # TODO make ymax a bit greater than the highest point of either PDF.
    plt.vlines(benchmark, 0, 2*max(pdf), color="black", linestyles="--", label="Benchmark")
    plt.title("PDF")
    plt.xlabel("Amount")
    plt.legend()
    plt.show()
  #for elm in strats:  # Numerically computed CDF
  #  plt.plot(elm.cum_dstr())
  # TODO show points of intersection on CDF plot? (Consider the interpretation
  # of this statistic.)
  if 'd' in show:
    inverse = True # TODO Prompt user or show both plots?
    plt.plot(*strat1.cum_dstr(inverse), label=labelA)  # Maybe strats = [strat1, strat2]
    plt.plot(*strat2.cum_dstr(inverse), label=labelB)
    plt.xlabel("Amount")
    # Math print for ylabel?
    if inverse:
      plt.ylabel("P(>x)")
    else:
      plt.ylabel("P(<x)")
    plt.vlines(benchmark, 0, 1, color="black", linestyles="--")
    plt.title("CDF Complement (chance of ending with at least x)")
    plt.legend()
    plt.show()








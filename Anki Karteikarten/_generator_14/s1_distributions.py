# -*- coding: utf-8 -*-
"""Section 1 - distributions: shape picture + natural context, plus formula cards."""
from plotlib import *

T = "Core distributions"

# ---------------------------------------------------------------------------
# picture cards: (front, svg-builder, back-text, tags)
# ---------------------------------------------------------------------------
PIC = []


def pic(front, builder, back, tags):
    PIC.append((front, builder, back, tags))


# --- Bernoulli -------------------------------------------------------------
def _bernoulli():
    cv = pmf_plot([dict(pts=[(0, 0.7), (1, 0.3)], color="blue")],
                  xlim=(-0.6, 1.6), xlabel="k", ylabel="P(X = k)", xticks=[0, 1],
                  caption=["one trial, two outcomes: the atom every count distribution is built from",
                           "mean p, variance p(1-p) - variance is largest at p = 0.5 and vanishes at 0 or 1"])
    cv.text(0.5, 0.78, "p = 0.3", size=10, opacity=0.8)
    return cv


pic("What does the Bernoulli distribution look like, and where does it arise naturally?",
    _bernoulli,
    "A single yes/no trial: all mass sits on 0 and 1. "
    "Natural context: any one-shot binary outcome - a coin flip, one patient responding or not, "
    "one click or no click, one insurance policy having a claim or not. "
    "It is the building block of the binomial, and the response distribution behind logistic regression.<br><br>"
    "\\[ P(X=k)=p^k(1-p)^{1-k},\\quad k\\in\\{0,1\\},\\qquad E[X]=p,\\ \\operatorname{Var}(X)=p(1-p) \\]",
    f"{T} bernoulli discrete diagram")


# --- Binomial --------------------------------------------------------------
def _binomial():
    cv = pmf_plot([dict(pts=[(k, binom(k, 20, 0.2)) for k in range(21)], color="blue", label="n=20, p=0.2"),
                   dict(pts=[(k, binom(k, 20, 0.5)) for k in range(21)], color="green", label="n=20, p=0.5"),
                   dict(pts=[(k, binom(k, 20, 0.85)) for k in range(21)], color="amber", label="n=20, p=0.85")],
                  xlim=(-0.8, 20.8), xlabel="k successes out of n", ylabel="P(X = k)",
                  xticks=[0, 4, 8, 12, 16, 20], legend_pos=dict(x=250, y=32),
                  caption=["skewed when p is far from 0.5, symmetric at p = 0.5,",
                           "and approximately normal once np and n(1-p) are both large (rule of thumb: > 5)"])
    return cv


pic("What does the binomial distribution look like, and where does it arise naturally?",
    _binomial,
    "Counts out of a <b>known denominator</b>: the number of successes in n independent trials with the same "
    "success probability p. Natural context: 7 of 20 seeds germinating, 12 of 50 patients responding, "
    "number of defective items in a batch of fixed size, number of heads in n tosses.<br><br>"
    "Key requirement: fixed n, independent trials, constant p. If p varies between trials or trials are "
    "clustered, the counts are overdispersed and you need beta-binomial or a random effect instead.<br><br>"
    "\\[ P(X=k)=\\binom{n}{k}p^k(1-p)^{n-k},\\qquad E[X]=np,\\ \\operatorname{Var}(X)=np(1-p) \\]",
    f"{T} binomial discrete diagram")


# --- Poisson ---------------------------------------------------------------
def _poisson():
    cv = pmf_plot([dict(pts=[(k, poisson(k, 1)) for k in range(21)], color="blue", label="λ = 1"),
                   dict(pts=[(k, poisson(k, 4)) for k in range(21)], color="green", label="λ = 4"),
                   dict(pts=[(k, poisson(k, 10)) for k in range(21)], color="amber", label="λ = 10")],
                  xlim=(-0.8, 20.8), xlabel="k events", ylabel="P(X = k)",
                  xticks=[0, 4, 8, 12, 16, 20], legend_pos=dict(x=430, y=32),
                  caption=["mean = variance = λ; strongly skewed for small λ, nearly normal for large λ",
                           "real count data are usually over dispersed (variance > mean) - check before using it"])
    return cv


pic("What does the Poisson distribution look like, and where does it arise naturally?",
    _poisson,
    "Counts with <b>no natural denominator</b>, observed over a fixed window of time, space or exposure. "
    "It is exactly the count of a Poisson process: events occur independently, at a constant rate, "
    "and never simultaneously.<br><br>"
    "Natural context: calls arriving per minute, mutations per genome, goals per match, "
    "insurance claims per policy-year, radioactive decays per second, typos per page.<br><br>"
    "Two derivations worth remembering: it is the limit of the binomial when \\(n\\to\\infty\\), \\(p\\to 0\\) "
    "with \\(np\\to\\lambda\\) (many chances, each tiny), and it is the law of independent increments in "
    "continuous time.<br><br>"
    "\\[ P(X=k)=e^{-\\lambda}\\frac{\\lambda^k}{k!},\\qquad E[X]=\\operatorname{Var}(X)=\\lambda \\]",
    f"{T} poisson discrete counts diagram")


# --- Geometric -------------------------------------------------------------
def _geometric():
    cv = pmf_plot([dict(pts=[(k, geom(k, 0.3)) for k in range(1, 16)], color="blue", label="p = 0.3"),
                   dict(pts=[(k, geom(k, 0.6)) for k in range(1, 16)], color="green", label="p = 0.6")],
                  xlim=(0.2, 15.8), xlabel="k trials until first success", ylabel="P(X = k)",
                  xticks=[1, 3, 5, 7, 9, 11, 13, 15], legend_pos=dict(x=430, y=32),
                  caption=["always monotone decreasing - the first trial is the single most likely success",
                           "memoryless: P(X > s+t | X > s) = P(X > t); no ageing, no wear-out"])
    return cv


pic("What does the geometric distribution look like, and where does it arise naturally?",
    _geometric,
    "The discrete waiting time to the first success, and it is always monotone decreasing. "
    "Natural context: number of interviews until the first offer, number of items inspected until the first "
    "defect, number of attempts until a link is up, length of a run in a Bernoulli sequence.<br><br>"
    "It is the unique <b>memoryless</b> discrete distribution - the discrete twin of the exponential. "
    "That also makes it the geometric-hazard baseline in discrete-time survival models.<br><br>"
    "\\[ P(X=k)=p(1-p)^{k-1},\\ k=1,2,\\dots,\\qquad E[X]=\\tfrac1p,\\ \\operatorname{Var}(X)=\\tfrac{1-p}{p^2} \\]",
    f"{T} geometric discrete waiting-time diagram")


# --- Negative binomial -----------------------------------------------------
def _nbinom():
    cv = pmf_plot([dict(pts=[(k, poisson(k, 4)) for k in range(26)], color="slate", label="Poisson, mean 4"),
                   dict(pts=[(k, nbinom(k, 4, 4 / 8.0)) for k in range(26)], color="blue", label="NB, mean 4, var 8"),
                   dict(pts=[(k, nbinom(k, 1.0, 1 / 5.0)) for k in range(26)], color="rose", label="NB, mean 4, var 20")],
                  xlim=(-0.8, 25.8), xlabel="k events", ylabel="P(X = k)",
                  xticks=[0, 5, 10, 15, 20, 25], legend_pos=dict(x=440, y=30),
                  caption=["same mean as the Poisson but a fatter right tail and more zeros",
                           "as the dispersion parameter grows the negative binomial converges back to the Poisson"])
    return cv


pic("What does the negative binomial distribution look like, and where does it arise naturally?",
    _nbinom,
    "The workhorse for <b>overdispersed counts</b>: same shape family as the Poisson but with variance above "
    "the mean, so it has more zeros and a heavier right tail.<br><br>"
    "Two equally useful readings:<br>"
    "1. <b>Waiting time</b>: number of failures before the r-th success in Bernoulli trials.<br>"
    "2. <b>Gamma-Poisson mixture</b> (the one that matters in modelling): each unit has its own Poisson rate, "
    "and those rates are Gamma-distributed across units. Unobserved heterogeneity in the rate is exactly what "
    "creates the extra variance.<br><br>"
    "Natural context: accidents per driver (drivers differ in proneness), doctor visits per person, "
    "reads per gene in RNA-seq, claims per policy in insurance.<br><br>"
    "\\[ \\operatorname{Var}(Y)=\\mu+\\frac{\\mu^2}{\\theta}\\quad(\\theta\\to\\infty\\ \\Rightarrow\\ \\text{Poisson}) \\]",
    f"{T} negative-binomial overdispersion counts diagram")


# --- Hypergeometric --------------------------------------------------------
def _hyper():
    cv = pmf_plot([dict(pts=[(k, hyper(k, 50, 10, 10)) for k in range(11)], color="blue",
                        label="N=50, K=10, n=10"),
                   dict(pts=[(k, binom(k, 10, 0.2)) for k in range(11)], color="slate",
                        label="binomial n=10, p=0.2")],
                  xlim=(-0.6, 10.6), xlabel="k successes in the sample", ylabel="P(X = k)",
                  xticks=list(range(0, 11, 2)), legend_pos=dict(x=440, y=30),
                  caption=["sampling without replacement: narrower than the binomial (finite-population correction)",
                           "the two coincide when the sample is a tiny fraction of the population (n / N &#8594; 0)"])
    return cv


pic("What does the hypergeometric distribution look like, and where does it arise naturally?",
    _hyper,
    "Successes in a sample drawn <b>without replacement</b> from a finite population - the binomial with the "
    "trials made dependent, so it has the same mean but a smaller variance.<br><br>"
    "Natural context: acceptance sampling from a finished batch, how many of the 10 cards you drew are hearts, "
    "capture-recapture, gene-set enrichment (how many of my hits fall in the pathway), and it is the exact null "
    "distribution behind <b>Fisher's exact test</b> for a 2x2 table with fixed margins.<br><br>"
    "\\[ P(X=k)=\\frac{\\binom{K}{k}\\binom{N-K}{n-k}}{\\binom{N}{n}},\\qquad "
    "\\operatorname{Var}(X)=n\\tfrac{K}{N}\\Big(1-\\tfrac{K}{N}\\Big)\\tfrac{N-n}{N-1} \\]",
    f"{T} hypergeometric discrete finite-population diagram")


# --- Beta-binomial ---------------------------------------------------------
def _betabinom():
    cv = pmf_plot([dict(pts=[(k, binom(k, 20, 0.4)) for k in range(21)], color="slate", label="binomial p=0.4"),
                   dict(pts=[(k, betabinom(k, 20, 4, 6)) for k in range(21)], color="blue", label="beta-bin. a=4, b=6"),
                   dict(pts=[(k, betabinom(k, 20, 0.8, 1.2)) for k in range(21)], color="rose", label="beta-bin. a=0.8, b=1.2")],
                  xlim=(-0.8, 20.8), xlabel="k successes out of 20", ylabel="P(X = k)",
                  xticks=[0, 4, 8, 12, 16, 20], legend_pos=dict(x=440, y=30),
                  caption=["clusters differ in their own success probability, so the counts spread out",
                           "small a, b &#8594; nearly U-shaped: groups are mostly all-success or all-failure"])
    return cv


pic("What does the beta-binomial distribution look like, and where does it arise naturally?",
    _betabinom,
    "A binomial whose success probability varies from cluster to cluster, with p drawn from a Beta. "
    "That mixing inflates the variance, so it is the standard model for <b>overdispersed proportions</b>.<br><br>"
    "Natural context: litters of animals where pups within a litter are correlated, seeds per pot, "
    "click-through per user, exam items per school, any 'k out of n' where the n units share something unobserved. "
    "Its variance carries the intra-cluster correlation, which is why a random-intercept binomial GLMM does a "
    "similar job.<br><br>"
    "\\[ \\operatorname{Var}(Y)=np(1-p)\\big[1+(n-1)\\rho\\big],\\qquad \\rho=\\frac{1}{a+b+1} \\]",
    f"{T} beta-binomial overdispersion proportions diagram")


# --- Zipf / power law ------------------------------------------------------
def _zipf():
    cv = Canvas(w=460, h=270)
    ks = list(range(1, 61))
    xs = [math.log10(k) for k in ks]
    y1 = [math.log10(zipf(k, 1.0)) for k in ks]
    y2 = [math.log10(zipf(k, 2.0)) for k in ks]
    lam = 6.0
    y3 = [math.log10(poisson(k, lam)) for k in ks if poisson(k, lam) > 1e-12]
    x3 = [math.log10(k) for k in ks if poisson(k, lam) > 1e-12]
    cv.limits((0, math.log10(60)), (-8, 0))
    cv.axes(xlabel="log10 rank k", ylabel="log10 P(k)",
            xticks=[0, 0.5, 1, 1.5], yticks=[0, -2, -4, -6, -8])
    cv.path(list(zip(xs, y1)), color=C["blue"], width=1.9)
    cv.path(list(zip(xs, y2)), color=C["violet"], width=1.9)
    cv.path(list(zip(x3, y3)), color=C["slate"], width=1.6, dash="4 3")
    cv.legend([("Zipf s = 1", C["blue"]), ("Zipf s = 2", C["violet"]),
               ("Poisson λ = 6", C["slate"], "4 3")], x=440, y=30)
    cv.caption(["straight line on a log-log plot = power law; the Poisson falls off a cliff instead",
                "heavy tail: the largest observation is not an outlier, it is the shape of the distribution"])
    return cv


pic("What does a power-law (Zipf) distribution look like on a log-log plot, and where does it arise naturally?",
    _zipf,
    "A <b>straight line on a log-log plot</b> - that is the defining signature. The probability of an outcome "
    "falls off as a power of its size, not exponentially, so extreme values stay far more likely than any "
    "light-tailed distribution would allow.<br><br>"
    "Natural context: word frequencies (Zipf's law), city sizes, wealth and income tails, firm sizes, "
    "citations, node degrees in networks, file sizes, earthquake magnitudes (Gutenberg-Richter), "
    "word-of-mouth and sales rankings.<br><br>"
    "Why it appears: <b>scale invariance</b>. Mechanisms that generate it are multiplicative growth with a "
    "floor, preferential attachment ('rich get richer'), self-organised criticality, and optimisation under "
    "cost. Because it is scale-free, there is no typical size - the mean is a poor summary and moments above "
    "\\(s-1\\) do not exist.<br><br>"
    "\\[ P(K=k)\\propto k^{-s}\\ \\Longleftrightarrow\\ \\log P=-s\\log k+c \\]",
    f"{T} power-law zipf heavy-tails diagram")


# --- Uniform ---------------------------------------------------------------
def _uniform():
    cv = density_plot([dict(f=lambda x: uniform_pdf(x, 0, 1), color="blue", label="U(0, 1)")],
                      (-0.35, 1.35), xlabel="x", ylabel="density",
                      xticks=[0, 0.25, 0.5, 0.75, 1], ymax=1.45,
                      caption=["flat: every value in the interval is equally likely; maximum entropy on [a, b]",
                               "F(X) ~ U(0,1) for any continuous X - the basis of inverse-CDF sampling, QQ plots and p-values"])
    return cv


pic("What does the uniform distribution look like, and where does it arise naturally?",
    _uniform,
    "Flat over an interval, zero outside - the maximum-entropy distribution when all you know is the range.<br><br>"
    "Natural context: rounding error, the phase of an arriving signal, a randomised time within a day, "
    "position of a random point on a line.<br><br>"
    "Its real importance is technical, through the <b>probability integral transform</b>: if X is continuous "
    "with CDF F, then F(X) is standard uniform. That single fact gives you inverse-CDF simulation, uniform "
    "residuals for model checking (as DHARMa uses), the null distribution of a valid p-value, "
    "and the theory behind QQ plots and the Kolmogorov-Smirnov test.<br><br>"
    "\\[ f(x)=\\frac{1}{b-a}\\ \\text{on }[a,b],\\qquad E[X]=\\frac{a+b}{2},\\ \\operatorname{Var}(X)=\\frac{(b-a)^2}{12} \\]",
    f"{T} uniform continuous diagram")


# --- Normal ----------------------------------------------------------------
def _normal():
    cv = density_plot([dict(f=lambda x: normal(x, 0, 1), color="blue", label="σ = 1"),
                       dict(f=lambda x: normal(x, 0, 0.6), color="green", label="σ = 0.6"),
                       dict(f=lambda x: normal(x, 0, 2), color="amber", label="σ = 2")],
                      (-6, 6), xlabel="x", ylabel="density", xticks=[-6, -4, -2, 0, 2, 4, 6],
                      legend_pos=dict(x=440, y=30),
                      caption=["symmetric, thin-tailed: 68 / 95 / 99.7 % within 1 / 2 / 3 σ",
                               "tails die like exp(-x²/2), so genuinely large deviations are effectively impossible"])
    cv.line(-1, 0, -1, normal(-1), color=C["blue"], width=1, dash="3 3", opacity=0.6)
    cv.line(1, 0, 1, normal(1), color=C["blue"], width=1, dash="3 3", opacity=0.6)
    return cv


pic("What does the normal distribution look like, and where does it arise naturally?",
    _normal,
    "The symmetric bell: light exponential-square tails, fully described by mean and variance.<br><br>"
    "Why it appears everywhere: the <b>central limit theorem</b>. Anything that is a sum of many small, "
    "roughly independent contributions ends up approximately normal regardless of the parts - measurement "
    "error, height, aggregate demand, average of many observations, estimator sampling distributions.<br><br>"
    "It is also the maximum-entropy distribution for a given mean and variance, which is why it is the honest "
    "default when you only want to commit to a location and a spread.<br><br>"
    "Warning: it is a poor model for anything <b>multiplicative</b> (use lognormal), bounded, or heavy-tailed "
    "(financial returns, city sizes). Under normality the mean is the efficient estimator; under heavy tails "
    "it is not.<br><br>"
    "\\[ f(x)=\\frac{1}{\\sqrt{2\\pi}\\sigma}\\exp\\!\\Big(\\!-\\frac{(x-\\mu)^2}{2\\sigma^2}\\Big) \\]",
    f"{T} normal gaussian continuous clt diagram")


# --- Lognormal -------------------------------------------------------------
def _lognormal():
    cv = density_plot([dict(f=lambda x: lognormal(x, 0, 0.4), color="blue", label="σ = 0.4"),
                       dict(f=lambda x: lognormal(x, 0, 0.8), color="green", label="σ = 0.8"),
                       dict(f=lambda x: lognormal(x, 0, 1.4), color="rose", label="σ = 1.4")],
                      (0, 6), xlabel="x", ylabel="density", xticks=[0, 1, 2, 3, 4, 5, 6],
                      legend_pos=dict(x=440, y=30),
                      caption=["positive, right-skewed, mode < median < mean; log of it is exactly normal",
                               "products of many independent positive factors &#8594; lognormal (multiplicative CLT)"])
    return cv


pic("What does the lognormal distribution look like, and where does it arise naturally?",
    _lognormal,
    "Positive, right-skewed, with a long upper tail; taking logs makes it exactly normal.<br><br>"
    "Why: the <b>multiplicative CLT</b>. If a quantity is the product of many independent positive factors, "
    "its log is a sum, so its log is normal. Anything that grows by percentages rather than by increments "
    "lands here.<br><br>"
    "Natural context: incomes and wealth (bulk of the distribution), particle and droplet sizes, "
    "insurance claim severities, biological concentrations, reaction and survival times, city populations, "
    "stock prices under geometric Brownian motion.<br><br>"
    "Practical consequence: the mean is not \\(e^{\\mu}\\). Back-transforming a fitted log-scale mean gives the "
    "<b>median</b>, and you need the variance correction to get the mean - the usual trap when reporting "
    "predictions from a log-transformed regression.<br><br>"
    "\\[ E[X]=e^{\\mu+\\sigma^2/2},\\qquad \\text{median}=e^{\\mu},\\qquad \\text{mode}=e^{\\mu-\\sigma^2} \\]",
    f"{T} lognormal continuous skewed diagram")


# --- Exponential -----------------------------------------------------------
def _expon():
    cv = density_plot([dict(f=lambda x: expon(x, 1.0), color="blue", label="rate 1"),
                       dict(f=lambda x: expon(x, 0.5), color="green", label="rate 0.5"),
                       dict(f=lambda x: expon(x, 2.0), color="amber", label="rate 2")],
                      (0, 6), xlabel="t (waiting time)", ylabel="density",
                      xticks=[0, 1, 2, 3, 4, 5, 6], legend_pos=dict(x=440, y=30),
                      caption=["constant hazard: the only continuous distribution with no memory",
                               "inter-arrival times of a Poisson process are exactly exponential"])
    return cv


pic("What does the exponential distribution look like, and where does it arise naturally?",
    _expon,
    "Monotone decreasing on the positive half-line - the continuous waiting time with <b>constant hazard</b>.<br><br>"
    "It is the unique memoryless continuous distribution: a component that has already survived an hour is "
    "exactly as likely to fail in the next minute as a brand-new one. No ageing, no wear-out, no burn-in.<br><br>"
    "Natural context: time between arrivals in a Poisson process (calls, customers, decays), time to failure "
    "of an electronic part in its flat useful-life phase, service times in basic queueing models, "
    "and time to an event in the simplest survival models.<br><br>"
    "It is also maximum entropy on \\([0,\\infty)\\) for a fixed mean. If the hazard is clearly not constant, "
    "generalise to Weibull (monotone hazard) or Gamma.<br><br>"
    "\\[ f(t)=\\lambda e^{-\\lambda t},\\quad S(t)=e^{-\\lambda t},\\quad h(t)=\\lambda,\\qquad "
    "E[T]=\\operatorname{sd}(T)=1/\\lambda \\]",
    f"{T} exponential continuous hazard waiting-time diagram")


# --- Gamma -----------------------------------------------------------------
def _gamma():
    cv = density_plot([dict(f=lambda x: gamma_pdf(x, 1, 1), color="slate", label="shape 1 (= exponential)"),
                       dict(f=lambda x: gamma_pdf(x, 2, 1), color="blue", label="shape 2"),
                       dict(f=lambda x: gamma_pdf(x, 5, 1), color="green", label="shape 5"),
                       dict(f=lambda x: gamma_pdf(x, 9, 1), color="amber", label="shape 9")],
                      (0, 16), xlabel="x", ylabel="density", xticks=[0, 4, 8, 12, 16],
                      legend_pos=dict(x=445, y=28), ymax=1.15,
                      caption=["sum of k independent exponentials; grows more symmetric as the shape increases",
                               "constant coefficient of variation 1/&#8730;k - the multiplicative-error scale"])
    return cv


pic("What does the Gamma distribution look like, and where does it arise naturally?",
    _gamma,
    "A flexible positive, right-skewed family: at shape 1 it is the exponential, and it becomes increasingly "
    "symmetric as the shape grows.<br><br>"
    "Two derivations: it is the <b>sum of k independent exponentials</b> (waiting time until the k-th event of "
    "a Poisson process - the Erlang case for integer k), and it is the conjugate prior for a Poisson rate, "
    "which is how it enters the Gamma-Poisson mixture behind the negative binomial.<br><br>"
    "Natural context: rainfall amounts, insurance claim sizes, time to complete k sequential steps, "
    "service and repair times, and any strictly positive response whose spread grows with its level - "
    "since the coefficient of variation is constant, a Gamma GLM with log link is the natural model for "
    "<b>proportional (multiplicative) error</b>.<br><br>"
    "\\[ E[X]=\\frac{k}{\\lambda},\\quad \\operatorname{Var}(X)=\\frac{k}{\\lambda^2},\\quad "
    "\\operatorname{CV}=\\frac{1}{\\sqrt{k}}\\qquad(\\text{GLM variance }\\propto\\mu^2) \\]",
    f"{T} gamma continuous positive-skew diagram")


# --- Chi-square ------------------------------------------------------------
def _chisq():
    cv = density_plot([dict(f=lambda x: chisq(x, 1), color="rose", label="df = 1"),
                       dict(f=lambda x: chisq(x, 3), color="blue", label="df = 3"),
                       dict(f=lambda x: chisq(x, 6), color="green", label="df = 6"),
                       dict(f=lambda x: chisq(x, 12), color="amber", label="df = 12")],
                      (0, 26), xlabel="x", ylabel="density", xticks=[0, 5, 10, 15, 20, 25],
                      legend_pos=dict(x=445, y=28), ymax=0.30,
                      caption=["mean = df, variance = 2 df; the mode moves right as df grows",
                               "one-sided by construction - test statistics reject in the right tail only"])
    return cv


pic("What does the chi-square distribution look like, and where does it arise naturally?",
    _chisq,
    "Positive and right-skewed, becoming more symmetric as the degrees of freedom grow. "
    "It is the distribution of a <b>sum of squared standard normals</b>.<br><br>"
    "That is why it shows up whenever a statistic is a squared distance or a quadratic form:<br>"
    "- the scaled sample variance \\((n-1)s^2/\\sigma^2\\) under normality;<br>"
    "- Pearson's goodness-of-fit and independence statistics for contingency tables;<br>"
    "- the asymptotic null distribution of the <b>likelihood ratio, Wald and score tests</b> "
    "(Wilks' theorem), with df equal to the number of restrictions;<br>"
    "- the numerator and denominator of an F statistic.<br><br>"
    "\\[ \\sum_{i=1}^{k}Z_i^2\\sim\\chi^2_k,\\qquad E=k,\\ \\operatorname{Var}=2k \\]",
    f"{T} chi-square continuous testing diagram")


# --- Student t -------------------------------------------------------------
def _t():
    cv = density_plot([dict(f=lambda x: student_t(x, 1), color="rose", label="df = 1 (Cauchy)"),
                       dict(f=lambda x: student_t(x, 3), color="amber", label="df = 3"),
                       dict(f=lambda x: student_t(x, 10), color="green", label="df = 10"),
                       dict(f=lambda x: normal(x, 0, 1), color="slate", label="normal", dash="4 3")],
                      (-5, 5), xlabel="x", ylabel="density", xticks=[-5, -3, -1, 1, 3, 5],
                      legend_pos=dict(x=445, y=28), fill_first=False,
                      caption=["same bell shape, heavier tails and a lower peak; &#8594; normal as df &#8594; &#8734;",
                               "df 1: no mean. df 2: no variance. Moment k exists only if df > k."])
    return cv


pic("What does the Student t distribution look like, and where does it arise naturally?",
    _t,
    "Symmetric and bell-shaped like the normal, but with <b>heavier tails</b> and a flatter peak; it converges "
    "to the normal as the degrees of freedom grow (already close by df ≈ 30).<br><br>"
    "It arises when you standardise a normal mean by an <b>estimated</b> standard deviation: the extra "
    "uncertainty in \\(s\\) widens the tails, which is exactly why t-tests and regression coefficient tests "
    "use t rather than z in small samples.<br><br>"
    "Second use: as a <b>model</b> rather than a null distribution. Since t is a scale mixture of normals "
    "(normal divided by an independent chi-based scale), it is the standard robust error distribution for data "
    "with occasional outliers - t-regression, robust state-space models, and heavy-tailed priors.<br><br>"
    "\\[ T=\\frac{Z}{\\sqrt{V/k}}\\sim t_k,\\qquad \\operatorname{Var}(T)=\\frac{k}{k-2}\\ (k>2) \\]",
    f"{T} student-t continuous testing robustness diagram")


# --- F ---------------------------------------------------------------------
def _f():
    cv = density_plot([dict(f=lambda x: f_pdf(x, 1, 10), color="rose", label="F(1, 10)"),
                       dict(f=lambda x: f_pdf(x, 5, 10), color="blue", label="F(5, 10)"),
                       dict(f=lambda x: f_pdf(x, 10, 30), color="green", label="F(10, 30)"),
                       dict(f=lambda x: f_pdf(x, 30, 100), color="amber", label="F(30, 100)")],
                      (0, 4.5), xlabel="x", ylabel="density", xticks=[0, 1, 2, 3, 4],
                      legend_pos=dict(x=445, y=28), ymax=1.35,
                      caption=["centred near 1 under the null; concentrates around 1 as both df grow",
                               "F(1, k) = t_k squared, and k·F(k, &#8734;) &#8594; chi-square with k df"])
    return cv


pic("What does the F distribution look like, and where does it arise naturally?",
    _f,
    "Positive and right-skewed, with mass concentrating near 1 as the degrees of freedom grow. "
    "It is the distribution of a <b>ratio of two independent chi-squares</b>, each divided by its df.<br><br>"
    "So it appears wherever you compare two variances or two sums of squares:<br>"
    "- <b>ANOVA</b>: between-group mean square over within-group mean square;<br>"
    "- <b>nested model comparison</b> in linear regression: the extra sum of squares per extra parameter, "
    "over the residual mean square;<br>"
    "- tests for equality of two variances (very sensitive to non-normality);<br>"
    "- the Wald F test of a general linear hypothesis.<br><br>"
    "Useful identities: \\(F_{1,k}=t_k^2\\), and \\(k_1F_{k_1,k_2}\\to\\chi^2_{k_1}\\) as \\(k_2\\to\\infty\\) - "
    "the F test is the finite-sample version of a chi-square test with the error variance estimated.<br><br>"
    "\\[ F=\\frac{U_1/k_1}{U_2/k_2},\\qquad U_i\\sim\\chi^2_{k_i}\\ \\text{independent} \\]",
    f"{T} f-distribution continuous anova testing diagram")


# --- Beta ------------------------------------------------------------------
def _beta():
    cv = density_plot([dict(f=lambda x: beta_pdf(x, 1, 1), color="slate", label="1, 1 (uniform)"),
                       dict(f=lambda x: beta_pdf(x, 2, 5), color="blue", label="2, 5"),
                       dict(f=lambda x: beta_pdf(x, 5, 5), color="green", label="5, 5"),
                       dict(f=lambda x: beta_pdf(x, 0.5, 0.5), color="rose", label="0.5, 0.5")],
                      (0, 1), xlabel="x", ylabel="density", xticks=[0, 0.25, 0.5, 0.75, 1],
                      legend_pos=dict(x=445, y=28), ymax=3.4, fill_first=False,
                      caption=["supported on (0,1): can be bell-shaped, skewed, flat, J-shaped or U-shaped",
                               "a, b < 1 gives a U shape - mass piles up at both ends"])
    return cv


pic("What does the Beta distribution look like, and where does it arise naturally?",
    _beta,
    "The all-purpose distribution on the unit interval: depending on its two shape parameters it can be flat, "
    "bell-shaped, skewed either way, J-shaped or U-shaped.<br><br>"
    "Natural context: anything that <b>is</b> a proportion rather than a count of successes - percentage of "
    "budget spent, fraction of area covered, loss given default, sports win rates, "
    "test scores rescaled to (0,1). That is the domain of <b>beta regression</b>.<br><br>"
    "Technical roles: it is the <b>conjugate prior for a binomial probability</b> (posterior is "
    "Beta(a+k, b+n-k), so a and b read as prior successes and failures); it is the distribution of the "
    "<b>order statistics of uniforms</b>, hence the reference line and confidence bands in a QQ plot; "
    "and mixing it into a binomial gives the beta-binomial.<br><br>"
    "\\[ f(x)=\\frac{x^{a-1}(1-x)^{b-1}}{B(a,b)},\\qquad E[X]=\\frac{a}{a+b},\\ "
    "\\operatorname{Var}=\\frac{ab}{(a+b)^2(a+b+1)} \\]",
    f"{T} beta continuous proportions diagram")


# --- Weibull ---------------------------------------------------------------
def _weibull():
    cv = Canvas(w=460, h=270)
    # top: densities; we instead show hazards, which is the informative part
    cv.limits((0, 3), (0, 3.2))
    cv.axes(xlabel="t", ylabel="hazard h(t)", xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3],
            yticks=[0, 1, 2, 3])
    for shape, col, lab in ((0.6, "blue", "k = 0.6  decreasing (infant mortality)"),
                            (1.0, "slate", "k = 1  constant (exponential)"),
                            (2.0, "green", "k = 2  increasing linearly"),
                            (3.5, "rose", "k = 3.5  strong wear-out")):
        pts = [(t, (shape / 1.0) * (t / 1.0) ** (shape - 1)) for t in
               [0.02 + 2.98 * i / 200 for i in range(201)]]
        pts = [(x, y) for x, y in pts if y <= 3.2]
        cv.path(pts, color=C[col], width=1.9, dash="4 3" if shape == 1 else None)
    cv.legend([("k = 0.6", C["blue"]), ("k = 1", C["slate"], "4 3"),
               ("k = 2", C["green"]), ("k = 3.5", C["rose"])], x=445, y=28)
    cv.caption(["the shape parameter k is the whole story: k<1 wears in, k=1 memoryless, k>1 wears out",
                "h(t) = (k/λ)(t/λ)^(k-1) - a power-law hazard, hence a straight line on a log-log hazard plot"])
    return cv


pic("What does the Weibull hazard look like, and where does the Weibull distribution arise naturally?",
    _weibull,
    "The Weibull is the exponential generalised to a <b>monotone power-law hazard</b>, and the shape parameter "
    "k decides the whole story: k < 1 means a decreasing hazard (early failures, infant mortality), k = 1 is "
    "the constant-hazard exponential, k > 1 means an increasing hazard (ageing, wear-out).<br><br>"
    "Why it appears: it is the <b>extreme-value limit for minima</b> - the weakest-link law. If a system fails "
    "when its weakest of many components fails, the failure time is Weibull. That is the classic derivation "
    "for material strength and fatigue.<br><br>"
    "Natural context: component and machine lifetimes, material strength, wind-speed distributions, "
    "time-to-event data in survival analysis (it is the only model that is both proportional-hazards <b>and</b> "
    "accelerated-failure-time), and reliability engineering generally.<br><br>"
    "\\[ S(t)=\\exp\\!\\big(-(t/\\lambda)^{k}\\big),\\qquad h(t)=\\frac{k}{\\lambda}\\Big(\\frac{t}{\\lambda}\\Big)^{k-1} \\]",
    f"{T} weibull continuous survival hazard diagram")


# --- Pareto ----------------------------------------------------------------
def _pareto():
    cv = density_plot([dict(f=lambda x: pareto(x, 1.0), color="rose", label="α = 1"),
                       dict(f=lambda x: pareto(x, 2.0), color="blue", label="α = 2"),
                       dict(f=lambda x: pareto(x, 3.0), color="green", label="α = 3"),
                       dict(f=lambda x: expon(x - 1, 1.0) if x >= 1 else 0.0, color="slate",
                            label="exponential", dash="4 3")],
                      (0.8, 6), xlabel="x", ylabel="density", xticks=[1, 2, 3, 4, 5, 6],
                      legend_pos=dict(x=445, y=28), fill_first=False, ymax=3.4,
                      caption=["tail falls off polynomially, not exponentially - extremes remain plausible",
                               "α ≤ 1: infinite mean. α ≤ 2: infinite variance. The sample mean stops being meaningful."])
    return cv


pic("What does the Pareto distribution look like, and where does it arise naturally?",
    _pareto,
    "A continuous power law on \\([x_m,\\infty)\\): monotone decreasing with a <b>polynomially heavy tail</b>, "
    "so the largest observations dominate everything.<br><br>"
    "Natural context: the upper tail of income and wealth (the original 80/20 observation), city sizes, "
    "firm sizes, large insurance losses and operational-risk losses, file and packet sizes, "
    "the tail of any preferential-attachment process.<br><br>"
    "Consequences you must remember: the mean exists only if α > 1 and the variance only if α > 2, so sample "
    "means and standard errors can be worthless; the CLT converges extremely slowly or not at all; and "
    "'remove the outlier' destroys the signal, because the extremes <b>are</b> the distribution. "
    "In extreme-value theory the <b>generalised Pareto</b> is the limit law for peaks over a high threshold.<br><br>"
    "\\[ S(x)=\\Big(\\frac{x_m}{x}\\Big)^{\\alpha},\\qquad E[X]=\\frac{\\alpha x_m}{\\alpha-1}\\ (\\alpha>1) \\]",
    f"{T} pareto power-law heavy-tails continuous diagram")


# --- Cauchy / Laplace / Logistic comparison -------------------------------
def _heavy_light():
    cv = density_plot([dict(f=lambda x: normal(x, 0, 1), color="slate", label="normal"),
                       dict(f=lambda x: laplace(x, 0, 1), color="blue", label="Laplace"),
                       dict(f=lambda x: logistic_pdf(x, 0, 0.55), color="green", label="logistic"),
                       dict(f=lambda x: cauchy(x, 0, 1), color="rose", label="Cauchy")],
                      (-5, 5), xlabel="x", ylabel="density", xticks=[-5, -3, -1, 1, 3, 5],
                      legend_pos=dict(x=445, y=28), fill_first=False, ymax=0.62,
                      caption=["Laplace: peaked at 0 with exponential tails. Cauchy: no mean, enormous tails.",
                               "logistic sits just above the normal in the tails - hence logit ≈ probit × 1.7"])
    return cv


pic("How do the normal, Laplace, logistic and Cauchy densities compare, and when is each the right error distribution?",
    _heavy_light,
    "All four are symmetric and unimodal; they differ in how much tail they allow.<br><br>"
    "<b>Normal</b> - tails \\(e^{-x^2}\\): sums of many small effects, MLE = least squares / mean.<br>"
    "<b>Logistic</b> - slightly heavier tails, and the latent error whose threshold-crossing gives the "
    "<b>logit</b> model; also the sigmoid growth curve.<br>"
    "<b>Laplace</b> - a sharp peak with exponential tails: it is the difference of two exponentials, "
    "its MLE is the <b>median</b> (L1 loss), and as a prior it produces the lasso. Good for data with "
    "occasional moderate outliers and for quantile-style modelling.<br>"
    "<b>Cauchy</b> - the ratio of two independent normals: <b>no mean and no variance</b>. The sample mean of "
    "n draws is distributed exactly like a single draw, so averaging buys you nothing. Used as a deliberately "
    "vague heavy-tailed prior (half-Cauchy for scale parameters) and as a stress test for robustness.",
    f"{T} normal laplace logistic cauchy tails diagram")


# --- Gumbel / extreme value -----------------------------------------------
def _gumbel():
    cv = density_plot([dict(f=lambda x: gumbel(x, 0, 1), color="blue", label="Gumbel (max)"),
                       dict(f=lambda x: normal(x, 0, 1), color="slate", label="normal", dash="4 3")],
                      (-4, 6), xlabel="x", ylabel="density", xticks=[-4, -2, 0, 2, 4, 6],
                      legend_pos=dict(x=445, y=28), fill_first=True, ymax=0.55,
                      caption=["right-skewed: a maximum can be surprisingly large but not surprisingly small",
                               "block maxima of light-tailed data converge to Gumbel (EV type I)"])
    return cv


pic("What does the Gumbel distribution look like, and where does it arise naturally?",
    _gumbel,
    "A right-skewed bell: the limit law for the <b>maximum</b> of many independent light-tailed variables "
    "(extreme value type I). Asymmetry is the point - a block maximum can overshoot far more easily than it "
    "can undershoot.<br><br>"
    "Natural context: annual maximum river level, rainfall or wind speed, record temperatures, "
    "peak load on a network, largest claim of the year. Fitting maxima of blocks is the 'block maxima' "
    "approach; the general family is the <b>GEV</b>, which nests Gumbel (light tail), Fréchet (heavy tail, "
    "from power-law data) and reversed Weibull (bounded tail).<br><br>"
    "A second, very different appearance: if the utility errors in a discrete choice model are iid Gumbel, "
    "the choice probabilities are exactly <b>multinomial logit</b> - that is where the softmax comes from.<br><br>"
    "\\[ F(x)=\\exp\\!\\big(-e^{-(x-\\mu)/\\beta}\\big) \\]",
    f"{T} gumbel extreme-value continuous diagram")


# --- Inverse Gaussian -----------------------------------------------------
def _invgauss():
    cv = density_plot([dict(f=lambda x: invgauss(x, 1, 1), color="blue", label="μ=1, λ=1"),
                       dict(f=lambda x: invgauss(x, 1, 3), color="green", label="μ=1, λ=3"),
                       dict(f=lambda x: invgauss(x, 1, 0.4), color="rose", label="μ=1, λ=0.4")],
                      (0, 3.2), xlabel="t", ylabel="density", xticks=[0, 0.5, 1, 1.5, 2, 2.5, 3],
                      legend_pos=dict(x=445, y=28), ymax=1.9,
                      caption=["strongly right-skewed positive density; GLM variance function is μ³",
                               "first time a Brownian motion with drift reaches a fixed barrier"])
    return cv


pic("What does the inverse Gaussian distribution look like, and where does it arise naturally?",
    _invgauss,
    "A sharply right-skewed density on the positive half-line, more extreme in its skew than the Gamma at the "
    "same mean.<br><br>"
    "Its natural derivation is a <b>first-passage time</b>: the time at which a Brownian motion with positive "
    "drift first hits a fixed barrier. That makes it the canonical model for accumulation-to-threshold "
    "processes - reaction times in psychology (the Wald model), time until a tumour reaches detectable size, "
    "time to accumulate enough damage to fail.<br><br>"
    "In GLM terms it is the exponential-family member with variance function \\(\\mu^3\\), so it is the choice "
    "when a positive response's spread grows even faster than the Gamma's \\(\\mu^2\\) allows.<br><br>"
    "\\[ E[T]=\\mu,\\qquad \\operatorname{Var}(T)=\\mu^3/\\lambda \\]",
    f"{T} inverse-gaussian continuous glm diagram")


# --- Multivariate normal --------------------------------------------------
def _mvn():
    cv = Canvas(w=460, h=270, pad=(46, 14, 34, 16))
    cv.limits((-3.4, 3.4), (-2.6, 2.6))
    cv.axes(xlabel="x", ylabel="y", xticks=[-3, -2, -1, 0, 1, 2, 3], yticks=[-2, -1, 0, 1, 2],
            y_axis=False)
    cv.line(-3.4, 0, 3.4, 0, width=1, opacity=0.35)
    cv.line(0, -2.6, 0, 2.6, width=1, opacity=0.35)
    # rotated ellipses for rho = 0.7
    rho, sx, sy = 0.7, 1.0, 0.8
    for scale, op in ((1.0, 0.30), (1.7, 0.18), (2.4, 0.10)):
        pts = []
        for i in range(101):
            th = 2 * math.pi * i / 100
            # cholesky of covariance
            a, b = sx, 0.0
            c, d = rho * sy, sy * math.sqrt(1 - rho ** 2)
            u, v = math.cos(th) * scale, math.sin(th) * scale
            pts.append((a * u, c * u + d * v))
        cv.path(pts, color=C["blue"], width=1.5, fill=C["blue"], fo=op, close_to=None)
        cv.raw(f'<path d="M' + " L".join(f"{n(cv.X(x))},{n(cv.Y(y))}" for x, y in pts) +
               f' Z" fill="{C["blue"]}" fill-opacity="{op*0.35}" stroke="none"/>')
    cv.line(-2.6, -0.7 * 2.6 * 0.8, 2.6, 0.7 * 2.6 * 0.8, color=C["rose"], width=1.4, dash="4 3")
    cv.text(400, 40, "ρ = 0.7", size=10, opacity=0.85, data=False, anchor="end")
    cv.text(400, 56, "E[Y|X=x] is linear in x", size=9, opacity=0.75, data=False, anchor="end",
            color=C["rose"])
    cv.caption(["elliptical contours; the tilt is the correlation, the axes are the eigenvectors of Σ",
                "all marginals and all conditionals are again normal - the property that makes it tractable"])
    return cv


pic("What does the bivariate normal distribution look like, and which properties make it so central?",
    _mvn,
    "Elliptical contours whose orientation is the correlation and whose principal axes are the eigenvectors of "
    "the covariance matrix (that is exactly what PCA extracts).<br><br>"
    "The properties that make it the backbone of multivariate statistics:<br>"
    "- every <b>marginal</b> and every <b>conditional</b> is again normal;<br>"
    "- \\(E[Y\\mid X=x]\\) is <b>linear</b> in x, with slope \\(\\rho\\sigma_y/\\sigma_x\\) - linear regression is "
    "exactly right here;<br>"
    "- uncorrelated <b>implies</b> independent (only in the joint normal case);<br>"
    "- linear combinations stay normal, which is where OLS inference, mixed models and Kalman filters come "
    "from.<br><br>"
    "\\[ Y\\mid X=x\\ \\sim\\ N\\!\\Big(\\mu_y+\\rho\\tfrac{\\sigma_y}{\\sigma_x}(x-\\mu_x),\\ "
    "\\sigma_y^2(1-\\rho^2)\\Big) \\]",
    f"{T} multivariate-normal continuous diagram")


# --- Mixture --------------------------------------------------------------
def _mixture():
    f = lambda x: 0.6 * normal(x, -1.2, 0.7) + 0.4 * normal(x, 2.2, 1.1)
    cv = density_plot([dict(f=f, color="blue", label="mixture"),
                       dict(f=lambda x: 0.6 * normal(x, -1.2, 0.7), color="green",
                            label="60 % · N(-1.2, 0.7²)", dash="4 3"),
                       dict(f=lambda x: 0.4 * normal(x, 2.2, 1.1), color="amber",
                            label="40 % · N(2.2, 1.1²)", dash="4 3")],
                      (-4, 6), xlabel="x", ylabel="density", xticks=[-4, -2, 0, 2, 4, 6],
                      legend_pos=dict(x=445, y=28), fill_first=False, ymax=0.42,
                      caption=["bimodality is a symptom of an omitted grouping variable",
                               "fit with EM (or as a latent-class model); do not average the two modes away"])
    return cv


pic("What does a mixture distribution look like, and what does multimodality usually tell you?",
    _mixture,
    "A weighted sum of component densities. Two well-separated components give a visibly bimodal shape; "
    "closer components just look skewed or fat-tailed.<br><br>"
    "Interpretation: a mixture is what you see when a <b>latent grouping variable is missing</b> from the "
    "model - two machines, two disease subtypes, treated and untreated units, fraudulent and honest "
    "transactions. The single overall mean sits between the modes and describes nobody.<br><br>"
    "Uses: model-based clustering and latent-class analysis (fit by EM), heavy-tail and outlier modelling "
    "(a scale mixture of normals is exactly how the t distribution arises), zero-inflated counts "
    "(a mixture of a point mass at zero and a count distribution), and flexible density estimation.<br><br>"
    "\\[ f(x)=\\sum_{g=1}^{G}\\pi_g\\,f_g(x),\\qquad \\sum_g\\pi_g=1 \\]",
    f"{T} mixture latent-class continuous diagram")


# --- Tweedie / zero inflation --------------------------------------------
def _tweedie():
    cv = Canvas(w=460, h=270)
    f = lambda x: 0.55 * gamma_pdf(x, 1.6, 0.9) if x > 0 else 0.0
    grid = [0.02 + 8 * i / 300 for i in range(301)]
    pts = [(x, f(x)) for x in grid]
    top = 0.42
    cv.limits((-0.9, 8), (0, top))
    cv.axes(xlabel="claim cost y", ylabel="density / mass", xticks=[0, 2, 4, 6, 8],
            y_axis=False)
    cv.line(-0.9, 0, 8, 0, width=1.2, opacity=0.85)
    cv.path(pts, color=C["blue"], width=1.9, fill=C["blue"], close_to=0, fo=0.16)
    cv.rect(-0.18, 0, 0.36, 0.34, fill=C["rose"], fo=0.4, stroke=C["rose"], width=1.4)
    cv.text(0.15, 0.37, "point mass at 0: P(no claim)", size=9.5, opacity=0.85, anchor="start")
    cv.text(3.4, 0.20, "continuous positive part", size=9.5, opacity=0.85, anchor="start",
            color="currentColor")
    cv.caption(["compound Poisson-Gamma: N ~ Poisson claims, each of Gamma size, total Y = ΣX",
                "one model for 'mostly zero, sometimes a positive amount' - variance function μ^p, 1 < p < 2"])
    return cv


pic("What does a Tweedie (compound Poisson-Gamma) distribution look like, and where is it used?",
    _tweedie,
    "A <b>point mass at zero plus a continuous positive density</b> - a shape no ordinary GLM family can "
    "produce. It arises as a compound sum: the number of events is Poisson, each event contributes a Gamma "
    "amount, and you observe the total.<br><br>"
    "Natural context: insurance pure premium (most policies cost nothing, some cost a lot), rainfall per day, "
    "spend per customer, fish biomass per haul, healthcare cost per patient.<br><br>"
    "In the exponential dispersion family it is the member with variance function \\(\\mu^p\\); "
    "\\(1<p<2\\) is the compound Poisson-Gamma case, and p = 1, 2, 3 recover Poisson, Gamma and inverse "
    "Gaussian. It is the reason to reach for `tweedie` / `statmod` rather than modelling the zeros and the "
    "amounts in two separate steps - though a two-part (hurdle) model is the alternative when the two "
    "processes are genuinely different.<br><br>"
    "\\[ \\operatorname{Var}(Y)=\\phi\\mu^{p} \\]",
    f"{T} tweedie compound-poisson zeros diagram")


# --- von Mises -----------------------------------------------------------
def _vonmises():
    cv = Canvas(w=460, h=270)
    def vm(x, kappa):
        # unnormalised is fine for a shape plot; normalise numerically
        return math.exp(kappa * math.cos(x))
    for kappa, col, lab in ((0.0, "slate", "κ = 0 (uniform)"), (1.0, "blue", "κ = 1"),
                            (4.0, "green", "κ = 4")):
        Z = sum(vm(-math.pi + 2 * math.pi * i / 500, kappa) for i in range(501)) * (2 * math.pi / 500)
        pts = [( -math.pi + 2 * math.pi * i / 300, vm(-math.pi + 2 * math.pi * i / 300, kappa) / Z)
               for i in range(301)]
        if kappa == 0:
            cv.limits((-math.pi, math.pi), (0, 0.75))
            cv.axes(xlabel="angle (radians)", ylabel="density",
                    xticks=[-3.14159, -1.5708, 0, 1.5708, 3.14159],
                    xfmt=lambda v: {"-3.14": "-π", "-1.57": "-π/2", "0": "0",
                                    "1.57": "π/2", "3.14": "π"}.get(f"{v:.2f}", f"{v:g}"))
        cv.path(pts, color=C[col], width=1.9, dash="4 3" if kappa == 0 else None)
    cv.legend([("κ = 0 uniform", C["slate"], "4 3"), ("κ = 1", C["blue"]), ("κ = 4", C["green"])],
              x=445, y=28)
    cv.caption(["the circle wraps: -π and π are the same point, so ordinary means are wrong",
                "κ is the concentration; κ = 0 is no preferred direction, large κ ≈ normal on the circle"])
    return cv


pic("What does the von Mises distribution look like, and where is it needed?",
    _vonmises,
    "The 'normal distribution on the circle': a unimodal density over angles that wraps around, "
    "with a concentration parameter κ (κ = 0 is uniform on the circle, large κ is approximately normal).<br><br>"
    "Needed whenever the sample space is <b>periodic</b>, where ordinary means and variances are meaningless: "
    "the average of 350° and 10° is 0°, not 180°. Natural context: wind and current directions, animal "
    "orientation and migration bearings, time of day or day of year (circadian and seasonal effects), "
    "phase angles, compass and protein dihedral angles.<br><br>"
    "In modelling terms this is why seasonal effects are usually entered as sine-cosine pairs or as cyclic "
    "splines (`bs = \"cc\"` in mgcv) rather than as a plain smooth - the fit must join up at the ends.",
    f"{T} von-mises circular continuous diagram")


# ---------------------------------------------------------------------------
# text-only cards for section 1
# ---------------------------------------------------------------------------
TXT = [
    ("Which distribution should you reach for when modelling a count, and how do you choose?",
     "Ask two questions: is there a known denominator, and is the variance bigger than the mean?<br><br>"
     "- <b>Known denominator, k out of n</b>: binomial. Overdispersed version: beta-binomial or a "
     "binomial GLMM with a random intercept.<br>"
     "- <b>No denominator, rate over exposure</b>: Poisson (with an offset log(exposure)). "
     "Overdispersed version: negative binomial, or quasi-Poisson if you only want corrected standard "
     "errors.<br>"
     "- <b>Too many zeros even for the negative binomial</b>: zero-inflated (a mixture with structural "
     "zeros) or hurdle (two-part: any event yes/no, then how many).<br>"
     "- <b>Counts that are actually amounts</b>, zero or positive continuous: Tweedie.<br><br>"
     "The diagnostic is the ratio of Pearson chi-square to residual df, or a dispersion test; "
     "overdispersion left uncorrected makes standard errors too small and p-values too optimistic.",
     f"{T} counts overdispersion model-choice"),

    ("What does it mean that a distribution belongs to the exponential family, and why does it matter?",
     "Its density can be written with the parameter entering only through an inner product with a sufficient "
     "statistic. Members: normal, Bernoulli/binomial, Poisson, negative binomial (fixed θ), Gamma, "
     "inverse Gaussian, Beta, chi-square, and the multinomial.<br><br>"
     "Why it matters:<br>"
     "- the mean determines the variance through a <b>variance function</b> \\(V(\\mu)\\), which is what a GLM "
     "exploits (normal: 1, Poisson: μ, negative binomial: μ + μ²/θ, Gamma: μ², inverse Gaussian: μ³, "
     "binomial: μ(1-μ)/n);<br>"
     "- the log-likelihood is concave in the canonical parameter, so IRLS/Fisher scoring converges reliably "
     "to a unique MLE;<br>"
     "- there are low-dimensional <b>sufficient statistics</b>, and conjugate priors exist;<br>"
     "- the canonical link makes the score equations take the clean form \\(X^\\top(y-\\mu)=0\\), so fitted "
     "residuals are orthogonal to the covariates.<br><br>"
     "\\[ f(y\\mid\\theta)=\\exp\\!\\Big(\\frac{y\\theta-b(\\theta)}{\\phi}+c(y,\\phi)\\Big),\\quad "
     "E[Y]=b'(\\theta),\\ \\operatorname{Var}(Y)=\\phi\\,b''(\\theta) \\]",
     f"{T} exponential-family glm variance-function"),

    ("Which limiting and mixture relations between the standard distributions are worth knowing by heart?",
     "<b>Limits</b><br>"
     "- Binomial(n, p) → Poisson(λ) when n → ∞, np → λ.<br>"
     "- Binomial and Poisson → normal for large mean (CLT).<br>"
     "- \\(t_k\\) → normal, and \\(\\chi^2_k\\) → normal (after standardising), as k → ∞.<br>"
     "- \\(k_1F_{k_1,k_2}\\to\\chi^2_{k_1}\\) as \\(k_2\\to\\infty\\).<br>"
     "- Hypergeometric → binomial when the sample is a small fraction of the population.<br><br>"
     "<b>Sums</b><br>"
     "- Sum of exponentials = Gamma (Erlang); sum of Gammas with the same rate = Gamma.<br>"
     "- Sum of squared standard normals = chi-square; sum of Poissons = Poisson; "
     "sum of independent normals = normal.<br><br>"
     "<b>Mixtures</b><br>"
     "- Poisson with Gamma rate = negative binomial.<br>"
     "- Binomial with Beta probability = beta-binomial.<br>"
     "- Normal with inverse-gamma variance = Student t.<br>"
     "- Poisson number of Gamma amounts = Tweedie.<br><br>"
     "<b>Ratios</b>: normal / normal = Cauchy; normal / √(χ²/k) = t; (χ²/k₁)/(χ²/k₂) = F; "
     "\\(t_k^2=F_{1,k}\\).",
     f"{T} relations limits mixtures"),

    ("Which conjugate prior goes with which likelihood, and what is the intuition?",
     "- <b>Binomial p</b> → Beta(a, b); posterior Beta(a + k, b + n - k). Read a and b as prior "
     "successes and failures.<br>"
     "- <b>Poisson λ</b> → Gamma(a, b); posterior Gamma(a + Σy, b + n). Read a as prior events in b "
     "units of exposure.<br>"
     "- <b>Multinomial</b> → Dirichlet; posterior adds the observed category counts.<br>"
     "- <b>Normal mean, known variance</b> → normal; the posterior mean is a precision-weighted average "
     "of prior mean and sample mean.<br>"
     "- <b>Normal variance</b> → inverse-gamma (or scaled inverse chi-square); jointly, normal-inverse-gamma.<br>"
     "- <b>Exponential rate</b> → Gamma.<br>"
     "- <b>Multivariate normal precision</b> → Wishart; covariance → inverse Wishart.<br><br>"
     "The common structure: the prior mimics data, so the posterior parameters are prior pseudo-counts plus "
     "real counts, and the posterior mean is a <b>shrinkage</b> of the sample estimate toward the prior mean - "
     "the same algebra that produces BLUPs in mixed models.",
     f"{T} bayes conjugate-priors shrinkage"),

    ("What are the Dirichlet and Wishart distributions used for?",
     "<b>Dirichlet</b>: a distribution over the simplex, i.e. over vectors of proportions that sum to 1. "
     "It is the multivariate Beta and the conjugate prior for multinomial probabilities. Used for "
     "compositional data (soil composition, budget shares, cell-type fractions), as the prior in "
     "latent Dirichlet allocation for topic models, and as the base of the Dirichlet process for "
     "nonparametric clustering. A single concentration parameter controls how spiky versus even the "
     "sampled compositions are.<br><br>"
     "<b>Wishart</b>: the distribution of a sample covariance matrix (a sum of outer products of normal "
     "vectors), i.e. the matrix analogue of the chi-square. Its inverse is the conjugate prior for a "
     "multivariate normal covariance matrix, which is why the <b>inverse Wishart</b> shows up in Bayesian "
     "multivariate models and in random-effects covariance priors. Modern practice often prefers an "
     "LKJ prior on the correlation matrix plus separate scale priors, because the inverse Wishart couples "
     "variances and correlations in unintuitive ways.",
     f"{T} dirichlet wishart multivariate bayes"),

    ("What does 'heavy-tailed' actually mean, and what practical consequences does it have?",
     "A tail is heavy if it decays more slowly than exponentially - typically like a power \\(x^{-\\alpha}\\). "
     "Formally, moments only exist up to order α: with α ≤ 2 the variance is infinite, with α ≤ 1 even the "
     "mean is.<br><br>"
     "Consequences:<br>"
     "- <b>Sample means and standard errors mislead</b>: they keep changing as n grows, and CLT-based "
     "confidence intervals under-cover.<br>"
     "- <b>The maximum dominates the sum</b>: a single observation can carry most of the total, so 'the "
     "outlier' is data, not error.<br>"
     "- <b>Estimating a mean is the wrong target</b>: report quantiles, medians, or model the tail directly "
     "with extreme-value theory (GPD over a threshold).<br>"
     "- <b>Risk measures matter</b>: value-at-risk and expected shortfall exist precisely because the mean "
     "and variance say too little.<br><br>"
     "Diagnostics: a log-log survival plot that is straight, a mean-excess plot that keeps rising, "
     "a QQ plot against the normal that bends up sharply, or a Hill estimate of α.",
     f"{T} heavy-tails power-law diagnostics"),

    ("Why is the choice of response distribution mostly a choice about the mean-variance relationship?",
     "In practice the fitted mean structure is fairly robust to the distributional assumption, but the "
     "<b>standard errors, tests and prediction intervals are not</b>. What the family really encodes is how "
     "the variance grows with the mean.<br><br>"
     "- Constant spread on the original scale → normal.<br>"
     "- Spread growing like the mean → Poisson (counts).<br>"
     "- Spread growing like the mean squared, i.e. constant relative error → Gamma (positive amounts).<br>"
     "- Spread growing like the mean cubed → inverse Gaussian.<br>"
     "- Spread largest at 0.5 and vanishing at the boundaries → binomial/Bernoulli (proportions).<br>"
     "- Zero-inflated positive amounts → Tweedie.<br><br>"
     "This is why quasi-likelihood works at all: specify only the mean and the variance function, and "
     "estimation stays valid. And it is why the practical model check is a plot of "
     "\\(|\\text{residual}|\\) against the fitted value - if the spread trends, the variance function, "
     "not the link, is what needs changing.",
     f"{T} mean-variance model-choice glm"),
]

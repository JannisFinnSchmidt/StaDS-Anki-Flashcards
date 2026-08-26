# -*- coding: utf-8 -*-
"""Section 3 - model classes: what exists, what each relaxes, when to use it."""
from plotlib import *

T = "Core model-classes"
PIC = []
TXT = []


def pic(front, builder, back, tags):
    PIC.append((front, builder, back, tags))


def txt(front, back, tags):
    TXT.append((front, back, tags))


def _taxonomy():
    cv = Canvas(w=470, h=300, pad=(10, 10, 10, 10))

    def box(x, y, w, h, label, col, sub=None, size=9.5):
        cv.rect(x, y, w, h, fill=C[col], fo=0.18, stroke="currentColor", width=1.1, rx=4,
                data=False)
        cv.text(x + w / 2, y + (h / 2 + 3.4 if not sub else h / 2 - 1.5), label, size=size,
                data=False)
        if sub:
            cv.text(x + w / 2, y + h / 2 + 11, sub, size=8, opacity=0.72, data=False)

    def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None):
        cv.line(x1, y1, x2, y2, width=1.1, opacity=0.7, arrow=True, data=False)
        if label:
            cv.text(lx, ly, label, size=8, opacity=0.72, data=False)

    box(160, 14, 150, 26, "linear model", "slate", size=10)
    cv.text(235, 52, "y = Xβ + ε,  ε ~ N(0, σ²I)", size=8.5, opacity=0.7, data=False)

    box(14, 74, 130, 36, "GLM", "blue", sub="non-normal y, link g(μ)")
    box(170, 74, 130, 36, "GAM", "green", sub="smooth f(x) instead of βx")
    box(326, 74, 130, 36, "LMM / GLMM", "violet", sub="random effects, clusters")
    arrow(200, 42, 90, 72)
    arrow(235, 42, 235, 72)
    arrow(270, 42, 390, 72)

    box(14, 132, 130, 36, "GAMM", "cyan", sub="smooths + random effects")
    arrow(79, 110, 79, 130)
    arrow(235, 110, 130, 130)
    arrow(391, 110, 140, 130)

    box(170, 132, 130, 36, "GEE", "amber", sub="marginal, working corr.")
    arrow(391, 110, 300, 130)

    box(326, 132, 130, 36, "GAMLSS", "rose", sub="model σ, ν, τ too")
    arrow(235, 110, 340, 130)

    box(14, 190, 138, 34, "quantile regression", "amber", sub="model Q_τ(y), no σ needed")
    box(166, 190, 138, 34, "penalised (lasso/ridge)", "blue", sub="bias for variance, p ≫ n")
    box(318, 190, 138, 34, "trees / boosting / NN", "green", sub="learn interactions, no link")

    cv.caption(["each arrow relaxes exactly one assumption of the linear model:",
                "the distribution of y, linearity in x, independence of observations, or homoscedasticity",
                "penalised splines ARE random effects - which is why GAM and mixed-model software overlap"],
               x=14, y0=246)
    return cv


pic("Sketch the map of regression model classes and what each one relaxes",
    _taxonomy,
    "Everything hangs off the linear model, and each extension drops exactly one of its assumptions:<br><br>"
    "- <b>GLM</b> - drops normality and constant variance: a distribution from the exponential family plus a "
    "link g(μ) = Xβ.<br>"
    "- <b>GAM</b> - drops linearity: unknown smooth functions f(x), estimated with penalised splines.<br>"
    "- <b>LMM / GLMM</b> - drops independence: random effects for clusters, giving a conditional "
    "interpretation.<br>"
    "- <b>GEE</b> - also handles dependence, but targets the <b>marginal (population-average)</b> mean and "
    "treats the correlation as a nuisance.<br>"
    "- <b>GAMM</b> - smooths and random effects together.<br>"
    "- <b>GAMLSS / distributional regression</b> - drops the idea that only the mean depends on covariates: "
    "the scale and shape do too.<br>"
    "- <b>Quantile regression</b> - drops the mean as the target entirely.<br>"
    "- <b>Penalised regression</b> - keeps the structure but trades bias for variance, which is what makes "
    "p ≫ n tractable.<br>"
    "- <b>Trees, boosting, neural nets</b> - drop the additive parametric form to learn interactions "
    "automatically, at the cost of interpretable coefficients and honest inference.<br><br>"
    "The deep connection worth remembering: a <b>penalised spline is formally a random effect</b>, so a GAM "
    "is a mixed model in disguise - which is why `mgcv` can fit random effects and `lme4` can fit splines.",
    f"{T} taxonomy overview diagram")


# ---------------------------------------------------------------------------
txt("What defines a generalised linear model, and what are its three components?",
    "1. a <b>random component</b>: the response follows an exponential-family distribution "
    "(normal, binomial, Poisson, Gamma, inverse Gaussian, ...), which fixes the mean-variance "
    "relationship \\(\\operatorname{Var}(Y)=\\phi V(\\mu)\\);<br>"
    "2. a <b>systematic component</b>: a linear predictor \\(\\eta=X\\beta\\);<br>"
    "3. a <b>link function</b> connecting them: \\(g(\\mu)=\\eta\\).<br><br>"
    "What stays and what changes relative to the linear model: linearity is still assumed, but on the "
    "<b>link scale</b>; the errors are no longer additive or normal; and estimation is by maximum "
    "likelihood via iteratively reweighted least squares (Fisher scoring), so there is no closed form.<br><br>"
    "Assumptions to check: correct mean model (linearity on the link scale, right covariates), correct "
    "variance function (look for over/underdispersion), independence, and no excessive influence. "
    "Note what is <b>not</b> assumed: normal residuals, constant variance, or a normally distributed "
    "response.<br><br>"
    "\\[ g(\\mu_i)=x_i^\\top\\beta,\\qquad \\operatorname{Var}(Y_i)=\\phi\\,V(\\mu_i)/w_i \\]",
    f"{T} glm components assumptions")

txt("What is a GAM, and how do the smooths avoid overfitting?",
    "A GAM keeps the additive structure but replaces linear terms with unknown smooth functions:<br><br>"
    "\\[ g(\\mu)=\\beta_0+f_1(x_1)+f_2(x_2)+\\dots \\]<br>"
    "Each \\(f_j\\) is expanded in a spline basis (thin-plate, cubic regression, B-spline, cyclic, "
    "tensor-product for interactions) with generously many basis functions, and overfitting is prevented by "
    "a <b>wiggliness penalty</b> - typically the integrated squared second derivative - whose weight "
    "\\(\\lambda\\) is chosen by REML or GCV.<br><br>"
    "So the effective degrees of freedom (EDF) are estimated, not chosen: EDF ≈ 1 means the term is "
    "effectively linear, high EDF means genuine curvature. This is why a GAM is both a test of nonlinearity "
    "and a fix for it.<br><br>"
    "Use it when the relationship is clearly nonlinear but you have no parametric form in mind, for "
    "smooth time trends and seasonality (cyclic splines), for spatial surfaces (2-D smooths), and for "
    "exposure-response curves. Assumptions: same as GLM plus the assumption that the effect really is "
    "additive and smooth - and remember the p-values for smooth terms are approximate because "
    "\\(\\lambda\\) was estimated.",
    f"{T} gam splines penalty edf")

txt("What does 'penalised splines are random effects' mean, and why is it useful?",
    "Both a ridge-type penalty and a random effect shrink coefficients toward zero, and the algebra is "
    "identical: a penalty \\(\\lambda\\beta^\\top S\\beta\\) is exactly the log-density of a normal prior "
    "\\(\\beta\\sim N(0,\\sigma^2S^{-}/\\lambda)\\). So a spline's wiggliness penalty can be re-expressed "
    "as a variance component, with \\(\\lambda=\\sigma^2_{\\varepsilon}/\\sigma^2_{b}\\).<br><br>"
    "Consequences worth remembering:<br>"
    "- <b>REML is the natural way to choose the smoothing parameter</b>, because it is just variance-"
    "component estimation - which is why `mgcv` recommends `method = \"REML\"`;<br>"
    "- a random intercept is the special case of a smooth with a ridge penalty, which is why you can write "
    "`s(group, bs = \"re\")` in `mgcv`;<br>"
    "- a spline can be fitted in `lme4`, and a mixed model can be fitted in `mgcv`;<br>"
    "- confidence bands for smooths are Bayesian credible bands under that prior;<br>"
    "- the same duality explains ridge = normal prior, lasso = Laplace prior, and shrinkage/BLUP in mixed "
    "models.",
    f"{T} splines random-effects duality penalty")

txt("What is a GEE, and when do you prefer it over a GLMM?",
    "GEE (generalised estimating equations) models the <b>marginal</b> mean of clustered data - "
    "\\(g(E[Y_{ij}])=x_{ij}^\\top\\beta\\) averaged over the population - and treats the within-cluster "
    "correlation as a nuisance through a <b>working correlation matrix</b> (independence, exchangeable, "
    "AR(1), unstructured).<br><br>"
    "Its key property: the coefficients stay <b>consistent even if the working correlation is wrong</b>, "
    "as long as you use the sandwich (robust) standard errors. It is a quasi-likelihood method, so there is "
    "no likelihood - no AIC, no LR tests (use QIC and Wald tests instead).<br><br>"
    "Choose GEE when the target is a <b>population-average effect</b> (public-health or policy questions: "
    "'what happens to the average if everyone is treated'), when you have many clusters and few "
    "observations each, and when you would rather not commit to a random-effects distribution.<br><br>"
    "Choose a GLMM when you want <b>subject-specific</b> predictions, when the variance components are of "
    "interest (ICC, heritability, between-centre variation), when the design has crossed or nested levels, "
    "or when data are missing at random - GEE needs MCAR unless you weight.<br><br>"
    "Caveat: GEE needs a decent number of clusters (rule of thumb ≥ 30-40) for the sandwich estimator to "
    "behave.",
    f"{T} gee marginal-model clustered")

txt("What is quantile regression, and when is it the right tool?",
    "Instead of the conditional mean it models a conditional <b>quantile</b>, by minimising an asymmetric "
    "'check' (pinball) loss:<br><br>"
    "\\[ \\hat\\beta_\\tau=\\arg\\min_\\beta\\sum_i\\rho_\\tau\\big(y_i-x_i^\\top\\beta\\big),\\qquad "
    "\\rho_\\tau(u)=u\\big(\\tau-\\mathbb 1\\{u<0\\}\\big) \\]<br>"
    "with τ = 0.5 giving median regression (L1).<br><br>"
    "Use it when:<br>"
    "- the <b>tails</b> are the question, not the average - growth charts and reference curves, low birth "
    "weight, value-at-risk, wage inequality, worst-case latency;<br>"
    "- covariates change the <b>spread or shape</b>, not just the level (fitting several τ reveals fanning "
    "out that a mean model hides);<br>"
    "- the data have outliers or heavy tails, since quantiles are robust;<br>"
    "- you need prediction intervals without assuming a distribution.<br><br>"
    "Properties: no distributional assumption, equivariant to monotone transformations (the quantile of a "
    "log is the log of the quantile - untrue for means), but no likelihood, slower inference (rank or "
    "bootstrap based), and separately fitted quantile curves can cross.",
    f"{T} quantile-regression pinball-loss robust")

txt("What are robust regression methods and when do you need them?",
    "They replace the squared-error loss, whose influence function is unbounded, with one that limits the "
    "pull of extreme residuals.<br><br>"
    "- <b>M-estimation</b> (`MASS::rlm`, Huber or Tukey bisquare loss): downweights large residuals. "
    "Protects against outliers in <b>y</b> but not against high-leverage outliers in <b>x</b>.<br>"
    "- <b>MM-estimation</b> (`robustbase::lmrob`): high breakdown point (up to 50 %) and high efficiency - "
    "the practical default.<br>"
    "- <b>Least trimmed squares / LMS</b>: fits the majority of the data by construction.<br>"
    "- <b>Quantile / median regression</b>: robust by targeting a quantile.<br>"
    "- <b>Heavy-tailed likelihoods</b> (t errors): robustness as an explicit model rather than a loss "
    "hack, so likelihood inference still applies.<br><br>"
    "Important distinction: <b>robust standard errors</b> (sandwich/HC, cluster) fix the <b>inference</b> "
    "under heteroscedasticity or clustering while leaving the OLS point estimates untouched; robust "
    "<b>regression</b> changes the estimates themselves. They solve different problems and are often "
    "needed together.<br><br>"
    "Before reaching for either, check whether the outliers are data errors, a missing covariate, or the "
    "wrong scale for the response - fixing the model beats down-weighting the evidence.",
    f"{T} robust-regression m-estimation sandwich")

txt("What do ridge, lasso and elastic net do, and when do you use each?",
    "All three add a penalty to the least-squares (or likelihood) objective to trade a little bias for a "
    "large reduction in variance.<br><br>"
    "- <b>Ridge</b> (L2, \\(\\lambda\\|\\beta\\|_2^2\\)): shrinks all coefficients smoothly, never to "
    "exactly zero. Best when predictors are many and <b>correlated</b> and you believe most contribute a "
    "little (dense signal); it stabilises multicollinear fits and always has a unique solution even when "
    "p > n.<br>"
    "- <b>Lasso</b> (L1, \\(\\lambda\\|\\beta\\|_1\\)): the corners of the constraint region set "
    "coefficients exactly to zero, so it selects variables. Best for a <b>sparse</b> truth. Weaknesses: it "
    "picks arbitrarily among correlated predictors, selects at most n variables, and its estimates are "
    "biased toward zero (hence the relaxed and adaptive lasso).<br>"
    "- <b>Elastic net</b>: a mix; keeps sparsity while handling groups of correlated predictors "
    "together.<br>"
    "- Structured variants: <b>group lasso</b> (drop a whole factor or spline basis at once), "
    "<b>fused lasso</b> (piecewise-constant in an ordering).<br><br>"
    "Practical points: standardise the predictors, choose λ by cross-validation, do not interpret p-values "
    "from a penalised fit naively (post-selection inference is needed), and remember these are prediction "
    "tools - shrunken coefficients are not unbiased causal effects.",
    f"{T} regularisation ridge lasso elastic-net")

txt("Which model classes exist for ordinal outcomes, and what do they assume?",
    "- <b>Proportional odds (cumulative logit)</b>: models the log-odds of being at or below each category "
    "with a <b>common</b> slope and category-specific intercepts. Interpretation: one odds ratio for "
    "'moving up' anywhere on the scale. Assumption: <b>proportional odds</b> - the effect is the same at "
    "every cut point. Check with a Brant test or by plotting the separate binary fits at each cut.<br>"
    "- <b>Partial proportional odds</b>: relax the assumption for selected covariates only.<br>"
    "- <b>Continuation ratio</b>: models the odds of stopping at a category given that you have reached it - "
    "the natural choice for genuinely <b>sequential</b> processes (education stages, disease progression), "
    "and it can be fitted as a binary GLM on expanded data.<br>"
    "- <b>Adjacent categories</b>: compares each category with its neighbour; convenient when local "
    "contrasts are what matter.<br>"
    "- <b>Cumulative probit / ordered probit</b>: same structure with a latent normal - the threshold model.<br>"
    "- <b>Multinomial logit</b> as a fallback: no ordering assumed, more parameters, less power.<br><br>"
    "Why not just use linear regression on the numeric codes: it assumes equally spaced categories and can "
    "predict outside the range, though for many-category scales it is a defensible approximation.",
    f"{T} ordinal proportional-odds continuation-ratio")

txt("Which model classes exist for nominal (unordered multi-category) outcomes?",
    "- <b>Multinomial logistic regression (baseline-category logit)</b>: one set of coefficients per "
    "category relative to a reference. Interpretation is always relative to that reference. This is exactly "
    "the softmax model.<br>"
    "- <b>Conditional (McFadden) logit</b>: covariates that vary <b>by alternative</b> (price and travel "
    "time of each mode of transport), not just by individual. Standard in discrete-choice modelling; "
    "it follows from iid Gumbel utility errors.<br>"
    "- <b>Mixed / random-parameters logit</b>: coefficients vary across individuals - taste heterogeneity.<br>"
    "- <b>Nested logit</b>: groups similar alternatives, relaxing the independence-of-irrelevant-alternatives "
    "assumption.<br>"
    "- <b>Multinomial probit</b>: correlated errors across alternatives, no IIA, but computationally "
    "heavier.<br><br>"
    "The assumption to know is <b>IIA</b>: in plain multinomial and conditional logit, the ratio of two "
    "choice probabilities does not depend on which other options exist. The classic counterexample is the "
    "red-bus/blue-bus problem, where adding a near-identical alternative should steal share only from its "
    "twin but does not.",
    f"{T} multinomial conditional-logit iia discrete-choice")

txt("Which model classes exist for proportions and rates that are not counts?",
    "- <b>Beta regression</b>: a continuous proportion strictly inside (0,1) - percentage of budget spent, "
    "share of area covered, fraction of time on task. Models the mean with a logit link plus a precision "
    "parameter; `betareg`, or `mgcv` family `betar`.<br>"
    "- <b>Zero-and-one-inflated beta</b>: when exact 0s and 1s occur, since the beta density cannot handle "
    "them.<br>"
    "- <b>Quasi-binomial / fractional logit</b>: a GLM with logit link and a dispersion parameter, valid "
    "for any y in [0,1] including the boundaries; the standard econometric choice for fractional "
    "outcomes.<br>"
    "- <b>Binomial GLM with weights</b>: when you actually know the denominator (k out of n) - always "
    "preferable to modelling the proportion, because it carries the information about how precise each "
    "proportion is.<br>"
    "- <b>Dirichlet regression</b>: several proportions that must sum to one (compositional data), or "
    "log-ratio transforms.<br>"
    "- <b>Rates</b>: model the count with a Poisson/NB GLM and an <b>offset</b> log(exposure) - this "
    "correctly keeps the uncertainty tied to the count rather than treating a rate as a continuous "
    "response.",
    f"{T} beta-regression proportions offset rates")

txt("Which model classes exist for time-to-event data?",
    "- <b>Kaplan-Meier / Nelson-Aalen</b>: nonparametric estimates of survival and cumulative hazard; "
    "descriptive, no covariates.<br>"
    "- <b>Cox proportional hazards</b>: semiparametric - leaves the baseline hazard unspecified and "
    "estimates covariate effects by partial likelihood. Assumes <b>proportional hazards</b> (check with "
    "Schoenfeld residuals; fix with time-varying effects or stratification) and independent censoring.<br>"
    "- <b>Parametric AFT models</b> (Weibull, lognormal, log-logistic): covariates accelerate or decelerate "
    "time. Interpretable as time ratios, better for extrapolation and for predicting absolute survival; "
    "the Weibull is the only model that is both PH and AFT.<br>"
    "- <b>Competing risks</b>: cause-specific hazards (etiology) or Fine-Gray subdistribution hazards "
    "(absolute risk / prediction). Kaplan-Meier overestimates risk here - use cumulative incidence "
    "functions.<br>"
    "- <b>Frailty models</b>: random effects for clustered or recurrent event data.<br>"
    "- <b>Multi-state models</b>: several transitions (illness-death, disease stages).<br>"
    "- <b>Discrete-time survival</b>: a binary GLM (usually cloglog or logit) on person-period data - "
    "the easy way to include time-varying covariates.<br><br>"
    "The one assumption underlying all of them: censoring must be <b>non-informative</b>.",
    f"{T} survival cox aft competing-risks")

txt("Which model classes exist for time series and what do they assume?",
    "- <b>ARIMA</b>: autocorrelation modelled directly, differencing for trends, seasonal terms for "
    "seasonality. Assumes (after differencing) stationarity and white-noise residuals - check with "
    "Ljung-Box.<br>"
    "- <b>Exponential smoothing / ETS</b>: level, trend and seasonal components with geometrically decaying "
    "weights; excellent robust baseline for forecasting.<br>"
    "- <b>State-space models and the Kalman filter</b>: an unobserved state evolving over time with "
    "observations that are noisy functions of it. The general framework - ARIMA and ETS are special "
    "cases - and it handles missing data and time-varying parameters naturally.<br>"
    "- <b>Dynamic regression / ARIMAX</b>: covariates plus autocorrelated errors, when you want an "
    "explanatory effect and honest standard errors.<br>"
    "- <b>VAR / VECM</b>: several series influencing each other; VECM when they are cointegrated.<br>"
    "- <b>GARCH</b>: the <b>variance</b> is autocorrelated - volatility clustering in finance.<br>"
    "- <b>Prophet / GAM with time smooths</b>: trend plus seasonality plus holidays, regression-style and "
    "easy to interpret.<br><br>"
    "The cross-cutting rules: never use random-split cross-validation (use rolling-origin evaluation), "
    "beware spurious regression between non-stationary series, and always compare against a naive or "
    "seasonal-naive benchmark.",
    f"{T} time-series arima ets state-space garch")

txt("Which model classes exist for spatial data?",
    "- <b>Areal data (regions, counties)</b>: <b>CAR</b> (conditional autoregressive) and <b>SAR</b> "
    "(simultaneous autoregressive) models specify dependence through a neighbourhood matrix; the "
    "<b>BYM</b> model combines spatially structured and unstructured random effects and is the standard for "
    "disease mapping. Everything depends on the neighbourhood definition you chose.<br>"
    "- <b>Geostatistical (point-referenced) data</b>: <b>kriging</b> / Gaussian processes with a "
    "covariance function (exponential, Matérn) fitted via the variogram; assumes stationarity and "
    "isotropy unless you relax them explicitly.<br>"
    "- <b>Spline surfaces</b>: `mgcv` 2-D smooths (`s(lon, lat)`, soap-film smooths for complicated "
    "boundaries) - often the pragmatic choice when the spatial term is a nuisance you just need to absorb.<br>"
    "- <b>INLA / SPDE</b>: fast approximate Bayesian inference for large spatial and spatio-temporal "
    "models.<br>"
    "- <b>Point-process models</b> (Poisson process, log-Gaussian Cox process) when the <b>locations "
    "themselves</b> are the data - crime events, tree positions, disease cases.<br><br>"
    "Why bother: spatial autocorrelation makes ordinary standard errors far too small, and unmodelled "
    "spatial confounding can flip signs.",
    f"{T} spatial car sar kriging point-process")

txt("What is distributional regression (GAMLSS), and why go beyond the mean?",
    "Instead of modelling only the mean, every parameter of the response distribution gets its own "
    "predictor:<br><br>"
    "\\[ g_1(\\mu)=X_1\\beta_1,\\quad g_2(\\sigma)=X_2\\beta_2,\\quad g_3(\\nu)=X_3\\beta_3,\\ \\dots \\]<br>"
    "so location, scale, skewness and kurtosis can all depend on covariates, with any of dozens of "
    "distributions.<br><br>"
    "When you need it:<br>"
    "- the <b>spread itself is the question</b> - variability of outcomes across hospitals, forecast "
    "uncertainty, volatility;<br>"
    "- <b>reference curves and centiles</b> (growth charts) where the whole conditional distribution "
    "matters, not the average child;<br>"
    "- <b>prediction intervals</b> that must be honest across the covariate range;<br>"
    "- heteroscedasticity that is <b>structural</b> rather than a nuisance;<br>"
    "- probabilistic forecasting evaluated by CRPS.<br><br>"
    "R: `gamlss`, `mgcv` with families like `gaulss` or `twlss`, `bamlss`, or `brms` with distributional "
    "formulas (`sigma ~ x`). The cost is many more parameters, so it needs data and careful model "
    "selection - and quantile regression is the assumption-light alternative when you only care about "
    "specific quantiles.",
    f"{T} gamlss distributional-regression heteroscedasticity")

txt("What are latent-variable model classes and when are they used?",
    "- <b>Finite mixture / latent-class models</b>: the population consists of unobserved subgroups with "
    "different parameters. Fitted by EM. Used for model-based clustering, market segmentation, "
    "distinguishing disease subtypes.<br>"
    "- <b>Hidden Markov models</b>: a latent <b>state that evolves over time</b> and drives the "
    "observations - animal behaviour phases, sleep staging, regime switching in markets, speech.<br>"
    "- <b>Factor analysis</b>: a few continuous latent factors explain the correlation among many measured "
    "items; the measurement model behind psychometrics.<br>"
    "- <b>Structural equation models (SEM)</b>: a measurement model plus a path model of relations between "
    "latent constructs; identification and fit indices (CFI, RMSEA) matter, and the causal claims rest "
    "entirely on the assumed structure.<br>"
    "- <b>Item response theory</b>: item difficulty and discrimination plus a latent ability - a GLMM with "
    "crossed random effects for persons and items.<br>"
    "- <b>PCA and PLS</b>: not latent-variable models in the inferential sense, but the same "
    "dimension-reduction role; PCA ignores y, PLS uses it.<br><br>"
    "Shared caveats: label switching and non-identifiability, local optima, and the fact that the number of "
    "components is a modelling decision more than an estimable quantity (use BIC plus interpretability).",
    f"{T} latent-variables mixture hmm sem factor-analysis")

txt("Which model classes are used for causal questions rather than prediction?",
    "The model class matters less than the identification strategy - what makes the estimate causal is the "
    "design, not the regression.<br><br>"
    "- <b>Regression adjustment / G-computation</b>: adjust for a sufficient set of confounders (chosen "
    "with a DAG and the back-door criterion), then standardise the predictions.<br>"
    "- <b>Propensity score</b> matching, weighting (IPTW) or stratification: balance covariates instead of "
    "modelling the outcome; check balance, not the propensity model's fit.<br>"
    "- <b>Doubly robust / AIPW / TMLE</b>: combine outcome and treatment models, consistent if either is "
    "right; the natural home for machine learning nuisance estimates.<br>"
    "- <b>Instrumental variables / two-stage least squares</b>: exploit a variable that affects treatment "
    "but has no direct path to the outcome. Assumes relevance, exogeneity and exclusion; weak instruments "
    "are badly biased.<br>"
    "- <b>Difference-in-differences</b>: parallel-trends assumption; check pre-trends, and beware "
    "staggered adoption with two-way fixed effects.<br>"
    "- <b>Regression discontinuity</b>: a cutoff in an assignment variable creates a local experiment.<br>"
    "- <b>Fixed effects / within estimators</b>: absorb all time-constant confounders.<br>"
    "- <b>Marginal structural models</b>: time-varying treatments and confounders.<br><br>"
    "Common pitfalls: adjusting for a <b>mediator</b> (removes part of the effect), adjusting for a "
    "<b>collider</b> (creates bias), and reading every coefficient in a multivariable model as a causal "
    "effect - the 'table 2 fallacy'.",
    f"{T} causal-inference iv did rdd propensity")

txt("When do tree ensembles beat a GLM, and what do you give up?",
    "Random forests and gradient boosting (xgboost, LightGBM) win when there are many predictors with "
    "<b>nonlinearities and interactions you cannot pre-specify</b>, when the sample is large, when "
    "predictors are mixed and messy, and when the goal is purely predictive accuracy on tabular data - "
    "gradient boosting is still the practical benchmark there.<br><br>"
    "What you give up:<br>"
    "- <b>Interpretable, testable parameters</b>: no coefficients, no standard errors, no likelihood; "
    "importance measures and SHAP values are descriptive, not inferential, and correlated features "
    "distort them.<br>"
    "- <b>Extrapolation</b>: trees predict a constant outside the observed range; a GLM's trend "
    "continues.<br>"
    "- <b>Smoothness and monotonicity</b> unless you impose constraints.<br>"
    "- <b>Calibration</b>: raw scores often need Platt scaling or isotonic regression.<br>"
    "- <b>Natural handling of clustered/longitudinal structure</b>: random splits leak; you must group the "
    "CV folds and even then the model has no notion of within-subject correlation.<br><br>"
    "The middle ground: a GAM (smooth nonlinearity, still additive and interpretable), boosting with "
    "monotone constraints, GAMs with tensor interactions, or a GLM whose functional form was informed by "
    "what the ensemble found.",
    f"{T} trees boosting interpretability comparison")

txt("How do you decide which model class fits a given data structure?",
    "Ask five questions in order:<br><br>"
    "1. <b>What is the outcome?</b> Continuous, binary, count with or without a denominator, proportion, "
    "ordered category, nominal category, time-to-event, or several outcomes at once. This fixes the "
    "distribution and link.<br>"
    "2. <b>Are observations independent?</b> Repeated measures, clusters, spatial or temporal ordering all "
    "demand mixed models, GEE, or explicit correlation structures. This is the assumption whose violation "
    "does the most damage.<br>"
    "3. <b>Is the effect of the covariates linear on the link scale?</b> If not: transformations, splines, "
    "or a GAM.<br>"
    "4. <b>Is the mean the quantity of interest?</b> If the spread, a quantile, or the whole distribution "
    "matters, go to quantile regression or distributional regression.<br>"
    "5. <b>Is the goal explanation or prediction?</b> Explanation needs an identification strategy, "
    "parsimony and interpretable parameters; prediction needs honest out-of-sample validation and permits "
    "black boxes.<br><br>"
    "Then the practical order of work: plot the data, fit the simplest defensible model, check residuals "
    "and the mean-variance relationship, and only add complexity that the diagnostics or the design "
    "demand.",
    f"{T} model-choice workflow")

txt("What is the difference between a marginal and a conditional effect, and why does it matter?",
    "A <b>conditional</b> effect is the effect for a specific unit or cluster, holding its random effect "
    "fixed ('for a given patient, treatment multiplies the odds by...'). A <b>marginal</b> effect is the "
    "effect on the population average ('if everyone were treated, the average risk would change by...').<br><br>"
    "In a <b>linear</b> model with random effects the two coincide. In a <b>nonlinear</b> model they do not: "
    "averaging a nonlinear function is not the same as the function of the average. For logistic models "
    "the marginal effect is <b>attenuated</b> toward zero relative to the conditional one, by roughly<br><br>"
    "\\[ \\beta_{\\text{marginal}}\\approx\\frac{\\beta_{\\text{conditional}}}{\\sqrt{1+0.346\\,\\sigma_b^2}} \\]<br>"
    "so a GLMM coefficient and a GEE coefficient on the same data are estimating <b>different quantities</b> - "
    "they are not supposed to match.<br><br>"
    "Practical consequences: choose according to the question (clinical/subject-specific versus "
    "policy/population-average); do not compare coefficients across models with different random-effect "
    "structures; and if you want population-level statements from a GLMM, compute <b>average marginal "
    "effects</b> by integrating over the random effects rather than by plugging in b = 0.",
    f"{T} marginal-vs-conditional glmm interpretation")

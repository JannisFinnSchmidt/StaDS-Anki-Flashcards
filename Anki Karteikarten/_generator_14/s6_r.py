# -*- coding: utf-8 -*-
"""Section 6 - which R function fits which model."""
from plotlib import *

T = "Core R"
PIC = []
TXT = []


def txt(front, back, tags):
    TXT.append((front, back, tags))


def code(s):
    """One-line-safe code block: Anki rows are tab separated, so no literal newlines."""
    body = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace("\n", "<br>"))
    return ('<pre style="text-align:left;font-size:0.85em;white-space:pre-wrap;'
            'padding:0.5em 0.7em;border-radius:4px;background:rgba(127,127,127,0.12);'
            'overflow-x:auto">' + body + "</pre>")


txt("Which R function fits which model class? (overview)",
    "<b>Linear and generalised linear</b><br>"
    "- `lm()` - linear model; `glm(family = ...)` - GLM; `MASS::glm.nb()` - negative binomial;<br>"
    "- `nls()` - nonlinear least squares; `glm(family = quasipoisson)` - dispersion-corrected counts.<br><br>"
    "<b>Dependence / clusters</b><br>"
    "- `lme4::lmer()`, `lme4::glmer()` - linear and generalised linear mixed models;<br>"
    "- `nlme::lme()`, `nlme::gls()` - mixed models plus explicit correlation and variance structures;<br>"
    "- `glmmTMB::glmmTMB()` - GLMMs with zero inflation, dispersion models, exotic families;<br>"
    "- `geepack::geeglm()` - GEE (marginal models);<br>"
    "- `fixest::feols()` - high-dimensional fixed effects with clustered standard errors.<br><br>"
    "<b>Smooth / flexible</b><br>"
    "- `mgcv::gam()`, `mgcv::bam()` - GAMs (bam for large data); `mgcv::gamm()`, `gamm4::gamm4()` - GAMMs;<br>"
    "- `gamlss::gamlss()`, `mgcv` `*lss` families, `bamlss` - distributional regression.<br><br>"
    "<b>Beyond the mean / robustness</b><br>"
    "- `quantreg::rq()` - quantile regression; `MASS::rlm()`, `robustbase::lmrob()` - robust regression;<br>"
    "- `glmnet::cv.glmnet()` - lasso/ridge/elastic net.<br><br>"
    "<b>Special outcomes</b><br>"
    "- `survival::coxph()`, `survreg()` - survival; `MASS::polr()`, `ordinal::clm()` - ordinal;<br>"
    "- `nnet::multinom()`, `mlogit` - nominal; `pscl::zeroinfl()`, `hurdle()` - zero-inflated counts;<br>"
    "- `betareg::betareg()` - proportions.<br><br>"
    "<b>Bayesian</b>: `brms::brm()` (lme4-style formulas), `rstanarm`, `INLA`, `nimble`.",
    f"{T} overview packages")

txt("What is the R model formula syntax you need to know?",
    code("y ~ x1 + x2            # main effects\n"
         "y ~ x1 * x2            # main effects + interaction (= x1 + x2 + x1:x2)\n"
         "y ~ x1:x2              # interaction only (rarely what you want)\n"
         "y ~ . - x3             # everything in the data except x3\n"
         "y ~ poly(x, 2)         # orthogonal polynomial\n"
         "y ~ I(x^2)             # literal arithmetic: I() protects it from formula parsing\n"
         "y ~ log(x)             # transformations inline\n"
         "y ~ splines::ns(x, df = 4)   # natural cubic spline basis\n"
         "y ~ x + offset(log(t))       # offset (or: offset = log(t))\n"
         "y ~ 0 + g              # drop the intercept: one mean per level of g\n"
         "cbind(succ, fail) ~ x  # binomial with a known denominator") +
    "Other essentials:<br>"
    "- `weights =` prior weights (grouped data, WLS, survey weights); `offset =` fixed-coefficient term.<br>"
    "- `contrasts`: R defaults to treatment contrasts (`contr.treatment`), so a factor coefficient is the "
    "difference from the reference level. For type-III-style ANOVA use sum contrasts "
    "(`contr.sum`) - `car::Anova()` warns you about this.<br>"
    "- Factors matter: a numeric-coded group variable is treated as continuous. Always check `str()`.<br>"
    "- `na.action = na.exclude` keeps residual vectors aligned with the original data.<br>"
    "- `update(fit, . ~ . - x)` refits with one term removed - convenient for LR tests.",
    f"{T} formula-syntax contrasts")

txt("How do you specify families and links in `glm()`, and which combinations are standard?",
    code("glm(y ~ x, family = gaussian(link = \"identity\"))\n"
         "glm(y ~ x, family = binomial(link = \"logit\"))     # also probit, cloglog, log, identity\n"
         "glm(y ~ x, family = poisson(link = \"log\"))        # also identity, sqrt\n"
         "glm(y ~ x, family = Gamma(link = \"log\"))          # canonical is \"inverse\"\n"
         "glm(y ~ x, family = inverse.gaussian(link = \"1/mu^2\"))\n"
         "glm(y ~ x, family = quasipoisson())               # dispersion-corrected SEs\n"
         "glm(y ~ x, family = quasibinomial())              # fractional / overdispersed proportions\n"
         "MASS::glm.nb(y ~ x)                               # negative binomial, estimates theta\n"
         "statmod::tweedie(var.power = 1.5, link.power = 0)  # with glm(family = tweedie(...))") +
    "Notes that save time:<br>"
    "- Binomial responses can be a factor, a 0/1 vector, a proportion with `weights = n`, or "
    "`cbind(successes, failures)` - the last two are the ones that carry the denominator information.<br>"
    "- `summary(fit)$dispersion` and `sum(residuals(fit, \"pearson\")^2)/df.residual(fit)` diagnose "
    "over-dispersion; well above 1 means switch to quasi-, negative binomial, or a random effect.<br>"
    "- `family = binomial(link = \"log\")` gives relative risks but often fails to converge - try "
    "`logbin` / `brglm2`, or compute the risk ratio from a logistic fit with `marginaleffects`.<br>"
    "- `brglm2::brglmFit` (Firth) handles separation and rare events.",
    f"{T} glm family link")

txt("What does `lme4::lmer()` syntax mean, term by term?",
    code("lmer(y ~ x + (1 | school), data = d)              # random intercept per school\n"
         "lmer(y ~ x + (x | school), data = d)              # random intercept AND slope, correlated\n"
         "lmer(y ~ x + (x || school), data = d)             # same, correlation forced to 0\n"
         "lmer(y ~ x + (1 | school/class), data = d)        # NESTED: class within school\n"
         "lmer(y ~ x + (1 | subject) + (1 | item), data = d) # CROSSED random effects\n"
         "lmer(y ~ x + (0 + x | school), data = d)          # random slope, no random intercept\n"
         "lmer(y ~ x + (1 | school), REML = FALSE)          # ML instead of REML (for LR tests)") +
    "Reading the syntax: `(left | right)` means 'the terms on the left vary randomly across the levels of "
    "the grouping factor on the right'. `1` is the intercept, so `(1|g)` is a group-specific offset and "
    "`(x|g)` additionally lets the effect of x differ by group.<br><br>"
    "Practical points:<br>"
    "- The grouping variable must be a <b>factor</b>, and nesting requires either unique labels or the "
    "`g1/g2` syntax.<br>"
    "- `(x|g)` estimates 3 parameters (two variances plus their correlation); `(x||g)` estimates 2.<br>"
    "- `summary()` gives variance components; `VarCorr()`, `ranef()` (BLUPs), `fixef()`, "
    "`confint(fit, method = \"profile\")`.<br>"
    "- `lmerTest::lmer()` adds Satterthwaite p-values; `pbkrtest` gives Kenward-Roger.<br>"
    "- `lme4` deliberately reports no p-values for `lmer` because the denominator df are not well "
    "defined.",
    f"{T} lme4 lmer random-effects syntax")

txt("When do you use `glmer()`, `glmmTMB()` or `nlme::lme()` instead of `lmer()`?",
    "- <b>`lme4::glmer()`</b> - non-normal responses with random effects (binomial, Poisson, "
    "`glmer.nb()`). Fitted by Laplace approximation, or `nAGQ = k` for adaptive Gauss-Hermite quadrature "
    "(more accurate, only for a single grouping factor, much slower). Binary outcomes with few "
    "observations per cluster need nAGQ > 1 to avoid bias.<br><br>"
    "- <b>`glmmTMB::glmmTMB()`</b> - the modern workhorse when `glmer` runs out: zero inflation "
    "(`ziformula = ~1`), an explicit dispersion model (`dispformula = ~x`, i.e. heteroscedasticity), "
    "beta, Tweedie, Conway-Maxwell and truncated families, and spatial/temporal correlation structures "
    "(`ou()`, `ar1()`, `exp()`). Faster and more stable for complex random-effect structures.<br><br>"
    "- <b>`nlme::lme()` / `gls()`</b> - when you need <b>residual</b> correlation and variance structures "
    "rather than (or in addition to) random effects:<br>"
    + code("gls(y ~ x, correlation = corAR1(form = ~ time | subject),\n"
           "    weights = varPower(form = ~ fitted(.)), data = d)\n"
           "lme(y ~ x, random = ~ 1 | subject, correlation = corCAR1(form = ~ time | subject))") +
    "This is the classical route for longitudinal data with unequally spaced times, for explicit "
    "unstructured or AR(1) covariance over time, and for modelling heteroscedasticity - things `lme4` "
    "cannot do. `nlme` also gives p-values for fixed effects by default.<br><br>"
    "- <b>`brms::brm()`</b> - same formula syntax as lme4 plus priors, distributional parameters, "
    "monotonic and measurement-error terms, and honest uncertainty for variance components.",
    f"{T} glmer glmmTMB nlme choice")

txt("How do you fit smooths with `mgcv::gam()`, and what are the important arguments?",
    code("library(mgcv)\n"
         "gam(y ~ s(x1) + s(x2, k = 20) + x3, family = poisson, method = \"REML\", data = d)\n"
         "gam(y ~ s(time, bs = \"cc\") + s(x, by = group) + group, ...)   # cyclic; smooth per group\n"
         "gam(y ~ te(lon, lat) + s(day, bs = \"cc\"), ...)                # tensor interaction + season\n"
         "gam(y ~ s(x) + ti(x, z), ...)                                 # main effects + interaction only\n"
         "bam(y ~ s(x1) + s(x2), discrete = TRUE, ...)                  # big data (millions of rows)") +
    "Arguments that matter:<br>"
    "- <b>`bs`</b>: `\"tp\"` thin-plate (default), `\"cr\"` cubic regression, `\"cc\"` cyclic (seasons, "
    "angles), `\"ps\"` P-splines, `\"ad\"` adaptive, `\"re\"` random effect, `\"mrf\"` Markov random field "
    "for areal data, `\"so\"` soap film for awkward boundaries.<br>"
    "- <b>`k`</b>: basis dimension - an <b>upper bound</b> on wiggliness, not the fitted complexity. Set it "
    "generously and let the penalty decide; check with `gam.check()` (if EDF is close to k-1, raise k).<br>"
    "- <b>`method = \"REML\"`</b>: the recommended smoothing-parameter criterion (less prone to "
    "undersmoothing than GCV).<br>"
    "- <b>`select = TRUE`</b> or `bs = \"ts\"`: shrinkage that can remove a term entirely.<br>"
    "- <b>`te()` vs `ti()` vs `s(x, by = z)`</b>: full tensor interaction, interaction-only (with main "
    "effects fitted separately), and a separate smooth per level of a factor.<br><br>"
    "Inspection: `summary()` gives EDF per smooth (EDF ≈ 1 means linear) and approximate p-values, "
    "`plot(fit, pages = 1, shade = TRUE)` shows the curves, `gam.check()` does the residual diagnostics, "
    "and `concurvity()` is the smooth analogue of collinearity.",
    f"{T} mgcv gam splines arguments")

txt("Can you fit random effects with `mgcv::gam()`, and what is the limit?",
    "Yes - and not just random intercepts, which is a common misconception. In `mgcv` a random effect is "
    "just a smooth with a ridge penalty, so:<br><br>"
    + code("gam(y ~ s(x) + s(school, bs = \"re\"), ...)              # random intercept\n"
           "gam(y ~ s(x) + s(school, bs = \"re\") + s(school, age, bs = \"re\"), ...)\n"
           "                                                     # random intercept + random SLOPE of age\n"
           "gam(y ~ s(x) + s(school, bs = \"re\") + s(school, x, bs = \"re\"), method = \"REML\", ...)") +
    "The `s(g, x, bs = \"re\")` form gives a random slope of x by g. So `gam` covers random intercepts "
    "<b>and</b> uncorrelated random slopes perfectly well.<br><br>"
    "Where the limit actually is:<br>"
    "- <b>No correlation between random intercept and random slope</b> - `bs = \"re\"` terms are "
    "independent, whereas `lmer`'s `(x|g)` estimates that correlation. If the correlation is of interest, "
    "`gam` is the wrong tool (this is what `(x||g)` in lme4 corresponds to).<br>"
    "- <b>No residual correlation structures</b> (AR(1) within subject) in plain `gam`.<br>"
    "- Fitting is <b>slow with many levels</b>, because the random effect enters as a dense penalised "
    "term rather than through sparse mixed-model machinery.<br><br>"
    "When you need the full mixed model with smooths: `gamm()` (wraps `nlme`, so it allows `correlation = "
    "corAR1()`), `gamm4::gamm4()` (wraps `lme4`, better for non-normal families and crossed effects), or "
    "`brms`/`glmmTMB` with spline bases. Conversely `lme4` can fit splines directly by putting "
    "`splines::ns(x, df)` in the fixed part.",
    f"{T} mgcv random-effects re-smooth gamm")

txt("How do you fit a GEE, and what do you have to specify?",
    code("library(geepack)\n"
         "geeglm(y ~ time + treat, id = subject, data = d,\n"
         "       family = binomial, corstr = \"exchangeable\")   # or \"ar1\", \"unstructured\", \"independence\"") +
    "What each argument does:<br>"
    "- <b>`id`</b>: the clustering variable. The data must be <b>sorted by id</b> for `corstr = \"ar1\"` to "
    "mean what you think, and `waves =` specifies the time ordering explicitly.<br>"
    "- <b>`corstr`</b>: the working correlation. Coefficients stay consistent even if it is wrong, but a "
    "closer guess buys efficiency: `exchangeable` for clusters with no ordering, `ar1` for equally spaced "
    "repeated measures, `unstructured` only with few time points and many clusters.<br>"
    "- Standard errors are the <b>sandwich</b> estimator by default - that is what makes the "
    "misspecification robustness real. With fewer than ~30-40 clusters they are anti-conservative; use a "
    "small-sample correction (`geesmv`, or cluster bootstrap).<br><br>"
    "Consequences of it being quasi-likelihood: no AIC and no LR tests - use <b>QIC</b> "
    "(`MuMIn::QIC`) for correlation-structure choice and Wald tests (`anova()`) for coefficients. "
    "Missing data must be MCAR unless you use weighted GEE.<br><br>"
    "Alternatives: `gee::gee()` (older), `geeM`, or a plain `glm()` with `sandwich::vcovCL()` cluster-robust "
    "standard errors - which is the same marginal estimate with an independence working correlation.",
    f"{T} geepack gee corstr sandwich")

txt("Which R functions do survival analysis?",
    code("library(survival)\n"
         "Surv(time, status)                       # right-censored\n"
         "Surv(t1, t2, status)                     # interval / counting process (time-varying covariates)\n"
         "survfit(Surv(time, status) ~ group)      # Kaplan-Meier\n"
         "survdiff(Surv(time, status) ~ group)     # log-rank test\n"
         "coxph(Surv(time, status) ~ x + strata(site) + frailty(id))\n"
         "cox.zph(fit)                             # test proportional hazards (Schoenfeld residuals)\n"
         "survreg(Surv(time, status) ~ x, dist = \"weibull\")   # parametric AFT\n"
         "coxme::coxme(), frailtyEM               # random effects / frailty") +
    "Around the core:<br>"
    "- <b>Competing risks</b>: `cmprsk::crr()` (Fine-Gray), `survival::finegray()`, "
    "`tidycmprsk`; cumulative incidence with `survfit(... , etype = )`.<br>"
    "- <b>Multi-state</b>: `mstate`, `msm`, `survival::survcheck()`.<br>"
    "- <b>Flexible parametric</b>: `flexsurv::flexsurvspline()` (Royston-Parmar) - good for extrapolation "
    "and for time-varying effects.<br>"
    "- <b>Prediction and validation</b>: `pec`, `riskRegression::Score()` (time-dependent AUC, IPCW Brier, "
    "calibration), `rms::validate()`.<br>"
    "- <b>Plots</b>: `survminer::ggsurvplot()` with risk tables.<br>"
    "- <b>Discrete-time survival</b>: expand to person-period data and use "
    "`glm(event ~ factor(period) + x, family = binomial(link = \"cloglog\"))`.<br><br>"
    "Detail worth remembering: `coxph` handles ties by Efron's method by default (better than Breslow), and "
    "time-varying covariates require the `(t1, t2]` counting-process format, not a wide layout.",
    f"{T} survival coxph survreg competing-risks")

txt("Which R functions fit ordinal, nominal and count models?",
    code("MASS::polr(y ~ x, method = \"logistic\")        # proportional odds (y an ordered factor)\n"
         "ordinal::clm(y ~ x, data = d)                 # more flexible: scale effects, other links\n"
         "ordinal::clmm(y ~ x + (1 | subject))          # ordinal MIXED model\n"
         "VGAM::vglm(y ~ x, family = cumulative(parallel = FALSE))  # partial proportional odds\n"
         "brant::brant(fit)                             # test the proportional-odds assumption\n\n"
         "nnet::multinom(y ~ x)                         # baseline-category multinomial logit\n"
         "mlogit::mlogit(), mclogit                     # conditional / discrete-choice logit\n\n"
         "MASS::glm.nb(y ~ x)                           # negative binomial\n"
         "pscl::zeroinfl(y ~ x | z), pscl::hurdle()     # zero-inflated / two-part\n"
         "glmmTMB(y ~ x, ziformula = ~1, family = nbinom2)   # ZI + random effects in one place\n"
         "betareg::betareg(y ~ x)                       # proportions in (0,1)") +
    "Practical notes:<br>"
    "- For `polr` the response must be an <b>ordered</b> factor, and the reported intercepts are "
    "thresholds; note the sign convention (`polr` parameterises as \\(\\eta=\\zeta_k-x^\\top\\beta\\)).<br>"
    "- In `zeroinfl(y ~ x | z)` the part after `|` is the <b>zero-inflation</b> model, which may use "
    "different covariates than the count part.<br>"
    "- Test zero inflation with `DHARMa::testZeroInflation()` rather than by intuition, and fit the "
    "negative binomial <b>first</b> - most apparent zero inflation is plain overdispersion.<br>"
    "- `emmeans` and `marginaleffects` work with all of these and are the sane way to get interpretable "
    "predictions rather than hand-decoding coefficient signs.",
    f"{T} polr multinom zeroinfl betareg")

txt("Which R functions do penalised, quantile and robust regression?",
    code("glmnet::cv.glmnet(x, y, alpha = 1, family = \"binomial\")   # lasso; alpha=0 ridge, 0<a<1 enet\n"
         "coef(cvfit, s = \"lambda.1se\")                             # or \"lambda.min\"\n"
         "glmnet(..., penalty.factor = , lower.limits = )            # exempt or constrain coefficients\n"
         "hdi, selectiveInference                                    # post-selection inference\n\n"
         "quantreg::rq(y ~ x, tau = c(0.1, 0.5, 0.9))                # quantile regression\n"
         "quantreg::rqss(y ~ qss(x))                                 # additive/nonparametric quantiles\n"
         "qgam::qgam(y ~ s(x), qu = 0.9)                             # smooth quantile regression\n\n"
         "MASS::rlm(y ~ x)                                           # M-estimation (Huber)\n"
         "robustbase::lmrob(y ~ x)                                   # MM-estimation, high breakdown\n"
         "sandwich::vcovHC(fit, type = \"HC3\"); sandwich::vcovCL(fit, cluster = ~ id)\n"
         "lmtest::coeftest(fit, vcov = vcovHC(fit, \"HC3\"))          # robust inference, OLS estimates") +
    "Reminders:<br>"
    "- `glmnet` needs a <b>model matrix</b>, not a formula (`model.matrix()` or `glmnetUtils`), and it "
    "standardises internally by default.<br>"
    "- `lambda.1se` is the more conservative choice; `lambda.min` maximises CV performance.<br>"
    "- Naive p-values after lasso selection are invalid - use `selectiveInference`, `hdi`, or split the "
    "data.<br>"
    "- Robust standard errors (`vcovHC`/`vcovCL`) fix <b>inference</b> for heteroscedasticity or "
    "clustering; robust regression (`lmrob`) changes the <b>estimates</b>. Different problems, often both "
    "needed.",
    f"{T} glmnet quantreg rlm sandwich")

txt("Which R packages do model diagnostics, contrasts and reporting?",
    code("# diagnostics\n"
         "plot(fit); car::vif(fit); car::Anova(fit, type = 3); car::influencePlot(fit)\n"
         "DHARMa::simulateResiduals(fit) |> plot()      # scaled residuals for GLM(M)s - the key tool\n"
         "DHARMa::testDispersion(); testZeroInflation(); testTemporalAutocorrelation()\n"
         "performance::check_model(fit)                 # one-call diagnostic panel\n"
         "lmtest::bptest(); dwtest(); bgtest(); resettest()\n"
         "mgcv::gam.check(fit); mgcv::concurvity(fit)\n\n"
         "# contrasts, predictions, marginal effects\n"
         "emmeans::emmeans(fit, ~ group, type = \"response\") |> pairs(adjust = \"tukey\")\n"
         "emmeans::emtrends(fit, ~ group, var = \"x\")   # slopes per group\n"
         "marginaleffects::avg_slopes(fit)              # average marginal effects\n"
         "marginaleffects::predictions(fit, newdata = datagrid(x = ...))\n\n"
         "# reporting\n"
         "broom::tidy(fit, conf.int = TRUE); broom::augment(fit); broom.mixed::tidy()\n"
         "modelsummary::modelsummary(list(m1, m2)); gtsummary::tbl_regression(fit)\n"
         "sjPlot::plot_model(fit, type = \"pred\")") +
    "The two that change how you work:<br>"
    "- <b>DHARMa</b> makes residual diagnostics meaningful for GLMs and GLMMs, where raw residual plots are "
    "uninformative - it simulates from the fitted model and transforms residuals to uniform.<br>"
    "- <b>emmeans / marginaleffects</b> free you from decoding coefficients: they compute predictions, "
    "contrasts and average marginal effects on the response scale with correct standard errors, "
    "including for interactions, splines and mixed models. This is how you get a risk difference from a "
    "logistic model or an interpretable slope from a GAM.",
    f"{T} diagnostics dharma emmeans reporting")

txt("Which R packages compute performance metrics?",
    code("pROC::roc(y, p); auc(); ci.auc(); roc.test(r1, r2)   # DeLong test for two AUCs\n"
         "PRROC::pr.curve(scores.class0 = , weights.class0 = ) # PR-AUC done properly\n"
         "yardstick::roc_auc(d, truth, .pred); pr_auc(); brier_class(); rmse(); mae(); mase()\n"
         "MLmetrics, Metrics                                   # quick one-off metrics\n"
         "rms::val.prob(p, y)                                  # calibration + discrimination at once\n"
         "rms::validate(fit, method = \"boot\"); rms::calibrate(fit)\n"
         "riskRegression::Score(list(m1, m2), formula = Hist(time, status) ~ 1, times = 5)\n"
         "dcurves::dca(y ~ p)                                  # decision curve analysis / net benefit\n"
         "scoringRules::crps_sample(); scoringutils                # probabilistic forecasts\n"
         "CalibrationCurves::valProbggplot()                   # calibration with a flexible smooth") +
    "Workflow advice:<br>"
    "- Compute metrics inside the resampling loop, not on the training data: `tidymodels` "
    "(`rsample` + `recipes` + `workflows` + `tune`), `caret::train()`, or `mlr3` with "
    "`resampling = rsmp(\"cv\")` and grouped/temporal variants.<br>"
    "- `rms::val.prob()` is the fastest way to see discrimination and calibration together for a binary "
    "model - and `rms`/`Hmisc` (Harrell) is the package built around 'validate and calibrate, do not "
    "step-select'.<br>"
    "- For comparing two models' AUCs on the same data use `pROC::roc.test()` (DeLong), not two "
    "independent confidence intervals.",
    f"{T} metrics proc yardstick rms")

txt("Which R packages handle time series, spatial data, missing data and causal inference?",
    code("# time series\n"
         "forecast::auto.arima(), ets(), forecast(); fable + tsibble (tidy successor)\n"
         "stats::arima(), StructTS; KFAS, dlm (state space); rugarch (GARCH); vars (VAR)\n"
         "prophet; mgcv::gam(y ~ s(t) + s(month, bs = \"cc\"))    # regression-style alternative\n\n"
         "# spatial\n"
         "sf (geometry); spdep::moran.test(), lagsarlm(), errorsarlm()\n"
         "gstat (variogram, kriging); INLA / spaMM; mgcv::gam(y ~ s(lon, lat))\n"
         "CARBayes, nimble (BYM disease mapping); spatstat (point processes)\n\n"
         "# missing data\n"
         "mice::mice(d, m = 20) |> with(lm(y ~ x)) |> pool()     # multiple imputation + Rubin's rules\n"
         "naniar, VIM (visualise patterns); missForest; Amelia\n\n"
         "# causal inference\n"
         "MatchIt::matchit(); WeightIt; cobalt::bal.tab()        # matching / weighting + BALANCE checks\n"
         "AER::ivreg(); fixest::feols(y ~ x | fe | z ~ w)        # IV, fixed effects, clustered SEs\n"
         "did::att_gt(); fixest::sunab()                         # staggered difference-in-differences\n"
         "rdrobust::rdrobust()                                   # regression discontinuity\n"
         "tmle, SuperLearner, DoubleML                           # doubly robust / ML nuisance models\n"
         "dagitty, ggdag                                         # draw the DAG, find adjustment sets") +
    "Two habits worth copying: check <b>covariate balance</b> (`cobalt`) rather than the propensity model's "
    "fit, and draw the <b>DAG</b> before choosing covariates - `dagitty::adjustmentSets()` will tell you "
    "which variables to include and, importantly, which to leave out.",
    f"{T} time-series spatial missing-data causal packages")

txt("What do you do when `lmer` or `glmer` reports a singular fit or fails to converge?",
    "<b>Singular fit</b> means a variance component is estimated at (or near) zero, or a random-effect "
    "correlation at ±1. It is a message about the <b>data</b>, not a bug: the design does not support that "
    "much random-effect structure.<br><br>"
    "In order:<br>"
    "1. Check the design: how many <b>levels</b> does the grouping factor have (fewer than ~5-6 and it "
    "should probably be a fixed effect), and how many observations per level? A random slope needs several "
    "observations per group spanning a range of x.<br>"
    "2. <b>Simplify</b>: drop the intercept-slope correlation (`(x||g)`), then the random slope. Keep the "
    "structure the design implies, but do not fit what the data cannot identify.<br>"
    "3. <b>Rescale and centre</b> the predictors - a huge share of convergence warnings are just badly "
    "scaled covariates. `scale()` the continuous ones.<br>"
    "4. Try another optimiser: `control = lmerControl(optimizer = \"bobyqa\", optCtrl = list(maxfun = 2e5))`, "
    "or `allFit()` to see whether all optimisers agree (if they do, the fit is fine and the warning is "
    "cosmetic).<br>"
    "5. For GLMMs, raise `nAGQ`, or switch to `glmmTMB`, which is often more stable.<br>"
    "6. If the variance is genuinely near zero and the design still demands it, a <b>Bayesian</b> fit "
    "(`brms`, `blme`) with a weakly informative prior gives a sensible answer instead of a boundary "
    "estimate.<br><br>"
    "What not to do: ignore a convergence failure and report the coefficients anyway, or keep dropping "
    "terms until the warning disappears and then present the model as if it had been chosen a priori.",
    f"{T} lme4 singular-fit convergence troubleshooting")

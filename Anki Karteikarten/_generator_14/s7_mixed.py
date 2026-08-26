# -*- coding: utf-8 -*-
"""Section 7 - mixed models: what they are, when they are used."""
from plotlib import *

T = "Core mixed-models"
PIC = []
TXT = []


def pic(front, builder, back, tags):
    PIC.append((front, builder, back, tags))


def txt(front, back, tags):
    TXT.append((front, back, tags))


def _structures():
    cv = Canvas(w=470, h=290, pad=(10, 10, 10, 10))
    COLS = ["blue", "green", "amber"]

    def panel(px0, px1, title, lines, note):
        """lines: list of (intercept, slope), y measured in [-2.2, 2.2]."""
        top, bot = 58, 172

        def Yp(v):
            return bot - (v + 2.2) / 4.4 * (bot - top)

        cv.raw(f'<line x1="{px0}" y1="{bot}" x2="{px1}" y2="{bot}" stroke="currentColor"'
               f' stroke-width="1.1" stroke-opacity="0.8"/>')
        cv.raw(f'<line x1="{px0}" y1="{bot}" x2="{px0}" y2="{top}" stroke="currentColor"'
               f' stroke-width="1.1" stroke-opacity="0.8"/>')
        cv.text((px0 + px1) / 2, 44, title, size=9.5, weight="bold", data=False)
        cv.text((px0 + px1) / 2, bot + 15, "x", size=8.5, opacity=0.7, data=False)
        for (icpt, slope), col in zip(lines, COLS):
            x1p, x2p = px0 + 8, px1 - 8
            y1, y2 = icpt - slope * 0.5, icpt + slope * 0.5
            cv.raw(f'<line x1="{x1p}" y1="{n(Yp(y1))}" x2="{x2p}" y2="{n(Yp(y2))}"'
                   f' stroke="{C[col]}" stroke-width="2"/>')
        cv.text((px0 + px1) / 2, 190, note, size=8.5, opacity=0.75, data=False)

    # parallel lines, different levels
    panel(30, 148, "random intercept",
          [(-1.3, 1.1), (0.0, 1.1), (1.3, 1.1)], "(1 | g)   levels differ")
    # same level at mid-x, fanning out
    panel(178, 296, "random slope",
          [(0.0, 2.6), (0.0, 1.1), (0.0, -0.4)], "(0 + x | g)   effects differ")
    # both differ
    panel(326, 444, "both",
          [(-1.2, 2.6), (0.1, 1.1), (1.3, -0.4)], "(x | g)   level and effect")
    cv.text(235, 22, "three groups, one covariate x", size=10, weight="bold", data=False)
    cv.caption(["random effects are drawn from a distribution: b ~ N(0, σ²_b) - they are not free parameters",
                "so each group's line is SHRUNK toward the overall line, by how little data that group has",
                "(x | g) also estimates the intercept-slope correlation; (x || g) forces it to zero"],
               x=16, y0=224)
    return cv


pic("Sketch a random intercept, a random slope, and both together",
    _structures,
    "A mixed model gives each cluster its own line, but the lines are not estimated freely - they are "
    "assumed to be <b>draws from a distribution</b>.<br><br>"
    "- <b>Random intercept</b> `(1 | g)`: clusters differ in their <b>level</b>, the effect of x is common. "
    "One extra parameter, \\(\\sigma^2_b\\). This is the model that says 'observations in the same cluster "
    "are correlated'.<br>"
    "- <b>Random slope</b> `(0 + x | g)`: clusters differ in how strongly x acts.<br>"
    "- <b>Both</b> `(x | g)`: level and effect vary, plus their <b>correlation</b> (e.g. groups that start "
    "high improve more slowly). Three parameters.<br><br>"
    "\\[ y_{ij}=\\underbrace{\\beta_0+\\beta_1x_{ij}}_{\\text{fixed: population}}+"
    "\\underbrace{b_{0j}+b_{1j}x_{ij}}_{\\text{random: deviation of cluster }j}+\\varepsilon_{ij} \\]"
    "\\[ \\begin{pmatrix}b_{0j}\\\\ b_{1j}\\end{pmatrix}\\sim N(0,\\Sigma_b),\\qquad "
    "\\varepsilon_{ij}\\sim N(0,\\sigma^2) \\]<br>"
    "Because the \\(b_j\\) come from a common distribution, they are <b>shrunk</b> toward zero, and a "
    "cluster with little data is pulled strongly toward the population line. That is the whole trick: it "
    "buys stability compared with fitting each group separately, and honest standard errors compared with "
    "ignoring the grouping.",
    f"{T} random-intercept random-slope structure diagram")


def _shrinkage():
    cv = Canvas(w=460, h=290, pad=(56, 16, 34, 20))
    cv.limits((0, 1), (0, 1))
    cv.axes(y_axis=True, xticks=[], yticks=[],
            xlabel="", ylabel="estimated group mean")
    # three columns: no pooling, partial pooling, complete pooling
    cols = [0.16, 0.5, 0.84]
    labels = ["no pooling\n(fit each group)", "partial pooling\n(mixed model)",
              "complete pooling\n(ignore groups)"]
    raw = [0.10, 0.28, 0.42, 0.55, 0.72, 0.93]
    ns = [2, 40, 6, 30, 3, 50]          # group sizes: small n shrinks more
    grand = 0.52
    part = []
    for r, k in zip(raw, ns):
        w = k / (k + 12.0)
        part.append(w * r + (1 - w) * grand)
    cv.line(0, grand, 1, grand, width=1.1, dash="4 3", opacity=0.5)
    cv.text(0.985, grand + 0.03, "overall mean", size=8.5, opacity=0.65, anchor="end")
    palette = ["blue", "green", "amber", "violet", "rose", "cyan"]
    for i, (r, p) in enumerate(zip(raw, part)):
        col = C[palette[i % len(palette)]]
        cv.line(cols[0], r, cols[1], p, color=col, width=1.2, opacity=0.55, dash="2 3")
        cv.line(cols[1], p, cols[2], grand, color=col, width=1.2, opacity=0.35, dash="2 3")
        cv.circle(cols[0], r, r=3.4, fill=col)
        cv.circle(cols[1], p, r=3.4, fill=col)
        cv.circle(cols[2], grand, r=3.0, fill=col, fo=0.55)
        cv.text(cols[0] - 0.035, r + 0.012, f"n={ns[i]}", size=8, opacity=0.7, anchor="end")
    for x, lab in zip(cols, ["no pooling", "partial pooling", "complete pooling"]):
        cv.text(x, 1.03, lab, size=9.5, weight="bold")
    cv.caption(["the BLUP is a precision-weighted compromise between the group's own mean and the overall mean",
                "shrinkage weight = n / (n + σ²/σ²_b): big groups keep their estimate, small groups borrow strength",
                "this is why mixed models beat per-group fits for prediction - and why they are 'credibility' in insurance"])
    return cv


pic("What is shrinkage / partial pooling in a mixed model?",
    _shrinkage,
    "A mixed-model estimate for cluster j - its <b>BLUP</b> (best linear unbiased predictor) - is a "
    "precision-weighted compromise between that cluster's own mean and the overall mean:<br><br>"
    "\\[ \\hat\\mu_j=w_j\\bar y_j+(1-w_j)\\bar y,\\qquad "
    "w_j=\\frac{n_j}{n_j+\\sigma^2/\\sigma^2_b} \\]<br><br>"
    "So a large, well-measured cluster keeps essentially its own estimate, while a cluster with three "
    "observations is pulled hard toward the population mean - it <b>borrows strength</b> from the others. "
    "The two extremes are special cases: \\(\\sigma^2_b\\to\\infty\\) gives no pooling (a fixed effect per "
    "group), \\(\\sigma^2_b\\to 0\\) gives complete pooling (ignore the grouping).<br><br>"
    "Why this matters in practice:<br>"
    "- It solves the small-sample ranking problem: the hospital with 4 patients and a 100 % success rate is "
    "not really the best hospital. League tables, teacher value-added, small-area estimation and sports "
    "ratings all need this.<br>"
    "- It is the same mathematics as <b>credibility weighting</b> in insurance, Stein estimation, and a "
    "normal prior in Bayesian analysis - shrinkage lowers variance far more than it adds bias, so it "
    "improves prediction.<br>"
    "- The BLUPs are <b>predictions, not parameters</b>: their intervals must account for the estimated "
    "variance components, and you should not treat them as if each group had been fitted independently.",
    f"{T} shrinkage blup partial-pooling diagram")


def _icc():
    cv = Canvas(w=460, h=280, pad=(52, 16, 34, 20))
    cv.limits((0, 1), (0, 1))
    cv.axes(xticks=[], yticks=[], xlabel="", ylabel="outcome")
    # left: low ICC, right: high ICC
    import random as _r
    _r.seed(7)
    palette = ["blue", "green", "amber", "rose"]
    for panel, (spread_b, spread_w, title, x0) in enumerate(
            [(0.06, 0.22, "low ICC: groups overlap", 0.06),
             (0.26, 0.06, "high ICC: groups separate", 0.56)]):
        centres = [0.30, 0.45, 0.58, 0.72]
        mean = sum(centres) / 4
        for gi, c in enumerate(centres):
            cen = mean + (c - mean) * (spread_b / 0.16)
            col = C[palette[gi]]
            gx = x0 + 0.085 * gi + 0.02
            for k in range(7):
                jitter = (_r.random() - 0.5) * 0.05
                y = cen + (_r.random() - 0.5) * 2 * spread_w
                cv.circle(gx + jitter, min(0.97, max(0.03, y)), r=2.4, fill=col, fo=0.85)
            cv.line(gx - 0.028, cen, gx + 0.028, cen, color=col, width=2)
        cv.text(x0 + 0.18, 1.02, title, size=9.5, weight="bold")
    cv.line(0.5, 0, 0.5, 1.0, width=1, opacity=0.25, dash="3 3")
    cv.caption(["ICC = σ²_b / (σ²_b + σ²) = the share of total variance that is BETWEEN clusters",
                "= the correlation of two observations in the same cluster",
                "design effect = 1 + (m-1)·ICC: ICC 0.1 with clusters of 20 &#8658; 1000 obs are worth ~345"])
    return cv


pic("What is the intraclass correlation, and why does it decide your effective sample size?",
    _icc,
    "The ICC is the fraction of the total variance that lies <b>between</b> clusters:<br><br>"
    "\\[ \\text{ICC}=\\rho=\\frac{\\sigma^2_b}{\\sigma^2_b+\\sigma^2} \\]<br><br>"
    "Equivalently - and this is the more useful reading - it is the <b>correlation between two "
    "observations from the same cluster</b>. ICC ≈ 0 means the grouping is irrelevant; ICC ≈ 1 means "
    "everything within a cluster is a repeat of the same information.<br><br>"
    "Why it drives sample size: with clusters of size m, the variance of the mean is inflated by the "
    "<b>design effect</b><br><br>"
    "\\[ \\text{DE}=1+(m-1)\\rho,\\qquad n_{\\text{eff}}=\\frac{n}{1+(m-1)\\rho} \\]<br><br>"
    "So an ICC of only 0.05 with clusters of 50 gives a design effect of 3.5 - 1000 observations carry the "
    "information of about 290. This is why:<br>"
    "- <b>adding clusters helps far more than adding observations per cluster</b> once m is moderate;<br>"
    "- cluster-randomised trials need an explicit ICC assumption in their power calculation;<br>"
    "- analysing clustered data as independent produces standard errors that are far too small.<br><br>"
    "Typical values worth knowing: 0.01-0.05 for patients within GP practices, 0.1-0.2 for pupils within "
    "classes, higher for repeated measures within one person. For GLMMs the ICC needs a latent-scale "
    "definition (e.g. \\(\\sigma^2_b/(\\sigma^2_b+\\pi^2/3)\\) for logistic models).",
    f"{T} icc design-effect sample-size diagram")


# ---------------------------------------------------------------------------
txt("What exactly is a mixed model?",
    "A regression model containing <b>both</b> fixed and random effects:<br><br>"
    "\\[ y=X\\beta+Zb+\\varepsilon,\\qquad b\\sim N(0,G),\\quad \\varepsilon\\sim N(0,R) \\]<br><br>"
    "- <b>Fixed effects</b> \\(\\beta\\): the population-level coefficients you want to estimate and report. "
    "One parameter per covariate.<br>"
    "- <b>Random effects</b> \\(b\\): cluster-specific deviations that are <b>not</b> free parameters but "
    "draws from a distribution. You estimate their <b>variance</b> (a few numbers), not each deviation, so "
    "a factor with 500 levels costs one parameter rather than 499.<br><br>"
    "The consequence that defines the model class: marginalising over b induces a <b>covariance structure</b> "
    "in y,<br><br>"
    "\\[ \\operatorname{Var}(y)=ZGZ^\\top+R \\]<br><br>"
    "so observations sharing a cluster are correlated. A random intercept implies exactly the exchangeable "
    "(compound-symmetry) correlation ICC within each cluster.<br><br>"
    "Two equivalent ways to read the same model: as a two-level data-generating process (clusters drawn "
    "from a population, observations drawn within clusters), or as a single regression with a structured "
    "error term. The first view is better for design, the second for understanding the standard errors.",
    f"{T} definition variance-structure")

txt("When do you need a mixed model?",
    "Whenever observations are <b>grouped</b> and that grouping is a sample from a population of groups you "
    "want to generalise to. Concretely:<br><br>"
    "- <b>Repeated measures / longitudinal data</b>: several measurements per patient, per plot, per "
    "customer over time.<br>"
    "- <b>Clustered sampling</b>: pupils in classes in schools, patients in hospitals, employees in firms, "
    "plots in fields.<br>"
    "- <b>Multi-centre studies</b>: a centre effect you do not care about individually but must account "
    "for.<br>"
    "- <b>Crossed designs</b>: subjects × items in psycholinguistics, raters × cases in agreement studies "
    "(this is where 'random effects' become unavoidable, since neither factor nests in the other).<br>"
    "- <b>Split-plot and blocked experiments</b>: different treatments randomised at different levels, "
    "hence different error terms.<br>"
    "- <b>Meta-analysis</b>: studies as random effects, which is literally what a random-effects "
    "meta-analysis is.<br>"
    "- <b>Small-area estimation and league tables</b>: you need shrinkage to avoid ranking noise.<br>"
    "- <b>Variance is the question</b>: heritability, measurement-reliability studies, between-hospital "
    "variation, insurance credibility.<br><br>"
    "Three things it buys you: <b>correct standard errors</b> (dependence accounted for), "
    "<b>shrunken, more accurate group-level predictions</b>, and an explicit <b>decomposition of "
    "variance</b> across levels. What it is not: a way to fix confounding.",
    f"{T} when-to-use clustered longitudinal")

txt("How do you decide whether a factor should be a fixed or a random effect?",
    "Ask what you want to conclude and how many levels there are.<br><br>"
    "<b>Fixed</b> when:<br>"
    "- the levels are the <b>specific ones you care about</b> (treatment arms, sex, dose groups);<br>"
    "- the levels exhaust the population (all four seasons, both eyes);<br>"
    "- there are <b>few levels</b> - with fewer than about 5-6 the variance is barely estimable;<br>"
    "- the factor may be <b>correlated with your covariates</b>, i.e. it is a potential confounder. A "
    "fixed-effect (within) specification absorbs all time-constant cluster-level confounding; a random "
    "effect assumes there is none.<br><br>"
    "<b>Random</b> when:<br>"
    "- the levels are a <b>sample</b> from a larger population and you want to generalise to it "
    "(these 40 schools stand for schools in general);<br>"
    "- you want to <b>predict for a new level</b>, or to predict shrunken values for existing ones;<br>"
    "- there are many levels and the fixed version would burn the degrees of freedom;<br>"
    "- the <b>variance itself</b> is of interest;<br>"
    "- the design is <b>crossed</b> or has several nested levels.<br><br>"
    "The trade-off in one line: random effects assume the cluster effects are <b>independent of the "
    "covariates</b> and buy you efficiency, shrinkage and generalisability; fixed effects drop that "
    "assumption and buy you robustness to cluster-level confounding. The <b>Hausman test</b> checks the "
    "assumption, and the <b>Mundlak device</b> (adding cluster means as covariates) gives you both at once.",
    f"{T} fixed-vs-random choice hausman")

txt("What is the difference between nested and crossed random effects?",
    "<b>Nested</b>: each level of the inner factor belongs to exactly one level of the outer factor - "
    "pupils in classes in schools, patients in wards in hospitals, measurements within samples within "
    "batches. Class 1 in school A has nothing to do with class 1 in school B.<br><br>"
    "\\[ \\texttt{(1 | school) + (1 | school:class)}\\quad\\text{or}\\quad\\texttt{(1 | school/class)} \\]<br><br>"
    "<b>Crossed</b>: every level of one factor can appear with every level of the other - subjects × items "
    "(each participant sees each word), raters × cases, drivers × cars, players × opponents.<br><br>"
    "\\[ \\texttt{(1 | subject) + (1 | item)} \\]<br><br>"
    "Practical notes:<br>"
    "- <b>Implicit nesting is a classic bug</b>: if classes are labelled 1, 2, 3 within every school, R "
    "treats class 1 in all schools as the same level. Either use `school/class` or create unique labels.<br>"
    "- Crossed random effects are why classical repeated-measures ANOVA fails on psycholinguistic data - it "
    "cannot handle two crossed sources of variation at once, and 'aggregate over items then over subjects' "
    "loses power and inflates error rates (Clark's language-as-fixed-effect fallacy).<br>"
    "- `lme4` handles crossed effects efficiently through sparse matrices; `nlme` is built around nesting "
    "and struggles with crossing.<br>"
    "- Partially crossed designs (each rater sees some cases) are fine - no balance is required.",
    f"{T} nested crossed design syntax")

txt("Why must you centre covariates in a mixed model - what are within and between effects?",
    "A covariate measured at the observation level usually carries <b>two different effects</b>, and an "
    "uncentred model reports an uninterpretable blend of them.<br><br>"
    "Example: does a heavier workload reduce performance? The <b>within-person</b> effect (in weeks where "
    "<i>I</i> work more than usual, how do I perform?) and the <b>between-person</b> effect (do people who "
    "generally work more perform worse?) can differ in size and even in <b>sign</b> - this is Simpson's "
    "paradox at the multilevel level, and the between version is vulnerable to all the confounding among "
    "persons that the within version is immune to.<br><br>"
    "The fix is to split the variable explicitly:<br><br>"
    "\\[ y_{ij}=\\beta_0+\\beta_W(x_{ij}-\\bar x_j)+\\beta_B\\bar x_j+b_{0j}+\\varepsilon_{ij} \\]<br><br>"
    "- <b>Group-mean centring</b> \\((x_{ij}-\\bar x_j)\\) gives the pure within-cluster effect, free of "
    "cluster-level confounding (equivalent to a fixed-effects estimator).<br>"
    "- The cluster mean \\(\\bar x_j\\) as an extra covariate gives the between-cluster effect. Including "
    "both is the <b>Mundlak</b> specification, and testing \\(\\beta_W=\\beta_B\\) is a Hausman test.<br><br>"
    "Also: with a random slope, centring changes what the random <b>intercept</b> means (the level at x = 0), "
    "so grand-mean centring makes the intercept variance interpretable and usually improves convergence.",
    f"{T} centering within-between mundlak simpsons-paradox")

txt("What is the difference between ML and REML, and when does it matter?",
    "Both estimate the variance components by maximising a likelihood, but ML treats the fixed effects as "
    "known while REML integrates them out.<br><br>"
    "- <b>ML</b> variance estimates are <b>biased downward</b>, because they do not account for the degrees "
    "of freedom used up by estimating \\(\\beta\\) - the same reason the naive variance estimator divides "
    "by n instead of n-1.<br>"
    "- <b>REML</b> corrects for that, so it is the default for reporting variance components, ICCs and "
    "standard errors. The bias matters most with <b>few clusters</b> or many fixed effects.<br><br>"
    "The rule that follows:<br>"
    "- comparing models that differ in their <b>fixed</b> effects → refit with <b>ML</b> "
    "(`REML = FALSE`), because REML likelihoods computed under different fixed-effect structures are "
    "<b>not comparable</b> - this includes AIC and LR tests;<br>"
    "- comparing models that differ in their <b>random</b> effects → REML is fine (and preferable), "
    "keeping the fixed part identical;<br>"
    "- final reporting of variance components → REML.<br><br>"
    "Related: REML is also the recommended criterion for choosing smoothing parameters in `mgcv`, which is "
    "the same problem in disguise, since a penalised spline is a random effect. For Bayesian fits the "
    "distinction dissolves - the posterior already integrates over the fixed effects.",
    f"{T} reml ml variance-components comparison")

txt("How do you test fixed effects in a mixed model, and why is it awkward?",
    "The awkwardness is real: the denominator degrees of freedom are not well defined, because the "
    "effective sample size lies somewhere between the number of clusters and the number of observations, "
    "depending on the ICC and the design. That is why `lme4` refuses to print p-values.<br><br>"
    "Options, best first:<br>"
    "- <b>Kenward-Roger</b> (`pbkrtest::KRmodcomp`) - adjusts both the covariance and the df; the most "
    "reliable for small samples in linear mixed models.<br>"
    "- <b>Satterthwaite</b> (`lmerTest`) - nearly as good, much cheaper, hence the practical default.<br>"
    "- <b>Parametric bootstrap</b> (`pbkrtest::PBmodcomp`, `bootMer`) - assumption-light, expensive, and "
    "the honest choice for GLMMs.<br>"
    "- <b>LR test with ML fits</b> - fine when the number of clusters is large; anti-conservative "
    "otherwise.<br>"
    "- <b>Wald z / chi-square</b> - what `glmer` and `glmmTMB` report; acceptable with many clusters, "
    "optimistic with few.<br><br>"
    "For a <b>random</b> effect the problem is different: the null sits on the boundary (variance = 0), so "
    "the LR statistic follows a \\(\\tfrac12\\chi^2_0+\\tfrac12\\chi^2_1\\) mixture and the naive p-value "
    "is roughly twice too large. Use `RLRsim::exactRLRT`, a parametric bootstrap, or simply keep the term "
    "because the design implies it.<br><br>"
    "Rule of thumb: with fewer than about 30-40 clusters, take any p-value from a mixed model with "
    "suspicion and prefer KR, bootstrap or Bayesian intervals.",
    f"{T} testing kenward-roger satterthwaite boundary")

txt("How do you choose the random-effects structure?",
    "Two schools, and both have a point.<br><br>"
    "- <b>Keep it maximal</b> (Barr et al.): include every random slope the design justifies - i.e. for "
    "every within-cluster covariate. Omitting a random slope that is really there makes the corresponding "
    "fixed effect's test <b>anti-conservative</b>: you manufacture significance by treating repeated "
    "measurements as independent replicates.<br>"
    "- <b>Keep it parsimonious</b> (Bates et al.): maximal models are frequently unidentifiable, produce "
    "singular fits and degenerate correlation estimates, and then the reported uncertainty is not "
    "trustworthy either.<br><br>"
    "A workable compromise:<br>"
    "1. Start from the <b>design</b>: what was randomised or measured at which level? Random intercepts for "
    "every grouping factor, random slopes for covariates that vary <b>within</b> those groups. A covariate "
    "that is constant within a cluster cannot have a random slope.<br>"
    "2. Fit it, and if it is singular, simplify in this order: intercept-slope <b>correlations</b> first "
    "(`||`), then the least-supported random slopes.<br>"
    "3. Use REML and keep the fixed part fixed while doing this.<br>"
    "4. Report what you did, and prefer a Bayesian fit with weakly informative priors "
    "(`brms`, `blme`) if you need the full structure that ML cannot identify.<br><br>"
    "Never simplify the random structure by testing the fixed effect of interest under each variant and "
    "picking the version you like.",
    f"{T} random-structure maximal parsimonious")

txt("What changes when you move from a linear mixed model to a GLMM?",
    "Four things get harder:<br><br>"
    "1. <b>No closed-form likelihood.</b> The random effects must be integrated out numerically - Laplace "
    "approximation (default), adaptive Gauss-Hermite quadrature (`nAGQ`, more accurate but only for one "
    "grouping factor), or MCMC. Laplace can be noticeably biased for <b>binary</b> outcomes with few "
    "observations per cluster.<br>"
    "2. <b>Marginal ≠ conditional.</b> Coefficients are conditional on the random effect, and the "
    "population-average effect is <b>attenuated</b> toward zero: "
    "\\(\\beta_{\\text{marg}}\\approx\\beta_{\\text{cond}}/\\sqrt{1+0.346\\sigma_b^2}\\) for logistic "
    "models. So a GLMM and a GEE on the same data legitimately give different numbers.<br>"
    "3. <b>ICC needs a latent-scale definition</b>, e.g. \\(\\sigma^2_b/(\\sigma^2_b+\\pi^2/3)\\) for the "
    "logit link, because there is no separate residual variance on the response scale.<br>"
    "4. <b>Diagnostics need simulation.</b> Raw residuals from a binomial or Poisson GLMM are "
    "uninformative; use `DHARMa` scaled residuals, and check dispersion and zero inflation explicitly.<br><br>"
    "Also note: overdispersion in a Poisson GLMM can be handled with an <b>observation-level random "
    "effect</b> (which makes it a lognormal-Poisson), or by switching to a negative binomial family in "
    "`glmmTMB` - the cleaner option.",
    f"{T} glmm laplace attenuation dharma")

txt("What are the alternatives to a mixed model for clustered data, and when is each preferable?",
    "- <b>Cluster-robust standard errors</b> on a plain GLM (`sandwich::vcovCL`, `fixest`): keeps the "
    "marginal estimate, fixes the inference, assumes nothing about the correlation structure. Excellent "
    "when you only need valid standard errors and have many clusters; useless if you want variance "
    "components or cluster-level predictions, and unreliable with few clusters.<br>"
    "- <b>GEE</b>: marginal (population-average) coefficients, robust to a misspecified correlation "
    "structure. Choose it when the population-average effect is the target and you have many clusters.<br>"
    "- <b>Fixed effects / within estimator</b> (a dummy per cluster, or `feols`): removes <b>all</b> "
    "time-constant cluster-level confounding - the strongest protection against unobserved cluster "
    "characteristics. Costs: cannot estimate effects of cluster-constant covariates, no prediction for new "
    "clusters, no shrinkage, and it discards all between-cluster information.<br>"
    "- <b>Aggregate to the cluster level</b> and analyse cluster means: valid, simple, and sometimes the "
    "right answer for cluster-randomised trials - but it throws away within-cluster covariates.<br>"
    "- <b>Bayesian hierarchical model</b> (`brms`, `rstanarm`): same structure, better behaved with few "
    "clusters or complex random structures, honest uncertainty for variance components.<br><br>"
    "Choosing: variance components or shrunken group predictions → mixed model. Population-average effect "
    "with minimal assumptions → GEE or robust SEs. Fear of cluster-level confounding → fixed effects "
    "(or Mundlak).",
    f"{T} alternatives gee fixed-effects robust-se")

txt("How do you model longitudinal data, and how do random effects relate to correlation structures?",
    "Two equivalent-looking routes that make different assumptions:<br><br>"
    "- <b>Random effects</b>: a random intercept implies <b>compound symmetry</b> - the same correlation "
    "between any two time points, however far apart. Adding a random slope of time gives a growth-curve "
    "model, in which the implied variance grows with time² and the correlation decays realistically. "
    "Natural when subject-specific trajectories are the object of interest.<br>"
    "- <b>Residual correlation structures</b> (`nlme::lme(..., correlation = corAR1())`, `gls`, "
    "`glmmTMB` `ar1()`): correlation decaying with the time gap - usually more realistic for closely spaced "
    "measurements; `corCAR1` handles unequally spaced times, and an <b>unstructured</b> covariance is the "
    "most general option when there are few time points and many subjects.<br><br>"
    "In practice they are often combined: a random intercept for the subject plus AR(1) residuals.<br><br>"
    "Other essentials for longitudinal work:<br>"
    "- model <b>time flexibly</b> (splines or a GAM) rather than assuming linearity;<br>"
    "- separate <b>within</b> and <b>between</b> effects for time-varying covariates (centring);<br>"
    "- mixed models handle <b>unbalanced, missing and irregular</b> data under MAR by likelihood, which is "
    "a major advantage over repeated-measures ANOVA (which needs complete balanced data) and over GEE "
    "(which needs MCAR without weighting);<br>"
    "- beware treating a lagged outcome as a covariate alongside random effects - it biases everything "
    "(Nickell bias).",
    f"{T} longitudinal growth-curve ar1 covariance-structures")

txt("How do you interpret and report the output of a mixed model?",
    "Report three blocks:<br><br>"
    "1. <b>Fixed effects</b>: estimates with confidence intervals, on an interpretable scale. For "
    "nonlinear links state whether they are conditional (subject-specific) or marginal, and use "
    "`emmeans`/`marginaleffects` to produce the contrasts you actually want rather than raw coefficients.<br>"
    "2. <b>Variance components</b>: each \\(\\hat\\sigma_b\\) in the units of the outcome (an SD is more "
    "intuitive than a variance), the <b>ICC</b>, and the intercept-slope correlation if fitted. "
    "This is where the scientific content about heterogeneity lives - 'between-hospital SD of 0.3 on the "
    "log-odds scale' is a substantive finding, not a nuisance.<br>"
    "3. <b>What structure you fitted and why</b>: grouping factors, which slopes were random, "
    "nested/crossed, REML or ML, the df method used for p-values, and any simplification forced by "
    "convergence.<br><br>"
    "Also useful: marginal and conditional \\(R^2\\) (`performance::r2_nakagawa`), a caterpillar plot of the "
    "BLUPs with intervals (`lattice::dotplot(ranef(fit))`), and predictions at both levels - "
    "population-level (`re.form = NA`) versus cluster-specific.<br><br>"
    "Pitfalls to avoid in the write-up: reading BLUPs as if each group had been fitted independently, "
    "comparing coefficients across models with different random structures (the implicit scale changes for "
    "nonlinear links), and reporting p-values from a model whose random structure was chosen after looking "
    "at those p-values.",
    f"{T} reporting interpretation variance-components")

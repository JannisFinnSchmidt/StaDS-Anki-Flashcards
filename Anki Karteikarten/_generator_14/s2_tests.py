# -*- coding: utf-8 -*-
"""Section 2 - hypothesis tests: when to use, assumptions, what is actually tested."""
from plotlib import *

T = "Core tests"
PIC = []
TXT = []


def pic(front, builder, back, tags):
    PIC.append((front, builder, back, tags))


def txt(front, back, tags):
    TXT.append((front, back, tags))


# ---------------------------------------------------------------------------
# diagrams
# ---------------------------------------------------------------------------
def _chooser():
    cv = Canvas(w=470, h=300, pad=(10, 10, 10, 10))

    def box(x, y, w, h, label, col, size=9, sub=None):
        cv.rect(x, y, w, h, fill=C[col], fo=0.18, stroke="currentColor", width=1.1, rx=4, data=False)
        cv.text(x + w / 2, y + (h / 2 + 3.2 if not sub else h / 2 - 2), label, size=size,
                opacity=1.0, data=False)
        if sub:
            cv.text(x + w / 2, y + h / 2 + 11, sub, size=8, opacity=0.7, data=False)

    def arrow(x1, y1, x2, y2):
        cv.line(x1, y1, x2, y2, width=1.1, opacity=0.7, arrow=True, data=False)

    cv.text(235, 14, "what is the outcome?", size=10, weight="bold", data=False)

    # continuous branch
    box(12, 28, 150, 24, "continuous outcome", "blue")
    box(178, 28, 130, 24, "binary / nominal", "amber")
    box(324, 28, 136, 24, "time-to-event", "violet")
    arrow(235, 18, 90, 26)
    arrow(235, 18, 240, 26)
    arrow(235, 18, 390, 26)

    box(12, 66, 72, 40, "2 groups", "blue", sub="t / Welch")
    box(90, 66, 72, 40, "> 2 groups", "blue", sub="ANOVA")
    arrow(60, 52, 48, 64)
    arrow(115, 52, 126, 64)
    box(12, 118, 150, 38, "not normal, small n", "green",
        sub="Wilcoxon / Kruskal-Wallis / permutation")
    arrow(87, 106, 87, 116)
    box(12, 168, 150, 38, "same units measured twice", "cyan",
        sub="paired t / signed-rank / mixed model")
    arrow(87, 156, 87, 166)

    box(178, 66, 130, 38, "2x2 table", "amber", sub="chi-square, Fisher if sparse")
    arrow(243, 52, 243, 64)
    box(178, 116, 130, 38, "paired binary", "amber", sub="McNemar / Cochran's Q")
    arrow(243, 104, 243, 114)
    box(178, 166, 130, 40, "ordered categories", "amber",
        sub="Cochran-Armitage trend")
    arrow(243, 154, 243, 164)

    box(324, 66, 136, 38, "compare curves", "violet", sub="log-rank (needs prop. hazards)")
    arrow(392, 52, 392, 64)
    box(324, 116, 136, 38, "with covariates", "violet", sub="Cox model, Wald / LR test")
    arrow(392, 104, 392, 114)
    box(324, 166, 136, 40, "non-proportional", "violet",
        sub="RMST, weighted log-rank")
    arrow(392, 154, 392, 164)

    cv.caption(["independence of observations is the assumption no test can rescue you from -",
                "clustered or repeated data needs a mixed model / GEE, not a different two-sample test",
                "with n large enough, normality of the outcome matters far less than the shape of the tails"],
               x=14, y0=228)
    return cv


pic("Sketch a decision tree for choosing a hypothesis test",
    _chooser,
    "Work down three questions: what kind of outcome, how many groups, and are the observations "
    "independent?<br><br>"
    "The third question is the one people skip and the only one that cannot be patched: if measurements "
    "are repeated within subjects, clustered in schools, or ordered in time, then no choice of two-sample "
    "test is valid - you need a paired test, a mixed model, GEE, or cluster-robust standard errors.<br><br>"
    "Normality matters much less than it is given credit for: by the CLT, means are approximately normal "
    "for moderate n, so t-based tests are robust to mild non-normality. What actually breaks them is "
    "<b>heavy tails, strong skew with small n, and unequal variances</b> - hence Welch as a default, and "
    "permutation or rank tests when the tails are wild.",
    f"{T} test-choice overview diagram")


def _pvalues():
    cv = Canvas(w=460, h=270)
    cv.limits((0, 1), (0, 3.6))
    cv.axes(xlabel="p-value", ylabel="density", xticks=[0, 0.05, 0.25, 0.5, 0.75, 1],
            yticks=[0, 1, 2, 3])
    # H0: uniform
    cv.path([(0, 1), (1, 1)], color=C["slate"], width=1.9, dash="5 3")
    # H1: beta(0.3, 3)-ish concentrated near zero
    f = lambda x: max(0.02, 3.4 * math.exp(-9 * x))
    pts = [(i / 300, f(i / 300)) for i in range(301)]
    cv.path(pts, color=C["blue"], width=1.9, fill=C["blue"], close_to=0, fo=0.15)
    cv.rect(0, 0, 0.05, 1, fill=C["rose"], fo=0.30, stroke=C["rose"], width=1)
    cv.text(0.20, 1.35, "false positives: α · (# true nulls)", size=9, opacity=0.85,
            anchor="start", color=C["rose"])
    cv.legend([("under H0: uniform", C["slate"], "5 3"), ("under H1: piled near 0", C["blue"])],
              x=445, y=30)
    cv.caption(["a valid p-value is uniform under the null - that is the whole definition",
                "BH-FDR sorts the p-values and keeps the largest k with p(k) ≤ k·q/m",
                "so the threshold adapts: many small p-values buy a more lenient cutoff"])
    return cv


pic("What does the distribution of p-values look like under the null and under the alternative, and how does BH-FDR use it?",
    _pvalues,
    "Under the null a valid p-value is <b>uniform on (0,1)</b> - that is essentially its definition, and it "
    "is why an α-level test has exactly probability α of a false positive. Under the alternative the "
    "distribution piles up near zero; the more power, the steeper the pile.<br><br>"
    "The Benjamini-Hochberg procedure exploits exactly this shape. Sort the m p-values, find the largest k "
    "with \\(p_{(k)}\\le kq/m\\), and reject the k smallest. Because the threshold depends on how many small "
    "p-values you actually observed, FDR control adapts to the signal, unlike Bonferroni's fixed α/m.<br><br>"
    "The distinction to keep straight: <b>FWER</b> (Bonferroni, Holm) controls the probability of "
    "<b>any</b> false positive - right for a single confirmatory decision. <b>FDR</b> (BH, BY, Storey's "
    "q-value) controls the expected <b>proportion</b> of false positives among rejections - right for "
    "screening thousands of candidates for follow-up.<br><br>"
    "A histogram of p-values is also a diagnostic: a spike at 1, or a non-uniform bulk under the null, "
    "means the test is misspecified (usually dependence you ignored).",
    f"{T} p-values multiple-testing fdr diagram")


def _power():
    cv = Canvas(w=460, h=270)
    cv.limits((-3.2, 6.2), (0, 0.47))
    cv.axes(xlabel="test statistic", ylabel="density", xticks=[-3, -1, 1, 3, 5], y_axis=False)
    cv.line(-3.2, 0, 6.2, 0, width=1.2, opacity=0.85)
    crit = 1.96
    g0 = [(x, normal(x, 0, 1)) for x in [-3.2 + 9.4 * i / 300 for i in range(301)]]
    g1 = [(x, normal(x, 3.0, 1)) for x in [-3.2 + 9.4 * i / 300 for i in range(301)]]
    # beta region (under H1, left of crit)
    b = [(x, y) for x, y in g1 if x <= crit]
    cv.path(b, color=C["amber"], width=0, fill=C["amber"], close_to=0, fo=0.30)
    a = [(x, y) for x, y in g0 if x >= crit]
    cv.path(a, color=C["rose"], width=0, fill=C["rose"], close_to=0, fo=0.35)
    cv.path(g0, color=C["slate"], width=1.9)
    cv.path(g1, color=C["blue"], width=1.9)
    cv.line(crit, 0, crit, 0.44, width=1.3, dash="4 3", opacity=0.8)
    cv.text(crit, 0.455, "critical value", size=9, opacity=0.8)
    cv.text(-1.4, 0.30, "H0", size=10, opacity=0.9, color=C["slate"])
    cv.text(4.4, 0.30, "H1", size=10, opacity=0.9, color=C["blue"])
    cv.text(2.35, 0.035, "α", size=10, opacity=1.0, color=C["rose"])
    cv.text(1.05, 0.035, "β", size=10, opacity=1.0, color=C["amber"])
    cv.caption(["power = 1 - β; it rises with effect size, with √n, and with smaller residual noise",
                "shrinking α (moving the line right) always costs power - that is the entire trade-off",
                "a non-significant result with low power says nothing; report the CI, not just the p-value"])
    return cv


pic("Sketch the relationship between significance level, power and effect size",
    _power,
    "Two sampling distributions of the same statistic - one under the null, one under a specific "
    "alternative - separated by the effect size, with a critical value between them.<br><br>"
    "- <b>α</b> (type I error) is the null-density mass beyond the critical value: rejecting a true null.<br>"
    "- <b>β</b> (type II error) is the alternative-density mass on the non-rejection side.<br>"
    "- <b>Power = 1 - β</b> increases with the true effect size, with \\(\\sqrt{n}\\), with lower noise, "
    "and with a larger α.<br><br>"
    "For a two-sample comparison of means:<br>"
    "\\[ n_{\\text{per group}}\\approx\\frac{2(z_{1-\\alpha/2}+z_{1-\\beta})^2}{d^2},\\qquad d=\\frac{\\Delta}{\\sigma} \\]"
    "which for 80 % power at α = 0.05 is roughly \\(16/d^2\\) per group.<br><br>"
    "Two consequences: <b>power analysis must happen before the study</b> (post-hoc 'observed power' from the "
    "estimated effect is circular), and a non-significant result from an underpowered study is not evidence "
    "of no effect - only the confidence interval can tell you whether a meaningful effect has been ruled out.",
    f"{T} power type-I type-II sample-size diagram")


# ---------------------------------------------------------------------------
# text cards
# ---------------------------------------------------------------------------
txt("What exactly is a p-value, and what is it not?",
    "It is the probability, <b>assuming the null hypothesis and the whole model are true</b>, of observing a "
    "test statistic at least as extreme as the one you got.<br><br>"
    "What it is not:<br>"
    "- not the probability that the null is true (that requires a prior; it is a posterior quantity);<br>"
    "- not the probability the result was due to chance;<br>"
    "- not a measure of effect size - with large n, trivial effects give tiny p-values;<br>"
    "- not comparable across studies as evidence strength unless power is comparable;<br>"
    "- not valid if the hypothesis, the model, or the stopping rule was chosen after seeing the data.<br><br>"
    "It also tests the <b>entire</b> model, not just the parameter: a small p can equally mean the null is "
    "false, the independence assumption is violated, the functional form is wrong, or the data were "
    "selected. That is why 'p < 0.05' should always be accompanied by an estimate with a confidence "
    "interval.",
    f"{T} p-value inference interpretation")

txt("When do you use a one-sample z test versus a one-sample t test?",
    "Both test whether a mean equals a hypothesised value; they differ in whether the variance is known.<br><br>"
    "- <b>z test</b>: σ known (rare in practice) or n large enough that estimating it is negligible. "
    "Reference distribution: standard normal.<br>"
    "- <b>t test</b>: σ estimated from the data. Reference distribution: \\(t_{n-1}\\), whose fatter tails "
    "pay for that extra uncertainty.<br><br>"
    "Assumptions, in order of importance:<br>"
    "1. <b>independent observations</b> - violated by clustering or serial correlation, and this cannot be "
    "fixed by a different test;<br>"
    "2. identically distributed data (no drift or regime change);<br>"
    "3. approximate normality of the <b>sampling distribution of the mean</b>, not of the raw data - hence "
    "robustness for moderate n unless the data are heavily skewed or heavy-tailed.<br><br>"
    "\\[ t=\\frac{\\bar x-\\mu_0}{s/\\sqrt{n}}\\ \\sim\\ t_{n-1}\\ \\text{under }H_0 \\]",
    f"{T} t-test z-test one-sample assumptions")

txt("Why should Welch's t test be the default for comparing two means?",
    "The pooled (Student) two-sample t test assumes <b>equal variances</b> in the two groups and pools them "
    "into one estimate. Welch's version estimates each group's variance separately and adjusts the degrees "
    "of freedom (Welch-Satterthwaite).<br><br>"
    "Why Welch as the default: when variances are equal it loses almost nothing, and when they are unequal - "
    "especially with unequal group sizes - the pooled test's type I error can be badly wrong. The classic "
    "two-step 'first test for equal variance with Levene, then choose' is worse than just using Welch: the "
    "pre-test inflates the overall error rate and is itself underpowered in exactly the small samples where "
    "it would matter.<br><br>"
    "Assumptions that remain: independence within and between groups, and approximate normality of the two "
    "means. Unequal variances plus strong skew plus tiny n is the case for a permutation test.<br><br>"
    "\\[ t=\\frac{\\bar x_1-\\bar x_2}{\\sqrt{s_1^2/n_1+s_2^2/n_2}} \\]",
    f"{T} welch t-test two-sample variance-heterogeneity")

txt("When is a paired test appropriate, and what does pairing buy you?",
    "Whenever the two measurements come from the <b>same unit</b> or from deliberately matched units: "
    "before/after on the same patient, left/right eye, twin pairs, the same subject under two conditions, "
    "matched case-control pairs.<br><br>"
    "The paired t test just reduces the problem to a one-sample t test on the within-pair differences. "
    "What that buys you is the removal of all between-subject variation - if subjects differ a lot but "
    "respond consistently, the paired test can be dramatically more powerful than the unpaired one at the "
    "same n. Conversely, analysing paired data as independent is a real error: it uses the wrong (larger) "
    "variance and the wrong df.<br><br>"
    "Assumptions: pairs independent of each other, and the <b>differences</b> approximately normal (their "
    "distribution can be much better behaved than the raw values). The nonparametric counterparts are the "
    "Wilcoxon signed-rank test and the sign test; the general version for more than two occasions is a "
    "mixed model.",
    f"{T} paired-test within-subject blocking")

txt("When do you use one-way ANOVA and what are its assumptions?",
    "To test whether the means of three or more groups are all equal, in a single omnibus test that keeps "
    "the type I error at α - instead of running all pairwise t tests.<br><br>"
    "It is the F test comparing between-group to within-group variability, and it is exactly a linear model "
    "with one factor.<br><br>"
    "Assumptions:<br>"
    "1. <b>independent observations</b> (repeated measures need repeated-measures ANOVA or a mixed model);<br>"
    "2. <b>homoscedasticity</b> - equal variance across groups (the Welch ANOVA relaxes this and is a good "
    "default with unequal group sizes);<br>"
    "3. approximately normal residuals (robust for moderate n; Kruskal-Wallis or a permutation F test "
    "otherwise).<br><br>"
    "A significant F says 'not all means are equal' and nothing more. Follow up with <b>planned contrasts</b> "
    "if you had hypotheses, or a corrected multiple-comparison procedure: Tukey HSD for all pairs, Dunnett "
    "for all-versus-control, Scheffé for arbitrary post-hoc contrasts, Bonferroni/Holm for a small "
    "pre-specified set.<br><br>"
    "\\[ F=\\frac{MS_{\\text{between}}}{MS_{\\text{within}}}\\sim F_{k-1,\\,n-k} \\]",
    f"{T} anova f-test assumptions post-hoc")

txt("What do the Wilcoxon rank-sum (Mann-Whitney) and signed-rank tests actually test?",
    "They replace values by ranks, so they need no distributional assumption beyond continuity - but the "
    "null they test is often misstated.<br><br>"
    "- <b>Rank-sum / Mann-Whitney U</b> (two independent groups) tests \\(P(X>Y)=1/2\\): whether a random "
    "draw from one group tends to exceed a random draw from the other. It equals a test of equal medians "
    "<b>only</b> under the additional location-shift assumption (same shape and spread, shifted). With "
    "unequal variances or different shapes, a significant result can occur with identical medians.<br>"
    "- <b>Signed-rank</b> (paired) tests whether the distribution of the within-pair differences is "
    "symmetric about zero.<br><br>"
    "Practical notes: they are highly efficient (≈ 95 % of the t test's power under normality, and much "
    "better under heavy tails), they handle ordinal outcomes, and they are invariant to monotone "
    "transformations. What they do not give you is an interpretable effect size on the original scale - "
    "report the Hodges-Lehmann estimate or a probability-of-superiority, and remember that they are not a "
    "cure for dependence or for unequal variances.",
    f"{T} wilcoxon mann-whitney nonparametric ranks")

txt("When do you use the Kruskal-Wallis and Friedman tests?",
    "<b>Kruskal-Wallis</b>: the rank-based analogue of one-way ANOVA - three or more <b>independent</b> "
    "groups, ordinal or non-normal continuous outcomes, or small samples with outliers. Null: all groups "
    "have the same distribution (interpreted as stochastic equivalence). Follow up with Dunn's test or "
    "pairwise Wilcoxon plus a multiplicity correction.<br><br>"
    "<b>Friedman</b>: the analogue of repeated-measures ANOVA - the same subjects (or blocks) measured "
    "under k conditions, ranks taken <b>within</b> each subject. Null: no systematic difference between "
    "conditions. Follow up with Nemenyi or pairwise signed-rank tests. This is the standard test when "
    "comparing several algorithms across many datasets.<br><br>"
    "Both inherit the same caveats as the Wilcoxon tests: heteroscedasticity and shape differences muddy "
    "the interpretation, and neither models covariates. Once you need covariate adjustment, go to a "
    "mixed model, an ordinal (proportional-odds) model, or a rank-transformed regression instead.",
    f"{T} kruskal-wallis friedman nonparametric blocks")

txt("When are permutation and bootstrap methods the right answer?",
    "<b>Permutation (randomisation) test</b>: build the null distribution by relabelling the data in every "
    "way the null says is exchangeable, and compare your observed statistic to it. Assumption: "
    "<b>exchangeability</b> under the null - nothing about normality. Use it when you have a statistic with "
    "no tractable null distribution, tiny samples, weird outcomes, or when you want exact validity. Under "
    "randomised assignment it is the assumption-free gold standard. It does not fix unequal variances "
    "when the null is 'equal means'.<br><br>"
    "<b>Bootstrap</b>: resample the data with replacement to approximate the <b>sampling distribution</b> of "
    "an estimator, then read off standard errors or percentile / BCa confidence intervals. Assumption: the "
    "sample represents the population and observations are independent (for clustered data resample "
    "clusters; for time series use a block bootstrap). It struggles at boundaries and for extremes (maxima, "
    "quantiles at the very tail).<br><br>"
    "Rule of thumb: permutation for <b>testing</b>, bootstrap for <b>intervals</b>, and both for statistics "
    "where the delta method would be painful (differences of AUCs, ratios, indirect effects).",
    f"{T} permutation bootstrap resampling")

txt("When do you use a chi-square goodness-of-fit test versus a chi-square test of independence?",
    "Both compare observed with expected counts via the same statistic; the difference is where 'expected' "
    "comes from.<br><br>"
    "- <b>Goodness of fit</b>: one categorical variable against a hypothesised distribution "
    "(e.g. are digits uniform, does the genotype ratio match 1:2:1). df = categories - 1 - (parameters "
    "estimated from the data).<br>"
    "- <b>Independence / homogeneity</b>: two categorical variables in a contingency table; expected counts "
    "come from the product of the margins. df = (r-1)(c-1).<br><br>"
    "Assumptions: independent observations (counts, not proportions or repeated measures), and expected "
    "counts large enough for the chi-square approximation - the usual rule is all expected ≥ 5, or at least "
    "80 % of cells ≥ 5. With sparse tables use <b>Fisher's exact test</b> or a permutation/Monte-Carlo "
    "p-value.<br><br>"
    "It is an omnibus test: it says the table is not consistent with the null but not where or how. Look at "
    "the standardised (Pearson) residuals per cell for that, and report an effect size such as Cramér's V "
    "or an odds ratio.<br><br>"
    "\\[ X^2=\\sum\\frac{(O-E)^2}{E} \\]",
    f"{T} chi-square goodness-of-fit independence contingency")

txt("When do you use Fisher's exact test, and what is the argument against it?",
    "For a 2x2 (or small r x c) table where expected counts are too small for the chi-square approximation. "
    "It conditions on both sets of margins and computes the exact hypergeometric probability of tables at "
    "least as extreme.<br><br>"
    "Assumptions: independent observations and the conditioning on fixed margins. In genuinely "
    "margin-fixed designs (Fisher's tea-tasting, some case-control designs) that is exactly right.<br><br>"
    "The argument against: conditioning on margins that were <b>not</b> actually fixed by the design makes "
    "the test <b>conservative</b> - the true type I error can be well below α, so it loses power, and the "
    "discreteness makes the p-value granular. Alternatives worth knowing: the mid-p adjustment, "
    "Barnard's unconditional exact test (more powerful), or a Monte-Carlo permutation p-value for larger "
    "tables. For paired binary data, Fisher is the wrong test entirely - use McNemar.",
    f"{T} fisher-exact small-samples conservative")

txt("When do you use McNemar's test and Cochran's Q?",
    "For <b>paired binary</b> outcomes, where the two measurements come from the same unit.<br><br>"
    "- <b>McNemar</b>: two paired binary measurements - the same patients tested by two diagnostic methods, "
    "before/after on the same subjects, matched case-control pairs. The insight is that only the "
    "<b>discordant pairs</b> carry information: the test asks whether the b and c off-diagonal counts are "
    "balanced, ignoring the agreements entirely. Exact version (binomial on b out of b+c) for small "
    "counts.<br>"
    "- <b>Cochran's Q</b>: the same idea with k > 2 repeated binary measurements per subject - the binary "
    "analogue of the Friedman test.<br><br>"
    "Using a plain chi-square on paired binary data is a genuine error: it treats 2n dependent observations "
    "as independent and gives a wildly wrong standard error. The regression version of McNemar is "
    "conditional logistic regression, which is what lets you add covariates.<br><br>"
    "\\[ X^2=\\frac{(b-c)^2}{b+c}\\ \\sim\\ \\chi^2_1 \\]",
    f"{T} mcnemar cochran-q paired-binary")

txt("Which tests are made for ordered categories or stratified tables?",
    "- <b>Cochran-Armitage trend test</b>: a binary outcome across <b>ordered</b> exposure levels (dose "
    "groups, quintiles). It tests for a monotone trend rather than for any difference, so it has much more "
    "power than a generic chi-square when the effect really is monotone. Assumes correctly assigned "
    "numeric scores for the levels.<br>"
    "- <b>Mantel-Haenszel test / estimator</b>: a common odds ratio across <b>strata</b> (centres, age "
    "bands, matched sets), which controls for the stratifying variable without modelling it. Assumes the "
    "odds ratio is constant across strata.<br>"
    "- <b>Breslow-Day test</b>: checks exactly that constancy assumption, i.e. tests for interaction "
    "(effect modification) between exposure and stratum.<br>"
    "- <b>Linear-by-linear association</b> / Kendall's tau-b: both variables ordinal.<br><br>"
    "The modern alternative to all of these is a regression model - logistic with a linear dose term, or "
    "with stratum as a covariate - which additionally gives you an interpretable estimate and lets you test "
    "the interaction directly.",
    f"{T} trend-test mantel-haenszel breslow-day stratified")

txt("How do you test a proportion, and why is the Wald interval a bad choice?",
    "Three approaches to a single proportion:<br>"
    "- <b>Wald</b>: \\(\\hat p\\pm z\\sqrt{\\hat p(1-\\hat p)/n}\\). Simple and widely taught, but its "
    "coverage is poor for small n or p near 0 or 1 - it can even produce limits outside [0,1], and it has "
    "zero width when \\(\\hat p=0\\).<br>"
    "- <b>Score / Wilson</b>: inverts the score test; stays inside [0,1], has good coverage even for small "
    "n, and is the sensible default. The 'add 2 successes and 2 failures' Agresti-Coull interval "
    "approximates it.<br>"
    "- <b>Exact (Clopper-Pearson)</b>: guaranteed coverage of at least 1-α, but conservative and therefore "
    "wider than necessary.<br><br>"
    "For two proportions: a chi-square / two-sample z test on the difference, Fisher or Barnard when "
    "sparse, and report the effect as a risk difference, risk ratio or odds ratio - each answers a "
    "different question, and the odds ratio is the one that exaggerates when the outcome is common.",
    f"{T} proportions wilson clopper-pearson intervals")

txt("What does the Kolmogorov-Smirnov test do, and what are its weaknesses?",
    "It compares distributions through the largest vertical gap between the empirical CDF and either a "
    "hypothesised CDF (one-sample) or another empirical CDF (two-sample).<br><br>"
    "Weaknesses that matter in practice:<br>"
    "- it is most sensitive near the <b>centre</b> of the distribution and quite blind in the <b>tails</b>, "
    "which is usually where you care;<br>"
    "- the standard critical values are invalid if you <b>estimated parameters from the same data</b> - "
    "using the sample mean and sd to test normality makes the test far too conservative (that is what the "
    "Lilliefors correction fixes);<br>"
    "- it assumes continuous data; with ties the p-value is wrong;<br>"
    "- with large n it rejects for practically irrelevant deviations, and with small n it detects almost "
    "nothing.<br><br>"
    "Better alternatives: <b>Anderson-Darling</b> (tail-weighted, better for normality) or "
    "<b>Cramér-von Mises</b> (integrates the whole discrepancy). For model checking, a QQ plot answers the "
    "real question - how and where the fit fails - which no single test statistic can.",
    f"{T} kolmogorov-smirnov anderson-darling distributional-fit")

txt("Which tests check normality, and why are they less useful than they look?",
    "<b>Shapiro-Wilk</b> (best all-round power for small to moderate n), <b>Anderson-Darling</b> "
    "(tail-sensitive), <b>Jarque-Bera</b> (based on skewness and kurtosis, common in econometrics), "
    "<b>Lilliefors</b> (KS with estimated parameters).<br><br>"
    "Why they mislead:<br>"
    "- <b>Sample size drives the answer</b>. With n = 20 nothing is rejected even for clearly non-normal "
    "data; with n = 10 000 everything is rejected for deviations that do not matter.<br>"
    "- The assumption that matters is usually normality of the <b>residuals</b> or of the "
    "<b>sampling distribution</b>, not of the raw data.<br>"
    "- Since t and F procedures are robust to mild non-normality anyway, the relevant question is 'is the "
    "deviation big enough to matter for this inference' - a magnitude question a test cannot answer.<br>"
    "- Using the pre-test to choose the main test invalidates the error rate of the whole procedure.<br><br>"
    "Better practice: look at a <b>QQ plot</b>, judge skew and tail weight, and if in doubt use a method "
    "that does not need the assumption (permutation, bootstrap, robust or rank-based procedures).",
    f"{T} normality-tests shapiro-wilk diagnostics")

txt("Which tests diagnose heteroscedasticity, and what do you do about it?",
    "Tests: <b>Breusch-Pagan</b> (regress squared residuals on the covariates - detects variance that is a "
    "linear function of predictors), <b>White</b> (adds squares and cross-products, so it also picks up "
    "misspecification), <b>Levene</b> / <b>Brown-Forsythe</b> / <b>Fligner-Killeen</b> for group "
    "comparisons (Levene on the median and Fligner are the robust ones; <b>Bartlett</b> is powerful but "
    "very sensitive to non-normality), <b>Goldfeld-Quandt</b> for a variance that changes with an ordering.<br><br>"
    "What to do, in increasing order of ambition:<br>"
    "1. <b>Heteroscedasticity-robust (sandwich / HC3) standard errors</b> - keeps the OLS estimates, fixes "
    "the inference. Usually the right first move, and cluster-robust when the variance structure is "
    "grouped.<br>"
    "2. <b>Weighted least squares</b>, if you know or can model the variance.<br>"
    "3. <b>Change the model</b>: a GLM with a variance function that matches (Poisson, Gamma) or a "
    "transformation of the response - often the trending spread was telling you the mean model was on the "
    "wrong scale.<br>"
    "4. <b>Model the variance explicitly</b>: `nlme::gls(weights = varPower())`, GAMLSS, or distributional "
    "regression.",
    f"{T} heteroscedasticity breusch-pagan white robust-se")

txt("Which tests detect autocorrelation and dependence, and when do you need them?",
    "Whenever observations have an order or a location, because dependence is what invalidates the standard "
    "errors most severely.<br><br>"
    "- <b>Durbin-Watson</b>: first-order serial correlation in regression residuals. Limited (only lag 1, "
    "invalid with lagged dependent variables).<br>"
    "- <b>Breusch-Godfrey</b>: LM test for autocorrelation up to order p; valid with lagged regressors, so "
    "the general-purpose choice.<br>"
    "- <b>Ljung-Box (portmanteau)</b>: are the first m autocorrelations jointly zero? Standard residual "
    "check for ARIMA models.<br>"
    "- <b>Moran's I</b> / Geary's C: <b>spatial</b> autocorrelation given a chosen neighbourhood matrix - "
    "and the result depends on that choice.<br>"
    "- <b>Intraclass correlation</b> and a likelihood ratio test on a random intercept: dependence within "
    "clusters.<br><br>"
    "Consequences of ignoring it: point estimates stay roughly unbiased but standard errors are far too "
    "small, so everything looks significant. The fixes are modelling the dependence (ARMA errors, "
    "`corAR1()`, random effects, spatial CAR/SAR terms, Gaussian processes) or using "
    "Newey-West / cluster-robust standard errors.",
    f"{T} autocorrelation durbin-watson ljung-box morans-i")

txt("Which tests check stationarity and lead-lag structure in time series?",
    "- <b>ADF (augmented Dickey-Fuller)</b> and <b>Phillips-Perron</b>: null is a <b>unit root</b> "
    "(non-stationary). Failing to reject is weak evidence, since these tests have notoriously low power "
    "against near-unit roots.<br>"
    "- <b>KPSS</b>: null is <b>stationarity</b> - the reverse. Best practice is to run both and see whether "
    "they agree; disagreement means the data are ambiguous or fractionally integrated.<br>"
    "- <b>Granger causality</b>: does the past of X improve the prediction of Y beyond Y's own past? Note "
    "carefully that this is <b>predictive precedence, not causation</b>: it is confounded by common causes "
    "and broken by omitted variables, aggregation and anticipation.<br>"
    "- <b>Johansen / Engle-Granger</b>: cointegration, i.e. a stationary long-run combination of "
    "non-stationary series - the right framework when differencing would throw away the level "
    "relationship.<br><br>"
    "Why it matters: regressing one random walk on another produces <b>spurious regression</b> with high "
    "R² and huge t statistics. Difference, detrend, or model in a cointegration framework first.",
    f"{T} stationarity adf kpss granger cointegration")

txt("What do the Ramsey RESET and Chow tests check?",
    "- <b>RESET</b>: adds powers of the fitted values (or of the regressors) to the model and tests whether "
    "they matter. If they do, the <b>functional form</b> is wrong - a missing nonlinearity or interaction, "
    "or the wrong link. It is a general specification test, not a diagnosis: it tells you something is "
    "wrong, not what.<br>"
    "- <b>Chow test</b>: are the coefficients the same in two known subsamples (before/after a policy, two "
    "regions)? An F test comparing one pooled fit against two separate fits. Requires you to know the break "
    "point and assumes homoscedasticity across regimes; for an unknown break point use "
    "supremum-Wald / Quandt-Andrews or CUSUM tests.<br><br>"
    "The modern habit is to skip both in favour of flexible modelling and inspection: a partial-residual or "
    "component-plus-residual plot shows the missing curvature directly, and fitting a spline "
    "(`mgcv::gam` with `s(x)`) both tests and repairs it in one step - the reported EDF of the smooth is "
    "itself the answer to 'is it nonlinear'.",
    f"{T} reset chow specification structural-break")

txt("What is the difference between the likelihood ratio, Wald and score tests?",
    "All three test the same null and are asymptotically equivalent (all \\(\\chi^2_q\\) with q = number of "
    "restrictions), but they measure different geometric features of the log-likelihood.<br><br>"
    "- <b>Likelihood ratio</b>: the vertical drop in log-likelihood from the unrestricted to the restricted "
    "maximum. Needs both models fitted. Usually the most reliable in finite samples and invariant to "
    "reparameterisation.<br>"
    "- <b>Wald</b>: the distance from the estimate to the null value, scaled by the estimated curvature at "
    "the estimate. Needs only the full model - which is why every regression table reports Wald tests. "
    "<b>Not</b> invariant to reparameterisation, and it fails badly when the likelihood is very asymmetric "
    "(the Hauck-Donner effect: with near-perfect separation in logistic regression, a huge coefficient can "
    "give a Wald statistic near zero).<br>"
    "- <b>Score (Lagrange multiplier)</b>: the slope of the log-likelihood at the null. Needs only the "
    "restricted model, which is why it is used to test for adding something (heteroscedasticity, "
    "autocorrelation, zero inflation, an extra random effect).<br><br>"
    "When they disagree materially, the asymptotics have not kicked in: trust the LR test, or use a "
    "profile-likelihood interval, bootstrap or exact method.",
    f"{T} likelihood-ratio wald score trinity")

txt("What goes wrong when you test a variance component (a random effect) with a likelihood ratio test?",
    "The null puts the parameter on the <b>boundary</b> of the parameter space (a variance of exactly 0), so "
    "the standard regularity conditions for Wilks' theorem fail. The LR statistic is then not "
    "\\(\\chi^2_1\\) but a 50:50 mixture \\(\\tfrac12\\chi^2_0+\\tfrac12\\chi^2_1\\).<br><br>"
    "Consequence: using the naive \\(\\chi^2_1\\) p-value is <b>conservative</b> - roughly twice too large - "
    "so you under-detect real random effects. The quick fix for a single variance component is to halve the "
    "p-value; for several correlated components the correct mixture is messier.<br><br>"
    "Practical options: `RLRsim::exactRLRT` (exact restricted LR test), a parametric bootstrap "
    "(`lme4::bootMer`, `pbkrtest::PBmodcomp`), or simply keeping the random effect because the design "
    "implies it. Note also that LR tests comparing <b>fixed</b> effects must be fitted with ML, not REML, "
    "since REML likelihoods with different fixed-effect structures are not comparable - and that Wald tests "
    "of fixed effects in mixed models need a df correction (Kenward-Roger or Satterthwaite) to behave in "
    "small samples.",
    f"{T} variance-components boundary lrt mixed-models")

txt("How do you compare models that are not nested?",
    "The LR test does not apply. Options:<br>"
    "- <b>Information criteria</b>: AIC (asymptotically equivalent to leave-one-out CV, targets predictive "
    "fit), BIC (consistent for the true model if it is in the candidate set, penalises harder), "
    "AICc for small n, WAIC/LOO-IC for Bayesian models. They require the <b>same data and the same "
    "response scale</b> - you cannot compare a model of y with a model of log y by AIC.<br>"
    "- <b>Cross-validation</b> on a proper scoring rule - the most honest answer if prediction is the goal, "
    "with CV folds respecting any grouping or time ordering.<br>"
    "- <b>Vuong test</b> for two non-nested likelihoods (classically used for zero-inflated versus plain "
    "count models, though its use for that comparison is problematic because the models are actually "
    "nested at the boundary).<br>"
    "- <b>Encompassing / Cox tests</b>, or simply fitting the union model.<br>"
    "- <b>Diebold-Mariano</b> for comparing forecast accuracy of two time-series models on a loss "
    "differential.<br><br>"
    "Note that AIC/BIC differences are interpretable, not testable: a difference of 2 is weak, 10 is "
    "decisive - and neither tells you whether either model is any good.",
    f"{T} model-comparison aic bic vuong cross-validation")

txt("What is the Hausman test used for?",
    "Comparing an estimator that is <b>efficient but only valid under a stronger assumption</b> with one "
    "that is <b>consistent under weaker assumptions</b>. If the two agree, the stronger assumption is "
    "credible; if they differ systematically, it is not.<br><br>"
    "Its two classic uses:<br>"
    "- <b>Random versus fixed effects</b> in panel data. The random-effects estimator assumes the random "
    "effects are <b>uncorrelated with the covariates</b>; the fixed-effects (within) estimator does not "
    "need that. A significant Hausman statistic says that assumption fails, i.e. there is unobserved "
    "cluster-level confounding, so use fixed effects (or add the cluster means as covariates - the "
    "Mundlak device, which decomposes within and between effects while keeping the random-effects "
    "machinery).<br>"
    "- <b>Endogeneity</b>: OLS versus instrumental variables.<br><br>"
    "Assumptions and caveats: it needs one estimator to be efficient under the null, it has low power in "
    "short panels, and a non-significant result is not proof of exogeneity.",
    f"{T} hausman fixed-vs-random endogeneity")

txt("How do you test for overdispersion and zero inflation in count models?",
    "<b>Overdispersion</b>:<br>"
    "- the quick check is Pearson \\(\\chi^2/\\text{df}\\) - values well above 1 signal it (this is the "
    "quasi-Poisson dispersion estimate);<br>"
    "- a formal score test regresses squared Pearson residuals on the fitted mean "
    "(`AER::dispersiontest`);<br>"
    "- or fit a negative binomial and LR-test θ against the Poisson limit - again a boundary problem, so "
    "halve the p-value;<br>"
    "- `DHARMa::testDispersion` gives a simulation-based version that works for GLMMs.<br><br>"
    "<b>Zero inflation</b>: compare the observed number of zeros with the number simulated from the fitted "
    "model (`DHARMa::testZeroInflation`) - this is the check that actually answers the question. Note that "
    "apparent zero inflation is very often just unmodelled overdispersion or a missing covariate, so fit "
    "the negative binomial <b>first</b>; only then consider zero-inflated or hurdle models.<br><br>"
    "Why it matters: overdispersion barely moves the coefficients but shrinks the standard errors "
    "dramatically, so ignoring it manufactures significance.",
    f"{T} overdispersion zero-inflation dharma counts")

txt("Which tests belong to logistic regression, and what is wrong with Hosmer-Lemeshow?",
    "- <b>Coefficients</b>: Wald z tests (with the Hauck-Donner caveat under near-separation), or better, "
    "LR tests and profile-likelihood intervals. With separation or very rare events use Firth's penalised "
    "logistic regression or exact conditional logistic regression.<br>"
    "- <b>Overall fit</b>: the LR test against the null model, plus pseudo-R² measures (McFadden, "
    "Nagelkerke) which are not proportions of variance and should not be read as such.<br>"
    "- <b>Calibration</b>: the <b>Hosmer-Lemeshow</b> test bins predicted probabilities into (usually) ten "
    "groups and compares observed with expected. Its problems: the result depends on the arbitrary number "
    "of bins, it has poor power to detect the specific miscalibration you care about, and with large n it "
    "rejects trivial deviations. Prefer a <b>calibration plot</b> with a smooth (loess or a spline), plus "
    "the calibration intercept and slope, or the Spiegelhalter z test.<br>"
    "- <b>Discrimination</b>: the c-statistic (AUC), which is a ranking measure and says nothing about "
    "calibration.<br>"
    "- <b>Functional form</b>: partial residual plots, or fit `s(x)` in a GAM and check the EDF.<br>"
    "- <b>Influence</b>: standardised Pearson/deviance residuals, dfbeta, leverage.",
    f"{T} logistic-regression hosmer-lemeshow calibration")

txt("When do you use the log-rank test, and what does it assume?",
    "To compare survival curves between groups when the data are <b>right-censored</b>. It is the score test "
    "of the Cox model with a single group indicator, and it uses the whole follow-up rather than a fixed "
    "time point.<br><br>"
    "Assumptions:<br>"
    "1. <b>Independent (non-informative) censoring</b> - censoring must not carry information about the "
    "hazard. This is the critical one and no test rescues you from it.<br>"
    "2. <b>Proportional hazards</b> - it has maximum power against a constant hazard ratio and can lose "
    "almost all power when the curves <b>cross</b>, since early and late differences cancel.<br>"
    "3. Same underlying survival distribution apart from the group effect; no covariate adjustment.<br><br>"
    "When proportional hazards clearly fails: weighted log-rank tests (Fleming-Harrington, "
    "Peto-Prentice) to emphasise early or late differences, a test on <b>restricted mean survival time</b> "
    "(RMST) which needs no proportionality and has a direct interpretation in months of life, "
    "landmark analysis, or a milestone comparison of survival at a pre-specified time.",
    f"{T} log-rank survival censoring proportional-hazards")

txt("Which correlation coefficient and test should you use?",
    "- <b>Pearson r</b>: strength of a <b>linear</b> association. Its test assumes bivariate normality (or "
    "large n) and it is highly sensitive to outliers and to nonlinearity - r can be near zero for a perfect "
    "curved relationship. Always look at the scatter plot first (Anscombe's quartet).<br>"
    "- <b>Spearman ρ</b>: Pearson on ranks, so it captures any <b>monotone</b> association and is robust to "
    "outliers and monotone transformations. The right default for skewed or ordinal data.<br>"
    "- <b>Kendall τ</b>: based on concordant versus discordant pairs. More interpretable "
    "(a probability difference), better behaved in small samples and with many ties, and it generalises to "
    "<b>Somers' D</b>, the quantity behind the c-index.<br>"
    "- <b>Partial and semi-partial correlation</b>: association after adjusting for other variables.<br>"
    "- <b>Distance correlation</b> or mutual information: detects nonmonotone dependence too; zero implies "
    "independence, unlike the others.<br><br>"
    "Reminders: correlation needs paired independent observations (repeated measures require a "
    "within-subject correlation), and none of these establishes causation or direction.",
    f"{T} correlation pearson spearman kendall")

txt("How do you handle multiple testing, and which method fits which situation?",
    "The problem: with m independent tests at α, the chance of at least one false positive is "
    "\\(1-(1-\\alpha)^m\\) - about 40 % for m = 10.<br><br>"
    "<b>Control the family-wise error rate (any false positive)</b> - for confirmatory decisions:<br>"
    "- Bonferroni (α/m): valid always, simple, conservative under dependence.<br>"
    "- Holm: uniformly more powerful than Bonferroni, equally assumption-free. Use it as the default "
    "instead.<br>"
    "- Hochberg / Hommel: slightly better still, need positive dependence.<br>"
    "- Tukey HSD (all pairs), Dunnett (versus control), Šidák, Scheffé (arbitrary contrasts), "
    "closed-testing and gatekeeping strategies for hierarchical endpoints.<br><br>"
    "<b>Control the false discovery rate (proportion of false positives among rejections)</b> - for "
    "screening:<br>"
    "- Benjamini-Hochberg under independence or positive dependence, Benjamini-Yekutieli for arbitrary "
    "dependence, Storey's q-value when the proportion of true nulls can be estimated.<br><br>"
    "What no correction can fix: testing many models and reporting the best (use a held-out set), "
    "optional stopping (use group-sequential alpha spending), or a hypothesis chosen after seeing the data.",
    f"{T} multiple-testing bonferroni holm fdr")

txt("How do you test that two things are the same rather than different?",
    "Not with a non-significant difference test - absence of evidence is not evidence of absence, and with "
    "small n you can fail to reject almost anything.<br><br>"
    "The correct framework is an <b>equivalence test</b>: pre-specify an equivalence margin Δ, the largest "
    "difference you would consider practically irrelevant, and then <b>reverse the burden of proof</b>.<br><br>"
    "- <b>TOST (two one-sided tests)</b>: reject the null of 'difference ≥ Δ' on both sides. Operationally "
    "identical to checking that the whole 90 % confidence interval for the difference lies inside "
    "(-Δ, +Δ).<br>"
    "- <b>Non-inferiority</b>: the one-sided version - show the new treatment is not worse than the "
    "reference by more than Δ. Standard in drug trials.<br><br>"
    "The hard part is scientific rather than statistical: Δ must be justified from domain knowledge before "
    "the data are seen. The same logic applies to model checking - report the CI for the deviation and ask "
    "whether all values in it are negligible.",
    f"{T} equivalence tost non-inferiority")

txt("Which multivariate tests exist for comparing groups on several outcomes at once?",
    "- <b>Hotelling's \\(T^2\\)</b>: the multivariate two-sample t test - compares mean vectors, using the "
    "covariance between outcomes. It can detect a difference that no single univariate test finds, because "
    "the discriminating direction may be a combination of variables.<br>"
    "- <b>MANOVA</b> (Wilks' lambda, Pillai's trace, Hotelling-Lawley, Roy's largest root): the ANOVA "
    "extension. Pillai is the most robust to assumption violations.<br>"
    "- <b>Box's M</b>: tests equality of covariance matrices across groups (very sensitive to "
    "non-normality, so interpret cautiously).<br>"
    "- <b>Mauchly's test of sphericity</b> in repeated-measures ANOVA; if it fails, apply the "
    "Greenhouse-Geisser or Huynh-Feldt df correction - or simply use a mixed model with an explicit "
    "covariance structure, which is the cleaner modern route.<br>"
    "- <b>PERMANOVA</b> / Mantel tests: distance-based, permutation-driven versions for ecology and "
    "high-dimensional data where n < p makes the classical tests undefined.<br><br>"
    "All of the classical ones assume multivariate normality and equal covariance matrices, and they need "
    "n comfortably larger than the number of outcomes.",
    f"{T} multivariate hotelling manova sphericity")

txt("What are the practical rules for interpreting a test result honestly?",
    "1. <b>Report the estimate and its confidence interval</b>, not just the p-value: the interval shows "
    "both what is plausible and how precise the study was.<br>"
    "2. <b>Separate statistical from practical significance</b>. With large n almost everything is "
    "significant; ask whether the effect size matters.<br>"
    "3. <b>Non-significant ≠ no effect</b>. Check the interval: is a relevant effect excluded, or was the "
    "study simply uninformative?<br>"
    "4. <b>p = 0.049 and p = 0.051 are the same evidence.</b> The threshold is a convention, not a "
    "discontinuity in nature.<br>"
    "5. <b>The test assumes the model.</b> A significant result can reflect violated independence, "
    "selection, measurement error or a missing covariate rather than the effect of interest.<br>"
    "6. <b>Pre-specify.</b> Choosing outcome, subgroup, covariates or stopping point after seeing the data "
    "invalidates the error rate however clean the arithmetic looks.<br>"
    "7. <b>Do not interpret the significance of a covariate as its causal effect</b>: adjusted "
    "coefficients are conditional associations, and adjusting for a mediator or collider actively creates "
    "bias.",
    f"{T} inference interpretation good-practice")

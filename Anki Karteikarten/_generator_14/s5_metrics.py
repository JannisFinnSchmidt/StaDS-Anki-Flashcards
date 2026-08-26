# -*- coding: utf-8 -*-
"""Section 5 - performance measures for predictions: binary, multi-class, regression."""
from plotlib import *

T = "Core metrics"
PIC = []
TXT = []


def pic(front, builder, back, tags):
    PIC.append((front, builder, back, tags))


def txt(front, back, tags):
    TXT.append((front, back, tags))


# ---------------------------------------------------------------------------
# helper: an ROC-like curve from a two-normal score model
# ---------------------------------------------------------------------------
def _roc_points(delta, sd1=1.0):
    """ROC for scores N(0,1) in the negatives and N(delta, sd1) in the positives."""
    pts = []
    for i in range(0, 401):
        c = 6.0 - 12.0 * i / 400
        fpr = 1 - norm_cdf(c, 0, 1)
        tpr = 1 - norm_cdf(c, delta, sd1)
        pts.append((fpr, tpr))
    return pts


def _confusion():
    cv = Canvas(w=470, h=300, pad=(10, 10, 10, 10))
    x0, y0, w, h = 130, 54, 128, 96
    # header
    cv.text(x0 + w / 2, 26, "predicted", size=10, weight="bold", opacity=0.9, data=False)
    cv.text(x0 + w / 4, 44, "positive", size=9, opacity=0.8, data=False)
    cv.text(x0 + 3 * w / 4, 44, "negative", size=9, opacity=0.8, data=False)
    cv.parts.append(f'<text x="26" y="102" font-size="10" text-anchor="middle" fill="currentColor"'
                    f' fill-opacity="0.9" font-weight="bold" stroke="none"'
                    f' transform="rotate(-90 26 102)">actual</text>')
    cv.text(58, 82, "positive", size=9, opacity=0.8, data=False)
    cv.text(58, 130, "negative", size=9, opacity=0.8, data=False)
    cells = [("TP", C["green"], 0, 0), ("FN", C["amber"], 1, 0),
             ("FP", C["amber"], 0, 1), ("TN", C["green"], 1, 1)]
    for lab, col, cx, cy in cells:
        X = x0 + cx * w / 2
        Y = y0 + cy * h / 2
        cv.rect(X, Y, w / 2, h / 2, fill=col, fo=0.20, stroke="currentColor", width=1.1, data=False)
        cv.text(X + w / 4, Y + h / 4 + 4, lab, size=11, data=False)
    # rates
    cv.text(x0 + w + 12, y0 + h / 4 + 4, "sensitivity = TP/(TP+FN)", size=9, opacity=0.85,
            anchor="start", data=False)
    cv.text(x0 + w + 12, y0 + 3 * h / 4 + 4, "specificity = TN/(TN+FP)", size=9, opacity=0.85,
            anchor="start", data=False)
    cv.text(x0 + w / 4, y0 + h + 16, "PPV = TP/(TP+FP)", size=9, opacity=0.85, data=False)
    cv.text(x0 + 3 * w / 4, y0 + h + 30, "NPV = TN/(TN+FN)", size=9, opacity=0.85, data=False)
    cv.line(x0 + w + 8, y0 + h / 4, x0 + w + 4, y0 + h / 4, width=1, opacity=0.5, data=False)

    cv.text(20, 196, "read ACROSS a row: sensitivity / specificity - properties of the test, independent of prevalence",
            size=9, opacity=0.78, anchor="start", data=False)
    cv.text(20, 212, "read DOWN a column: PPV / NPV - what the user actually wants, and they depend on prevalence",
            size=9, opacity=0.78, anchor="start", data=False)
    cv.text(20, 236, "PPV = sens·prev / [sens·prev + (1-spec)(1-prev)]     (Bayes' rule)",
            size=9.5, opacity=0.9, anchor="start", data=False)
    cv.text(20, 256, "rare disease + good test still gives a poor PPV - the base-rate fallacy",
            size=9, opacity=0.78, anchor="start", data=False)
    cv.text(20, 272, "accuracy = (TP+TN)/n is misleading under imbalance: always-negative can score 99 %",
            size=9, opacity=0.78, anchor="start", data=False)
    return cv


pic("Draw the confusion matrix and define every rate that comes out of it",
    _confusion,
    "The four cells give two families of measures, and confusing them is the most common error in "
    "classification reporting.<br><br>"
    "<b>Row-wise (test properties, prevalence-free)</b><br>"
    "- Sensitivity / recall / TPR = TP/(TP+FN)<br>"
    "- Specificity / TNR = TN/(TN+FP), so FPR = 1 - specificity<br>"
    "- These are what ROC analysis uses, and they transfer between populations with different prevalence.<br><br>"
    "<b>Column-wise (what a user gets from a positive result, prevalence-dependent)</b><br>"
    "- PPV / precision = TP/(TP+FP)<br>"
    "- NPV = TN/(TN+FN)<br>"
    "- These are the clinically or commercially relevant numbers, and they change completely when the base "
    "rate changes:<br><br>"
    "\\[ \\text{PPV}=\\frac{\\text{sens}\\cdot\\pi}{\\text{sens}\\cdot\\pi+(1-\\text{spec})(1-\\pi)} \\]<br><br>"
    "<b>Summaries</b><br>"
    "- Accuracy = (TP+TN)/n - useless under imbalance.<br>"
    "- Balanced accuracy = (sens + spec)/2; Youden's J = sens + spec - 1.<br>"
    "- F1 = harmonic mean of precision and recall (ignores TN entirely).<br>"
    "- Likelihood ratios: LR+ = sens/(1-spec), LR- = (1-sens)/spec - the numbers that update the pre-test "
    "odds, and the cleanest way to think about a diagnostic test.",
    f"{T} confusion-matrix sensitivity specificity ppv diagram")


def _roc():
    cv = Canvas(w=460, h=280, pad=(46, 90, 34, 16))
    cv.limits((0, 1), (0, 1))
    cv.axes(xlabel="false positive rate (1 - specificity)", ylabel="true positive rate (sensitivity)",
            xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1])
    good = _roc_points(1.9)
    mid = _roc_points(0.9)
    cv.path(good, color=C["blue"], width=2.0, fill=C["blue"], close_to=0, fo=0.13)
    cv.path(mid, color=C["green"], width=1.8)
    cv.line(0, 0, 1, 1, color="currentColor", width=1.2, dash="4 3", opacity=0.55)
    cv.text(0.62, 0.30, "AUC = 0.5", size=9, opacity=0.7, anchor="start")
    cv.text(0.42, 0.62, "AUC", size=10, opacity=0.9, color=C["blue"])
    # youden point on the good curve
    best = max(good, key=lambda p: p[1] - p[0])
    cv.circle(best[0], best[1], r=3.4, fill=C["rose"])
    cv.line(best[0], best[0], best[0], best[1], color=C["rose"], width=1.1, dash="3 2", opacity=0.8)
    cv.text(best[0] + 0.03, best[1] - 0.10, "Youden J = max(sens+spec-1)", size=8.5, opacity=0.9,
            anchor="start", color=C["rose"])
    cv.legend([("AUC 0.91", C["blue"]), ("AUC 0.74", C["green"]), ("random", "currentColor", "4 3")],
              x=458, y=30)
    cv.caption(["each point is one threshold; the curve is threshold-free, which is its strength and its limit",
                "AUC = P(score of a random positive > score of a random negative) = Mann-Whitney U / (n₁n₀)",
                "Gini = 2·AUC - 1 = Somers' D. A curve can have high AUC and be badly miscalibrated."])
    return cv


pic("Draw an ROC curve and define AUC and Gini",
    _roc,
    "The ROC curve plots sensitivity against 1 - specificity as the classification threshold sweeps from "
    "+∞ to -∞. Each point is one threshold; the diagonal is random guessing; the top-left corner is "
    "perfection.<br><br>"
    "<b>AUC</b> - the area under it - has an exact probabilistic meaning:<br><br>"
    "\\[ \\text{AUC}=P\\big(\\hat s(\\text{positive})>\\hat s(\\text{negative})\\big)=\\frac{U}{n_1n_0} \\]<br><br>"
    "i.e. the probability that a randomly chosen positive is ranked above a randomly chosen negative - "
    "which makes it the normalised <b>Mann-Whitney U</b> statistic, and identical to the <b>c-index</b> in "
    "survival analysis.<br><br>"
    "<b>Gini coefficient</b> (as used in credit scoring) = 2·AUC - 1 = <b>Somers' D</b>: 0 for random, "
    "1 for perfect. Same information as AUC, rescaled.<br><br>"
    "What AUC is good for: comparing the <b>ranking ability</b> of models independently of any threshold or "
    "of prevalence. What it cannot tell you:<br>"
    "- whether the predicted probabilities are <b>calibrated</b> (a monotone distortion leaves AUC "
    "unchanged);<br>"
    "- whether the model is useful at the threshold you will actually use - it averages over all "
    "thresholds, including absurd ones;<br>"
    "- anything reliable under severe class imbalance, where the ROC looks flattering because the FPR "
    "denominator is huge.<br><br>"
    "For choosing a threshold, use costs, or Youden's J (max sens+spec-1) if the two error types are "
    "equally bad.",
    f"{T} roc auc gini somers-d diagram")


def _pr():
    cv = Canvas(w=460, h=280, pad=(46, 90, 34, 16))
    cv.limits((0, 1), (0, 1))
    cv.axes(xlabel="recall (sensitivity)", ylabel="precision (PPV)",
            xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1])
    for prev, col, lab in ((0.5, "blue", "prevalence 50 %"), (0.1, "green", "prevalence 10 %"),
                           (0.01, "rose", "prevalence 1 %")):
        pts = []
        for fpr, tpr in _roc_points(1.9):
            denom = tpr * prev + fpr * (1 - prev)
            if denom <= 0 or tpr <= 0.005:
                continue
            pts.append((tpr, tpr * prev / denom))
        cv.path(pts, color=C[col], width=1.9)
        cv.line(0, prev, 1, prev, color=C[col], width=1, dash="3 3", opacity=0.55)
    cv.legend([("prev 50 %", C["blue"]), ("prev 10 %", C["green"]), ("prev 1 %", C["rose"])],
              x=458, y=30)
    cv.text(0.52, 0.06, "dashed = baseline precision = prevalence", size=8.5, opacity=0.72,
            anchor="middle")
    cv.caption(["same model, same AUC (0.91) in all three - only the prevalence differs",
                "PR curves collapse under imbalance because precision has FP in its denominator",
                "so report PR-AUC (average precision) when positives are rare and FPs are costly"])
    return cv


pic("Why does a precision-recall curve show something an ROC curve hides?",
    _pr,
    "All three curves in the picture come from the <b>same model with the same AUC of 0.91</b>. Only the "
    "prevalence differs - and precision collapses as positives become rare.<br><br>"
    "The reason is which denominators the two curves use. ROC uses TPR = TP/(TP+FN) and FPR = FP/(FP+TN): "
    "both are computed <b>within</b> a class, so they are insensitive to the class mix. Precision = "
    "TP/(TP+FP) mixes classes, so when negatives outnumber positives 99:1, even a small FPR floods the "
    "predicted positives with false alarms.<br><br>"
    "Practical guidance:<br>"
    "- <b>Balanced classes, both errors matter</b> → ROC/AUC is fine.<br>"
    "- <b>Rare positives, and you care about the positives you flag</b> (fraud, disease screening, "
    "information retrieval, defect detection) → precision-recall curve and <b>PR-AUC / average "
    "precision</b>; the no-skill baseline is the prevalence, not 0.5.<br>"
    "- Note that PR-AUC is <b>not</b> comparable across datasets with different prevalence, whereas AUC "
    "is.<br>"
    "- Neither is the right answer if you know the costs: then compute expected cost, or use decision curve "
    "analysis / net benefit, which weights false positives against false negatives explicitly.",
    f"{T} precision-recall pr-auc imbalance diagram")


def _lorenz():
    cv = Canvas(w=460, h=285, pad=(46, 90, 34, 16))
    cv.limits((0, 1), (0, 1))
    cv.axes(xlabel="cumulative share of population (ranked by score)",
            ylabel="cumulative share of outcome",
            xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1])
    cv.line(0, 0, 1, 1, width=1.3, dash="4 3", opacity=0.6)
    # Lorenz-type curve (concentration): concave, ranked worst-to-best
    pts = [(t, t ** 2.4) for t in [i / 200 for i in range(201)]]
    cv.path(pts, color=C["blue"], width=2.0)
    # fill between diagonal and curve
    poly = pts + [(1, 1)]
    cv.raw('<path d="M' + " L".join(f"{n(cv.X(x))},{n(cv.Y(y))}" for x, y in poly) +
           f' Z" fill="{C["blue"]}" fill-opacity="0.16" stroke="none"/>')
    cv.text(0.53, 0.63, "A", size=11, opacity=0.95, color=C["blue"])
    cv.text(0.72, 0.24, "B", size=11, opacity=0.8)
    cv.text(0.30, 0.40, "line of equality", size=9, opacity=0.7, anchor="start")
    # gain curve (mirrored, ranked best first) for comparison
    g = [(t, 1 - (1 - t) ** 2.4) for t in [i / 200 for i in range(201)]]
    cv.path(g, color=C["green"], width=1.8, dash="5 3")
    cv.text(0.30, 0.86, "gain / CAP curve", size=9, opacity=0.85, anchor="start", color=C["green"])
    cv.text(0.30, 0.76, "(same info, ranked best first)", size=8.5, opacity=0.7, anchor="start")
    cv.caption(["Gini = A / (A + B) = 2 × area between the curve and the diagonal",
                "in inequality: 0 = everyone equal, 1 = one person has everything",
                "in scoring: how concentrated the events are among the highest-ranked cases"])
    return cv


pic("Draw the Lorenz curve and define the Gini coefficient",
    _lorenz,
    "Rank all units by the score, then plot the cumulative share of the <b>population</b> against the "
    "cumulative share of the <b>outcome</b>. The 45° line is perfect equality (every unit contributes the "
    "same); the further the curve bows away, the more concentrated the outcome.<br><br>"
    "\\[ \\text{Gini}=\\frac{A}{A+B}=2A=1-2\\int_0^1 L(p)\\,dp \\]<br><br>"
    "Two uses that are easy to conflate:<br>"
    "- <b>Inequality measurement</b> (the original): x is the population ranked by income, y is the "
    "cumulative income share. Gini 0 = perfect equality, 1 = one person owns everything. It is a "
    "scale-free, mean-independent summary, but very different distributions can share a Gini, and it is "
    "insensitive to <b>where</b> in the distribution the inequality sits (hence Theil, Atkinson, "
    "percentile ratios as complements).<br>"
    "- <b>Model performance</b> (credit scoring, insurance): rank cases by predicted risk and plot the "
    "cumulative share of actual events captured. Then <b>Gini = 2·AUC - 1</b>, and the mirrored version "
    "ranked best-first is the <b>gain / CAP curve</b>. Same information, different convention.<br><br>"
    "Related: the <b>concentration curve</b> keeps the ranking variable different from the outcome (e.g. "
    "rank by income, plot health), which is how health-inequality indices are built.",
    f"{T} lorenz gini concentration inequality diagram")


def _lift():
    cv = Canvas(w=460, h=285, pad=(46, 90, 34, 16))
    cv.limits((0, 1), (0, 3.6))
    cv.axes(xlabel="fraction of population contacted (highest score first)",
            ylabel="lift = response rate / baseline",
            xticks=[0, 0.2, 0.4, 0.6, 0.8, 1], yticks=[0, 1, 2, 3])
    # cumulative lift from a gain curve g(t) = 1-(1-t)^k
    k = 2.4
    pts = [(t, (1 - (1 - t) ** k) / t) for t in [0.02 + 0.98 * i / 200 for i in range(201)]]
    cv.path(pts, color=C["blue"], width=2.0)
    cv.line(0, 1, 1, 1, width=1.2, dash="4 3", opacity=0.6)
    cv.text(0.62, 1.16, "lift = 1: no better than random", size=9, opacity=0.72, anchor="start")
    cv.circle(0.1, (1 - 0.9 ** k) / 0.1, r=3.4, fill=C["rose"])
    cv.text(0.14, (1 - 0.9 ** k) / 0.1 + 0.12, "lift@10 % ≈ 2.4", size=9.5, opacity=0.9,
            anchor="start", color=C["rose"])
    cv.caption(["the operational metric: 'if I contact the top decile, how many more events do I catch?'",
                "lift always decays to 1 at 100 % contacted - only the left-hand part is informative",
                "cumulative lift@k relates directly to the gain curve: lift(t) = gain(t) / t"])
    return cv


pic("Draw a lift chart and define lift and gain",
    _lift,
    "Sort cases by predicted score, highest first, and walk down the list.<br><br>"
    "- <b>Gain (cumulative response) curve</b>: what fraction of all actual events have I captured after "
    "contacting the top t of the population? Perfect model rises to 1 at t = prevalence; random gives the "
    "diagonal.<br>"
    "- <b>Lift</b>: gain(t)/t - how many times better than random the selected group is.<br><br>"
    "\\[ \\text{lift}(t)=\\frac{\\text{response rate in top }t}{\\text{overall response rate}}=\\frac{\\text{gain}(t)}{t} \\]<br><br>"
    "Why practitioners prefer these to AUC: they answer the actual operational question - 'we can only call "
    "5 000 customers, how much better is that than calling at random?' - and they map onto a budget. "
    "Standard reporting is lift or gain at the top decile.<br><br>"
    "Related curves: the <b>CAP curve</b> (same as the gain curve, common in credit risk), the "
    "<b>decile table</b> (event rate per score decile, which also reveals monotonicity problems), and the "
    "<b>KS statistic</b> - the maximum vertical distance between the cumulative score distributions of "
    "events and non-events, a single number widely used in scorecard validation.<br><br>"
    "Limitation: lift depends on prevalence and on the chosen cutoff fraction, so it is not comparable "
    "across datasets, and like AUC it is purely a ranking measure - it says nothing about whether the "
    "probabilities themselves are right.",
    f"{T} lift gain cap ks-statistic diagram")


def _calibration():
    cv = Canvas(w=460, h=285, pad=(46, 90, 34, 16))
    cv.limits((0, 1), (0, 1))
    cv.axes(xlabel="predicted probability", ylabel="observed frequency",
            xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.25, 0.5, 0.75, 1])
    cv.line(0, 0, 1, 1, width=1.3, dash="4 3", opacity=0.6)
    cv.text(0.72, 0.78, "perfect", size=9, opacity=0.7, anchor="start")
    # overconfident: predictions too extreme (slope < 1)
    over = [(p, min(1, max(0, 0.5 + 0.55 * (p - 0.5)))) for p in [i / 200 for i in range(201)]]
    cv.path(over, color=C["rose"], width=1.9)
    # underconfident
    under = [(p, min(1, max(0, 0.5 + 1.45 * (p - 0.5)))) for p in [i / 200 for i in range(201)]]
    cv.path(under, color=C["green"], width=1.9)
    # systematic overprediction
    bias = [(p, max(0, p - 0.13)) for p in [i / 200 for i in range(201)]]
    cv.path(bias, color=C["amber"], width=1.7, dash="5 3")
    for p in (0.1, 0.3, 0.5, 0.7, 0.9):
        cv.circle(p, 0.5 + 0.55 * (p - 0.5), r=2.6, fill=C["rose"])
    cv.legend([("slope < 1: overconfident", C["rose"]), ("slope > 1: underconfident", C["green"]),
               ("intercept < 0: over-predicts", C["amber"], "5 3")], x=458, y=28)
    cv.caption(["calibration is invisible to AUC: any monotone rescaling of the scores leaves AUC unchanged",
                "report the calibration intercept (bias) and slope (spread); slope < 1 = overfitted",
                "fix by re-calibrating: Platt scaling (logistic) or isotonic regression on held-out data"])
    return cv


pic("Draw a calibration plot and say what the intercept and slope mean",
    _calibration,
    "Bin or smooth the predicted probabilities and plot the observed event frequency against the predicted "
    "one. Perfect calibration is the 45° line: among cases predicted at 20 %, 20 % should have the event.<br><br>"
    "Read it as a regression of outcome on predicted risk (on the logit scale):<br>"
    "- <b>Calibration intercept</b> ('calibration in the large'): overall bias. Negative means the model "
    "over-predicts risk on average - the usual result when a model is transported to a lower-prevalence "
    "population.<br>"
    "- <b>Calibration slope</b>: spread of the predictions. Slope < 1 means predictions are too extreme "
    "(the classic signature of <b>overfitting</b>, since apparent-fit slope is 1 by construction and drops "
    "on validation); slope > 1 means too timid.<br><br>"
    "Why it deserves its own plot: <b>AUC is invariant to any monotone transformation of the scores</b>, so "
    "a model can rank perfectly and still assign wildly wrong probabilities. If a decision depends on the "
    "probability - expected cost, treatment thresholds, pricing, expected loss - calibration is the part "
    "that matters.<br><br>"
    "Summaries and fixes: the Brier score decomposes into calibration and refinement; ECE (expected "
    "calibration error) summarises the gap; Platt scaling (fit a logistic on the scores) and isotonic "
    "regression re-calibrate on held-out data. Tree ensembles and SVMs typically need this; a "
    "well-specified logistic GLM is calibrated on its own training data by construction.",
    f"{T} calibration brier platt-scaling diagram")


# ---------------------------------------------------------------------------
# text cards
# ---------------------------------------------------------------------------
txt("What is a proper scoring rule, and why is accuracy not one?",
    "A scoring rule evaluates a <b>probabilistic</b> prediction. It is <b>proper</b> if the expected score "
    "is optimised only by reporting your true belief, and <b>strictly proper</b> if that optimum is unique. "
    "So a proper rule cannot be gamed by distorting your probabilities.<br><br>"
    "Proper rules:<br>"
    "- <b>Brier score</b> \\(\\frac1n\\sum(\\hat p_i-y_i)^2\\) - a bounded quadratic rule; for a rare "
    "outcome it is small for everyone, so compare it against the base-rate model (a skill score).<br>"
    "- <b>Log loss</b> (cross-entropy) \\(-\\frac1n\\sum[y\\log\\hat p+(1-y)\\log(1-\\hat p)]\\) - the "
    "likelihood, and it punishes confident mistakes infinitely, which is why it is the natural training "
    "loss.<br>"
    "- <b>CRPS</b> for continuous or full-distribution forecasts; the <b>pinball loss</b> for quantiles.<br><br>"
    "Improper measures: <b>accuracy</b>, F1, sensitivity, specificity and precision are all functions of a "
    "<b>thresholded</b> prediction, so they reward distorting probabilities toward the threshold and can "
    "prefer a worse model. AUC is proper only as a measure of <b>ranking</b>, not of probabilities.<br><br>"
    "Practical recipe: train and select on a proper rule (log loss or Brier), then report discrimination "
    "(AUC), calibration (plot plus intercept/slope), and finally a threshold-based operating point chosen "
    "from the actual costs.",
    f"{T} proper-scoring-rules brier log-loss")

txt("How does the Brier score decompose, and what does that tell you?",
    "Murphy's decomposition splits it into three interpretable parts:<br><br>"
    "\\[ \\text{BS}=\\underbrace{\\text{reliability}}_{\\text{calibration error}}-"
    "\\underbrace{\\text{resolution}}_{\\text{discrimination}}+"
    "\\underbrace{\\text{uncertainty}}_{\\bar y(1-\\bar y)} \\]<br><br>"
    "- <b>Reliability</b>: how far the observed frequencies deviate from the predicted probabilities within "
    "each prediction group - smaller is better, and it is exactly what a calibration plot shows.<br>"
    "- <b>Resolution</b>: how much the group-wise event rates differ from the overall rate - larger is "
    "better; it measures the model's ability to separate cases. A model that always predicts the base rate "
    "is perfectly calibrated with zero resolution.<br>"
    "- <b>Uncertainty</b>: the variance of the outcome itself - a property of the data, not the model, "
    "which is why raw Brier scores are not comparable across datasets.<br><br>"
    "The practical implication: a good score requires <b>both</b> calibration and discrimination, and the "
    "decomposition tells you which one is failing. Use a <b>skill score</b> - "
    "\\(1-\\text{BS}/\\text{BS}_{\\text{ref}}\\) against the base rate or the previous model - to remove the "
    "uncertainty term and make comparisons meaningful.",
    f"{T} brier decomposition calibration resolution")

txt("Which measures exist for multi-class classification, and how does averaging change the answer?",
    "Start from the k x k confusion matrix, then choose an averaging scheme - and this choice, not the "
    "metric, usually dominates the number:<br><br>"
    "- <b>Macro average</b>: compute the metric per class, then average unweighted. Every class counts "
    "equally, so rare classes dominate the score. Use when small classes matter as much as large ones.<br>"
    "- <b>Micro average</b>: pool all TP/FP/FN across classes first. Large classes dominate; for "
    "single-label problems micro-F1 equals accuracy.<br>"
    "- <b>Weighted average</b>: per-class metric weighted by class support - a compromise that hides "
    "failures on rare classes.<br><br>"
    "Other measures:<br>"
    "- <b>Multi-class AUC</b>: one-vs-rest averaged, or Hand-Till's pairwise M measure (prevalence-"
    "independent).<br>"
    "- <b>Multi-class log loss</b> and the <b>multi-class Brier</b> (Ranked Probability Score) - the proper "
    "rules, and the ones to select on.<br>"
    "- <b>Cohen's kappa</b>: agreement corrected for chance; <b>quadratic weighted kappa</b> for ordered "
    "classes, since it penalises being off by two more than off by one.<br>"
    "- <b>MCC</b>: a balanced correlation-style measure that works under imbalance.<br>"
    "- <b>Top-k accuracy</b> when a shortlist is the deliverable.<br><br>"
    "Always look at the <b>normalised confusion matrix</b> as well: a single number cannot show you that "
    "the model systematically confuses two specific classes.",
    f"{T} multiclass macro-micro kappa mcc")

txt("Which measures exist for regression predictions, and what does each penalise?",
    "- <b>MSE / RMSE</b>: quadratic, so it is dominated by large errors; RMSE is in the units of y. "
    "The minimiser is the conditional <b>mean</b>. Use when big errors are disproportionately bad.<br>"
    "- <b>MAE</b>: linear, robust to outliers; its minimiser is the conditional <b>median</b>. If you "
    "report MAE you should be modelling the median (quantile regression), not the mean - a mismatch "
    "people rarely notice.<br>"
    "- <b>Huber / pseudo-Huber</b>: quadratic near zero, linear in the tails - a compromise.<br>"
    "- <b>MAPE</b>: percentage error, but undefined at y = 0, exploding for small y, and <b>asymmetric</b> "
    "(it prefers under-prediction). Avoid unless y is comfortably positive.<br>"
    "- <b>sMAPE</b>: patched symmetry, still awkward.<br>"
    "- <b>MASE</b>: error scaled by the in-sample naive forecast's error - scale-free, defined at zero, "
    "the sane default for comparing across time series.<br>"
    "- <b>RMSLE</b>: penalises relative error and under-prediction more - use for multiplicative, "
    "right-skewed targets.<br>"
    "- <b>Pinball loss</b> for quantile predictions; <b>CRPS</b> and <b>interval score</b> for full "
    "predictive distributions; <b>PIT histogram</b> and <b>interval coverage</b> for calibration.<br><br>"
    "The rule behind all of them: the metric implies the estimand. Choose the loss first, then fit the model "
    "that targets it.",
    f"{T} regression rmse mae mape mase crps")

txt("What does R² actually measure, and what are its traps?",
    "\\[ R^2=1-\\frac{\\text{SS}_{\\text{res}}}{\\text{SS}_{\\text{tot}}}=1-"
    "\\frac{\\sum(y_i-\\hat y_i)^2}{\\sum(y_i-\\bar y)^2} \\]<br><br>"
    "It is the proportion of variance explained <b>relative to the mean-only model</b>, on the training "
    "data.<br><br>"
    "Traps:<br>"
    "- it <b>never decreases</b> when you add a predictor, however useless - hence adjusted R², which "
    "penalises parameters;<br>"
    "- it depends on the <b>spread of x</b> in your sample, so it is not a property of the relationship: "
    "the same model can have R² of 0.2 or 0.9 in two samples;<br>"
    "- a high R² is compatible with a completely wrong functional form, and a low R² with a perfectly "
    "correct one (just noisy);<br>"
    "- it says nothing about causal validity or about prediction on new data - report "
    "<b>out-of-sample R²</b> (computed with the training mean as the baseline), which can be negative;<br>"
    "- comparing R² across different response transformations is meaningless;<br>"
    "- for models without an intercept, or with weights, the usual formula loses its interpretation.<br><br>"
    "For GLMs there is no variance to decompose, so use <b>pseudo-R²</b> - McFadden "
    "\\(1-\\ell_{\\text{full}}/\\ell_{\\text{null}}\\), Nagelkerke (rescaled to reach 1), or "
    "<b>deviance explained</b> - and remember none of them is a proportion of variance. For mixed models "
    "report marginal (fixed effects only) and conditional (with random effects) R² separately.",
    f"{T} r-squared pseudo-r2 deviance-explained")

txt("Which performance measures are used for survival models?",
    "Censoring breaks the ordinary metrics, so each one needs a censoring-aware version.<br><br>"
    "- <b>Harrell's c-index</b>: the fraction of comparable pairs whose predicted risk ordering matches "
    "their observed event ordering - the survival analogue of AUC. Pairs where censoring makes the order "
    "unknown are dropped, which makes it dependent on the censoring distribution; <b>Uno's c</b> uses "
    "inverse-probability-of-censoring weights to fix that.<br>"
    "- <b>Time-dependent AUC</b>: discrimination for the event happening before a specific horizon - the "
    "honest way to report 'how well does it predict 5-year risk'.<br>"
    "- <b>Brier score at time t / integrated Brier score</b> (IPCW-weighted): the calibration-plus-"
    "discrimination measure, with the reference being the Kaplan-Meier marginal prediction.<br>"
    "- <b>Calibration plots at fixed horizons</b>: predicted versus Kaplan-Meier-observed survival by risk "
    "group.<br>"
    "- <b>Royston-Sauerbrei R²</b> or the explained variation measures for the Cox model.<br>"
    "- <b>Decision curve analysis</b> at a horizon, for clinical usefulness.<br><br>"
    "Two reminders: a c-index of 0.7 in survival is not comparable to an AUC of 0.7 from binary data on the "
    "same problem, and the proportional-hazards assumption affects predictions much more than it affects "
    "the c-index.",
    f"{T} survival c-index time-dependent-auc ipcw")

txt("Which information criteria exist and how should they be used?",
    "- <b>AIC</b> = -2ℓ + 2p: estimates out-of-sample predictive deviance and is asymptotically equivalent "
    "to leave-one-out cross-validation. Targets <b>prediction</b>; tends to pick larger models.<br>"
    "- <b>AICc</b>: small-sample correction, use when n/p < 40.<br>"
    "- <b>BIC</b> = -2ℓ + p·log n: approximates the Bayes factor and is consistent for the true model if it "
    "is among the candidates. Targets <b>identification</b>; penalises harder, so it picks smaller models.<br>"
    "- <b>DIC, WAIC, LOO-IC (PSIS-LOO)</b>: Bayesian versions using the posterior; WAIC and LOO are "
    "preferred, and `loo` reports Pareto-k diagnostics that warn you when the approximation fails.<br>"
    "- <b>Mallows' Cp</b>: equivalent to AIC for linear models with known σ².<br>"
    "- <b>GCV</b>: used for smoothing-parameter selection in GAMs.<br><br>"
    "Rules for using them: same data, same response, same likelihood - otherwise the comparison is void "
    "(this rules out comparing across response transformations, and across REML fits with different fixed "
    "effects). Differences are what matter, not levels: Δ < 2 is negligible, Δ > 10 is decisive. For mixed "
    "models the effective p is ambiguous, so use conditional AIC or cross-validate by cluster. And note "
    "that selecting a model by an information criterion and then reporting its p-values as if the model had "
    "been pre-specified is a real inferential error.",
    f"{T} aic bic waic loo model-selection")

txt("How do you validate a model honestly, and where does leakage creep in?",
    "Hierarchy of validation:<br>"
    "1. <b>Apparent</b> performance on the training data - always optimistic, essentially useless for "
    "flexible models.<br>"
    "2. <b>k-fold cross-validation</b> (5 or 10 folds; repeated for stability) - the default. "
    "Stratify on the outcome for imbalanced classification.<br>"
    "3. <b>Nested CV</b> when hyperparameters are tuned: the inner loop tunes, the outer loop estimates "
    "performance. Tuning on the same folds you report is a classic source of optimism.<br>"
    "4. <b>Grouped / blocked CV</b> whenever observations are clustered: split by patient, school, subject "
    "or site, never by row.<br>"
    "5. <b>Rolling-origin (time-series) CV</b> for anything temporal: train on the past, test on the "
    "future.<br>"
    "6. <b>External validation</b> on a different population, time period or centre - the only thing that "
    "tests transportability. Expect the calibration slope to fall.<br>"
    "7. <b>Bootstrap optimism correction</b> is efficient for small samples.<br><br>"
    "Common leakage: preprocessing (scaling, imputation, feature selection, SMOTE) fitted on the full data "
    "before splitting; target-derived features; duplicated or near-duplicate rows across folds; using "
    "future information; and selecting the reported metric after seeing all results. The fix is to put "
    "<b>every</b> data-dependent step inside the resampling loop - which is exactly what "
    "`tidymodels` recipes, `caret` and `mlr3` pipelines are for.",
    f"{T} validation cross-validation leakage")

txt("Which metric should you pick for which prediction task?",
    "<b>Binary classification</b><br>"
    "- Selection/training: log loss or Brier (proper).<br>"
    "- Ranking quality: AUC; PR-AUC when positives are rare.<br>"
    "- Probability quality: calibration plot, intercept and slope.<br>"
    "- Operating point: expected cost, or sensitivity at a fixed specificity / precision at a fixed recall - "
    "whichever the application fixes. Decision curve analysis when the cost ratio is only roughly known.<br><br>"
    "<b>Multi-class</b>: multi-class log loss for selection, macro-F1 or macro-AUC when small classes "
    "matter, quadratic weighted kappa for ordered classes, plus the normalised confusion matrix.<br><br>"
    "<b>Regression</b>: RMSE if the mean is the target and large errors hurt; MAE if the median is; MASE or "
    "MAPE-style relative measures when scales differ across series; pinball loss for quantiles; "
    "CRPS plus interval coverage for probabilistic forecasts.<br><br>"
    "<b>Survival</b>: c-index for ranking, time-dependent AUC and IPCW Brier at the horizon you care "
    "about, calibration by risk group.<br><br>"
    "<b>Ranking / recommendation</b>: precision@k, recall@k, MAP, NDCG.<br><br>"
    "Two overarching rules: the metric must match the <b>decision</b> the prediction feeds into, and you "
    "should always report at least one measure of discrimination <b>and</b> one of calibration - they fail "
    "independently.",
    f"{T} metric-choice summary")

txt("Why do discrimination, calibration and clinical usefulness need to be reported separately?",
    "They are three genuinely independent properties of a prediction model, and a model can pass one while "
    "failing the others.<br><br>"
    "- <b>Discrimination</b> (AUC, c-index): can the model order cases correctly? Invariant to any monotone "
    "rescaling of the scores, so it is blind to systematic over- or under-prediction.<br>"
    "- <b>Calibration</b> (calibration plot, intercept and slope, Brier reliability): are the predicted "
    "probabilities numerically right? A perfectly discriminating model can still be badly calibrated, and "
    "recalibration is usually the first thing that breaks when a model moves to a new population.<br>"
    "- <b>Clinical / practical usefulness</b> (decision curve analysis, net benefit, expected cost): does "
    "acting on the model beat the default policies of 'treat everyone' and 'treat nobody' at plausible "
    "thresholds? A model can have good AUC and good calibration and still provide no net benefit at any "
    "threshold anyone would use.<br><br>"
    "Net benefit makes the trade-off explicit by weighting false positives at the odds implied by the "
    "threshold:<br><br>"
    "\\[ \\text{NB}=\\frac{TP}{n}-\\frac{FP}{n}\\cdot\\frac{p_t}{1-p_t} \\]<br><br>"
    "This is why reporting guidelines (TRIPOD) ask for all three plus external validation, rather than a "
    "single headline number.",
    f"{T} discrimination calibration net-benefit tripod")

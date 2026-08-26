# -*- coding: utf-8 -*-
"""Section 4 - link functions: which one when, what they assume, which natural
process each one encodes."""
from plotlib import *

T = "Core links"
PIC = []
TXT = []


def pic(front, builder, back, tags):
    PIC.append((front, builder, back, tags))


def txt(front, back, tags):
    TXT.append((front, back, tags))


# ---------------------------------------------------------------------------
def _binary_links():
    cv = Canvas(w=460, h=270)
    cv.limits((-4.5, 4.5), (0, 1.05))
    cv.axes(xlabel="linear predictor η", ylabel="μ = P(Y = 1)",
            xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.25, 0.5, 0.75, 1])
    logit = lambda e: 1 / (1 + math.exp(-e))
    probit = lambda e: norm_cdf(e * 1.7)          # scaled to be comparable
    cloglog = lambda e: 1 - math.exp(-math.exp(e))
    grid = [-4.5 + 9 * i / 300 for i in range(301)]
    cv.path([(e, logit(e)) for e in grid], color=C["blue"], width=2.0)
    cv.path([(e, probit(e)) for e in grid], color=C["green"], width=1.8, dash="5 3")
    cv.path([(e, cloglog(e)) for e in grid], color=C["rose"], width=1.8)
    cv.line(-4.5, 0.5, 4.5, 0.5, width=0.9, dash="2 3", opacity=0.35)
    cv.line(0, 0, 0, 1.05, width=0.9, dash="2 3", opacity=0.35)
    cv.legend([("logit", C["blue"]), ("probit (×1.7)", C["green"], "5 3"),
               ("cloglog", C["rose"])], x=200, y=40)
    cv.text(2.6, 0.32, "cloglog is asymmetric:", size=9, opacity=0.8, anchor="start")
    cv.text(2.6, 0.22, "approaches 1 faster", size=9, opacity=0.8, anchor="start")
    cv.caption(["logit and probit are symmetric about 0.5 and nearly identical after rescaling (β_logit ≈ 1.7 β_probit)",
                "cloglog is skewed - use it when the two tails should not behave the same way",
                "all three map the whole real line into (0,1), which is the entire point of a link"])
    return cv


pic("Compare the logit, probit and cloglog links for a binary outcome",
    _binary_links,
    "All three squash the linear predictor into (0,1), so predictions can never leave the legal range.<br><br>"
    "<b>Logit</b> \\(\\log\\frac{\\mu}{1-\\mu}\\): canonical for the Bernoulli. Coefficients are log odds "
    "ratios, it is the only link whose effects are invariant to case-control sampling, and it is symmetric "
    "about 0.5. Default choice.<br><br>"
    "<b>Probit</b> \\(\\Phi^{-1}(\\mu)\\): the same shape, from a <b>latent normal</b> crossing a threshold. "
    "Practically indistinguishable in fit; after rescaling by ≈ 1.7 the coefficients match. Preferred when "
    "the latent-variable story is the model (psychophysics, threshold models, ordered probit) or when "
    "you need normal latent errors for a bigger model.<br><br>"
    "<b>Cloglog</b> \\(\\log(-\\log(1-\\mu))\\): <b>asymmetric</b>, and the one with a real mechanism behind "
    "it - it is what you get when an event occurs as soon as a hidden Poisson count reaches one, and it "
    "gives <b>proportional hazards</b> in discrete-time survival. Use it for infection or failure after "
    "many small exposures, for dose-response where the upper tail saturates quickly, and whenever the event "
    "is rare on one side but not the other.<br><br>"
    "The choice barely changes the fitted probabilities in the middle; it changes the <b>tails</b> and the "
    "interpretation of the coefficients.",
    f"{T} logit probit cloglog binary diagram")


def _loglog():
    cv = Canvas(w=470, h=270, pad=(46, 14, 34, 16))
    # left panel: raw scale, right: log-log
    # Draw as a single canvas with two sub-areas using absolute coords
    def panel(x0, x1, title):
        cv.text((x0 + x1) / 2, 26, title, size=9.5, weight="bold", opacity=0.9, data=False)

    # raw
    cv.limits((0, 10), (0, 10))
    # left axes manually
    LX0, LX1, TOP, BOT = 40, 218, 46, 200
    cv.raw(f'<line x1="{LX0}" y1="{BOT}" x2="{LX1}" y2="{BOT}" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85"/>')
    cv.raw(f'<line x1="{LX0}" y1="{BOT}" x2="{LX0}" y2="{TOP}" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85"/>')
    pts = []
    for i in range(101):
        x = 0.05 + 9.95 * i / 100
        y = 0.35 * x ** 0.75
        pts.append((LX0 + (x / 10) * (LX1 - LX0), BOT - (y / 2.2) * (BOT - TOP)))
    cv.raw('<path d="M' + " L".join(f"{n(a)},{n(b)}" for a, b in pts) +
           f'" fill="none" stroke="{C["blue"]}" stroke-width="2"/>')
    cv.text((LX0 + LX1) / 2, 26, "raw scale: curved", size=9.5, weight="bold", data=False)
    cv.text((LX0 + LX1) / 2, BOT + 16, "x", size=9, opacity=0.75, data=False)
    cv.text(LX0 - 8, TOP + 6, "y", size=9, opacity=0.75, anchor="end", data=False)
    cv.text((LX0 + LX1) / 2, 100, "y = c · x^0.75", size=9.5, opacity=0.85, data=False)

    # log-log
    RX0, RX1 = 262, 440
    cv.raw(f'<line x1="{RX0}" y1="{BOT}" x2="{RX1}" y2="{BOT}" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85"/>')
    cv.raw(f'<line x1="{RX0}" y1="{BOT}" x2="{RX0}" y2="{TOP}" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.85"/>')
    cv.raw(f'<line x1="{RX0 + 6}" y1="{BOT - 12}" x2="{RX1 - 6}" y2="{TOP + 26}" stroke="{C["blue"]}" stroke-width="2"/>')
    cv.text((RX0 + RX1) / 2, 26, "log-log scale: straight", size=9.5, weight="bold", data=False)
    cv.text((RX0 + RX1) / 2, BOT + 16, "log x", size=9, opacity=0.75, data=False)
    cv.text(RX0 - 8, TOP + 6, "log y", size=9, opacity=0.75, anchor="end", data=False)
    cv.text(RX1 - 20, TOP + 52, "slope = 0.75", size=9.5, opacity=0.9, anchor="end", data=False,
            color=C["blue"])
    cv.text(RX1 - 20, TOP + 66, "= the exponent", size=9, opacity=0.75, anchor="end", data=False)
    cv.raw(f'<line x1="230" y1="{TOP}" x2="230" y2="{BOT}" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.3"/>')
    cv.pb = cv.h - BOT
    cv.caption(["log link + log covariate = power law: log E[y] = a + b log x  &#8658;  E[y] = e^a x^b",
                "b is an elasticity: a 1 % change in x gives a b % change in y, at every scale",
                "scale invariance is the signature - no characteristic size, so doubling x always does the same thing"],
               x=16)
    return cv


pic("How does a log link with a log-transformed covariate produce a power law, and what does the slope mean?",
    _loglog,
    "Put a log link on the mean and a log on the covariate, and the model becomes multiplicative in both "
    "directions:<br><br>"
    "\\[ \\log E[Y]=a+b\\log x\\quad\\Longleftrightarrow\\quad E[Y]=e^{a}x^{b} \\]<br><br>"
    "So a straight line on a log-log plot <b>is</b> a power law, and the slope b is the <b>exponent</b>. "
    "In economics b is an <b>elasticity</b>: a 1 % increase in x produces a b % change in y - the same "
    "relative response at every scale. That scale invariance is the defining property; there is no "
    "characteristic size at which the relationship changes character.<br><br>"
    "Natural processes that produce it:<br>"
    "- <b>Allometric scaling</b> in biology: metabolic rate ∝ mass<sup>3/4</sup> (Kleiber's law), "
    "lifespan, heart rate, bone dimensions - because transport networks and surface-to-volume ratios "
    "constrain growth geometrically.<br>"
    "- <b>Urban scaling</b>: infrastructure grows sublinearly with population (b ≈ 0.85), while innovation "
    "and wages grow superlinearly (b ≈ 1.15).<br>"
    "- <b>Physics and engineering</b>: drag, Reynolds-number relations, fracture and fatigue laws.<br>"
    "- <b>Learning and experience curves</b>: cost per unit falls as a power of cumulative production "
    "(Wright's law).<br><br>"
    "Practical hint: if a scatter looks curved and both variables are positive, plot it on log-log axes "
    "before choosing a transformation - a straight line there tells you the mechanism is multiplicative, "
    "and that a Gamma or lognormal GLM with a log link and log(x) is the model you want.",
    f"{T} log-link power-law elasticity allometric diagram")


# ---------------------------------------------------------------------------
txt("What is a link function, and why not simply transform the response?",
    "A link maps the <b>mean</b> of the response onto the linear predictor: \\(g(E[Y])=X\\beta\\). "
    "Transforming the response instead models \\(E[g(Y)]=X\\beta\\), and by Jensen's inequality those are "
    "not the same thing.<br><br>"
    "Consequences of the difference:<br>"
    "- Back-transforming a fitted log-scale mean gives the <b>median</b> (or a biased mean), not the mean; "
    "a log link needs no retransformation correction at all.<br>"
    "- log(y) is undefined for <b>zeros</b>, which forces the notorious log(y + 1) fudge; a log link "
    "handles zeros without complaint.<br>"
    "- Transforming y changes the <b>variance structure</b> as a side effect, mixing two decisions together. "
    "The link and the variance function are separate in a GLM, which is exactly what makes it a better "
    "tool.<br>"
    "- The link keeps the model's predictions in the legal range (probabilities in (0,1), rates positive) "
    "without truncation.<br><br>"
    "Note also what the link does <b>not</b> assume: nothing about the distribution of the errors on the "
    "link scale. What it does assume is <b>linearity on the link scale</b> - and that is the assumption to "
    "check.",
    f"{T} link-vs-transformation jensen retransformation")

txt("What is the canonical link of each exponential-family distribution, and why does it matter?",
    "- <b>Normal</b> → identity<br>"
    "- <b>Bernoulli / binomial</b> → logit<br>"
    "- <b>Poisson</b> → log<br>"
    "- <b>Gamma</b> → inverse (1/μ)<br>"
    "- <b>Inverse Gaussian</b> → inverse square (1/μ²)<br>"
    "- <b>Negative binomial</b> → log in practice (its true canonical link is awkward and rarely used)<br>"
    "- <b>Multinomial</b> → the multivariate logit, i.e. softmax<br><br>"
    "Why the canonical link is convenient: the score equations reduce to \\(X^\\top(y-\\mu)=0\\), so the "
    "observed and expected information coincide, Fisher scoring equals Newton-Raphson, the log-likelihood is "
    "concave (a unique maximum, reliable convergence), sufficient statistics are \\(X^\\top y\\), and the "
    "residuals are orthogonal to the covariates so the fitted totals match the observed totals within any "
    "level of a categorical predictor.<br><br>"
    "But canonical is a <b>mathematical</b> convenience, not a scientific requirement. In practice a "
    "Gamma model is almost always fitted with a log link rather than the canonical inverse, because "
    "multiplicative effects are what the science means and because the log keeps μ positive - the inverse "
    "link does not.",
    f"{T} canonical-link exponential-family fisher-scoring")

txt("When is the identity link the right choice, even for non-normal data?",
    "When the effects really are <b>additive on the natural scale</b> and that is the quantity you want to "
    "report.<br><br>"
    "- <b>Normal response</b>: the default, giving the classical linear model.<br>"
    "- <b>Binomial with identity link</b>: coefficients are <b>risk differences</b> (absolute risk "
    "reduction) - often the clinically or policy-relevant number, since 'number needed to treat' is its "
    "reciprocal. Odds ratios exaggerate for common outcomes.<br>"
    "- <b>Poisson with identity link</b>: an additive rate change, e.g. 'this intervention prevents 3 "
    "events per 1000 person-years'.<br><br>"
    "The price: an identity link places <b>no constraint</b> on the range, so the fitted mean can go "
    "negative or above 1. That produces convergence failures and predictions that are impossible, "
    "especially when covariates are extreme or the outcome is near a boundary.<br><br>"
    "Practical compromise: fit on a link that respects the range (logit or log), then report the additive "
    "contrast you actually want by computing <b>average marginal effects</b> or standardised predictions - "
    "you get the interpretable absolute difference without the estimation problems.",
    f"{T} identity-link risk-difference interpretation")

txt("When is a log link the right choice, and what does it imply about the process?",
    "Whenever the response is positive and effects are <b>multiplicative</b> - each covariate scales the "
    "mean by a factor rather than adding a constant.<br><br>"
    "\\[ \\log\\mu=\\beta_0+\\beta_1x\\ \\Longrightarrow\\ \\mu=e^{\\beta_0}e^{\\beta_1 x},\\qquad "
    "e^{\\beta_1}=\\text{multiplicative factor per unit of }x \\]<br><br>"
    "The processes that generate it: anything that <b>grows or decays proportionally</b> - exponential "
    "population growth, compound interest, dose-rate effects, reaction rates, epidemic spread, "
    "hazard rates. If two factors each double the risk, they jointly quadruple it: on the log scale that "
    "is an additive main-effects model with no interaction term needed, which is precisely why the log link "
    "so often removes interactions from a badly scaled model.<br><br>"
    "Standard uses: Poisson and negative binomial counts (with an <b>offset</b> log(exposure) so that the "
    "model is about a rate), Gamma or lognormal costs and durations, binomial with a log link to get "
    "<b>relative risks</b> instead of odds ratios (may fail to converge because it does not bound μ above), "
    "and multiplicative hazards in survival models.<br><br>"
    "Assumption to check: linearity of log μ in the covariates - i.e. that the effect is a constant "
    "<b>percentage</b> per unit, not a constant amount.",
    f"{T} log-link multiplicative offset relative-risk")

txt("Why does the cloglog link have a mechanism behind it, and when should you use it?",
    "Suppose an event happens as soon as at least one of many independent 'hits' occurs, with the number of "
    "hits Poisson with rate λ. Then<br><br>"
    "\\[ P(Y=1)=1-e^{-\\lambda}\\quad\\Longleftrightarrow\\quad \\log(-\\log(1-\\mu))=\\log\\lambda \\]<br><br>"
    "So a log-linear model for the <b>underlying rate</b> is exactly a cloglog model for the "
    "<b>binary indicator</b>. That gives it two properties no symmetric link has:<br><br>"
    "1. <b>Proportional hazards</b>: in discrete-time survival, a cloglog GLM on person-period data is the "
    "grouped-time version of the Cox model, so its coefficients are log hazard ratios and are comparable "
    "with a Cox fit.<br>"
    "2. <b>Asymmetry</b>: it approaches 1 much faster than 0, which fits saturating processes.<br><br>"
    "Use it for: infection or failure after repeated exposures, dose-response and toxicology where "
    "one 'success' suffices, presence-absence data derived from an underlying intensity (species "
    "occupancy, defect detection), discrete-time survival and interval-censored data, and any binary "
    "outcome that is really a thresholded count.<br><br>"
    "The mirror image (`loglog`) is the right choice when the <b>lower</b> tail is the one that saturates. "
    "The Aranda-Ordaz family embeds logit and cloglog in one parametric family so that the asymmetry can be "
    "estimated rather than assumed.",
    f"{T} cloglog proportional-hazards latent-poisson")

txt("What latent-variable story sits behind the logit and probit links?",
    "Assume an unobserved continuous quantity - propensity, utility, tolerance, damage - and an event that "
    "occurs when it crosses a threshold:<br><br>"
    "\\[ Y^*=x^\\top\\beta+\\varepsilon,\\qquad Y=\\mathbb 1\\{Y^*>0\\} \\]<br><br>"
    "- \\(\\varepsilon\\) <b>logistic</b> → <b>logit</b> model.<br>"
    "- \\(\\varepsilon\\) <b>normal</b> → <b>probit</b> model.<br>"
    "- \\(\\varepsilon\\) <b>Gumbel</b> and a choice among alternatives → <b>multinomial logit / softmax</b>.<br><br>"
    "Why this is worth knowing:<br>"
    "- it explains the arbitrary scale: the latent variance is not identified, so coefficients are only "
    "defined up to scale - hence the ≈ 1.7 factor between logit and probit, and hence why you cannot compare "
    "raw coefficients across models with different sets of covariates (the implicit rescaling changes);<br>"
    "- it generates <b>ordinal</b> models directly by putting several thresholds on the same latent scale "
    "(ordered logit = proportional odds, ordered probit = threshold model);<br>"
    "- it is the natural framing for tolerance distributions in bioassay (the LD50 is the dose at which the "
    "median tolerance is exceeded), for item response theory, and for random-utility models in "
    "economics.",
    f"{T} latent-variable threshold logit probit utility")

txt("When are the inverse and inverse-square links used?",
    "They are the canonical links for the Gamma and inverse Gaussian, and they encode a <b>reciprocal</b> "
    "relationship: the covariate acts additively on 1/μ rather than on μ.<br><br>"
    "The mechanism is <b>saturation</b>. If \\(1/\\mu=a+b/x\\), then μ rises with x toward an asymptote - "
    "exactly the Michaelis-Menten form of enzyme kinetics, and the same shape as Holling's functional "
    "response in ecology or a hyperbolic dose-response. Fitting a Gamma GLM with an inverse link is the "
    "linear way to estimate such a curve.<br><br>"
    "Also natural whenever the response is a <b>rate and the predictor acts on its reciprocal</b>: time = "
    "distance / speed, so covariates that act linearly on speed act on 1/time; or a queueing delay as a "
    "function of the service rate.<br><br>"
    "Caution: neither link constrains μ to stay positive, so fitted values can cross zero and produce "
    "impossible predictions or convergence failure. That is why the log link is the pragmatic default for "
    "Gamma models unless the reciprocal has a scientific meaning.",
    f"{T} inverse-link gamma michaelis-menten saturation")

txt("When is a square-root or other power link used?",
    "- <b>Square root with a Poisson</b>: it is the <b>variance-stabilising</b> transformation for counts "
    "(\\(\\sqrt{Y}\\) has roughly constant variance), and it makes sense when effects add on the sqrt "
    "scale - notably in spatial and area-based counts, and in some ecological abundance models. Like the "
    "identity, it does not force μ ≥ 0 for all β.<br>"
    "- <b>General power link</b> \\(\\mu^{\\lambda}\\) (with λ = 0 read as the log): the family that "
    "contains identity (λ = 1), square root (½), log (0) and inverse (-1). Fitting λ - or comparing a few "
    "values by deviance - is a data-driven way to <b>choose</b> the link instead of assuming it.<br>"
    "- <b>Tweedie models</b> use a power link together with a power variance function \\(\\mu^p\\); the two "
    "powers do different jobs and should not be confused.<br>"
    "- <b>Box-Cox</b> is the same idea applied to the <b>response</b> rather than the mean, with the "
    "Jensen-inequality problems that entails.<br><br>"
    "General rule: pick the link for interpretability and for the mechanism first, and only tune the power "
    "if the diagnostics (a partial-residual plot, or an added \\(\\hat\\eta^2\\) term coming out "
    "significant) say the scale is wrong.",
    f"{T} sqrt-link power-link box-cox variance-stabilising")

txt("Which link makes a natural-process claim, and what claim is it?",
    "The link is a statement about <b>how effects combine</b>:<br><br>"
    "- <b>identity</b> - effects <b>add</b> in the original units; no bounds, no scaling. Physical "
    "accumulation, additive contributions.<br>"
    "- <b>log</b> - effects <b>multiply</b>; constant percentage change. Growth, decay, rates, hazards, "
    "compounding, anything where 'twice as much' is the meaningful comparison.<br>"
    "- <b>logit</b> - effects add on the <b>log-odds</b> scale; symmetric saturation at both ends, "
    "sampling-invariant. Diffusion of adoption, dose-response with a symmetric tolerance distribution.<br>"
    "- <b>probit</b> - a <b>latent normal</b> crossing a threshold: many small additive influences plus a "
    "cutoff. Perception, tolerance, credit default as latent creditworthiness.<br>"
    "- <b>cloglog</b> - the event is a <b>hidden Poisson count reaching one</b>; proportional hazards, "
    "asymmetric saturation. Infection, failure, detection.<br>"
    "- <b>inverse</b> - the covariate acts on the <b>reciprocal</b>: saturating, hyperbolic mechanisms "
    "(enzyme kinetics, capacity constraints).<br>"
    "- <b>log link + log covariate</b> - a <b>power law</b>: scale-invariant, no characteristic size. "
    "Allometry, urban scaling, learning curves.<br><br>"
    "Which is why choosing a link is a modelling decision, not a technical one: you are choosing the shape "
    "of the mechanism, and the fit will usually not distinguish the candidates strongly in the middle of "
    "the data - only in the tails and in the extrapolations.",
    f"{T} link-choice mechanism interpretation")

txt("What is the difference between a power-law distribution and a power-law relationship?",
    "Two different statements that share a functional form and are constantly conflated.<br><br>"
    "- A <b>power-law distribution</b> is about one variable: \\(P(X>x)\\propto x^{-\\alpha}\\). It says "
    "the variable is heavy-tailed - city sizes, wealth, earthquake magnitudes. The consequence is about "
    "<b>extremes and moments</b>: means and variances may not exist, sample means are unstable, and the "
    "largest observation dominates.<br>"
    "- A <b>power-law relationship</b> is about two variables: \\(E[Y]=cx^{b}\\), i.e. a straight line on a "
    "log-log plot. It says the <b>elasticity is constant</b> - metabolic rate versus body mass, cost versus "
    "cumulative output. The consequence is about how y <b>responds</b> to x, and it says nothing about "
    "whether either variable is heavy-tailed.<br><br>"
    "Modelling: the first is a distributional assumption (Pareto, GPD, zeta / Zipf, extreme-value theory); "
    "the second is a mean-structure assumption (log link plus log covariate in a Gamma, lognormal or "
    "Poisson GLM).<br><br>"
    "They do interact: multiplicative growth processes tend to generate <b>both</b> - lognormal or "
    "power-law marginals <b>and</b> power-law relationships between the quantities involved - which is why "
    "the same mechanism (proportional growth, preferential attachment, scale invariance) keeps appearing in "
    "both discussions.",
    f"{T} power-law distinction heavy-tails elasticity")

txt("How do you check whether you picked the right link function?",
    "- <b>Partial residual / component-plus-residual plots</b> on the link scale: systematic curvature "
    "means either the link or the functional form of that covariate is wrong.<br>"
    "- <b>Fit a smooth instead</b>: replace the covariate with `s(x)` in a GAM. If the estimated smooth is "
    "essentially straight on the link scale, the link is fine.<br>"
    "- <b>Goodness-of-link test</b>: add \\(\\hat\\eta^2\\) (the squared linear predictor) as an extra "
    "covariate; if it is significant, the link is misspecified. This is the GLM version of the "
    "Pregibon / RESET idea.<br>"
    "- <b>Compare links by deviance or AIC</b> at the same family - links are not nested, but the "
    "comparison is legitimate since the response scale is unchanged.<br>"
    "- <b>Fit a flexible link family</b> (power link with estimated λ, Aranda-Ordaz for binary) and see "
    "whether the estimate is near your assumed value.<br>"
    "- <b>Plot observed against fitted</b> on the response scale and look for bias in the extremes.<br><br>"
    "Practical perspective: within the data range, different links usually fit almost equally well - "
    "the choice matters most for <b>extrapolation, tail predictions and interpretation</b>. So decide by "
    "mechanism and by which effect measure you need to report, and use the diagnostics to catch real "
    "misspecification rather than to pick a winner by a hair.",
    f"{T} link-diagnostics goodness-of-link model-checking")

txt("What is an offset, and how does it differ from a weight?",
    "An <b>offset</b> is a covariate whose coefficient is fixed at 1 on the link scale. Its standard use is "
    "to turn a count model into a <b>rate</b> model:<br><br>"
    "\\[ \\log\\mu_i=\\log t_i+x_i^\\top\\beta\\quad\\Longleftrightarrow\\quad "
    "\\log\\frac{\\mu_i}{t_i}=x_i^\\top\\beta \\]<br><br>"
    "with \\(t_i\\) the exposure - person-years, population at risk, area surveyed, time observed, number "
    "of trials. Note that it only makes sense with a <b>log</b> link, and that log(exposure) as a free "
    "covariate is a different (more flexible) model you can test against the offset version.<br><br>"
    "A <b>weight</b> changes how much each observation counts in the likelihood: prior weights for "
    "grouped/aggregated data (a binomial row representing n trials), known variance ratios in weighted "
    "least squares, or survey/inverse-probability weights.<br><br>"
    "The distinction in one line: the <b>offset scales the expected value</b>, the <b>weight scales the "
    "precision</b>. Using an offset where you needed weights (or vice versa) gives the wrong mean structure "
    "or the wrong standard errors respectively. Modelling a pre-computed ratio as the response instead of "
    "using an offset throws away the information about how many events each ratio was based on.",
    f"{T} offset weights rates exposure")

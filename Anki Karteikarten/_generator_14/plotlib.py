"""Minimal inline-SVG plotting for Anki cards.

Style matches the existing decks: single-line SVG, stroke/fill via currentColor so
it adapts to Anki night mode, accent fills at low opacity, no external assets.
"""
import math

FONT = ("-apple-system,'Segoe UI',Roboto,'Segoe UI Symbol','DejaVu Sans',"
        "'Noto Sans Symbols2','Arial Unicode MS',sans-serif")

# accent palette (same hues the other decks use)
C = {
    "blue":   "#3b82f6",
    "green":  "#10b981",
    "amber":  "#f59e0b",
    "violet": "#8b5cf6",
    "rose":   "#f43f5e",
    "cyan":   "#06b6d4",
    "slate":  "#64748b",
}


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def n(v):
    """Short number formatting for SVG coordinates."""
    return f"{v:.2f}".rstrip("0").rstrip(".")


class Canvas:
    def __init__(self, w=460, h=270, pad=(46, 14, 34, 16)):
        """pad = (left, right, bottom, top) of the data area inside the canvas."""
        self.w, self.h = w, h
        self.pl, self.pr, self.pb, self.pt = pad
        self.parts = []
        self.xlim = (0.0, 1.0)
        self.ylim = (0.0, 1.0)
        self._marker = False

    # ---- coordinate handling -------------------------------------------------
    def limits(self, xlim, ylim):
        self.xlim, self.ylim = xlim, ylim
        return self

    def X(self, x):
        a, b = self.xlim
        return self.pl + (x - a) / (b - a) * (self.w - self.pl - self.pr)

    def Y(self, y):
        a, b = self.ylim
        return (self.h - self.pb) - (y - a) / (b - a) * (self.h - self.pb - self.pt)

    # ---- primitives ---------------------------------------------------------
    def raw(self, s):
        self.parts.append(s)
        return self

    def text(self, x, y, s, size=10, anchor="middle", opacity=1.0,
             weight="normal", color="currentColor", italic=False, data=True):
        px, py = (self.X(x), self.Y(y)) if data else (x, y)
        it = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{n(px)}" y="{n(py)}" font-size="{size}" text-anchor="{anchor}"'
            f' fill="{color}" fill-opacity="{opacity}" font-weight="{weight}"{it}'
            f' stroke="none">{esc(s)}</text>')
        return self

    def line(self, x1, y1, x2, y2, color="currentColor", width=1.5, dash=None,
             opacity=1.0, arrow=False, data=True):
        if data:
            x1, y1, x2, y2 = self.X(x1), self.Y(y1), self.X(x2), self.Y(y2)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = ' marker-end="url(#ah)"' if arrow else ""
        if arrow:
            self._marker = True
        self.parts.append(
            f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}"'
            f' stroke="{color}" stroke-width="{width}" stroke-opacity="{opacity}"{d}{a}/>')
        return self

    def rect(self, x, y, w, h, fill=None, fo=0.22, stroke="currentColor",
             width=1.0, opacity=1.0, rx=None, data=True):
        if data:
            X0, Y0 = self.X(x), self.Y(y + h)
            w = self.X(x + w) - X0
            h = self.Y(y) - Y0
            x, y = X0, Y0
        f = f'fill="{fill}" fill-opacity="{fo}"' if fill else 'fill="none"'
        s = f' stroke="{stroke}" stroke-width="{width}" stroke-opacity="{opacity}"' if stroke else ' stroke="none"'
        r = f' rx="{rx}"' if rx else ""
        self.parts.append(f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}"{r} {f}{s}/>')
        return self

    def circle(self, x, y, r=3, fill="currentColor", fo=1.0, stroke="none", data=True):
        px, py = (self.X(x), self.Y(y)) if data else (x, y)
        s = f' stroke="{stroke}" stroke-width="1.2"' if stroke != "none" else ' stroke="none"'
        self.parts.append(
            f'<circle cx="{n(px)}" cy="{n(py)}" r="{r}" fill="{fill}" fill-opacity="{fo}"{s}/>')
        return self

    def path(self, pts, color="currentColor", width=1.8, dash=None, opacity=1.0,
             fill=None, fo=0.16, close_to=None):
        """pts in data coords. close_to: y-value to close the polygon down to (area fill)."""
        d = "M" + " L".join(f"{n(self.X(x))},{n(self.Y(y))}" for x, y in pts)
        if fill is not None and close_to is not None:
            base = self.Y(close_to)
            area = d + f" L{n(self.X(pts[-1][0]))},{n(base)} L{n(self.X(pts[0][0]))},{n(base)} Z"
            self.parts.append(f'<path d="{area}" fill="{fill}" fill-opacity="{fo}" stroke="none"/>')
        da = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"'
            f' stroke-opacity="{opacity}"{da} stroke-linejoin="round" stroke-linecap="round"/>')
        return self

    # ---- axes ---------------------------------------------------------------
    def axes(self, xlabel="", ylabel="", xticks=(), yticks=(), xfmt=None, yfmt=None,
             y_axis=True, zero_y=None):
        x0, x1 = self.xlim
        y0 = self.ylim[0] if zero_y is None else zero_y
        self.line(x0, y0, x1, y0, width=1.2, opacity=0.85)
        if y_axis:
            self.line(x0, self.ylim[0], x0, self.ylim[1], width=1.2, opacity=0.85)
        f = xfmt or (lambda v: f"{v:g}")
        for t in xticks:
            self.line(t, y0, t, y0, width=1)
            self.raw(f'<line x1="{n(self.X(t))}" y1="{n(self.Y(y0))}" x2="{n(self.X(t))}"'
                     f' y2="{n(self.Y(y0) + 4)}" stroke="currentColor" stroke-width="1"'
                     f' stroke-opacity="0.85"/>')
            self.text(self.X(t), self.Y(y0) + 15, f(t), size=9, opacity=0.75, data=False)
        g = yfmt or (lambda v: f"{v:g}")
        for t in yticks:
            self.raw(f'<line x1="{n(self.X(x0))}" y1="{n(self.Y(t))}" x2="{n(self.X(x0) - 4)}"'
                     f' y2="{n(self.Y(t))}" stroke="currentColor" stroke-width="1"'
                     f' stroke-opacity="0.85"/>')
            self.text(self.X(x0) - 7, self.Y(t) + 3.4, g(t), size=9, opacity=0.75,
                      anchor="end", data=False)
        if xlabel:
            self.text((self.pl + self.w - self.pr) / 2, self.h - self.pb + 29, xlabel,
                      size=10, opacity=0.85, data=False)
        if ylabel:
            px, py = 13, (self.pt + self.h - self.pb) / 2
            self.parts.append(
                f'<text x="{n(px)}" y="{n(py)}" font-size="10" text-anchor="middle"'
                f' fill="currentColor" fill-opacity="0.85" stroke="none"'
                f' transform="rotate(-90 {n(px)} {n(py)})">{esc(ylabel)}</text>')
        return self

    def legend(self, items, x=None, y=None, size=9.5, dy=14):
        """items: list of (label, color) or (label, color, dash)."""
        px = self.w - self.pr - 6 if x is None else x
        py = self.pt + 12 if y is None else y
        for i, it in enumerate(items):
            label, color = it[0], it[1]
            dash = it[2] if len(it) > 2 else None
            yy = py + i * dy
            da = f' stroke-dasharray="{dash}"' if dash else ""
            self.parts.append(
                f'<line x1="{n(px - 24)}" y1="{n(yy - 3)}" x2="{n(px - 6)}" y2="{n(yy - 3)}"'
                f' stroke="{color}" stroke-width="2.4"{da}/>')
            self.text(px - 28, yy, label, size=size, anchor="end", opacity=0.9, data=False)
        return self

    def caption(self, lines, size=9.5, x=None, y0=None, opacity=0.72, anchor="start"):
        """Footnote lines under the x label. Grows the canvas so they always fit;
        the data area is untouched because h and pb grow together."""
        px = self.pl - 22 if x is None else x
        py = (self.h - self.pb) + 43 if y0 is None else y0
        need = int(math.ceil(py + 14 * (len(lines) - 1) + 8))
        if need > self.h:
            self.pb += need - self.h
            self.h = need
        for i, ln in enumerate(lines):
            self.text(px, py + i * 14, ln, size=size, anchor=anchor, opacity=opacity, data=False)
        return self

    # ---- output -------------------------------------------------------------
    def svg(self, maxwidth=520):
        marker = ('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5"'
                  ' markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
                  '<path d="M0,0 L10,5 L0,10 z" fill="currentColor" stroke="none"/>'
                  '</marker></defs>') if self._marker else ""
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}"'
                f' width="100%" style="max-width:{maxwidth}px;height:auto;font-family:{FONT}"'
                f' fill="none" stroke="currentColor" stroke-width="1.5">'
                + marker + "".join(self.parts) + "</svg>")


# ---------------------------------------------------------------------------
# high-level chart builders
# ---------------------------------------------------------------------------
def density_plot(curves, xlim, xlabel="x", ylabel="density", xticks=None,
                 caption=(), h=270, legend_pos=None, fill_first=True, ymax=None,
                 vlines=(), w=460):
    """curves: list of dicts {f, color, label, dash, fill}. f evaluated on xlim grid."""
    cv = Canvas(w=w, h=h)
    grid = [xlim[0] + (xlim[1] - xlim[0]) * i / 300 for i in range(301)]
    series = []
    for c in curves:
        pts = []
        for x in grid:
            try:
                y = c["f"](x)
            except (ValueError, ZeroDivisionError, OverflowError):
                continue
            if y is None or not math.isfinite(y):
                continue
            pts.append((x, y))
        series.append((c, pts))
    top = ymax if ymax else max(y for _, pts in series for _, y in pts) * 1.18
    cv.limits(xlim, (0, top))
    cv.axes(xlabel=xlabel, ylabel=ylabel,
            xticks=xticks if xticks is not None else _nice_ticks(xlim))
    for x, lbl in vlines:
        cv.line(x, 0, x, top * 0.92, color="currentColor", width=1, dash="3 3", opacity=0.5)
        if lbl:
            cv.text(x, top * 0.96, lbl, size=9, opacity=0.7)
    for i, (c, pts) in enumerate(series):
        fill = c.get("fill", C[c["color"]] if (fill_first and i == 0) else None)
        cv.path(pts, color=C[c["color"]], dash=c.get("dash"), fill=fill,
                close_to=0 if fill else None, fo=c.get("fo", 0.15))
    labels = [(c["label"], C[c["color"]], c.get("dash")) for c, _ in series if c.get("label")]
    if labels:
        cv.legend(labels, **(legend_pos or {}))
    if caption:
        cv.caption(caption)
    return cv


def pmf_plot(bars, xlim=None, xlabel="k", ylabel="P(X = k)", caption=(), h=270,
             legend_pos=None, w=460, xticks=None):
    """bars: list of dicts {pts:[(k,p)], color, label}. Drawn as stems + dots."""
    ks = [k for b in bars for k, _ in b["pts"]]
    xlim = xlim or (min(ks) - 0.8, max(ks) + 0.8)
    top = max(p for b in bars for _, p in b["pts"]) * 1.2
    cv = Canvas(w=w, h=h).limits(xlim, (0, top))
    if xticks is None:
        allk = sorted(set(ks))
        step = max(1, len(allk) // 12)
        xticks = allk[::step]
    cv.axes(xlabel=xlabel, ylabel=ylabel, xticks=xticks)
    single = len(bars) == 1
    for i, b in enumerate(bars):
        col = C[b["color"]]
        for k, p in b["pts"]:
            if single:
                width_data = (xlim[1] - xlim[0]) * 0.030
                cv.rect(k - width_data, 0, 2 * width_data, p, fill=col, fo=0.30,
                        stroke=col, width=1.1)
            else:
                cv.line(k, 0, k, p, color=col, width=1.6, opacity=0.75)
                cv.circle(k, p, r=2.6, fill=col)
    labels = [(b["label"], C[b["color"]]) for b in bars if b.get("label")]
    if labels:
        cv.legend(labels, **(legend_pos or {}))
    if caption:
        cv.caption(caption)
    return cv


def _nice_ticks(xlim, target=6):
    a, b = xlim
    span = b - a
    raw = span / target
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        if raw <= m * mag:
            step = m * mag
            break
    t0 = math.ceil(a / step) * step
    out, t = [], t0
    while t <= b + 1e-9:
        out.append(round(t, 10))
        t += step
    return out


# ---------------------------------------------------------------------------
# distributions (pure python, no scipy)
# ---------------------------------------------------------------------------
def lgamma(x):
    return math.lgamma(x)


def lbeta(a, b):
    return lgamma(a) + lgamma(b) - lgamma(a + b)


def lchoose(n_, k):
    if k < 0 or k > n_:
        return -math.inf
    return lgamma(n_ + 1) - lgamma(k + 1) - lgamma(n_ - k + 1)


def normal(x, mu=0.0, sd=1.0):
    z = (x - mu) / sd
    return math.exp(-0.5 * z * z) / (sd * math.sqrt(2 * math.pi))


def norm_cdf(x, mu=0.0, sd=1.0):
    return 0.5 * (1 + math.erf((x - mu) / (sd * math.sqrt(2))))


def lognormal(x, mu=0.0, sd=1.0):
    if x <= 0:
        return 0.0
    z = (math.log(x) - mu) / sd
    return math.exp(-0.5 * z * z) / (x * sd * math.sqrt(2 * math.pi))


def expon(x, rate=1.0):
    return rate * math.exp(-rate * x) if x >= 0 else 0.0


def gamma_pdf(x, shape, rate=1.0):
    if x <= 0:
        return 0.0 if shape >= 1 else None
    return math.exp(shape * math.log(rate) + (shape - 1) * math.log(x) - rate * x - lgamma(shape))


def chisq(x, df):
    return gamma_pdf(x, df / 2, 0.5)


def student_t(x, df):
    return math.exp(lgamma((df + 1) / 2) - lgamma(df / 2)) / math.sqrt(df * math.pi) * \
        (1 + x * x / df) ** (-(df + 1) / 2)


def f_pdf(x, d1, d2):
    if x <= 0:
        return 0.0
    return math.exp(0.5 * d1 * math.log(d1 / d2) + (0.5 * d1 - 1) * math.log(x)
                    - 0.5 * (d1 + d2) * math.log(1 + d1 * x / d2) - lbeta(d1 / 2, d2 / 2))


def beta_pdf(x, a, b):
    if x <= 0 or x >= 1:
        return 0.0 if (a > 1 and b > 1) else None
    return math.exp((a - 1) * math.log(x) + (b - 1) * math.log(1 - x) - lbeta(a, b))


def weibull(x, shape, scale=1.0):
    if x < 0:
        return 0.0
    if x == 0:
        return 0.0 if shape > 1 else None
    return (shape / scale) * (x / scale) ** (shape - 1) * math.exp(-(x / scale) ** shape)


def pareto(x, alpha, xm=1.0):
    return alpha * xm ** alpha / x ** (alpha + 1) if x >= xm else 0.0


def cauchy(x, loc=0.0, scale=1.0):
    return 1 / (math.pi * scale * (1 + ((x - loc) / scale) ** 2))


def laplace(x, loc=0.0, b=1.0):
    return math.exp(-abs(x - loc) / b) / (2 * b)


def logistic_pdf(x, loc=0.0, s=1.0):
    e = math.exp(-(x - loc) / s)
    return e / (s * (1 + e) ** 2)


def gumbel(x, loc=0.0, beta=1.0):
    z = (x - loc) / beta
    return math.exp(-(z + math.exp(-z))) / beta


def invgauss(x, mu=1.0, lam=1.0):
    if x <= 0:
        return 0.0
    return math.sqrt(lam / (2 * math.pi * x ** 3)) * math.exp(-lam * (x - mu) ** 2 / (2 * mu ** 2 * x))


def uniform_pdf(x, a=0.0, b=1.0):
    return 1 / (b - a) if a <= x <= b else 0.0


# discrete
def bern(k, p):
    return p if k == 1 else 1 - p


def binom(k, n_, p):
    if p == 0:
        return 1.0 if k == 0 else 0.0
    if p == 1:
        return 1.0 if k == n_ else 0.0
    return math.exp(lchoose(n_, k) + k * math.log(p) + (n_ - k) * math.log(1 - p))


def poisson(k, lam):
    return math.exp(-lam + k * math.log(lam) - lgamma(k + 1)) if lam > 0 else float(k == 0)


def geom(k, p):
    """support k = 1, 2, ... (number of trials until first success)"""
    return p * (1 - p) ** (k - 1)


def nbinom(k, r, p):
    """number of failures k before the r-th success"""
    return math.exp(lgamma(k + r) - lgamma(r) - lgamma(k + 1) + r * math.log(p) + k * math.log(1 - p))


def hyper(k, N, K, n_):
    lo = max(0, n_ - (N - K))
    if k < lo or k > min(n_, K):
        return 0.0
    return math.exp(lchoose(K, k) + lchoose(N - K, n_ - k) - lchoose(N, n_))


def betabinom(k, n_, a, b):
    return math.exp(lchoose(n_, k) + lbeta(k + a, n_ - k + b) - lbeta(a, b))


def zipf(k, s, kmax=60):
    Z = sum(1 / j ** s for j in range(1, kmax + 1))
    return 1 / (k ** s * Z)


def logseries(k, theta):
    return -theta ** k / (k * math.log(1 - theta))

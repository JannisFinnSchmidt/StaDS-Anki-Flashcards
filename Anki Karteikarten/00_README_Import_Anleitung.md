# Anki-Karteikarten aus allen Formelblättern (Bachelor + Master)

**1876 Karten** aus 13 Lernzetteln, alle auf Englisch, alle als Anki-Importdateien.
Davon **638 Karten mit gerenderten Formeln** und **42 Karten mit Schaubildern**.

## Import in Anki

1. Anki öffnen → **Datei → Importieren…**
2. Eine der `.txt`-Dateien auswählen
3. Alle Einstellungen stecken bereits in der Datei (Kopfzeilen `#separator:tab`,
   `#notetype:Basic`, `#deck:…`, `#tags column:3`) — du musst nichts umstellen,
   einfach auf **Importieren** klicken.
4. Für jede der 13 Dateien wiederholen.

Anki legt die Decks automatisch als Baum an:

```
Knowledge
├── Bachelor
│   ├── Selected Topics of Statistics
│   ├── Statistics 1 (Mathematical Statistics)
│   ├── Statistics 2 (Linear Models and GLM)
│   ├── Numerical Analysis
│   └── Ordinary Differential Equations
└── Master
    ├── Deep Learning
    ├── Supervised Learning
    ├── Optimization
    ├── Statistical Inference
    ├── Survival Analysis
    ├── Statistical Modelling
    ├── Deep Learning for NLP
    └── Regression for Correlated Data
```

Du kannst also gezielt ein Fach lernen oder über das Oberdeck `Knowledge` alles
gemischt wiederholen.

> Voraussetzung: Anki 2.1.55 oder neuer (wegen der Kopfzeilen-Direktiven). Bei einer
> älteren Version im Importdialog manuell einstellen: Feldtrenner **Tab**, Notiztyp
> **Basic**, Feld 1 → Vorderseite, Feld 2 → Rückseite, Feld 3 → Tags.

## Inhalt

| Datei | Fach | Karten | Formeln | Schaubilder |
|---|---|---:|---:|---:|
| `01_Selected_Topics_of_Statistics.txt` | Selected Topics of Statistics | 188 | 68 | – |
| `02_Statistik_1_Mathematical_Statistics.txt` | Statistik 1 | 143 | 64 | 1 |
| `03_Statistik_2_Linear_Models_and_GLM.txt` | Statistik 2 | 145 | 54 | 1 |
| `04_Numerik_Numerical_Analysis.txt` | Numerik | 105 | 55 | 2 |
| `05_Ordinary_Differential_Equations.txt` | Differentialgleichungen | 82 | 30 | – |
| `06_Deep_Learning.txt` | Deep Learning | 182 | 47 | 12 |
| `07_Supervised_Learning.txt` | Supervised Learning | 140 | 52 | 6 |
| `08_Optimization.txt` | Optimization | 161 | 48 | 4 |
| `09_Statistical_Inference.txt` | Statistical Inference | 118 | 41 | – |
| `10_Survival_Analysis.txt` | Survival Analysis | 127 | 42 | 5 |
| `11_Statistical_Modelling.txt` | Statistical Modelling | 184 | 62 | 3 |
| `12_DL4NLP_Deep_Learning_for_NLP.txt` | Deep Learning for NLP | 166 | 34 | 6 |
| `13_Regression_for_Correlated_Data.txt` | Regression for Correlated Data | 135 | 41 | 2 |
| | **Summe** | **1876** | **638** | **42** |

## Aufbau der Karten

Jede Zeile ist eine Karte mit drei Tab-getrennten Feldern:

```
Vorderseite <TAB> Rückseite <TAB> Tags
```

**Inhaltliches Prinzip:** Erst die Idee in Worten, dann — wo es hilft — die Formel.
Die Rückseiten sagen nicht nur *was* etwas ist, sondern möglichst auch *warum*.

### Formeln (638 Karten)

Formeln stehen als **MathJax** auf der Rückseite und werden von Anki nativ gerendert,
auch in AnkiDroid und AnkiMobile. Es ist **keine LaTeX-Installation nötig** — MathJax
ist in Anki eingebaut.

Aufgenommen ist, was man wirklich im Kopf haben sollte: Verteilungen, Schätzer,
Optimierungsalgorithmen (SGD, Momentum, AdaGrad, RMSProp, Adam, Newton, Gauss-Newton,
Fisher-Scoring), lineare Algebra (Normen, Konditionszahl, SVD, Cholesky, Spektralsatz),
Verlustfunktionen, Informationsmaße, Copulas, Hazard-/Survival-Beziehungen, Attention,
Mixed Models, GEE. Bewusst weggelassen sind lange Herleitungen und Beweisapparat.

### Schaubilder (42 Karten)

Die Diagramme sind als **inline-SVG** direkt in der Importdatei — du musst also keine
Bilddateien in `collection.media` kopieren, es funktioniert nach dem Import sofort.

Sie passen sich außerdem dem **Anki-Nachtmodus** an: Linien und Beschriftung nutzen
`currentColor` und übernehmen damit die Textfarbe, statt fest schwarz zu sein.

Abgedeckt sind unter anderem:

- **Deep Learning:** MLP, Convolution, CNN-Pipeline, Max-Pooling, RNN (gefaltet und
  ausgerollt), LSTM-Zelle, Autoencoder/VAE, ResNet-Block, U-Net, Aktivierungsfunktionen
  und Vanishing Gradient, Dropout, rezeptives Feld
- **NLP:** Transformer Encoder-Decoder, Self-Attention (Q/K/V), Attention-Masken
  (fully visible / causal / prefix), BERT vs. GPT, Skip-Gram vs. CBOW, Beam Search
- **Supervised Learning:** Bias-Varianz-Trade-off, L1- vs. L2-Geometrie, SVM-Margin,
  Regressions- und Klassifikationsverluste, Boosting
- **Optimization:** Zickzack bei schlechter Kondition, Sattelpunkt vs. Minimum,
  Newton- vs. Gradientenschritt, Pareto-Front
- **Survival:** Survival- und Hazard-Formen, Kaplan-Meier, Zensierung/Trunkierung,
  Multi-State-Modell, Proportional-Hazards-Annahme
- **Statistik:** Fehler 1./2. Art und Power, OLS als Projektion, DAG (Confounder /
  Mediator / Collider), B-Spline-Basis, Tail Dependence von Copulas,
  Random Intercept vs. Random Slope, Missing-Data-Mechanismen

### Tags

Jede Karte hat ein Fach-Tag plus Themen-Tags, z. B. `Survival cox partial-likelihood`
oder `DL transformer self-attention`. Damit kannst du gezielt filtern, etwa mit der
Suche `tag:copulas` über AKS und Statistical Modelling hinweg, oder `tag:diagram`
für alle Schaubilder.

## Hinweis zu Überschneidungen

22 Fragen kamen in zwei Fächern gleichzeitig vor (z. B. Copulas in Selected Topics
*und* Statistical Modelling, Adam/AdaGrad in Deep Learning *und* Optimization,
Cox-Modell in Survival *und* Statistical Modelling). Diese sind bewusst **beide**
enthalten, weil die Lernzettel sie unterschiedlich framen. Die zweite Variante trägt
einen Zusatz in Klammern, z. B. `What is a copula? (Statistical Modelling)` — sonst
würde Anki sie beim Import als Duplikat behandeln und die erste überschreiben.

## Lernempfehlung

Bei 1876 Karten lohnt es sich, nicht alles auf einmal freizuschalten. In den
Deck-Optionen das Limit für neue Karten pro Tag auf etwa 15–20 setzen und fachweise
anfangen — dann ist der gesamte Bestand in ein paar Monaten aufgebaut und die tägliche
Wiederholungslast bleibt im Rahmen.

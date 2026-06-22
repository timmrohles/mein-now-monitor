"""
Die Suchbegriffe, die täglich überwacht werden.

Aufgeteilt in:
- OUR_TARGETS: Begriffe, auf die unsere künftigen Modul-Titel zielen.
  Hier wollen wir wissen, wer aktuell rankt (Baseline vor Einreichung)
  und später, wo wir selbst landen.
- MARKET_WATCH: breitere Marktbegriffe, um Index-/Algo-Bewegungen
  früh zu erkennen (große Trefferzahlen reagieren empfindlich auf Änderungen).

Beim Hinzufügen: Begriff einfach in die Liste schreiben. Kurz halten
(1-4 Wörter), so wie ein Nutzer wirklich suchen würde.
"""

OUR_TARGETS = [
    # Modul 2 — Owned
    "Content Marketing",
    "KI Content Marketing",
    # Modul 3 — Shared
    "Social Media Marketing",
    "KI Social Media",
    # Modul 4 — Paid
    "Performance Marketing",
    "KI Performance Marketing",
    # Modul 5 — Tools
    "KI Automation",
    "Marketing Automation",
    # Modul 6 — E-Commerce
    "E-Commerce Marketing",
    "KI E-Commerce",
    # Modul 7 — B2B
    "B2B Vertrieb",
    "KI B2B Vertrieb",
    # Modul 1 / Dach
    "KI Marketing Manager",
    "KI Manager",
]

MARKET_WATCH = [
    # Große, empfindliche Begriffe — Frühwarnung für Index-/Algo-Bewegungen
    "KI",
    "Marketing",
    "KI Marketing",
    "Digital Marketing",
]

CONTROL_QUERIES = [
    # These „Wortreihenfolge ist egal" — Vergleich mit "KI Marketing" (in MARKET_WATCH).
    # Wenn total_results und Top-10 identisch sind, ist die Reihenfolge tatsächlich egal.
    "Marketing KI",
    # These „Klammern werden ignoriert" — gleiche Vergleichsbasis "KI Marketing".
    # Wenn identisch zu "KI Marketing", werden Klammern wie nicht vorhanden behandelt.
    "(KI) Marketing",
]

OUR_TITLES = [
    # Geplante eigene Modul-Titel (noch nicht im Index). Baseline jetzt
    # gegen die heutigen Treffer — sobald eingereicht, sehen wir hier
    # direkt, wo unser eigener Eintrag für die exakte Titel-Suche landet.
    "Marketing Manager mit KI: Agenten und Automatisierung",
    "Content Marketing und Content Automatisierung mit KI",
    "Social Media Marketing und Social Media Automatisierung mit KI",
    "Performance Marketing und Ads-Automatisierung mit KI",
    "Marketing-Automation Manager: Pipelines, MCP und Workflows mit KI",
    "E-Commerce Marketing und E-Commerce Automatisierung mit KI",
    "B2B Vertrieb und Sales-Automatisierung mit KI",
]

TRIPLE_PATTERN_QUERIES = [
    # HECKER-Stil: Topic + (Topic-Fachfrau / Topic-Fachmann) — bringt das
    # distinktive Kernwort 3× im Titel unter. Diese Queries dienen zwei Zwecken:
    # 1) Aufklärung — welche Anbieter nutzen das Tripple-Muster schon?
    # 2) Wenn wir später selbst eine Variante mit diesem Muster einreichen,
    #    haben wir die Vorher-Nachher-Baseline.
    "KI-Marketing-Manager (KI-Marketing-Fachfrau / KI-Marketing-Fachmann)",
    "Content Marketing (Content Marketing Fachfrau / Content Marketing Fachmann)",
    "Social Media Marketing (Social Media Fachfrau / Social Media Fachmann)",
    "Performance Marketing (Performance Marketing Fachfrau / Performance Marketing Fachmann)",
    "Marketing Automation (Marketing Automation Fachfrau / Marketing Automation Fachmann)",
    "E-Commerce Marketing (E-Commerce Fachfrau / E-Commerce Fachmann)",
    "B2B Vertrieb (B2B Sales Fachfrau / B2B Sales Fachmann)",
]

PROPOSED_VARIANTS = [
    # Variant-Vorschläge zu OUR_TITLES, die in den Strategie-Diskussionen
    # entstanden sind. Wir monitoren sie als Queries, um zu sehen, wer
    # heute für diese exakten Wort-Kombinationen rankt — und um eine
    # saubere Vorher-Nachher-Baseline zu haben, falls wir tatsächlich
    # eine Variante einreichen.
    #
    # M1: KI 3× über Bindestriche, statt einfaches "mit KI"-Suffix —
    # adressiert das LOSE-Verdict bei "KI Marketing Manager" (heutiger
    # Top1 verdoppelt "Manager", unser Original verdoppelt nichts).
    "KI-Marketing-Manager: KI-Agenten und KI-Automatisierung",
    # M5: Tripple-Variante OHNE MCP (das ohnehin von der Engine gedroppt
    # wird), sauber im HECKER-Stil. Marketing Automation 3×.
    "Marketing Automation Manager (Marketing Automation Fachfrau / Marketing Automation Fachmann)",
    # M7: Tripple-Variante mit "B2B Vertrieb" 3× plus "KI" 1×. Kombiniert
    # die Modul-Disziplin mit dem KI-Anker.
    "B2B Vertrieb mit KI (B2B Vertrieb Fachfrau / B2B Vertrieb Fachmann)",
]

# Wie viele Plätze pro Begriff protokolliert werden
TOP_N = 20

ALL_QUERIES = (
    OUR_TARGETS
    + MARKET_WATCH
    + CONTROL_QUERIES
    + OUR_TITLES
    + TRIPLE_PATTERN_QUERIES
    + PROPOSED_VARIANTS
)

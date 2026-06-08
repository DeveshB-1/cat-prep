#!/usr/bin/env python3
"""
CAT Flashcard Popper
Usage:
    python flashcards.py              # quant formulas, every 60s
    python flashcards.py 30           # every 30 seconds
    python flashcards.py 60 vocab     # vocabulary only
    python flashcards.py 60 all       # quant + vocab mixed
"""

import sys
import random
import json
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor, QPalette

FLASHCARDS = [
    # --- AVERAGE ---
    ("Average", "Average = Sum of Items / Number of Items"),
    ("Average", "Average speed (equal distances at u, v)\n= 2uv / (u + v)"),
    ("Average", "Weighted Average\n= (a₁x₁ + a₂x₂ + … + aₙxₙ)\n  / (a₁ + a₂ + … + aₙ)"),

    # --- PERCENTAGE ---
    ("Percentage", "A is R% more than B\n→ B is less than A by R/(100+R) × 100 %"),
    ("Percentage", "A is R% less than B\n→ B is more than A by R/(100−R) × 100 %"),
    ("Percentage", "Increase R% then decrease R%\n→ Net decrease = R²/100 %"),
    ("Percentage", "Successive changes X% and Y%\n→ Net = X + Y + XY/100 %"),
    ("Percentage", "Price ↑ R% → cut consumption by 100R/(100+R) %\nPrice ↓ R% → raise consumption by 100R/(100−R) %"),
    ("Percentage", "Fraction → %  (memorise these)\n1/3=33.33%  1/4=25%  1/5=20%\n1/6=16.67% 1/7=14.28% 1/8=12.5%\n1/9=11.11% 1/11=9.09% 1/12=8.33%"),

    # --- SI & CI ---
    ("SI & CI", "SI = P×R×T / 100\nAmount = P + SI"),
    ("SI & CI", "CI: A = P(1 + R/100)ⁿ\nHalf-yearly: A = P(1 + R/200)²ⁿ\nQuarterly:   A = P(1 + R/400)⁴ⁿ"),
    ("SI & CI", "Rule of 72:  doubling time ≈ 72/R   (CI)\nRule of 69:  doubling time ≈ 0.35 + 69/R"),
    ("SI & CI", "CI − SI for 2 years = P(R/100)²"),

    # --- PROFIT & LOSS ---
    ("Profit & Loss", "Profit% = 100×Profit/CP\nLoss%   = 100×Loss/CP\nDiscount% = 100×Discount/MP"),
    ("Profit & Loss", "Two items sold at same SP, one +p% one −p%\n→ Always a LOSS of p²/100 %"),
    ("Profit & Loss", "Successive discounts a% and b%\n→ Effective discount = a + b − ab/100 %"),
    ("Profit & Loss", "Buy x get y free\n→ Discount% = y/(x+y) × 100"),
    ("Profit & Loss", "Wrong weight profit%\n= 100 × Error / (True Weight − Error)"),
    ("Profit & Loss", "CP of x articles = SP of y articles\n→ Profit% = (x−y)/y × 100"),

    # --- RATIO ---
    ("Ratio & Proportion", "Componendo-Dividendo:\na/b = c/d  ⟹  (a+b)/(a−b) = (c+d)/(c−d)"),
    ("Ratio & Proportion", "If a/b = c/d = e/f\n→ Each ratio = (a+c+e)/(b+d+f)"),
    ("Ratio & Proportion", "Duplicate ratio a:b  →  a²:b²\nTriplicate         →  a³:b³\nSub-duplicate      →  √a:√b"),
    ("Ratio & Proportion", "Mean proportional b of a & c:\nb = √(ac)   i.e. b² = ac"),

    # --- ALLIGATION ---
    ("Alligation", "Alligation rule:\n(Qty cheaper)/(Qty dearer)\n= (Dearer − Mean)/(Mean − Cheaper)"),
    ("Alligation", "Repeated dilution (remove n from m, t times):\nOriginal liquid left = m × (1 − n/m)ᵗ"),

    # --- TIME & WORK ---
    ("Time & Work", "A in a hrs, B in b hrs → together:\nTime = ab/(a+b)"),
    ("Time & Work", "A, B, C together:\nTime = abc / (ab+bc+ca)"),
    ("Time & Work", "A takes a hrs MORE than (A+B)\nB takes b hrs MORE than (A+B)\n→ Together = √(ab)"),
    ("Time & Work", "MDH Formula:\nM₁D₁H₁/W₁ = M₂D₂H₂/W₂"),

    # --- TSD ---
    ("TSD", "Avg speed (equal distances at a, b)\n= 2ab/(a+b)"),
    ("TSD", "Same dir: Relative speed = |a−b|\nOpp. dir: Relative speed = a+b"),
    ("TSD", "After crossing: S₁/S₂ = √(T₂/T₁)\n(T₁, T₂ = time each takes after meeting)"),
    ("TSD", "Train across pole:     time = L/S\nTrain across platform: time = (L₁+L₂)/S\nTwo trains opp. dir:   time = (L₁+L₂)/(S₁+S₂)"),
    ("TSD", "Boats:\nDownstream = B+W;  Upstream = B−W\nB = (D+U)/2;  W = (D−U)/2"),
    ("TSD", "1 km/hr = 5/18 m/s\n1 m/s = 18/5 km/hr"),
    ("TSD", "Circular track (same dir): meet every L/|sA−sB|\nOpposite dir: meet every L/(sA+sB)\nMeeting points: |x−y| same;  x+y opposite\n(x:y = speed ratio in lowest terms)"),

    # --- ALGEBRA ---
    ("Algebra", "a³+b³ = (a+b)(a²−ab+b²)\na³−b³ = (a−b)(a²+ab+b²)\nIf a+b+c=0 → a³+b³+c³ = 3abc"),
    ("Algebra", "xⁿ+yⁿ divisible by x+y  when n is ODD\nxⁿ−yⁿ divisible by x+y  when n is EVEN\nxⁿ−yⁿ always divisible by x−y"),
    ("Algebra", "Quadratic ax²+bx+c=0:\nD = b²−4ac\nRoots = (−b ± √D) / 2a\nSum = −b/a;  Product = c/a"),
    ("Algebra", "f(x) = ax²+bx+c\nMin/max value = −D/4a  at  x = −b/2a\n(min if a>0,  max if a<0)"),
    ("Algebra", "Two linear eqs A₁x+B₁y=C₁, A₂x+B₂y=C₂:\nUnique:    A₁/A₂ ≠ B₁/B₂\nInfinite:  A₁/A₂ = B₁/B₂ = C₁/C₂\nNo soln:   A₁/A₂ = B₁/B₂ ≠ C₁/C₂"),
    ("Inequalities", "AM ≥ GM:\n(a+b)/2 ≥ √(ab)   [equality iff a=b]\na + 1/a ≥ 2  for a > 0"),
    ("Inequalities", "|x| < a  →  −a < x < a\n|x| > a  →  x<−a  or  x>a\n|a+b| ≤ |a|+|b|"),

    # --- AP / GP ---
    ("AP & GP", "AP nth term: Tₙ = a+(n−1)d\nSum: Sₙ = n/2·[2a+(n−1)d] = n/2·(a+l)\nAM of a,c: b = (a+c)/2"),
    ("AP & GP", "GP nth term: Tₙ = ar^(n−1)\nSₙ = a(rⁿ−1)/(r−1)\nS∞ = a/(1−r)  for |r|<1"),
    ("AP & GP", "Σn  = n(n+1)/2\nΣn² = n(n+1)(2n+1)/6\nΣn³ = [n(n+1)/2]²"),

    # --- LOGARITHMS ---
    ("Logarithms", "log(xy)=logx+logy\nlog(x/y)=logx−logy\nlog(xⁿ)=n·logx"),
    ("Logarithms", "Change of base: log_x y = log_m y / log_m x\nlog_a b × log_b a = 1\nb^(log_b x) = x"),
    ("Logarithms", "Number of digits in N\n= ⌊log₁₀(N)⌋ + 1\n(i.e. characteristic + 1)"),

    # --- P & C ---
    ("P & C", "nPr = n!/(n−r)!   [order matters]\nnCr = n!/[r!(n−r)!]  [order doesn't]\nnPr = nCr × r!"),
    ("P & C", "Circular permutations = (n−1)!\nWith repetition: rⁿ\nnC₀+nC₁+…+nCₙ = 2ⁿ"),
    ("P & C", "Non-negative int. solutions of x₁+…+xᵣ=n\n→ ⁿ⁺ʳ⁻¹Cᵣ₋₁\nPositive int. solutions → ⁿ⁻¹Cᵣ₋₁"),
    ("P & C", "Derangement Dₙ:\n= n!·[1 − 1/1! + 1/2! − 1/3! + … + (−1)ⁿ/n!]"),

    # --- PROBABILITY ---
    ("Probability", "P(A) = Favourable/Total\nP(A') = 1−P(A)\nP(A∪B) = P(A)+P(B)−P(A∩B)"),
    ("Probability", "Independent: P(A∩B) = P(A)×P(B)\nMutually excl.: P(A∩B) = 0\nConditional: P(A|B) = P(A∩B)/P(B)"),
    ("Probability", "Binomial (r successes in n trials):\nP = nCr × pʳ × (1−p)^(n−r)"),

    # --- NUMBER SYSTEM ---
    ("Number System", "Divisibility:\n÷3:  digit sum ÷ 3\n÷4:  last 2 digits ÷ 4\n÷8:  last 3 digits ÷ 8\n÷9:  digit sum ÷ 9\n÷11: alt. digit diff = 0 or mult of 11"),
    ("Number System", "LCM of fractions = LCM(num)/HCF(den)\nHCF of fractions = HCF(num)/LCM(den)\nHCF × LCM = product of two numbers"),
    ("Number System", "Euler number E(N):\nN = pᵃqᵇrᶜ…\nE(N) = N×(1−1/p)(1−1/q)(1−1/r)…\nRemainder of M^E(N) ÷ N = 1  (gcd=1)"),
    ("Number System", "Wilson's theorem (p = prime):\n(p−1)! mod p = p−1\n(p−2)! mod p = 1"),
    ("Number System", "25 primes ≤ 100:\n2 3 5 7 11 13 17 19 23 29\n31 37 41 43 47 53 59 61 67\n71 73 79 83 89 97"),

    # --- GEOMETRY ---
    ("Geometry – Triangles", "Area = ½bh = √[s(s−a)(s−b)(s−c)]\n     = r·s = abc/4R\nr = Area/s;  R = abc/(4·Area)"),
    ("Geometry – Triangles", "∠BIC = 90 + A/2  (I = incenter)\n∠BOC = 2A       (O = circumcenter)\nCentroid divides median in 2:1"),
    ("Geometry – Triangles", "Equilateral side a:\nHeight = (√3/2)a\nArea   = (√3/4)a²\nr = a/(2√3);  R = a/√3"),
    ("Geometry – Triangles", "Pythagorean triplets:\n(3,4,5) (5,12,13) (7,24,25)\n(8,15,17) (9,40,41) (20,21,29)\n(multiples of these also work)"),
    ("Geometry – Triangles", "30-60-90:  1 : √3 : 2\n45-45-90:  1 :  1 : √2"),
    ("Geometry – Circles", "Arc length = 2πr·θ/360\nSector area = πr²·θ/360\nTangent ⊥ radius at contact point\n2 tangents from external pt are equal"),
    ("Geometry – Circles", "Intersecting chords inside:\nPA·PB = PC·PD\nTangent-secant from outside:\nPA·PB = PT²"),
    ("Geometry – Quads", "Rhombus: area = ½d₁d₂;  d₁²+d₂² = 4a²\nTrapezium: area = ½(a+b)h\nCyclic quad: area = √[(s−a)(s−b)(s−c)(s−d)]"),
    ("Geometry – Polygons", "Interior angle sum = (n−2)×180°\nEach angle (regular) = (n−2)×180/n\nDiagonals = n(n−3)/2\nExterior angle sum = 360°"),

    # --- 3D ---
    ("3D Solids", "Cylinder: V=πr²h; CSA=2πrh\nCone:     V=⅓πr²h; CSA=πrl; l=√(r²+h²)\nSphere:   V=⁴⁄₃πr³; SA=4πr²"),
    ("3D Solids", "Cuboid: V=lbh; diagonal=√(l²+b²+h²)\nCube:   V=a³; SA=6a²; diagonal=a√3\nFrustum V = πh/3·(R²+r²+Rr)"),

    # --- COORDINATE ---
    ("Coord. Geometry", "Distance = √[(x₂−x₁)²+(y₂−y₁)²]\nSlope m = (y₂−y₁)/(x₂−x₁)\nPerp. lines: m₁×m₂ = −1"),
    ("Coord. Geometry", "Section (m:n internal):\nx=(mx₂+nx₁)/(m+n); y=(my₂+ny₁)/(m+n)\nMidpoint: ((x₁+x₂)/2, (y₁+y₂)/2)"),

    # --- TRIG ---
    ("Trigonometry", "sin²θ+cos²θ = 1\n1+tan²θ  = sec²θ\n1+cot²θ  = cosec²θ"),
    ("Trigonometry", "sin(A±B) = sinA cosB ± cosA sinB\ncos(A±B) = cosA cosB ∓ sinA sinB\ntan(A+B) = (tanA+tanB)/(1−tanA tanB)"),
    ("Trigonometry", "Double angle:\nsin2x = 2sinx cosx\ncos2x = cos²x−sin²x = 1−2sin²x\ntan2x = 2tanx/(1−tan²x)"),
    ("Trigonometry", "ASTC (quadrant signs):\nQ1: All +\nQ2: Sin, Cosec +\nQ3: Tan, Cot +\nQ4: Cos, Sec +"),
    ("Trigonometry", "  θ    0°   30°   45°   60°  90°\nsin   0   1/2  1/√2  √3/2   1\ncos   1  √3/2  1/√2  1/2    0\ntan   0  1/√3   1    √3     ∞"),

    # --- CLOCKS ---
    ("Clocks & Calendars", "Minute hand: 6°/min\nHour hand:   0.5°/min\nRelative speed: 5.5°/min\nHands meet every 65 5/11 min"),
    ("Clocks & Calendars", "Coincide (0°):      11 times in 12 hrs\nRight angle (90°):  22 times in 12 hrs\nOpposite (180°):    11 times in 12 hrs"),
    ("Clocks & Calendars", "100 yrs = 5 odd days\n200 yrs = 3 odd days\n300 yrs = 1 odd day\n400 yrs = 0 odd days\nOdd days → 0=Sun 1=Mon … 6=Sat"),
]


class FlashCard(QWidget):
    def __init__(self, topic, content, card_num, total, on_close):
        super().__init__()
        self.on_close = on_close
        self._build_ui(topic, content, card_num, total)

    def _build_ui(self, topic, content, card_num, total):
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Position top-right
        screen = QApplication.primaryScreen().availableGeometry()
        self.setFixedWidth(420)
        self.move(screen.width() - 440, 40)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setObjectName("card")
        card.setStyleSheet("""
            QFrame#card {
                background-color: #1e1e2e;
                border-radius: 12px;
                border: 1px solid #313244;
            }
        """)
        outer.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(10)

        # Topic badge
        badge = QLabel(f"  {topic}  ")
        badge.setFont(QFont("Helvetica", 10, QFont.Weight.Bold))
        badge.setStyleSheet("""
            background-color: #7c3aed;
            color: white;
            border-radius: 4px;
            padding: 3px 8px;
        """)
        badge.setFixedHeight(26)
        badge.setSizePolicy(badge.sizePolicy().horizontalPolicy(),
                           badge.sizePolicy().verticalPolicy())

        badge_row = QHBoxLayout()
        badge_row.addWidget(badge)
        badge_row.addStretch()
        layout.addLayout(badge_row)

        # Formula content
        formula = QLabel(content)
        formula.setFont(QFont("Monospace", 12))
        formula.setStyleSheet("color: #e2e8f0; background: transparent;")
        formula.setWordWrap(True)
        formula.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(formula)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("color: #313244;")
        layout.addWidget(line)

        # Bottom row
        bottom = QHBoxLayout()

        counter = QLabel(f"{card_num}/{total}")
        counter.setFont(QFont("Helvetica", 9))
        counter.setStyleSheet("color: #64748b; background: transparent;")
        bottom.addWidget(counter)
        bottom.addStretch()

        btn_stop = QPushButton("Stop")
        btn_stop.setFont(QFont("Helvetica", 10))
        btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #374151; color: #9ca3af;
                border: none; border-radius: 6px;
                padding: 5px 14px;
            }
            QPushButton:hover { background-color: #4b5563; }
        """)
        btn_stop.clicked.connect(self._stop)
        bottom.addWidget(btn_stop)

        btn_ok = QPushButton("Got it ✓")
        btn_ok.setFont(QFont("Helvetica", 10, QFont.Weight.Bold))
        btn_ok.setStyleSheet("""
            QPushButton {
                background-color: #16a34a; color: white;
                border: none; border-radius: 6px;
                padding: 5px 14px;
            }
            QPushButton:hover { background-color: #15803d; }
        """)
        btn_ok.clicked.connect(self._done)
        bottom.addWidget(btn_ok)

        layout.addLayout(bottom)

        # Auto-dismiss after 45s
        self._auto = QTimer(self)
        self._auto.setSingleShot(True)
        self._auto.timeout.connect(self._done)
        self._auto.start(45000)

    def _done(self):
        self._auto.stop()
        self.close()
        self.on_close(stop=False)

    def _stop(self):
        self._auto.stop()
        self.close()
        self.on_close(stop=True)

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key.Key_Return, Qt.Key.Key_Space):
            self._done()
        elif e.key() == Qt.Key.Key_Escape:
            self._stop()


class FlashcardApp:
    def __init__(self, interval_sec, cards=None):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        self.interval = interval_sec * 1000  # ms
        self.cards = (cards if cards is not None else FLASHCARDS)[:]
        random.shuffle(self.cards)
        self.index = 0
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._show_card)
        self.timer.start(self.interval)
        print(f"First card in {interval_sec}s. Press Ctrl+C to quit.")

    def _show_card(self):
        topic, content = self.cards[self.index % len(self.cards)]
        self.index += 1
        if self.index % len(self.cards) == 0:
            random.shuffle(self.cards)
        card_num = ((self.index - 1) % len(self.cards)) + 1

        def on_close(stop):
            if stop:
                self.app.quit()
            else:
                self.timer.start(self.interval)

        self.card = FlashCard(topic, content, card_num, len(self.cards), on_close)
        self.card.show()
        self.card.activateWindow()

    def run(self):
        sys.exit(self.app.exec())


def load_vocab_cards():
    vocab_path = os.path.join(os.path.dirname(__file__), "vocab.json")
    if not os.path.exists(vocab_path):
        print("vocab.json not found, skipping vocab cards")
        return []
    with open(vocab_path) as f:
        words = json.load(f)
    cards = []
    for w in words:
        content = w['meaning'].strip()
        if w['syn']:
            content += f"\n\nSyn: {w['syn']}"
        if w['ant']:
            content += f"\nAnt: {w['ant']}"
        cards.append(("Vocab: " + w['word'], content))
    return cards


if __name__ == "__main__":
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    mode = sys.argv[2].lower() if len(sys.argv) > 2 else "quant"

    if mode == "vocab":
        cards = load_vocab_cards()
        print(f"Vocab mode: {len(cards)} words loaded")
    elif mode == "all":
        vocab = load_vocab_cards()
        cards = FLASHCARDS + vocab
        print(f"All mode: {len(FLASHCARDS)} quant + {len(vocab)} vocab = {len(cards)} cards")
    else:
        cards = FLASHCARDS
        print(f"Quant mode: {len(cards)} formula cards")

    FlashcardApp(interval, cards).run()

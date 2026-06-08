# CAT Prep

Flashcard popper + formula/vocab reference for CAT exam preparation.

## Contents

| File | Description |
|---|---|
| `flashcards.py` | Popup flashcard app (quant formulas + vocabulary) |
| `quant_formulas.md` | Complete CAT Quant formula sheet (18 topics) |
| `vocab.json` | 2874 vocabulary words with meanings, synonyms & antonyms |

---

## Requirements

```bash
pip install PyQt6
```

---

## Usage

### Quant Formulas (default)
```bash
python flashcards.py          # card every 60 seconds
python flashcards.py 30       # card every 30 seconds
python flashcards.py 120      # card every 2 minutes
```

### Vocabulary
```bash
python flashcards.py 60 vocab
```

### Both Mixed
```bash
python flashcards.py 60 all
```

### Run in background (doesn't block terminal)
```bash
python flashcards.py 60 &
python flashcards.py 60 vocab &
python flashcards.py 60 all &
```

---

## How it works

- A popup appears top-right of your screen at the set interval
- Shows **topic/word** and the **formula/meaning**
- **Got it ✓** — dismisses and schedules the next card
- **Stop** — quits the app
- Cards are shuffled randomly; cycles through all before repeating
- Auto-dismisses after 45 seconds if ignored

---

## Topics Covered

### Quant (18 topics)
Average · Percentage · SI & CI · Profit & Loss · Ratio & Proportion ·
Alligation & Mixture · Time & Work · Time Speed & Distance ·
Algebra · AP & GP · Logarithms · Permutation & Combination ·
Probability · Number System · Geometry & Mensuration ·
Coordinate Geometry · Trigonometry · Clocks & Calendars

### Vocabulary
2874 words from the Bodhee Prep CAT vocabulary list — each card shows:
- Word
- Meaning
- Synonyms
- Antonyms

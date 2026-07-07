# СЛО́ВО — Russian Trainer

A single-file, zero-dependency, offline-capable Russian learning app built around frequency-ranked word lists for CEFR levels A1–C2. Mobile-first (bottom nav, thumb-sized targets), works fine on desktop with keyboard shortcuts.

## Run it

Serve the folder with any local server (VS Code Live Server, or `python -m http.server`) and open `index.html`. After the first load it works fully offline (service worker). No CDNs, no build step — system fonts only.

## The four tabs

- **⚡ Learn** — spaced-repetition rounds of 10 cards (Leitner boxes: 4h → 1d → 3d → 7d → 16d → 35d). Only new and due words appear. New/shaky words get multiple choice (keys 1–4); words you know graduate to typed recall. Audio auto-plays for every card.
- **💬 Phrases** — comprehensible input. ~3,200 graded sentences (A1/A2/B1) pop in word-by-word with audio; tap any word for an instant dictionary lookup; reveal the translation, then Next = +3 XP. All sentences come from `tatoeba_sentences.json` — human-written [Tatoeba](https://tatoeba.org) sentence pairs (CC-BY 2.0 FR) filtered offline so each sentence only uses vocabulary from the frequency decks at that level (regenerate with a newer export any time using the same filter approach). Sentences containing your weak words (low Leitner box or due for review) are served first.
- **📖 Stories** — short graded readers. Every word is tappable (with smart stem matching for inflected forms). Finish a story for +15 XP (once per story per day). The **🌐 Random Wiki** chip pulls a random Russian Wikipedia intro (free API, needs internet) as untranslated "wild" reading — +5 XP per article.
- **🔍 Words** — searchable dictionary across all six decks, with per-word progress dots (gold = seen, green = learned).

## Progression

- +10 XP per correct card (x2 combo at 5 in a row, x3 at 10), +3 per phrase, +15 per story
- Daily goal: 150 XP (the ring in the header) — any mix of activities counts
- Hitting the goal on consecutive days builds the 🔥 streak
- Everything persists in localStorage

## Keyboard (desktop)

| Key | Action |
|---|---|
| 1–4 | Pick a multiple-choice answer |
| Enter | Submit typed answer / continue after a miss |
| V | Play audio (Learn and Phrases) |
| Space / → | Reveal / next phrase (Phrases tab) |
| Esc | Close the dictionary sheet |

## Design notes

The visual identity borrows from Russian lacquer miniature (Palekh): warm lacquer-black surfaces with a gold hairline inset, vermilion for actions, gold for rewards. Russian text is set in Georgia serif, and every stressed vowel is drawn in gold with an acute above it — the stress mark is rendered with CSS rather than the combining Unicode character, which Georgia spaces badly.

# Project notes: jazz tenor sax GA

Working notes for TP1 (Symbolic Music Generation, UFMG). Everything we used to build the genetic
algorithm: sources, music theory, instruments, training logic and experiment findings.

## 1. Assignment constraints

From the TP1 PDF (`tp1_geracao_musical_simbolica_1 (1).pdf`):

| Item | Requirement |
|---|---|
| Method | Genetic algorithm. Rule-based fitness is allowed, but every rule must be justified |
| Style | One style constraint must be applied |
| Experiments | At least one hyperparameter varied, 3 runs |
| Deliverables | Code, fitness graph, audio, 2-page ISMIR-style paper |
| AI use | Must be declared in the README with links to the conversations. Generating the whole method or the paper with AI is not allowed |

## 2. Style choice

- First idea was blues. We switched to **jazz over a fixed ii-V-I loop in C major**:
  `Dm7 | G7 | Cmaj7 | Cmaj7`, repeated for the whole melody.
- Instrument: **tenor sax**. The Weimar Jazz Database has 158 tenor solos against 80 alto solos, so
  the statistics we borrow from it are mostly tenor statistics.
- A fixed progression keeps the fitness simple: every bar has a known chord, so every rule can be
  checked bar by bar.

## 3. Sources

### 3.1 GA papers

| Source | What we took from it |
|---|---|
| Ozcan & Ercal (2007), "A Genetic Algorithm for Generating Improvised Music", Artificial Evolution (EA 2007), LNCS 4926, Springer, pp. 266-277, doi:10.1007/978-3-540-79305-2_23. PDF: https://people.cs.nott.ac.uk/pszeo/docs/publications/amuse07.pdf | **Main model.** One integer per eighth note as the genotype; fitness as the equal-weight mean of several objectives; chord tones on strong beats. They evaluated with 36 students |
| Biles (1994), "GenJam: A Genetic Algorithm for Generating Jazz Solos", ICMC, pp. 131-137 | Contrast: GenJam uses a human (interactive) fitness. Ours is rule-based |
| Papadopoulos & Wiggins (1998), "A genetic algorithm for the generation of jazz melodies", STeP'98. https://researchportal.vub.be/en/publications/a-genetic-algorithm-for-the-generation-of-jazz-melodies/ | Rule-based fitness for jazz that sums 8 criteria |
| Horner & Goldberg (1991), "Genetic algorithms and computer-assisted music composition" | Early GA for music, background |
| Towsey et al. (2001), "Towards melodic extension using genetic algorithms". https://eprints.qut.edu.au/169/ | 21 melodic metrics usable as fitness features |
| Freitas, Guimaraes & Barbosa (2012), PPSN XII | GA for bossa nova melodies. Authors are from UFMG |

### 3.2 Jazz data and theory

| Source | What we took from it |
|---|---|
| Weimar Jazz Database / "Inside the Jazzomat" (Pfleiderer, Frieler et al., 2017). https://schott-campus.com/wp-content/uploads/2017/11/inside_the_jazzomat_final_rev_oa4.pdf. Download (ODbL): https://jazzomat.hfm-weimar.de/download/download.html | Average interval about 2.7 semitones; leaps above 7 semitones about 2.2%; repeated notes about 5%; chromatic runs about 8%; about 4.8 notes/s; median tempo 170 BPM |
| Corcoran & Frieler (2021), "Playing It Straight: Analyzing Jazz Soloists' Swing Eighth-Note Distributions with the Weimar Jazz Database", Music Perception 38(4). https://online.ucpress.edu/mp/article-abstract/38/4/372/116701/Playing-It-StraightAnalyzing-Jazz-Soloists-Swing | Median soloist swing ratio about 1.3:1 |
| Friberg & Sundstrom (2002), "Swing Ratios and Ensemble Timing in Jazz Performance", Music Perception 19(3) | Swing ratio depends on tempo: about 3.5:1 at slow tempos, close to 1:1 at fast tempos |
| Smither, Music Theory Online 25(2). https://mtosmt.org/issues/mto.19.25.2/mto.19.25.2.smither.html | Guide tones: the 3rd and 7th define the chord; the 7th resolves down a half step to the 3rd of the next chord |
| Bebop scale references (Wikipedia "Bebop scale", learnjazzstandards.com) | Passing tones are placed so chord tones land on the beat. Basis for the chord tone and chromatic rules |
| Mark Levine, *The Jazz Theory Book* | General theory reference (ii-V-I, chord scales). Chapter not checked yet |

### 3.3 Not verified yet

Check these before citing them in the paper:

1. DOIs of Biles (1994) and Papadopoulos & Wiggins (1998).
2. The exact 8 criteria of Papadopoulos & Wiggins (we did not read the full text).
3. The tenor sax range, which came only from search snippets (Wikipedia "Tenor saxophone").

## 4. Music representation

### 4.1 Genome

- A tuple of `bars * 8` integers, one per **eighth note**.
- Values are MIDI pitches **44 to 76** (Ab2 to E5, concert pitch, tenor sax range). `43` means **REST**.
- No HOLD symbol. `decode()` merges equal neighbours into one `Note(pitch, start, length)` and
  splits notes at bar lines, so a long note is just the same pitch repeated.

Differences from Ozcan & Ercal: they encode scale degrees plus rest and hold symbols. We use MIDI
pitches so chromatic notes are possible, and drop the hold symbol because merging equal neighbours
gives the same effect.

### 4.2 Harmony (`core/music.py`)

Pitches are compared by pitch class (`pitch % 12`). C major scale: `{0, 2, 4, 5, 7, 9, 11}`.

| Bar | Chord | Chord tones | Guide tones (3rd, 7th) |
|---|---|---|---|
| 1 | Dm7 | D F A C | F, C |
| 2 | G7 | G B D F | B, F |
| 3 | Cmaj7 | C E G B | E, B |
| 4 | Cmaj7 | C E G B | E, B |

## 5. Fitness

Fitness is the weighted mean of 5 rule scores, each between 0 and 1:

```
fitness = sum(score_i * weight_i) / sum(weights)
```

Default weights are all 1, so fitness also stays between 0 and 1.

| # | Rule | How it is scored | Justification |
|---|---|---|---|
| 1 | Breathing | Longest phrase without a rest should be at most `max_phrase_eighths` = 16 (2 bars). Linear penalty beyond that | A sax player has to breathe. The value 16 is our own choice |
| 2 | Step | Average of two parts. `step_score = max(0, 1 - abs(avg - 2.7) / 2.7)` where `avg` is the mean interval. `leap_score = 1 - max(0, share - 0.02) / 0.98` where `share` is the fraction of intervals above 7 semitones | Weimar data: 2.7 semitone average, about 2% leaps |
| 3 | Chord tone | Fraction of strong eighths (even positions) whose sounding note is in the bar's chord | Ozcan & Ercal; bebop scale logic |
| 4 | Chromatic | A note outside the C major scale counts as correct only if it starts off the beat and the next note is exactly 1 semitone away. Score is 1 if there are no outside notes | Chromatic approach notes in bebop; about 8% chromatic runs in Weimar data |
| 5 | Guide tone | At each chord change, the first note of the new bar should be its 3rd or 7th. A rest there is a miss | Smither (guide tone voice leading) |

Our own design choices (no source, must be declared as ours in the paper): the 16-eighth breath
limit, the exact formulas, equal weights, `walk_step` 3, the rest rate, and the mutation parameters.

## 6. GA training logic (`core/ga.py`)

1. **Initialization (random walk).** Start at a random pitch. For each eighth: with probability
   `rest_rate` write a REST, otherwise move the pitch by `randint(-walk_step, walk_step)` and clamp to
   44..76.
2. **Evaluation.** Decode every individual and compute the 5 scores and the fitness.
3. **Elitism.** The 2 best individuals pass unchanged.
4. **Selection (roulette).** `rng.choices` weighted by fitness picks 2 parents. If every fitness is 0
   it falls back to `rng.sample`.
5. **Crossover (single point, at a bar line).** Cut point is a random bar boundary; the two children
   swap tails.
6. **Mutation.** Each eighth mutates with probability `mutation_rate`:
   - with probability `rest_rate` it becomes a REST;
   - a REST becomes a random pitch;
   - otherwise the pitch moves by `randint(-mutation_step, mutation_step)`, clamped to the range.
7. Repeat steps 2 to 6 for `generations`. The sorted population of every generation is kept.

### Default config (`core/config.py`)

| Parameter | Value |
|---|---|
| seed | 42 |
| bars | 12 |
| population_size | 100 |
| generations | 4000 |
| elite_size | 2 |
| mutation_rate | 0.05 |
| mutation_step | 2 |
| rest_rate | 0.1 |
| walk_step | 3 |
| max_phrase_eighths | 16 |
| weights | (1, 1, 1, 1, 1) |

## 7. Output: instruments and audio

| Part | Value |
|---|---|
| Melody | General MIDI **Tenor Sax**, velocity 100 |
| Accompaniment | General MIDI **Acoustic Grand Piano**, velocity 60, one sustained chord per bar |
| Tempo | 170 BPM (Weimar median) |
| Swing | 1.3:1, applied only when writing the MIDI. The GA works on a straight grid |
| Audio | FluidSynth CLI, GeneralUser GS SoundFont at `~/soundfonts/GeneralUser-GS.sf2` (override with `SOUNDFONT`), 44100 Hz |

Piano voicings (`output/midi.py`), root position, close voicing:

| Chord | MIDI | Notes |
|---|---|---|
| Dm7 | 50 53 57 60 | D3 F3 A3 C4 |
| G7 | 55 59 62 65 | G3 B3 D4 F4 |
| Cmaj7 | 48 52 55 59 | C3 E3 G3 B3 |

Swing timing: an off-beat eighth starts at `beat * ratio / (1 + ratio)` into the beat, so with 1.3
the first eighth gets about 57% of the beat.

## 8. Experiments and findings

### 8.1 Step score plateau (fixed)

| Attempt | Result |
|---|---|
| Uniform random initialization | Average interval about 9 semitones. Step score stuck at about 0.29, because a mutation of +-2 cannot fix intervals that large |
| Larger population | Did not help |
| Smoother step score formula | Did not help |
| **Random-walk initialization** | Fixed it. Step score reaches 0.99 |

### 8.2 Default run (seed 42)

| Generation | Fitness | Scores [breath, step, chord, chromatic, guide] |
|---|---|---|
| 0 | 0.568 | [0.88, 0.84, 0.40, 0.26, 0.45] |
| 999 | 0.873 | |
| 1999 | 0.907 | |
| 2999 | 0.923 | |
| 3999 | 0.935 | [1.00, 0.99, 0.87, 1.00, 0.82] |

A run takes about 29 s and about 20 MB on disk.

### 8.3 Earlier bug

A mutated REST used to become MIDI 44 or 45 most of the time, so the melody piled up at the bottom
of the range. Fixed in commit `73ddbfd` (a REST now becomes a uniform random pitch).

## 9. How to run

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
brew install fluid-synth
python run.py default
```

- Homebrew `python3` blocks global `pip install` (PEP 668), so use the venv. Do not use
  `--break-system-packages`.
- On macOS, multiprocessing uses spawn, so any script that uses it needs an
  `if __name__ == "__main__":` guard.

Output in `runs/<name>/`:

| File | Content |
|---|---|
| `config.json` | Config used |
| `history.json` | Best individual of each generation: notes, fitness, scores |
| `midi/gen_XXXX.mid`, `audio/gen_XXXX.wav` | Generations 0, 999, 1999, 2999, 3999 |

## 10. Open issues and remaining work

1. Guide tone score stays at 0.82 from about generation 999 on.
2. Fitness graph (max and mean per generation). `history.json` only stores the best individual, so
   the mean needs to be saved too.
3. Three runs varying one hyperparameter. Suggested: chord tone weight against chromatic weight.
4. The 2-page ISMIR-style paper.
5. AI-use declaration in the README with links to the conversations.

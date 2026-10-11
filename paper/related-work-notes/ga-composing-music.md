# A Genetic Algorithm for Composing Music

- url: https://yujor.fon.bg.ac.rs/index.php/yujor/article/download/291/285
- cite: \cite{matic2010}
- Dragan Matic, Yugoslav Journal of Operations Research, 2010

## Introduction

- GA that composes short melodies (four 4/4 bars) automatically, without human feedback
- interactive GAs (like GenJam) suffer from subjectivity and the "fitness bottleneck": a human has to listen to every candidate
- automatic fitness removes the human, but music rules must be mapped to numbers

## Methodology

- genome: one array of numbers, one slot per "shortest length" (an eighth note in the tests)
- 0 = rest, 1 to n = pitch (relative to a reference pitch), n+1 = hold the previous note
- initial population copies the rhythm of a reference melody (optional)
- fitness is minimized (0 = best), computed bar by bar as a weighted sum:
  - how "good" each interval is (perfect consonances get the best score)
  - mean and variance of the intervals in each bar, compared with reference values
  - penalty for notes outside the key (G major by default)
- no crossover: the pieces are short, so only three mutations are used
  - move a note by an octave, change one note, swap two neighbor notes
- selection: the best third is mutated many times, duplicates are removed, the worst are dropped
- no explicit elitism, but mutations change only two intervals, so good individuals survive

## Results

- population of about 30, 100 generations are enough for good (often optimal) solutions
- the GA tends to produce many rests, because rests avoid bad intervals
- the results sound more like improvisations than composed melodies
- many parameters change the style a lot (e.g. favoring seconds gives stepwise melodies)
- presented with simple chords and drums added by the author

## Conclusions

- the array encoding makes it easy to control pitch and rhythm with math
- reference values help to get rhythmic and harmonious results
- future work: other metaheuristics, and tuning parameters for a specific genre

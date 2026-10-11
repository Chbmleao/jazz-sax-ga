# GenJam: An Interactive Genetic Algorithm Jazz Improviser

- url: https://genjam.org/wp-content/uploads/2019/07/genjamasa97.pdf
- cite: \cite{biles1997}
- John A. Biles, 134th ASA Meeting, 1997

## Introduction

- jazz soloists use a personal store of melodic ideas and adapt them to the rhythm and harmony of the rhythm section
- soloists talk to each other by "trading fours" or "eights" (taking turns over 4 or 8 bars)
- GenJam (Genetic Jammer) is a soloist in the Al Biles Virtual Quintet: improvises in real time on any tune and trades fours with a human

## How GenJam works

- is a computer program that learns to play jazz solos, using GA
- GA searches for pleasing melodic ideas with which it contructs jazz improvisations
- two hierarchically related populations of melodic ideas, where each individual is a melodic idea
- a phrase individual represents a four-measure phrase made up of four individuals from the measure population
- it plays only theoretically correct notes
- fitness values como from a human mentor, who listens to genjam improvise on a tune and expresses opinions in real time
- the mentor provides the env in which individuals either survive or die
- its a INTERACTIVE GENETIC ALGORITHM
- musically meaningful mutation
  - transposition, inversion, retrograde, sorting, smoothing and sequencing
  - causes radical change instead of gradual, which speeds up learning
  - some mutations keep genetic diversity, so the population does not converge to a few super individuals
- genome is a string of bits; a measure individual decodes to eighth-note events
- melodies are abstract contours, the pitch is picked from the scale of the current chord only when the note is played
- crossover: random point, swap the bits after it
- the better ideas become parents, their children replace the worse ones

## Real-time interactivity

- pitch-to-MIDI: GenJam listens to the human with a microphone
- when trading fours, it maps the last 4 bars of the human to its chromosomes, mutates them and plays them back
- pitch tracking errors are not a problem, since the notes are always mapped to the chord scale
- the mutations make the answer different from, but related to, what the human played

## Results

- after about a dozen generations the population is mostly good ideas, ready to play live
- about a dozen trained soloists, for styles like bebop, bossa nova, ballad, Latin, waltz and 5/4
- repertoire of over 100 tunes, played in concerts and receptions
- problem: no visual interaction on stage
- audience-mediated performance: the audience trains a soloist with red/green paddles

## Conclusions

- an interactive GA can improvise jazz live and talk with a human soloist
- the human mentor is still needed to give the fitness (our GA replaces this with music theory rules)

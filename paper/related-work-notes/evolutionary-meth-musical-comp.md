# Evolutionary methods for musical composition

- url: https://homepages.inf.ed.ac.uk/rbf/MY_DAI_OLD_FTP/rp882.pdf
- cite: \cite{wiggins1998}
- ga for generation of music
- addition of domain specific knowledge can enhance the quality and speed of production of GA results
- conclude GAs are not idal for the simulation of human musical thought, because their operation in no way simulates human behaviour

## Introduction
- explore 2 aspects of GA applications to music:
  - the use of knoeledge rich structures and procedures within the algorithm itself, as opposed to the more traditional use of ga components which are not problem specific (THIS ONE LOOKS LIKE OUR IDEA IN THE PAPER, REPRESENT ONLY JAZZ INSTEAD OF ANY KIND OF MUSIC)
  - the strict use of objective methods
- interested in simulating human behaviour, not just achieving a musical result

## GA

- representation for chromosomes
- initial population of chromosomes
- set of operators to generate new candidate solutions from memebers of the population
- an evaluation function to assess the fitness quality of a given candidate solutino
- a selection method which gies good solutions a better chance of survival

## Harmonising choral melodies

### Method

- domain-specific knowledge
  - the user inputs the soprano, the music melody
  - the GA will them harmonise the input soprano, homphonically with a further three voices according to the musical domain knoeledge encoded in its operators
- reproductions operators:
  - crossover and mutation
- fitness function
  - music theoretical knowledge used to construct the fitness functions in objective logical terms
  - analyze the system more scientifically
  - 

### Results

- criteria a lecturer uses for first year undergraduate students harmony, the generated version scored 5 of 10
- while other examples were less successful, achieving 3 of 10

## Conclusion

- ga can be applied to the musical domain
- ga depends heavily on the amount of knowledge the system possesses
- the results are still far from ideal
- harmonisation producted has neither clear plan nor intention
- the solo gneerator too, lacks intention
- we cannot expect large scale structure to arise from the kind of programming inherent in a GA containing relatively little domain knowledge
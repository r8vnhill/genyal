# Genyal: The cheerful genetic algorithm framework

![http://creativecommons.org/licenses/by/4.0/](https://i.creativecommons.org/l/by/4.0/88x31.png)

This work is licensed under a 
[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)

<img src="resources/genyal-logo.png" alt="logo" height="200"/>

__Genyal__ is a genetic algorithm framework aimed to be as simple to use as it can be.
Evolution is natural, so using evolutionary algorithms should feel natural as well.

One of the main benefits of evolutionary programming is making it simple to solve complicated 
problems, and that's something that most implementations of this kind of algorithms seems to forget.
You'll find either, very simple implementations of genetic algorithms from scratch, or full fledged
libraries that are, by no means, something that someone with little experience in the field of
evolutionary programming can easily use; nothing in between.
_Genyal_ is that missing "in between", by providing a simple interface so users new to the topic
can learn and use it without need of being experts, and flexible enough so that people can adapt it
to more sophisticated scenarios.

## Usage

Just like using it, installing _Genyal_ should be a piece of cake (great, now I want cake).
To do so, you can get it directly from PyPi or, with pip:

```bash
pip install genyal
```

## Example: Guessing a word

Let's check a very simple example.
A program to guess a given word.

First, we need a way to create the individuals of the population, in this case, each individual will
represent a word, and each gene of the individual will be a letter (lowercase).
For this we can implement a generator function like:

```python
import random
import string

from genyal.genotype import GeneFactory
from genyal.engine import GenyalEngine

def random_char():
    return random.choice(string.ascii_lowercase)

gene_factory = GeneFactory[str]()
gene_factory.generator = random_char

# This is how the engine will select the fittest individuals
def fitness_fun(word: list[str]) -> float:
    return sum([word[i] == "owo"[i] for i in range(0, 3)])

# This is the condition to stop the evolution
def target(genyal_engine: GenyalEngine) -> bool:
    return "".join(genyal_engine.fittest.genes) == "owo"

engine = GenyalEngine(fitness_function=fitness_fun, terminating_function=target)
# We create an initial population of 16 words (Individuals) of 3 characters (genes)
# using our previously defined gene factory.
engine.create_population(16, 3, gene_factory)
engine.evolve()
print(f"Found solution in {engine.generation} generations")
print(
    f"Fittest individual: \"{''.join(engine.fittest.genes)}\" with fitness: "
    f"{engine.fittest.fitness}")
```

If you run the code it will print something like:
```
Found solution in 543 generations
Fittest individual: "owo" with fitness: 3
```

You can find the explanation of this code, along with other examples, at the project's 
[wiki](https://github.com/islaterm/genyal/wiki)

# Genyal: The cheerful genetic algorithm framework

![http://creativecommons.org/licenses/by/4.0/](https://i.creativecommons.org/l/by/4.0/88x31.png)

This work is licensed under a 
[Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/)

![logo](resources/genyal-logo.png)

__Genyal__ is a genetic algorithm framework aimed to be as simple to use as it can be.
Evolution is a natural process, so using evolutionary algorithms should feel natural.

One of the main benefits of evolutionary programming is making it simple to solve complicated 
problems, and that's something that most implementations of this kind of algorithms seems to forget.
You'll find either, very simple implementations of genetic algorithms from scratch, or full fledged
libraries that are, by no means, something that someone with little experience in the field of
evolutionary can easily use; nothing in between.
_Genyal_ is that missing "in between", by providing a simple interface so users new to the topic
can learn and use it without need of being experts and flexible enough so that people can adapt it
to mor sophisticated scenarios.

## Usage

Just like using it, installing _Genyal_ should be a piece of cake (great, now I want cake).
To do so, you can get it directly from PyPi or, with pip:

```bash
pip install genyal
```

## Examples

### Guessing a word

Let's check a very simple example.
A program to guess a given word.

First, we need a way to create the individuals of the population, in this case, each individual will
represent a word, and each gene of the individual will be a letter (lowercase).
For this we can implement a generator function like:

```python
import random
import string

def random_char():
    return random.choice(string.ascii_lowercase)
```

And then we create a factory with that function as its generator:

```python
from genyal.genotype import GeneFactory

gene_factory = GeneFactory[str]()
gene_factory.generator = random_char
```

Next, we're gonna need a way to check how close the individual is to our target word, let's try to 
make it guess _owo_.

```python
from genyal.engine import GenyalEngine

# This is how the engine will select the fittest individuals
def fitness_fun(word: list[str]) -> float:
    return sum([word[i] == "owo"[i] for i in range(0, 3)])

# This is the condition to stop the evolution
def target(genyal_engine: GenyalEngine) -> bool:
    return "".join(genyal_engine.fittest.genes) == "owo"
```

Now, we'll start the engine.
The engine will take care of maintaining and evolving the population.

```python
engine = GenyalEngine(fitness_function=fitness_fun, terminating_function=target)
# We create an initial population of 16 words (Individuals) with words of 3 characters (genes)
# using our previously defined gene factory.
engine.create_population(16, 3, gene_factory)
engine.evolve()
print(f"Found solution in {engine.generation} generations")
print(
    f"Fittest individual: \"{''.join(engine.fittest.genes)}\" with fitness: "
    f"{engine.fittest.fitness}")
```

If you run the code the script will print something like:
```
Found solution in 543 generations
Fittest individual: "owo" with fitness: 3
```

### More complex examples will be added in future iterations.
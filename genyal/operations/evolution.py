"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from copy import copy
from random import Random
from typing import List

from genyal.individuals import Individual
from genyal.utils.math_utils import cum_difference


def tournament_selection(population: List[Individual], random_generator: Random = Random(),
                         matches: int = 5) -> Individual:
    """
    Selects the fittest from a group of individuals.
    The tournament selection algorithm compares the fitness of two individuals at a time (a match)
    and chooses the one with the best fitness to continue to the next match.

    Args:
        population:
            the collection of individuals to play the tournament.
        random_generator:
            a random number generator to pick individuals for the matches.
        matches:
            the numbers of matches the tournament is going to last.
    Returns:
        The individual who won all the matches (i.e. the one with the highest fitness).
    """
    best_idx = 0
    for _ in range(0, matches):
        candidate_idx = random_generator.randrange(0, len(population))
        if best_idx is None or candidate_idx > best_idx:
            best_idx = candidate_idx
    return copy(population[best_idx])


def default_terminating_function(engine, max_generations=100):
    """
    By default the engine will finish after a certain number of generations have gone through
    evolution.

    Args:
        engine:
            The engine running the genetic algorithm.
        max_generations:
            The number of generations the population will advance.
            If none is given, it defaults to 100 generations.
    Returns:
        True when the engine has evolved the population until the indicated generation.
    """
    return engine.generation >= max_generations


def stale_for(engine, generations: int) -> bool:
    """
    Indicates if the engine population's fitness hasn't change in the last generations.

    Args:
        engine:
            the engine running the algorithm
        generations:
            the number of generations to check
    Returns:
        True if the population hasn't improved in the last generations; False otherswise
    """
    return len(engine.fitness_record) >= generations and cum_difference(engine[-generations:])

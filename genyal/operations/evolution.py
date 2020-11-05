"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from copy import copy
from random import Random

from genyal.individuals import Individual


def tournament_selection(population: list[Individual], random_generator: Random = Random(),
                         matches: int = 5) -> Individual:
    best_idx = 0
    for _ in range(0, matches):
        candidate_idx = random_generator.randrange(0, len(population))
        if best_idx is None or candidate_idx > best_idx:
            best_idx = candidate_idx
    return copy(population[best_idx])


def default_terminating_function(engine, max_generations=100):
    return engine.generation >= max_generations

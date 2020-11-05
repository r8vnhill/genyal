"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from random import Random

from genyal.individuals import Individual


def tournament_selection(population: list[Individual], random_generator: Random = Random(),
                         matches: int = 5) -> Individual:
    best = None
    for _ in range(0, matches):
        candidate = random_generator.choice(population)
        if best is None or candidate > best:
            best = candidate
    return best


def default_terminating_function(engine, max_generations=100):
    return engine.generation >= max_generations

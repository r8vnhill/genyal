"""
"genyal" (c) by Ignacio Slater M.
"genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory


def binary_match(candidates: str, target: int) -> float:
    actual_result = int("".join(candidates), 2)
    return -abs(target - actual_result)


def terminating_function(genyal_engine: GenyalEngine, target: int) -> bool:
    return binary_match(genyal_engine.fittest.genes, target) == 0


if __name__ == '__main__':
    factory = GeneFactory(generator=lambda: random.choice(['0', '1']))
    engine = GenyalEngine(fitness_function=binary_match, terminating_function=terminating_function)
    engine.fitness_function_args = (12345,)
    engine.create_population(50, 20, factory)
    engine.evolve(12345)
    print(engine.fittest.genes)
    print(f"Result found in: {engine.generation} generations.")
    print(f"{''.join(engine.fittest.genes)} = {int(''.join(engine.fittest.genes), 2)}")

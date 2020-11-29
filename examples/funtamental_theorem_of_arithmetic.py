"""
"Genyal" (c) by Ignacio Slater M.
"Genyal" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory
from genyal.operations.evolution import stale_for


def create_candidate_factors(hi: int) -> list[int]:
    """
    Creates a list with 1 and the prime numbers from 2 to 500 computed using the sieve of
    Eratosthenes.
    """
    is_prime = [True] * hi
    p = 2
    while p ** 2 < hi:
        if is_prime[p]:
            for i in range(p ** 2, hi, p):
                is_prime[i] = False
        p += 1
    primes = []
    for n in range(2, hi):
        if is_prime[n]:
            primes.append(n)
    return [1] + primes


def candidates_fitness(candidates: list[int], target: int) -> float:
    prod = 1
    for n in candidates:
        prod *= n
    return 1 / (abs(target - prod) + 1)


if __name__ == '__main__':
    candidate_factors = create_candidate_factors(100)
    factory = GeneFactory(generator=lambda: random.choice(candidate_factors))
    engine = GenyalEngine(fitness_function=candidates_fitness)
    engine.fitness_function_args = (50,)
    engine.create_population(10000, 5, factory)
    engine.evolve(500)
    print(engine.fittest)

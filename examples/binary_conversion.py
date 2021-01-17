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


# if __name__ == '__main__':
def main():
    factory = GeneFactory(generator=lambda: random.choice(['0', '1']))
    engine = GenyalEngine(fitness_function=binary_match, terminating_function=terminating_function)
    engine.fitness_function_args = (321,)
    engine.create_population(20, 10, factory)
    engine.evolve(321)
    print(engine.fittest.genes)
    print(f"Result found in: {engine.generation} generations.")
    print(f"{''.join(engine.fittest.genes)} = {int(''.join(engine.fittest.genes), 2)}")


import linecache


def display_top(snapshot, key_type='lineno', limit=10):
    snapshot = snapshot.filter_traces((
        tracemalloc.Filter(False, "<frozen importlib._bootstrap>"),
        tracemalloc.Filter(False, "<unknown>"),
    ))
    top_stats = snapshot.statistics(key_type)

    print("Top %s lines" % limit)
    for index, stat in enumerate(top_stats[:limit], 1):
        frame = stat.traceback[0]
        print("#%s: %s:%s: %.1f KiB"
              % (index, frame.filename, frame.lineno, stat.size / 1024))
        line = linecache.getline(frame.filename, frame.lineno).strip()
        if line:
            print('    %s' % line)

    other = top_stats[limit:]
    if other:
        size = sum(stat.size for stat in other)
        print("%s other: %.1f KiB" % (len(other), size / 1024))
    total = sum(stat.size for stat in top_stats)
    print("Total allocated size: %.1f KiB" % (total / 1024))


if __name__ == '__main__':
    import tracemalloc

    tracemalloc.start()

    main()

    first_size, first_peak = tracemalloc.get_traced_memory()

    tracemalloc.reset_peak()

    main()

    second_size, second_peak = tracemalloc.get_traced_memory()

    print(f"{first_size=}, {first_peak=}")
    print(f"{second_size=}, {second_peak=}")

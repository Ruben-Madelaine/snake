try:
    from population import Population
except ModuleNotFoundError:
    from back.population import Population


def test_population():
    generation = 10
    population = 10
    world_size = 10
    p = Population(population, world_size)

    gen_best_scores = []
    for gen in range(generation):
        p.live()
        best = p.get_sorted_gen_results()
        gen_best_scores += [best]
        p.nex_gen()

    for b in gen_best_scores:
        print(b)


def main():
    test_population()


if __name__ == "__main__":
    main()

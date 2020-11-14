try:
    from game import Game
    from snake import RandomAI
except ModuleNotFoundError:
    from back.game import Game
    from back.snake import RandomAI


class Population:
    def __init__(self, size, game_size, brain_type):
        self.size = size
        self.game_size = game_size
        self.brain_type = brain_type
        self.start()

    def start(self):
        self.population = [Game(self.game_size) for _ in range(self.size)]
        for game in self.population:
            game.start(self.brain_type)

    def live(self):
        for game in self.population:
            game.play()

    def get_gen_results(self):
        gen_results = {}
        for game in self.population:
            snake_size = game.snake.size
            snake_age = game.count
            gen_results[game] = (snake_size, snake_age)

        return gen_results

    def get_sorted_gen_results(self):
        results = self.get_gen_results()
        sorted_res = sorted(results.values(), reverse=True)
        return sorted_res

    def get_best(self):
        results = self.get_gen_results()
        best_res = sorted(results.values(), reverse=True)[0]
        best = [g for g, res in results.items() if res == best_res]
        return best[0]

    def nex_gen(self):
        best_snake = self.get_best().snake

        new_population = []
        for _ in range(self.size):
            game = Game(self.game_size)
            game.start(self.brain_type)

            game.snake.brain = best_snake.brain.clone()
            new_population += [game]

            # TODO improve !!!!

        self.population = new_population


def test_population():
    generation = 10
    population = 10
    world_size = 10
    brain_type = RandomAI
    # test another brain

    p = Population(population, world_size, brain_type)

    gen_best_scores = []
    for gen in range(generation):
        p.live()
        best = p.get_sorted_gen_results()
        gen_best_scores += [best]
        p.nex_gen()

    for i, b in enumerate(gen_best_scores):
        print(f"Gen #{i}:", b)


def main():
    test_population()


if __name__ == "__main__":
    main()

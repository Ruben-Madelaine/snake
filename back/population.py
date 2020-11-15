import random

import snake
import database as db
from game import Game

try:
    from game import Game
    from snake import RandomAI
except ModuleNotFoundError:
    from back.game import Game
    from back.snake import RandomAI


class Population:
    def __init__(self, size, game_size, brain_type):
        self.best_overall_score = 0
        self.gen = 0

        self.size = size
        self.game_size = game_size
        self.brain_type = brain_type
        self.mutation_rate = 0.2
        self.start()

    def start(self):
        self.population = [self.init_game() for _ in range(self.size)]

    def init_game(self):
        game = Game(self.game_size)
        game.start(self.brain_type)
        return game

    def live(self):
        for game in self.population:
            game.play()

    def evaluate_gen(self):
        gen_results = {}
        for game in self.population:
            snake_size = game.snake.size
            snake_age = game.count
            gen_results[game] = (snake_size, snake_age)

        self.gen_results = gen_results

        sorted_res = sorted(self.gen_results.values(), reverse=True)

        best_res = sorted_res[0]
        bests = [g for g, res in self.gen_results.items() if res == best_res]

        self.best_res = best_res
        self.best_game = bests[0]
        self.best_score = score(best_res)
        self.best_snake = bests[0].snake
        self.update_overall_stats()

    def update_overall_stats(self):
        if self.best_score > self.best_overall_score:
            self.best_overall_res = self.best_res
            self.best_overall_game = self.best_game
            self.best_overall_score = self.best_score
            self.best_overall_snake = self.best_snake
            self.best_gen = self.gen

    def natural_selection(self):
        self.evaluate_gen()

        new_gen = [self.clone(self.best_snake)]  # Best snake makes it to next gen

        for i in range(1, self.size):
            mother = self.get_a_parent()
            father = self.get_a_parent()

            game = self.crossover(mother, father)
            new_gen += [game]

        self.population = new_gen
        self.gen += 1

    def get_a_parent(self):
        #   get a parent from last gen
        #       best / with fitness > (rand?) threshold / randomly ?
        minimum_score = self.best_score
        minimum_score -= (
            minimum_score * random.random()
        )  # THIS might be a big source of variation in evolution
        for g, res in self.gen_results.items():
            if score(res) > minimum_score:
                return g.snake

        return self.best_snake

    def crossover(self, mother, father):
        game = self.init_game()

        game.snake.brain = mother.brain.crossover(father.brain)
        game.snake.brain.mutate(self.mutation_rate)
        return game

    def clone(self, snake):
        game = self.init_game()
        game.snake.brain = snake.brain.clone()
        return game


def score(res):
    return res[0] * 10 + res[1] / 100


# ----------------------- Test ---------------------------


def test_population():
    generation = 500
    population_size = 10
    world_size = 10

    # brain_type = snake.RandomAI
    brain_type = snake.AI

    p = Population(population_size, world_size, brain_type)

    res = []
    for gen in range(generation):
        p.live()
        p.evaluate_gen()
        p.natural_selection()

        if (gen % 10) == 0:
            print(f"Gen #{gen}:", p.best_res, p.best_score)
            res += [(*p.best_res, p.best_score)]

    print(f"Overall Results #{p.best_gen}:", p.best_overall_res, p.best_overall_score)

    res += [(*p.best_overall_res, p.best_overall_score)]
    return res


# ----------------------- Database ---------------------------


def access_db(db_name):
    return db.get_connection(db_name)


def populate_db(db_connection, list):
    db.create_table(db_connection)

    # convert list elements to tuple
    rows = [tuple(elm) for elm in list]

    db.insert_rows(db_connection, rows)


def load_db(db_connection):
    rows = db.get_all(db_connection)
    db.print_table(rows)

    snake = []
    for row in rows:
        snake += [row["size"], row["age"], row["score"]]

    return snake


def test_write_and_read_db():
    db_name = "database/snake.db"
    snake_db = access_db(db_name)

    # create
    scores = test_population()
    populate_db(snake_db, scores)
    snake_db.close()

    # access
    snake_db = access_db(db_name)
    rows = load_db(snake_db)
    snake_db.close()


def main():
    # test_population()
    test_write_and_read_db()


if __name__ == "__main__":
    main()

import random

import snake
import matrix
import network
import database as db
from game import Game

try:
    from game import Game
    from snake import RandomAI
except ModuleNotFoundError:
    from back.game import Game
    from back.snake import RandomAI


class Population:
    def __init__(self, size, game_size, brain_type, mutation_rate=0.2):
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

    # ----------------------- Selection ---------------------------

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
    return res[0] + res[1] / 10


# ----------------------- Tests ---------------------------


def test_population(generation, population_size, world_size):
    # brain_type = snake.RandomAI
    brain_type = snake.AI

    p = Population(population_size, world_size, brain_type)
    return run_generations(p, generation)

def run_generations(p, generation):
    stats = []
    networks = []
    for gen in range(generation):
        p.live()
        p.evaluate_gen()
        p.natural_selection()

        if (gen % 10) == 0:
            print(f"Gen #{gen}:", p.best_res, p.best_score)
            stats += [(*p.best_res, p.best_score)]
            networks += [(p.best_score, *p.best_game.snake.brain.nn.get_infos())]

    print(f"Overall Results #{p.best_gen}:", p.best_overall_res, p.best_overall_score)

    stats += [(*p.best_overall_res, p.best_overall_score)]
    return stats, networks


# ----------------------- Database ---------------------------

# ----------------------- Score
def access_db(db_name):
    return db.get_connection(db_name)


def populate_db(db_connection, list):
    db.create_table(db_connection)

    # convert list elements to tuple
    details = "AI, Diagonal vision, Best Net, New score mode" # Best Net Trained
    rows = [tuple([*elm, details]) for elm in list]

    db.insert_rows(db_connection, rows)


def load_db(db_connection):
    rows = db.get_all(db_connection)
    db.print_table(rows)


def save_score(db_name, scores):
    # Score
    snake_db = access_db(db_name)
    populate_db(snake_db, scores)
    snake_db.close()

    # access
    snake_db = access_db(db_name)
    rows = load_db(snake_db)
    snake_db.close()

# ----------------------- Network

def populate_networks_db(db_connection, list):
    db.create_networks_table(db_connection)

    # convert list elements to tuple
    rows = [tuple(elm) for elm in list]

    db.insert_networks_rows(db_connection, rows)


def load_networks_db(db_connection):
    rows = db.get_all_networks(db_connection)
    db.print_table(rows)


def load_network_db(db_connection, get_network):
    rows = get_network(db_connection)

    for row in rows:
        return load_network(row)


def load_network(config):
    score = config['score']
    print("Best score =", score)

    input_nodes = config['input_nodes']
    hidden_nodes = config['hidden_nodes']
    output_nodes = config['output_nodes']
    hidden_layers = config['hidden_layers']
    wheights_info = config['wheights_info']

    nn = network.Network(input_nodes, hidden_nodes, output_nodes, hidden_layers)
    weights = []
    weights_conf = wheights_info.split("\n")
    for conf in weights_conf:
        matrix_conf, raw_wheights = conf.split(":")
        row, col = [int(i) for i in matrix_conf.split(',')]
        w = matrix.Matrix(row, col)
        raw_wheights = raw_wheights.replace('[', '').replace(']', '').split(',')

        m = {}
        i = 0
        for r in range(row):
            for c in range(col):
                m[(r,c)] = float(raw_wheights[i])
                i += 1
        w.matrix = m
        weights += [w]

    nn.weights = weights
    return nn

def train_new_ai(generation, population_size, world_size):
    db_name = "database/snake.db"
    scores, networks = test_population(generation, population_size, world_size)

    save_score(db_name, scores)
    save_network(db_name, networks)


def save_network(db_name, networks):
    # Network
    snake_db = access_db(db_name)
    populate_networks_db(snake_db, networks)
    snake_db.close()

    # access
    snake_db = access_db(db_name)
    best_network = load_networks_db(snake_db)
    snake_db.close()


def play_one_game_with_best_ai(get_network):
    world_size = 20
    brain_type = snake.AI

    db_name = "database/snake.db"

    # Network
    snake_db = access_db(db_name)
    best_network = load_network_db(snake_db, get_network)
    snake_db.close()

    g = Game(world_size)
    g.start(brain_type)
    print(g)
    g.snake.brain.nn = best_network
    g.play(verbose=True)
    

def load_best_ai_and_train(generation, population_size, world_size, get_network):
    db_name = "database/snake.db"

    # Network
    snake_db = access_db(db_name)
    best_network = load_network_db(snake_db, get_network)
    snake_db.close()


    # brain_type = snake.RandomAI
    brain_type = snake.AI

    p = Population(population_size, world_size, brain_type)

    for g in p.population:
        g.snake.brain.nn = best_network.clone()
    
    scores, networks = run_generations(p, generation)

    save_score(db_name, scores)
    save_network(db_name, networks)


# ----------------------- Main ---------------------------


def main():
    import time
    # test_population()

    world_size = 20
    generation = 800
    population_size = 100
    mutation_rate = 0.1

    get_network = [db.get_best_network, db.get_latest_network][1]

    train_new_ai(generation, population_size, world_size)
    # load_best_ai_and_train(generation, population_size, world_size, get_network)
    # time.sleep(3)

    play_one_game_with_best_ai(get_network)


if __name__ == "__main__":
    main()

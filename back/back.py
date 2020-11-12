
try:
    from board import Board
    import snake
except ModuleNotFoundError:
    from back.board import Board
    import back.snake as snake


MAX_ITER = 100


class Game:
    def __init__(self, size):
        self.board = Board(size)
        self.count = 0

    def __str__(self):
        return str(self.board)

    # -------------- INIT --------------------

    def start(self):
        self.air_drop_fruit()
        self.hatch_from_egg()

    def air_drop_fruit(self, i=None, j=None):
        if i and j:
            self.fruit = self.board.place_fruit(i, j)
        else:
            self.fruit = self.board.drop_fruit()

    def hatch_from_egg(self):
        center = self.board.size // 2
        head = self.board.grid[center, center]
        tail = self.board.grid[center, center - 1]
        body = [head, tail]

        self.snake = snake.Snake(snake.RandomAI(), body, snake.DIRECTIONS[snake.RIGHT])

    def play(self):
        while self.snake.is_alive() and self.count < MAX_ITER:
            self.next()
        # logger(
        #     f"> Our fellow Snake friend died at the age of {self.count}. What a pitty..."
        # )

    def replay(self):
        pass

    # -------------- CONTROLLER --------------------

    def get_state(self):
        res = {
            "snake": [b.pos for b in self.snake.body],
            "fruit": self.fruit.pos if self.fruit else None,
            "moves": self.snake.history,
        }
        return res

    # -------------- CORE --------------------

    def next(self):
        self.count += 1

        self.snake.think()
        next_pos = self.snake.next_pos()
        cell = self.get_cell(next_pos)
        if cell:
            ate_a_fruit = self.snake.move(cell)
            if ate_a_fruit:
                self.fruit = self.board.drop_fruit()
                logger("Air dropping a new fruit in 3...2..1.. *BOOM*")

    def get_cell(self, next_pos):
        if self.is_available(next_pos):
            cell = self.board.grid[next_pos]
            if cell.is_empty() or cell.have_fruit():
                return cell
        else:
            self.snake.die()

    def is_available(self, next_pos):
        i, j = next_pos
        return (0 <= i < self.board.size) and (0 <= j < self.board.size)

    # -------------- POPULATION --------------------

class Population:
    def __init__(self, size, game_size):
        self.size = size
        self.game_size = game_size
        self.start()

    def start(self):
        self.population = [Game(self.game_size) for _ in range(self.size)]
        for game in self.population:
            game.start()

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
        print(best_res)
        best = [g for g,res in results.items() if res == best_res]
        return best[0]

    def nex_gen(self):
        best_snake = self.get_best().snake

        new_population = []
        for _ in range(self.size):
            game = Game(self.game_size)
            game.start()

            game.snake.brain = best_snake.brain.clone()
            new_population += [game]

        self.population = new_population


def logger(txt):
    if __name__ == "__main__":
        print(txt)


def test_game():
    g = Game(5)
    g.start()
    print(g)

    g2 = Game(10)
    g2.start()
    print(g2)
    print(g)

    g.play()

    print(g2)

    state = g.get_state()
    print(state)

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

    # p.get_best().replay()

def main():
    # test_game()
    test_population()


if __name__ == "__main__":
    main()

import board
import snake


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
        while self.snake.is_alive():
            yield self.next()
        logger(
            f"\n> Our fellow Snake friend died at the age of {self.count}. What a pitty..."
        )

    def replay(self):
        pass

    # -------------- SET --------------------

    def hard_start(self, i, j):
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
        else:
            logger("End of game!")

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

    # TODO useful ?
    def start(self):
        self.pop = [Game(10) for _ in range(self.size)]

    def breed(self, snake):
        self.snakes = [snake.clone() for _ in range(self.size)]

    def live(self):
        pass
    # next gen
        # get best and breed


    # copy snake N times
    # isolate each snake in its world
    # go for the fruit !
    # success or fail:
    #  - Ate the fruit
    #  - Died


def logger(txt):
    if __name__ == "__main__":
        print(txt)
        

def test_game():
    g = Game(10)
    g.start()
    print(g)
    
    for _ in g.play():
        pass

    print(g)
    state = g.get_state()
    print(state)

def test_population():
    p = Population(10, 10)
    p.live()

    # p.start()
    # for _ in g.play():

    # p.get_best().replay()

def main():
    test_game()
    # test_population()


if __name__ == "__main__":
    main()

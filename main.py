
import random


UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)


class Board:
    grid = {}
    size = 0

    def __init__(self, size):
        self.size = size
        self.create()

    def __str__(self):
        txt = ""

        for i in range(self.size):
            txt += "\n"
            line = " ".join(str(self.grid[(i, j)]) for j in range(self.size))
            txt += line

        return "The best Board !" + txt

    def create(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[(i, j)] = Cell(i, j)

    def drop_fruit(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)

        if self.grid[(i, j)].is_empty():
            self.grid[(i, j)].land_fruit()
        else:
            self.drop_fruit()


class Cell:
    empty = True
    fruit = False
    occupied = False

    def __init__(self, i, j):
        self.pos = i, j

    def __str__(self):
        herb = "\"" if self.empty else ""
        fruit = "#" if self.fruit else ""
        snake = "o" if self.occupied else ""

        return snake or fruit or herb

    def is_empty(self):
        return self.empty

    def have_fruit(self):
        return self.fruit

    def land_fruit(self):
        self.fruit = not self.fruit
        self.empty = not self.empty

    def consume_fruit(self):
        self.fruit = not self.fruit
        self.empty = not self.empty

    def slither_on(self):
        self.occupied = not self.occupied
        self.empty = not self.empty

    
class Snake:
    size = 2

    def __init__(self, body):
        self.body = body
        self.direction = RIGHT

    def move(self, head):
        self.body = [head] + self.body
        # check if fruit
        if head.have_fruit():
            self.eat(cell)
            head.slither_on()
        else:
            tail = self.body.pop()
            self.slither([head, tail])

    def slither(self, cells):
        for cell in cells:
            cell.slither_on()

    def eat(self, cell):
        cell.consume_fruit()
        size += 1

    def die(self):
        pass

    def next_pos(self):
        return self.add_pos(self.body[0].pos, self.direction)

    def add_pos(self, pos1, pos2):
        return tuple(p1+p2 for p1, p2 in zip(pos1, pos2))


class Game:
    def __init__(self, size):
        self.board = Board(size) 

    def __str__(self):
        return str(self.board)

    def start(self):
        self.board.drop_fruit()
        self.hatch()

    def hatch(self):
        center = self.board.size//2
        head = self.board.grid[center, center]
        tail = self.board.grid[center, center-1]
        body = [head, tail]
        self.snake = Snake(body)
        self.snake.slither(body)

    def next(self):
        next_pos = self.snake.next_pos()
        cell = self.get_cell(next_pos)
        if cell:
            self.snake.move(cell)
        else:
            print("End of game !")

    def get_cell(self, next_pos):
        if self.is_available(next_pos):
            cell = self.board.grid[next_pos]
            if cell.is_empty() or cell.have_fruit():
                return cell

    def is_available(self, next_pos):
        i, j = next_pos
        return (0 <= i < self.board.size) and (0 <= j < self.board.size)

def main():
    g = Game(20)
    g.start()
    print(g)

    next_pos = g.snake.next_pos()
    g.get_cell(next_pos).land_fruit()
    
    for x in range(9):
        g.next()
        print(g)


if __name__ == "__main__":
    main()

    pos = 5, 2
    print(pos)
    print(pos + RIGHT)

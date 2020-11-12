import random 


class Board:
    def __init__(self, size):
        self.grid = {}
        self.size = size
        self.create()

    def __str__(self):
        txt = ""

        for i in range(self.size):
            txt += "\n"
            line = " ".join(str(self.grid[(i, j)]) for j in range(self.size))
            txt += line

        return "The best Board!" + txt

    def create(self):
        for i in range(self.size):
            for j in range(self.size):
                self.grid[(i, j)] = Cell(i, j)

    def place_fruit(self, i, j):
        if self.grid[(i, j)].is_empty():
            return self.grid[(i, j)].land_fruit()
        else:
            return self.drop_fruit()

    def drop_fruit(self):
        i = random.randint(0, self.size - 1)
        j = random.randint(0, self.size - 1)
        return self.place_fruit(i, j)


class Cell:
    def __init__(self, i, j):
        self.pos = i, j

        self.empty = True
        self.fruit = False
        self.occupants = 0

    def __str__(self):
        herb = '"' if self.empty else ""
        fruit = "@" if self.fruit else ""
        snake = "o" if self.occupants else ""

        return snake or fruit or herb

    def is_empty(self):
        return self.empty

    def have_fruit(self):
        return self.fruit

    def land_fruit(self):
        self.fruit = not self.fruit
        self.empty = not self.empty
        return self

    def consume_fruit(self):
        self.fruit = not self.fruit
        self.empty = not self.empty

    def slither_in(self):
        self.occupants += 1

        if self.occupants: 
            self.empty = False

    def slither_out(self):
        self.occupants -= 1
        if not self.occupants: 
            self.empty = True



def main():
    board = Board(size=10)
    board.drop_fruit()
    print(board)

    board2 = Board(size=10)
    board2.drop_fruit()
    print(board2)


if __name__ == "__main__":
    main()

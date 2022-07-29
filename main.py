import random


class TicTacToe:
    FREE_CELL = 0  # свободная клетка
    HUMAN_X = 1  # крестик (игрок - человек)
    COMPUTER_O = 2  # нолик (игрок - компьютер)

    def __init__(self, pole_size=3):
        self.pole = tuple(tuple(Cell() for _ in range(pole_size)) for _ in range(pole_size))

    def __getitem__(self, item):
        self.check_index(item)
        return self.pole[item[0]][item[1]].value

    def __setitem__(self, key, value):
        self.check_index(key)
        i, j = key
        if self.pole[i][j]:
            self.pole[i][j].value = value

    def check_index(self, indx):
        if type(indx) == str:
            indx = tuple(int(x) for x in indx.split())
        if type(indx) != tuple and not all(map(lambda x: type(x) == int and 0 <= x < len(self.pole), indx)):
            raise IndexError('некорректно указанные индексы')

    def init(self):
        for row in self.pole:
            for cell in row:
                cell.value = 0

    def show(self):
        for row in self.pole:
            print(*[item.value for item in row])
        print('------')

    def human_go(self):
        if self:
            indx = input("Введите координаты клетки, в виде x y, например 1 1): ")
            try:
                i, j = int(indx.split()[0]) - 1, int(indx.split()[1]) - 1
                indx = (i, j)
            except Exception:
                raise IndexError('некорректно указанные индексы')
            self.check_index(indx)
            if not self.pole[i][j]:
                self.human_go()
            self[i, j] = self.HUMAN_X

    def computer_go(self):
        if self:
            free_line = []
            for line_indx in range(len(self.pole)):
                for cell in self.pole[line_indx]:
                    if cell:
                        free_line.append(line_indx)
                        break
            chosen_line = random.choice(free_line)
            free_items = []
            for item_indx in range(len(self.pole[chosen_line])):
                if self.pole[chosen_line][item_indx]:
                    free_items.append(item_indx)
            chosen_col = random.choice(free_items)
            if not self.pole[chosen_line][chosen_col]:
                self.computer_go()
            self[chosen_line, chosen_col] = self.COMPUTER_O

    @property
    def is_human_win(self):
        count = 0
        for i in range(len(self.pole)):
            if self[i, i] == self.HUMAN_X:
                count += 1
                if count == 3:
                    return True
        for line in self.pole:
            count = 0
            for item in line:
                if item.value != self.HUMAN_X:
                    continue
                if item.value == self.HUMAN_X:
                    count += 1
                    if count == 3:
                        return True
        for row in range(len(self.pole)):
            count = 0
            for col in range(len(self.pole)):
                if self[col, row] != self.HUMAN_X:
                    continue
                if self[col, row] == self.HUMAN_X:
                    count += 1
                    if count == 3:
                        return True
        return False
    
    @property
    def is_computer_win(self):
        count = 0
        for i in range(len(self.pole)):
            if self[i, i] == self.COMPUTER_O:
                count += 1
                if count == 3:
                    return True
        for line in self.pole:
            count = 0
            for item in line:
                if item.value != self.COMPUTER_O:
                    continue
                if item.value == self.COMPUTER_O:
                    count += 1
                    if count == 3:
                        return True
        for row in range(len(self.pole)):
            count = 0
            for col in range(len(self.pole)):
                if self[col, row] != self.COMPUTER_O:
                    continue
                if self[col, row] == self.COMPUTER_O:
                    count += 1
                    if count == 3:
                        return True
        return False
    
    @property
    def is_draw(self):
        for row in self.pole:
            for item in row:
                if item:
                    return False
        if not self.is_computer_win or self.is_human_win:
            return True
        return False

    def __bool__(self):
        if not any([bool(x) for row in self.pole for x in row]) or self.is_computer_win or self.is_human_win:
            return False
        return True


class Cell:
    def __init__(self):
        self.value = 0

    def __bool__(self):
        return self.value == 0


game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")
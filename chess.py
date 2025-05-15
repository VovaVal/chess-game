WHITE = 1
BLACK = 2
R_W_0 = [False, 0, 0]
R_W_7 = [False, 0, 7]
R_B_0 = [False, 7, 0]
R_B_7 = [False, 7, 7]
K_W = [False, 0, 4]
K_B = [False, 7, 4]


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def check_kings(board):
    kings = []
    for i in range(8):
        for n in range(8):
            if isinstance(board.field[i][n], King):
                kings.append(board.field[i][n])
    if len(kings) < 2:
        print(f'Победили {'белые!' if kings[0].get_color() == WHITE else 'чёрные!'}')
        return True
    return False


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <row1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        if board.move_piece(row, col, row1, col1):
            print('Ход успешен')
        else:
            print('Координаты некорректы! Попробуйте другой ход!')
        if check_kings(board):
            print_board(board)
            break


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if not (self.field[row][col] is None) and self.field[row][col].char() != 'P':
            return False
        if row1 == 7 or row1 == 0:
            if self.field[row1][col1] is None:
                if self.field[row][col].can_move(self, row, col, row1, col1) and char in ['Q', 'R', 'B', 'N']:
                    color = self.field[row][col].get_color()
                    self.field[row][col] = None
                    ch = None
                    match char:
                        case 'Q':
                            ch = Queen(color)
                        case 'R':
                            ch = Rook(color)
                        case 'B':
                            ch = Bishop(color)
                        case 'N':
                            ch = Knight(color)
                    self.field[row1][col1] = ch
                    return True
                return False
            else:
                if self.field[row][col].can_attack(self, row, col, row1, col1) and char in ['Q', 'R', 'B', 'N']:
                    color = self.field[row][col].get_color()
                    self.field[row][col] = None
                    ch = None
                    match char:
                        case 'Q':
                            ch = Queen(color)
                        case 'R':
                            ch = Rook(color)
                        case 'B':
                            ch = Bishop(color)
                        case 'N':
                            ch = Knight(color)
                    self.field[row1][col1] = ch
                    return True
                return False
        return False

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece(self, row, col, row1, col1):
        global R_W_0, R_B_0, R_W_7, R_B_7, K_B, K_W
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт True.
        Если нет --- вернёт False'''
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if isinstance(piece, King) and (row1 == 0 and col1 == 2) or (row1 == 0 and col1 == 6):
            if row1 == 0 and col1 == 2 and R_W_0[0] is False and K_W[0] is False:
                self.castling0()
            elif row1 == 0 and col1 == 6 and R_W_7[0] is False and K_W[0] is False:
                self.castling7()
        if isinstance(piece, King) and (row1 == 7 and col1 == 2) or (row1 == 7 and col1 == 6):
            if row1 == 7 and col1 == 2 and R_B_0[0] is False and K_B[0] is False:
                self.castling0()
            elif row1 == 7 and col1 == 6 and R_B_7[0] is False and K_B[0] is False:
                self.castling7()
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        if not (self.field[row][col].get_color() == self.current_player_color()):
            return False
        if isinstance(self.field[row][col], Rook):
            if piece.get_color() == WHITE:
                if (col == 0 and row == 0) or (col1 == 0 and row1 == 0):
                    R_W_0[0] = True
                else:
                    R_W_7[0] = True
            else:
                if (col == 0 and row == 7) or (col1 == 0 and row1 == 7):
                    R_B_0[0] = True
                else:
                    R_B_7[0] = True
        elif isinstance(self.field[row][col], King):
            if piece.get_color() == WHITE:
                K_W[0] = True
            else:
                K_B[0] = True
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece
        self.color = BLACK if self.color == WHITE else WHITE
        return True

    def castling0(self):
        global R_W_0, R_B_0, K_B, K_W
        if self.color == WHITE:
            if (isinstance(self.field[0][0], Rook) and R_W_0[0] is False and K_W[0] is False and
                    isinstance(self.field[0][4], King) and self.field[0][1] is None and self.field[0][2] is None and
                    self.field[0][3] is None):
                piece_k, piece_r = self.field[0][4], self.field[0][0]
                self.field[0][4] = None
                self.field[0][0] = None
                self.field[0][2] = piece_k
                self.field[0][3] = piece_r
                R_W_0[0] = True
                K_W[0] = True
                self.color = BLACK
                return True
            return False
        else:
            if (isinstance(self.field[7][0], Rook) and R_B_0[0] is False and K_B[0] is False and
                    isinstance(self.field[7][4], King) and self.field[7][1] is None and self.field[7][2] is None and
                    self.field[7][3] is None):
                piece_k, piece_r = self.field[7][4], self.field[7][0]
                self.field[7][4] = None
                self.field[7][0] = None
                self.field[7][2] = piece_k
                self.field[7][3] = piece_r
                R_W_0[0] = True
                K_W[0] = True
                self.color = WHITE
                return True
            return False

    def castling7(self):
        global R_W_7, R_B_7, K_B, K_W
        if self.color == WHITE:
            if (isinstance(self.field[0][7], Rook) and R_W_7[0] is False and K_W[0] is False and
                    isinstance(self.field[0][4], King) and self.field[0][5] is None and self.field[0][6] is None):
                piece_k, piece_r = self.field[0][4], self.field[0][7]
                self.field[0][4] = None
                self.field[0][7] = None
                self.field[0][6] = piece_k
                self.field[0][5] = piece_r
                R_W_0[0] = True
                K_W[0] = True
                self.color = BLACK
                return True
            return False
        else:
            if (isinstance(self.field[7][7], Rook) and R_B_7[0] is False and K_B[0] is False and
                    isinstance(self.field[7][4], King) and self.field[7][5] is None and self.field[7][6] is None):
                piece_k, piece_r = self.field[7][4], self.field[7][7]
                self.field[7][4] = None
                self.field[7][7] = None
                self.field[7][6] = piece_k
                self.field[7][5] = piece_r
                R_W_0[0] = True
                K_W[0] = True
                self.color = WHITE
                return True
            return False


class Rook:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может ходить только по вертикали
        # "взятие на проходе" не реализовано
        if col != col1:
            return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
        direction = 1 if (self.color == WHITE) else -1
        return (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1)) and board.field[row1][col1].get_color() != self.get_color()


class Knight:
    '''Класс коня. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        knight_pos = (row, col)
        if not (0 <= row1 < 8 and 0 <= col1 < 8):
            return False
        elif (((abs(knight_pos[0] - row1) == 2 and abs(knight_pos[1] - col1) == 1) or
               (abs(knight_pos[0] - row1) == 1 and abs(knight_pos[1] - col1) == 2)) and
              row != row1 and col != col1):
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    '''Класс короля. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        king_pos = (row, col)
        if not (
            (king_pos[0] == row1 and abs(king_pos[1] - col1)) == 1 or 
            (king_pos[1] == col1 and abs(king_pos[0] - row1) == 1)
        ):
            return False
        if board.field[row1][col1] is None:
            return True
        elif self.get_color() != board.field[row1][col1].get_color():
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    '''Класс ферзя. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row == row1 or col == col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                if not (board.get_piece(r, col) is None):
                    return False
            step = 1 if (col1 >= col) else -1
            for c in range(col + step, col1, step):
                if not (board.get_piece(row, c) is None):
                    return False
            return True
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        return False
    
    # def can_move(self, board, row, col, row1, col1):
    #     queen_pos = (row, col)
    #     if not (0 <= row1 < 8 and 0 <= col1 < 8):
    #         return False
    #     if abs(queen_pos[0] - row1) == abs(queen_pos[1] - col1) or row1 == queen_pos[0] or col1 == queen_pos[1]:
    #         return True
    #     return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    '''Класс слона. Пока что заглушка, которая может ходить в любую клетку.'''

    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if not correct_coords(row1, col1):
            return False
        piece1 = board.get_piece(row1, col1)
        if not (piece1 is None) and piece1.get_color() == self.color:
            return False
        if row - col == row1 - col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = col - row + r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        if row + col == row1 + col1:
            step = 1 if (row1 >= row) else -1
            for r in range(row + step, row1, step):
                c = row + col - r
                if not (board.get_piece(r, c) is None):
                    return False
            return True
        return False
    # def can_move(self, board, row, col, row1, col1):
    #     bishop_pos = (row, col)
    #     if not (0 <= row1 < 8 and 0 <= col1 < 8):
    #         return False
    #     if abs(bishop_pos[0] - row1) == abs(bishop_pos[1] - col1):
    #         return True
    #     return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


if __name__ == '__main__':
    main()

import pygame
import sys

# Инициализация Pygame
pygame.init()
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 300
CELL_SIZE = BOARD_SIZE // 3
MARGIN = (WIDTH - BOARD_SIZE) // 2
BOARD_Y = 150
PLAYER_X = 'X'
PLAYER_O = 'O'
EMPTY = ' '

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 180)
RED = (220, 60, 60)
GREEN = (60, 180, 110)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
BOARD_COLOR = (240, 240, 240)
GRID_COLOR = (100, 100, 100)

# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")
clock = pygame.time.Clock()

# Шрифты
font_large = pygame.font.SysFont('Arial', 48)
font_medium = pygame.font.SysFont('Arial', 36)
font_small = pygame.font.SysFont('Arial', 24)


class TicTacToe:
    def _init_(self):
        self.reset_game()

    def reset_game(self):
        """Сброс игры в начальное состояние"""
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.current_player = PLAYER_X
        self.game_over = False
        self.winner = None
        self.moves_count = 0

    def draw_board(self):
        """Отрисовка игрового поля как отдельной панели"""
        # Рисуем панель поля
        board_panel = pygame.Rect(MARGIN - 10, BOARD_Y - 10, BOARD_SIZE + 20, BOARD_SIZE + 20)
        pygame.draw.rect(screen, BOARD_COLOR, board_panel, border_radius=15)
        pygame.draw.rect(screen, BLUE, board_panel, 4, border_radius=15)

        # Рисуем сетку
        for i in range(1, 3):
            # Вертикальные линии
            pygame.draw.line(screen, GRID_COLOR,
                             (MARGIN + i * CELL_SIZE, BOARD_Y),
                             (MARGIN + i * CELL_SIZE, BOARD_Y + BOARD_SIZE), 3)
            # Горизонтальные линии
            pygame.draw.line(screen, GRID_COLOR,
                             (MARGIN, BOARD_Y + i * CELL_SIZE),
                             (MARGIN + BOARD_SIZE, BOARD_Y + i * CELL_SIZE), 3)

        # Рисуем символы
        for row in range(3):
            for col in range(3):
                cell_value = self.board[row][col]
                if cell_value != EMPTY:
                    x = MARGIN + col * CELL_SIZE + CELL_SIZE // 2
                    y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2

                    if cell_value == PLAYER_X:
                        # Рисуем крестик
                        color = RED
                        size = CELL_SIZE // 2 - 10
                        # Две диагональные линии
                        pygame.draw.line(screen, color,
                                         (x - size, y - size),
                                         (x + size, y + size), 6)
                        pygame.draw.line(screen, color,
                                         (x + size, y - size),
                                         (x - size, y + size), 6)
                    else:
                        # Рисуем нолик
                        color = GREEN
                        radius = CELL_SIZE // 2 - 10
                        pygame.draw.circle(screen, color, (x, y), radius, 6)

    def draw_info_panel(self):
        """Отрисовка информационной панели"""
        # Панель информации
        info_panel = pygame.Rect(20, 20, WIDTH - 40, 110)
        pygame.draw.rect(screen, LIGHT_BLUE, info_panel, border_radius=10)
        pygame.draw.rect(screen, BLUE, info_panel, 3, border_radius=10)

        # Заголовок
        title = font_medium.render("КРЕСТИКИ-НОЛИКИ", True, BLUE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 35))

        # Информация о текущем игроке
        if not self.game_over:
            player_text = f"Ход игрока: {self.current_player}"
            color = RED if self.current_player == PLAYER_X else GREEN
        elif self.winner:
            player_text = f"Победитель: {self.winner}!"
            color = RED if self.winner == PLAYER_X else GREEN
        else:
            player_text = "НИЧЬЯ!"
            color = BLUE

        player_surface = font_small.render(player_text, True, color)
        screen.blit(player_surface, (WIDTH // 2 - player_surface.get_width() // 2, 75))

        # Инструкция
        if not self.game_over:
            instruction = "Кликните на клетку для хода"
        else:
            instruction = "Нажмите R для новой игры"

        instr_surface = font_small.render(instruction, True, BLACK)
        screen.blit(instr_surface, (WIDTH // 2 - instr_surface.get_width() // 2, 105))

    def draw_coordinates(self):
        """Отрисовка координатной сетки"""
        # Подписи строк
        for i in range(3):
            text = font_small.render(str(i + 1), True, BLUE)
            screen.blit(text, (MARGIN - 30, BOARD_Y + i * CELL_SIZE + CELL_SIZE // 2 - 10))

        # Подписи столбцов
        for i in range(3):
            text = font_small.render(chr(65 + i), True, BLUE)  # A, B, C
            screen.blit(text, (MARGIN + i * CELL_SIZE + CELL_SIZE // 2 - 5, BOARD_Y - 30))

    def make_move(self, row, col):
        """Сделать ход"""
        if self.game_over or self.board[row][col] != EMPTY:
            return False

        self.board[row][col] = self.current_player
        self.moves_count += 1

        # Проверка на выигрыш
        if self.check_winner():
            self.winner = self.current_player
            self.game_over = True
        # Проверка на ничью
        elif self.moves_count == 9:
            self.game_over = True
        else:
            # Смена игрока
            self.current_player = PLAYER_O if self.current_player == PLAYER_X else PLAYER_X

        return True

    def check_winner(self):
        """Проверка победителя"""
        board = self.board

        # Проверка строк
        for row in board:
            if row[0] == row[1] == row[2] != EMPTY:
                return True

        # Проверка столбцов
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != EMPTY:
                return True

        # Проверка диагоналей
        if board[0][0] == board[1][1] == board[2][2] != EMPTY:
            return True
        if board[0][2] == board[1][1] == board[2][0] != EMPTY:
            return True

        return False

    def get_cell_from_pos(self, pos):
        """Получить координаты клетки из позиции мыши"""
        x, y = pos

        # Проверка, находится ли клик внутри поля
        if (MARGIN <= x <= MARGIN + BOARD_SIZE and
                BOARD_Y <= y <= BOARD_Y + BOARD_SIZE):

            col = (x - MARGIN) // CELL_SIZE
            row = (y - BOARD_Y) // CELL_SIZE

            if 0 <= row < 3 and 0 <= col < 3:
                return row, col

        return None, None


def main():
    game = TicTacToe()

    # Основной игровой цикл
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    row, col = game.get_cell_from_pos(event.pos)
                    if row is not None:
                        game.make_move(row, col)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Клавиша R для рестарта
                    game.reset_game()
                elif event.key == pygame.K_ESCAPE:  # ESC для выхода
                    running = False

        # Очистка экрана
        screen.fill(WHITE)

        # Отрисовка элементов
        game.draw_info_panel()
        game.draw_board()
        game.draw_coordinates()

        # Отображение координат при наведении
        mouse_pos = pygame.mouse.get_pos()
        row, col = game.get_cell_from_pos(mouse_pos)
        if row is not None and not game.game_over and game.board[row][col] == EMPTY:
            # Подсветка клетки
            highlight_rect = pygame.Rect(
                MARGIN + col * CELL_SIZE + 2,
                BOARD_Y + row * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            )
            pygame.draw.rect(screen, (255, 255, 200), highlight_rect, border_radius=5)

            # Отображение координат
            coord_text = f"{chr(65 + col)}{row + 1}"
            coord_surface = font_small.render(coord_text, True, BLUE)
            screen.blit(coord_surface, (mouse_pos[0] + 15, mouse_pos[1] - 20))

        # Отрисовка победы (подсветка выигрышной линии)
        if game.winner:
            # Проверка и подсветка выигрышной линии
            board = game.board
            winner = game.winner

            # Проверка строк
            for row in range(3):
                if board[row][0] == board[row][1] == board[row][2] == winner:
                    y = BOARD_Y + row * CELL_SIZE + CELL_SIZE // 2
                    pygame.draw.line(screen, (255, 215, 0),
                                     (MARGIN + 20, y),
                                     (MARGIN + BOARD_SIZE - 20, y), 8)
                    break
            if board[0][0] == board[1][1] == board[2][2] == winner:
                pygame.draw.line(screen, (255, 215, 0),
                                 (MARGIN + 20, BOARD_Y + 20),
                                 (MARGIN + BOARD_SIZE - 20, BOARD_Y + BOARD_SIZE - 20), 8)
            elif board[0][2] == board[1][1] == board[2][0] == winner:
                pygame.draw.line(screen, (255, 215, 0),
                                 (MARGIN + BOARD_SIZE - 20, BOARD_Y + 20),
                                 (MARGIN + 20, BOARD_Y + BOARD_SIZE - 20), 8)

                # Обновление экрана
            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
        sys.exit()

    if __name__ == "__main__":
        main()
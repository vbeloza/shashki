import pygame
import sys
import random


INITIAL_WIDTH, INITIAL_HEIGHT = 600, 700
WIDTH, HEIGHT = INITIAL_WIDTH, INITIAL_HEIGHT
SQUARE_SIZE = WIDTH // 8
LIGHT_BOARD = (138, 127, 142)
DARK_BOARD = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 102)
POSSIBLE_MOVE_COLOR = (144, 238, 144)
INFO_BG_COLOR = (220, 220, 220)
TEXT_COLOR = (70, 70, 70)
BUTTON_COLOR = (0, 120, 0)
BUTTON_HOVER_COLOR = (0, 120, 0)
SHADOW_COLOR = (100, 100, 100)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Шашки")


font = pygame.font.Font(None, 36)
font_large = pygame.font.Font(None, 48)  # Более крупный шрифт для заголовков
font_normal = pygame.font.Font(None, 36)  # Нормальный шрифт для основного текста
text_gap = 30


black_piece_img = pygame.image.load('black-pawn.png').convert_alpha()
white_piece_img = pygame.image.load('red-pawn.png').convert_alpha()

pygame.mixer.music.load('m.mp3')
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1)

def draw_frame():
    pygame.draw.rect(screen, (125, 125, 125), (30, 30, WIDTH - 60, HEIGHT - 60), 5)  # Рамка

def scale_images():
    global black_piece_img, white_piece_img, SQUARE_SIZE
    SQUARE_SIZE = WIDTH // 8
    black_piece_img = pygame.transform.scale(black_piece_img, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))
    white_piece_img = pygame.transform.scale(white_piece_img, (SQUARE_SIZE - 20, SQUARE_SIZE - 20))

scale_images()

board = [
    [0, 2, 0, 2, 0, 2, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0],
    [0, 2, 0, 2, 0, 2, 0, 2],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]
statistics = {
    'white_wins': 2,
    'black_wins': 0,
    'draws': 4
}

selected_piece = None
turn = 1
possible_moves = []
is_jumping = False
ai_difficulty = 0
game_mode = 0
game_state = 0

class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = (150, 150, 150)
        self.hover_color = (180, 180, 180)
        self.font_color = (50, 50, 50)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.action()
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.color = self.hover_color
            else:
                self.color = (150, 150, 150)

def scale_ui_elements():
    global menu_buttons, game_over_buttons, game_buttons, WIDTH, HEIGHT
    menu_buttons = [
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.2), 300, 50, "Играть с ИИ ", lambda: start_game(1, 0)),
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.4), 300, 50, "Играть вдвоем", lambda: start_game(2, 0)),
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.6), 300, 50, "Правила игры", lambda: show_rules()),
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.8), 300, 50, "Статистика", lambda: show_statistics())
    ]
    game_over_buttons = [
        Button(WIDTH // 2 - 100, int(HEIGHT * 0.8), 200, 50, "Назад", lambda: reset_and_menu())
    ]
    game_buttons = [
        Button(10, HEIGHT - 60, 100, 50, "Выход", lambda: return_to_menu()) # Кнопка во время игры
    ]

def reset_game():
    global board, selected_piece, turn, possible_moves, is_jumping
    board = [
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
    ]
    selected_piece = None
    turn = 1
    possible_moves = []
    is_jumping = False

def start_game(mode, difficulty):
    global game_state, ai_difficulty, game_mode
    ai_difficulty = difficulty
    game_mode = mode
    reset_game()
    game_state = 1
    scale_ui_elements()

def reset_and_menu():
    global game_state
    reset_game()
    game_state = 0
    scale_ui_elements()

def return_to_menu():
    global game_state
    reset_game()
    game_state = 0
    scale_ui_elements()

def show_rules():
    global game_state
    game_state = 3

def show_statistics():
    global game_state
    game_state = 4

def render_multiline_text(text, font, max_width):
    lines = []
    for line in text.splitlines():
        words = line.split(' ')
        current_line = ''
        for word in words:
            test_line = current_line + word + (' ' if current_line else '')
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + ' '
        if current_line:
            lines.append(current_line.strip())
    return lines

def draw_rules():
    screen.fill(INFO_BG_COLOR)
    draw_frame()

    header_surface = font_large.render("Правила игры в шашки", True, (0, 120, 0))  # Зеленый цвет
    screen.blit(header_surface, (WIDTH // 2 - header_surface.get_width() // 2, 40))

    rules_text = [
        "1. Игроки ходят по очереди.",
        "2. Шашки могут передвигаться на диагональные клетки.",
        "3. Если шашка достигает противоположного конца, она становится дамкой.",
        "4. Необходимо съедать шашки соперника, если это возможно.",
        "5. Игра заканчивается, когда один из игроков не имеет шашек.",
        "6. Игрок, который не может сделать ход, проигрывает."
    ]

    y_offset = 100
    max_height = HEIGHT - 100
    max_width = WIDTH - 60

    for line in render_multiline_text("\n".join(rules_text), font_normal, max_width):
        if y_offset > max_height:
            break

        text_surface = font_normal.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (50, y_offset))
        y_offset += text_gap

    for button in game_over_buttons:
        button.draw(screen)

def check_winner():
    global statistics
    white_pieces = 0
    black_pieces = 0
    for row in board:
        for piece in row:
            if piece == 1:
                white_pieces += 1
            elif piece == 2:
                black_pieces += 1

    if white_pieces == 0:
        statistics['black_wins'] += 1
        return 2
    elif black_pieces == 0:
        statistics['white_wins'] += 1
        return 1

    return 0


def check_for_draw():
    for row in range(8):
        for col in range(8):
            if board[row][col] == 1 or board[row][col] == 2:
                if get_possible_moves(row, col, board):
                    return False
    statistics['draws'] += 1
    return True


def draw_statistics():
    screen.fill(INFO_BG_COLOR)

    statistics_text = (
        f"Статистика:\n"
        f"Победы красных: {statistics['white_wins']}\n"
        f"Победы черных: {statistics['black_wins']}\n"
        f"Ничьи: {statistics['draws']}\n"
    )

    y_offset = 50
    max_height = HEIGHT - 100
    max_width = WIDTH - 100

    for line in render_multiline_text(statistics_text, font, max_width):
        if y_offset > max_height:
            break

        text_surface = font.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (50, y_offset))
        y_offset += 40
    for button in game_over_buttons:
        button.draw(screen)

menu_buttons = [
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.2), 300, 50, "Играть с ИИ ", lambda: start_game(1, 0)),
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.4), 300, 50, "Играть вдвоем", lambda: start_game(2, 0)),
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.6), 300, 50, "Правила игры", lambda: show_rules()),
        Button(WIDTH // 2 - 150, int(HEIGHT * 0.8), 300, 50, "Статистика", lambda: show_statistics())
    ]

game_over_buttons = [
    Button(WIDTH // 2 - 100, int(HEIGHT * 0.8), 200, 50, "Назад", lambda: reset_and_menu())
]

game_buttons = [
    Button(10, HEIGHT - 60, 150, 50, "Выход", lambda: return_to_menu()) # Кнопка во время игры
]

def draw_menu():
    screen.fill(INFO_BG_COLOR)
    for button in menu_buttons:
        button.draw(screen)

def draw_board():
    for row in range(8):
        for col in range(8):
            color = DARK_BOARD if (row + col) % 2 == 0 else LIGHT_BOARD
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if (row, col) in possible_moves:
                pygame.draw.rect(screen, POSSIBLE_MOVE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            if selected_piece == (row, col):
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            elif selected_piece is not None and (row, col) not in possible_moves and selected_piece != (row, col):
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill((0, 0, 0, 100))
                screen.blit(s, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_pieces():
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            x = col * SQUARE_SIZE + 10
            y = row * SQUARE_SIZE + 10

            if piece == 1:  # Красная шашка
                screen.blit(white_piece_img, (x, y))
                log_board_state()
            elif piece == 2:  # Черная шашка
                screen.blit(black_piece_img, (x, y))
                log_board_state()
            elif piece == 3:  # Красная дамка
                screen.blit(white_piece_img, (x, y))  # Используйте отдельное изображение дамки
                log_board_state()
            elif piece == 4:  # Черная дамка
                screen.blit(black_piece_img, (x, y))
                log_board_state()

def log_board_state():
    for row in board:
        print(' '.join(map(str, row)))
    print("---------")

def get_possible_jumps(row, col, board):
    jumps = []
    piece = board[row][col]

    if piece == 1 or piece == 3:  # Белые
        possible_directions = [(-2, -2), (-2, 2), (2, -2), (2, 2)] # добавили направления назад
        opponent_pieces = [2, 4]
    else:  # Черные
        possible_directions = [(2, -2), (2, 2), (-2, -2), (-2, 2)] # добавили направления назад
        opponent_pieces = [1, 3]

    for dr, dc in possible_directions:
        new_row = row + dr
        new_col = col + dc
        jumped_row = row + dr // 2
        jumped_col = col + dc // 2

        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == 0 and board[jumped_row][jumped_col] in opponent_pieces:
            jumps.append((new_row, new_col))
    return jumps


def get_possible_moves(row, col, board):
    moves = []
    piece = board[row][col]
    if piece == 0:
        return moves

    # Проверяем прыжки
    jumps = get_possible_jumps(row, col, board)
    if jumps:
        return jumps

    if turn == 1:  # Белые
        directions = [(-1, -1), (-1, 1)]
    else:  # Черные
        directions = [(1, -1), (1, 1)]

    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8 and board[new_row][new_col] == 0:
            moves.append((new_row, new_col))
    return moves

def handle_piece_click(pos):
    global selected_piece, possible_moves, turn, is_jumping, board

    col = pos[0] // SQUARE_SIZE
    row = pos[1] // SQUARE_SIZE

    if 0 <= row < 8 and 0 <= col < 8:
        piece = board[row][col]

        if selected_piece:
            if (row, col) in possible_moves:
                # Move the piece
                moved = move_piece(selected_piece, (row, col))

                if abs(selected_piece[0] - row) > 1:
                    #board[(selected_piece[0] + row) // 2][(selected_piece[1] + col) // 2] = 0 #Remove enemy piece
                    selected_piece = (row,col)
                    new_jumps = get_possible_jumps(selected_piece[0], selected_piece[1],board) #Get jumps

                    if new_jumps: #Check for more jumps
                        possible_moves = new_jumps #Can move again

                        return #return and dont run the others yet
                # Clear Selection and Swap Turn
                selected_piece = None
                possible_moves = []
                turn = 3- turn  # switch player
            elif piece == turn:
                selected_piece = (row, col)
                possible_moves = get_possible_moves(row, col, board)
            else:
                selected_piece = None
                possible_moves = []
        else:
            if piece == turn:
                selected_piece = (row, col)
                possible_moves = get_possible_moves(row, col, board)


def check_promotion(row, piece):
    if turn == 1 and row == 0 and piece == 1:
        return 3  # White becomes a queen
    if turn == 2 and row == 7 and piece == 2:
        return 4  # Black becomes a queen
    return piece

def move_piece(start_pos, end_pos):
    global board
    global turn
    global is_jumping

    start_row, start_col = start_pos
    end_row, end_col = end_pos

    piece_to_move = board[start_row][start_col]

    if abs(end_row - start_row) == 2 or abs(end_col - start_col) == 2:
        jumped_row = start_row + (end_row - start_row) // 2
        jumped_col = start_col + (end_col - start_col) // 2

        if (0 <= jumped_row < 8 and 0 <= jumped_col < 8):
            if (board[jumped_row][jumped_col] != 0 and
                    board[jumped_row][jumped_col] != piece_to_move):
                board[end_row][end_col] = piece_to_move
                board[start_row][start_col] = 0
                board[jumped_row][jumped_col] = 0  # Удаляем съеденную шашку
                is_jumping = True
                log_board_state()
                return True

    else:  # Обычный ход
        board[end_row][end_col] = piece_to_move
        board[start_row][start_col] = 0
        is_jumping = False
        log_board_state()
        return True
    log_board_state()
    return False


def evaluate_board(current_board, ai_turn):
    score = 0

    if ai_turn == 2:
        my_simple_piece = 2
        opponent_simple_piece = 1
    else:
        my_simple_piece = 1
        opponent_simple_piece = 2

    for row in range(8):
        for col in range(8):
            piece = current_board[row][col]
            if piece == my_simple_piece:
                score += 1
            elif piece == opponent_simple_piece:
                score -= 1

    return score

def is_protected(row, col, board, ai_turn):
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == ai_turn:
                return True
    return False

def minmax(current_board, depth, maximizing_player, ai_turn, alpha, beta):
    global turn, is_jumping, board #А вот и глобальная переменная
    #Если не указать - не будет работать как надо
    winner = check_winner(current_board) #Adding current board as argument
    if depth == 0 or winner != 0:
        return evaluate_board(current_board, ai_turn), None

    possible_moves = []
    for row in range(8):
        for col in range(8):
            if current_board[row][col] == ai_turn if maximizing_player else 3- ai_turn: #Ai_turn on maximizng otherwise not
                moves = get_possible_moves(row, col, current_board)
                possible_moves.extend([((row, col), move) for move in moves])

    if not possible_moves:
        if maximizing_player:
            return float('-inf'), None
        else:
            return float('inf'), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None

        for (start_row, start_col), (end_row, end_col) in possible_moves:
            temp_board = [row[:] for row in current_board] #Copy and create board
            temp_turn = turn
            board = [row[:] for row in temp_board] #И тут важно создать копию

            move_piece((start_row, start_col), (end_row, end_col))
            #move_piece((start_row, start_col), (end_row, end_col), temp_board)

            #Moving a variable doesn't create copy it reference

            evaluation, _ = minmax(temp_board, depth - 1, False, ai_turn, alpha, beta)
            if evaluation > max_eval:
                max_eval = evaluation
                best_move = ((start_row, start_col), (end_row, end_col))
            alpha = max(alpha, evaluation) #Update alphga
            if beta <= alpha: #Pruning
                break #Break out of for loop
            turn = temp_turn #Roll Back

        return max_eval, best_move

    else:
        min_eval = float('inf')
        best_move = None

        for (start_row, start_col), (end_row, end_col) in possible_moves:
            temp_board = [row[:] for row in current_board]
            temp_turn = turn
            board = [row[:] for row in temp_board]
            move_piece((start_row, start_col), (end_row, end_col))
            #move_piece((start_row, start_col), (end_row, end_col), temp_board)
            #Moving a variable doesn't create copy it reference

            evaluation, _ = minmax(temp_board, depth - 1, True, ai_turn, alpha, beta)

            if evaluation < min_eval:
                min_eval = evaluation
                best_move = ((start_row, start_col), (end_row, end_col))

            beta = min(beta, evaluation) #Update beta
            if beta <= alpha: #Pruning
                break #Break out of for loop
            turn = temp_turn #Rollback

        return min_eval, best_move

def ai_move():
    global board, turn

    ai_turn = 2  # Черные

    def make_ai_move(start_row, start_col):
        moves = get_possible_jumps(start_row, start_col, board)

        if moves:  # Прыжки есть, выполняем их
            end_row, end_col = random.choice(moves)  # Выбираем прыжок
            move_piece((start_row, start_col), (end_row, end_col))  # Делаем ход
            new_jumps = get_possible_jumps(end_row, end_col, board)
            if new_jumps:
                make_ai_move(end_row, end_col)

    # Поиск обязательных ходов
    possible_jumps_for_all_pieces = []
    for row in range(8):
        for col in range(8):
            if board[row][col] == ai_turn or board[row][col] == 4:  # 4 - это дамка
                jumps = get_possible_jumps(row, col, board)
                if jumps:
                    possible_jumps_for_all_pieces.append(((row, col), jumps))

    if possible_jumps_for_all_pieces:  # Если есть обязательные ходы
        (start_row, start_col), _ = random.choice(possible_jumps_for_all_pieces)
        make_ai_move(start_row, start_col)  # Делаем обязательный ход
        log_board_state()
        return

    # Если нет обязательных ходов, можно использовать минимакс
    best_move = minmax(board, 2, True, ai_turn, float('-inf'), float('inf'))[1]

    if best_move:
        (start_row, start_col), (end_row, end_col) = best_move
        move_piece((start_row, start_col), (end_row, end_col))  # Выполняем лучший ход

    turn = 3 - turn  # Смена игрока



def count_score(board):
    white_score = 0
    black_score = 0
    for row in board:
        for piece in row:
            if piece == 1:
                white_score += 1
            elif piece == 2:
                black_score += 1
    return white_score, black_score

def check_for_draw():
    for row in range(8):
        for col in range(8):
            if board[row][col] == 1 or board[row][col] == 2:
                if get_possible_moves(row, col, board):
                    return False
    return True

# Game End Logic
def check_winner(current_board=None):
    global statistics

    if current_board == None:
        current_board = board

    white_pieces = 0
    black_pieces = 0
    for row in current_board:
        for piece in row:
            if piece == 1 or piece == 3:
                white_pieces += 1
            elif piece == 2 or piece == 4:
                black_pieces += 1

    if white_pieces == 0:
        statistics['black_wins'] += 1
        return 2
    elif black_pieces == 0:
        statistics['white_wins'] += 1
        return 1

    return 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            SQUARE_SIZE = WIDTH // 8
            scale_images()
            scale_ui_elements()
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

        if game_state == 0:
            for button in menu_buttons:
                button.handle_event(event)
        elif game_state == 1:
            for button in game_buttons:
                button.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = (event.pos[0], event.pos[1])
                handle_piece_click(pos)
        elif game_state == 2:
            for button in game_over_buttons:
                button.handle_event(event)
        elif game_state == 3:
            for button in game_over_buttons:
                button.handle_event(event)
        elif game_state == 4:
            for button in game_over_buttons:
                button.handle_event(event)

    if game_state == 0:
        draw_menu()
    elif game_state == 1:
        winner = check_winner()
        if winner != 0:
            game_state = 2
        elif check_for_draw():
            game_state = 2
            winner = 3
        else:
            if game_mode == 1 and turn == 2:  # Ход ИИ
                ai_move()

        screen.fill(INFO_BG_COLOR)
        draw_board()
        draw_pieces()

        for button in game_buttons:
            button.draw(screen)

        white_score, black_score = count_score(board)
        if winner == 0:
            text = f"Ход: {'Красные' if turn == 1 else 'Черные'}"
            text_1 = f'Красные: {white_score} Черные: {black_score}'
        elif winner == 1:
            text = f"Красные победили!"
            text_1 = f'Красные: {white_score} Черные: {black_score}'
        elif winner == 2:
            text = f"Черные победили!"
            text_1 = f'Красные: {white_score} Черные: {black_score}'
        else:
            text = f"Ничья!"
            text_1 = f'Красные: {white_score} Черные: {black_score}'

        text_surface = font.render(text, True, TEXT_COLOR)
        text_surface1 = font.render(text_1, True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, WIDTH + (HEIGHT - WIDTH) // 2 ))
        text_rect1 = text_surface1.get_rect(center=(WIDTH // 2, WIDTH + (HEIGHT - WIDTH) // 2 - 30))
        screen.blit(text_surface, text_rect)
        screen.blit(text_surface1, text_rect1)

    elif game_state == 2:
        screen.fill(INFO_BG_COLOR)
        if winner == 1:
            text = font.render("Красные победили!", True, TEXT_COLOR)
        elif winner == 2:
            text = font.render("Черные победили!", True, TEXT_COLOR)
        else:
            text = font.render("Ничья", True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        for button in game_over_buttons:
            button.draw(screen)

    elif game_state == 3:
        draw_rules()

    elif game_state == 4:
        draw_statistics()

    pygame.display.flip()

pygame.mixer.music.stop()
pygame.quit()
sys.exit()
import pygame
import sys
import random

# Constants
WIDTH, HEIGHT = 300, 300
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 224)
CIRCLE_COLOR = (0, 0, 255)
CROSS_COLOR = (255, 0, 0)
CIRCLE_RADIUS = 15
LINE_WIDTH = 5
DOT_RADIUS = 7

# Intersection points
INTERSECTIONS = [(50, 50), (150, 50), (250, 50), (50, 150), (150, 150), (250, 150), (50, 250), (150, 250), (250, 250)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Three Men's Morris")
screen.fill(BG_COLOR)

# Global Variables
board = [' ' for _ in range(9)]
player_turn = 'X'
ai_turn = 'O'
current_turn = player_turn
moves = {'X': 0, 'O': 0}
phase = 'placement'
selected_piece = None

def draw_board():
    # Draw lines
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[0], INTERSECTIONS[2], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[3], INTERSECTIONS[5], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[6], INTERSECTIONS[8], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[0], INTERSECTIONS[6], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[1], INTERSECTIONS[7], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[2], INTERSECTIONS[8], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[0], INTERSECTIONS[8], LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, INTERSECTIONS[2], INTERSECTIONS[6], LINE_WIDTH)

    # Draw dots
    for point in INTERSECTIONS:
        pygame.draw.circle(screen, LINE_COLOR, point, DOT_RADIUS)

def draw_pieces():
    for i, spot in enumerate(board):
        if spot == 'O':
            pygame.draw.circle(screen, CIRCLE_COLOR, INTERSECTIONS[i], CIRCLE_RADIUS, LINE_WIDTH)
        elif spot == 'X':
            pygame.draw.line(screen, CROSS_COLOR, (INTERSECTIONS[i][0] - 15, INTERSECTIONS[i][1] - 15), 
                             (INTERSECTIONS[i][0] + 15, INTERSECTIONS[i][1] + 15), LINE_WIDTH)
            pygame.draw.line(screen, CROSS_COLOR, (INTERSECTIONS[i][0] - 15, INTERSECTIONS[i][1] + 15), 
                             (INTERSECTIONS[i][0] + 15, INTERSECTIONS[i][1] - 15), LINE_WIDTH)

def place_piece(index):
    global current_turn, phase
    if board[index] == ' ':
        board[index] = current_turn
        moves[current_turn] += 1
        if moves[player_turn] == 3 and moves[ai_turn] == 3:
            phase = 'movement'
        return True
    return False

def move_piece(start_index, end_index):
    global current_turn
    if board[start_index] == current_turn and board[end_index] == ' ':
        if abs(start_index - end_index) in [1, 3]:  # Check if move is to an adjacent cell
            if (start_index % 3 == end_index % 3) or (start_index // 3 == end_index // 3):  # Ensure same row or column
                board[start_index] = ' '
                board[end_index] = current_turn
                screen.fill(BG_COLOR)  # Clear the screen
                draw_board()  # Redraw the board
                draw_pieces()  # Redraw the pieces
                pygame.display.update()  # Update the display
                return True
    return False


def check_win():
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] != ' ':
            return True
    return False

def switch_turn():
    global current_turn
    current_turn = ai_turn if current_turn == player_turn else player_turn

def get_index_from_mouse(pos):
    for index, point in enumerate(INTERSECTIONS):
        if abs(pos[0] - point[0]) < 20 and abs(pos[1] - point[1]) < 20:
            return index
    return None

def ai_move():
    global selected_piece
    if phase == 'placement':
        empty_indices = [i for i, spot in enumerate(board) if spot == ' ']
        if empty_indices:
            place_piece(random.choice(empty_indices))
    elif phase == 'movement':
        own_indices = [i for i, spot in enumerate(board) if spot == ai_turn]
        random.shuffle(own_indices)
        for start in own_indices:
            # Check all valid adjacent moves
            adjacent_indices = []
            if start % 3 > 0:
                adjacent_indices.append(start - 1)  # Left
            if start % 3 < 2:
                adjacent_indices.append(start + 1)  # Right
            if start // 3 > 0:
                adjacent_indices.append(start - 3)  # Up
            if start // 3 < 2:
                adjacent_indices.append(start + 3)  # Down
            valid_moves = [idx for idx in adjacent_indices if board[idx] == ' ']
            if valid_moves:
                move_piece(start, random.choice(valid_moves))
                break

draw_board()

# Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and current_turn == player_turn:
            pos = event.pos
            index = get_index_from_mouse(pos)
            if index is not None:
                if phase == 'placement':
                    if place_piece(index):
                        if check_win():
                            draw_pieces()
                            pygame.display.update()
                            print(f"Player {current_turn} wins!")
                            pygame.time.wait(2000)
                            pygame.quit()
                            sys.exit()
                        switch_turn()
                elif phase == 'movement':
                    if selected_piece is None and board[index] == current_turn:
                        selected_piece = index
                    elif selected_piece is not None:
                        if move_piece(selected_piece, index):
                            if check_win():
                                draw_pieces()
                                pygame.display.update()
                                print(f"Player {current_turn} wins!")
                                pygame.time.wait(2000)
                                pygame.quit()
                                sys.exit()
                            switch_turn()
                        selected_piece = None
            screen.fill(BG_COLOR)
            draw_board()
            draw_pieces()
            pygame.display.update()

    if current_turn == ai_turn:
        pygame.time.wait(500)  # Add a small delay for AI moves
        ai_move()
        if check_win():
            draw_pieces()
            pygame.display.update()
            print(f"Player {current_turn} wins!")
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        switch_turn()
        screen.fill(BG_COLOR)
        draw_board()
        draw_pieces()
        pygame.display.update()

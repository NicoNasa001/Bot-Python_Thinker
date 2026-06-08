# ============================================
# BOT IA AJEDREZ REALISTA
# ============================================

import chess
import berserk
import random
import json
import os
import time

# ============================================
# TOKEN LICHESS
# ============================================

TOKEN = "lip_LIkvBy0CYUWQAJrv8Q0O"

# ============================================
# CONECTAR A LICHESS
# ============================================

session = berserk.TokenSession(TOKEN)

client = berserk.Client(session)

print("===================================")
print("BOT CONECTADO A LICHESS")
print("===================================")

# ============================================
# PERSONALIDAD
# ============================================

PERSONALITY = "aggressive"

# aggressive
# defensive
# positional
# chaotic

# ============================================
# CENTRO
# ============================================

CENTER_SQUARES = [

    chess.E4,
    chess.D4,
    chess.E5,
    chess.D5
]

# ============================================
# CEREBRO
# ============================================

brain = {

    "pawn": 100,
    "knight": 320,
    "bishop": 330,
    "rook": 500,
    "queen": 900
}

piece_values = {

    chess.PAWN: brain["pawn"],
    chess.KNIGHT: brain["knight"],
    chess.BISHOP: brain["bishop"],
    chess.ROOK: brain["rook"],
    chess.QUEEN: brain["queen"],
    chess.KING: 20000
}

# ============================================
# TABLAS POSICIONALES
# ============================================

pawn_table = [

     0, 0, 0, 0, 0, 0, 0, 0,
     5,10,10,-20,-20,10,10, 5,
     5,-5,-10,0,0,-10,-5, 5,
     0,0,0,20,20,0,0,0,
     5,5,10,25,25,10,5,5,
     10,10,20,30,30,20,10,10,
     50,50,50,50,50,50,50,50,
     0,0,0,0,0,0,0,0
]

knight_table = [

    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,0,5,5,0,-20,-40,
    -30,5,10,15,15,10,5,-30,
    -30,0,15,20,20,15,0,-30,
    -30,5,15,20,20,15,5,-30,
    -30,0,10,15,15,10,0,-30,
    -40,-20,0,0,0,0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

bishop_table = [

    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,5,0,0,0,0,5,-10,
    -10,10,10,10,10,10,10,-10,
    -10,0,10,10,10,10,0,-10,
    -10,5,5,10,10,5,5,-10,
    -10,0,5,10,10,5,0,-10,
    -10,0,0,0,0,0,0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

rook_table = [

     0,0,0,5,5,0,0,0,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
    -5,0,0,0,0,0,0,-5,
     5,10,10,10,10,10,10,5,
     0,0,0,0,0,0,0,0
]

queen_table = [

    -20,-10,-10,-5,-5,-10,-10,-20,
    -10,0,0,0,0,0,0,-10,
    -10,0,5,5,5,5,0,-10,
    -5,0,5,5,5,5,0,-5,
     0,0,5,5,5,5,0,-5,
    -10,5,5,5,5,5,0,-10,
    -10,0,5,0,0,0,0,-10,
    -20,-10,-10,-5,-5,-10,-10,-20
]

king_table = [

    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
     20,20,0,0,0,0,20,20,
     20,30,10,0,0,10,30,20
]

# ============================================
# CARGAR CEREBRO
# ============================================

def load_brain():

    global brain
    global piece_values

    if os.path.exists("brain.json"):

        with open("brain.json", "r") as file:

            brain = json.load(file)

        print("CEREBRO CARGADO")

    else:

        print("NUEVO CEREBRO")

    piece_values = {

        chess.PAWN: brain["pawn"],
        chess.KNIGHT: brain["knight"],
        chess.BISHOP: brain["bishop"],
        chess.ROOK: brain["rook"],
        chess.QUEEN: brain["queen"],
        chess.KING: 20000
    }

# ============================================
# GUARDAR CEREBRO
# ============================================

def save_brain():

    with open("brain.json", "w") as file:

        json.dump(
            brain,
            file,
            indent=4
        )

# ============================================
# APRENDER
# ============================================

def learn(result):

    print("IA APRENDIENDO")

    if result == "1-0":

        brain["knight"] += random.randint(1, 3)
        brain["bishop"] += random.randint(1, 3)

    elif result == "0-1":

        brain["rook"] += random.randint(1, 3)

    else:

        brain["pawn"] += 1

    brain["pawn"] = max(50, min(200, brain["pawn"]))
    brain["knight"] = max(200, min(500, brain["knight"]))
    brain["bishop"] = max(200, min(500, brain["bishop"]))
    brain["rook"] = max(300, min(800, brain["rook"]))
    brain["queen"] = max(500, min(1500, brain["queen"]))

    save_brain()

    load_brain()

    print(brain)

# ============================================
# POSICIONAL
# ============================================

def get_positional_value(piece, square):

    if piece.piece_type == chess.PAWN:
        table = pawn_table

    elif piece.piece_type == chess.KNIGHT:
        table = knight_table

    elif piece.piece_type == chess.BISHOP:
        table = bishop_table

    elif piece.piece_type == chess.ROOK:
        table = rook_table

    elif piece.piece_type == chess.QUEEN:
        table = queen_table

    elif piece.piece_type == chess.KING:
        table = king_table

    else:
        return 0

    if piece.color == chess.WHITE:
        return table[square]
    else:
        return table[chess.square_mirror(square)]

# ============================================
# PEONES DOBLADOS
# ============================================

def doubled_pawns(board, color):

    files = [0] * 8

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece:

            if piece.piece_type == chess.PAWN:

                if piece.color == color:

                    file = chess.square_file(square)

                    files[file] += 1

    penalty = 0

    for count in files:

        if count > 1:
            penalty += (count - 1) * 20

    return penalty

# ============================================
# ATAQUE AL REY
# ============================================

def king_attack(board, color):

    enemy_king = board.king(not color)

    if enemy_king is None:
        return 0

    score = 0

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece and piece.color == color:

            distance = chess.square_distance(
                square,
                enemy_king
            )

            score += max(0, 7 - distance)

    return score

# ============================================
# EVALUAR
# ============================================

def evaluate_board(board):

    if board.is_checkmate():

        if board.turn:
            return -999999
        else:
            return 999999

    if board.is_stalemate():
        return 0

    score = 0

    # MATERIAL

    for square in chess.SQUARES:

        piece = board.piece_at(square)

        if piece:

            value = piece_values[piece.piece_type]

            positional = get_positional_value(
                piece,
                square
            )

            if piece.color == chess.WHITE:
                score += value + positional
            else:
                score -= value + positional

    # CENTRO

    for square in CENTER_SQUARES:

        piece = board.piece_at(square)

        if piece:

            if piece.color == chess.WHITE:
                score += 25
            else:
                score -= 25

    # DESARROLLO

    white_knights = [

        board.piece_at(chess.B1),
        board.piece_at(chess.G1)
    ]

    black_knights = [

        board.piece_at(chess.B8),
        board.piece_at(chess.G8)
    ]

    for knight in white_knights:

        if knight and knight.piece_type == chess.KNIGHT:
            score -= 15

    for knight in black_knights:

        if knight and knight.piece_type == chess.KNIGHT:
            score += 15

    # ENROQUE

    if not board.has_kingside_castling_rights(chess.WHITE):
        score += 40

    if not board.has_kingside_castling_rights(chess.BLACK):
        score -= 40

    # PEONES DOBLADOS

    score -= doubled_pawns(board, chess.WHITE)
    score += doubled_pawns(board, chess.BLACK)

    # ATAQUE AL REY

    score += king_attack(board, chess.WHITE)
    score -= king_attack(board, chess.BLACK)

    # MOVILIDAD

    mobility = len(list(board.legal_moves))

    if board.turn == chess.WHITE:
        score += mobility * 2
    else:
        score -= mobility * 2

    return score

# ============================================
# SCORE MOVIMIENTO
# ============================================

def move_score(board, move):

    score = 0

    if board.is_capture(move):

        victim = board.piece_at(move.to_square)

        attacker = board.piece_at(move.from_square)

        if victim and attacker:

            score += (
                piece_values[victim.piece_type]
                - piece_values[attacker.piece_type]
            )

    if board.gives_check(move):
        score += 50

    # PERSONALIDAD

    if PERSONALITY == "aggressive":

        if board.is_capture(move):
            score += 50

        if board.gives_check(move):
            score += 100

    return score

# ============================================
# MINIMAX
# ============================================

def minimax(board, depth, alpha, beta, maximizing):

    if depth == 0 or board.is_game_over():

        return evaluate_board(board)

    moves = list(board.legal_moves)

    random.shuffle(moves)

    moves = sorted(
        moves,
        key=lambda move: move_score(board, move),
        reverse=True
    )

    if maximizing:

        max_eval = -999999

        for move in moves:

            board.push(move)

            evaluation = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                False
            )

            board.pop()

            max_eval = max(max_eval, evaluation)

            alpha = max(alpha, evaluation)

            if beta <= alpha:
                break

        return max_eval

    else:

        min_eval = 999999

        for move in moves:

            board.push(move)

            evaluation = minimax(
                board,
                depth - 1,
                alpha,
                beta,
                True
            )

            board.pop()

            min_eval = min(min_eval, evaluation)

            beta = min(beta, evaluation)

            if beta <= alpha:
                break

        return min_eval

# ============================================
# MEJOR MOVIMIENTO
# ============================================

def get_best_move(board, depth):

    moves = list(board.legal_moves)

    random.shuffle(moves)

    if random.random() < 0.10:

        return random.choice(moves)

    best_move = None

    if board.turn == chess.WHITE:
        best_value = -999999
    else:
        best_value = 999999

    for move in moves:

        board.push(move)

        value = minimax(
            board,
            depth - 1,
            -1000000,
            1000000,
            board.turn == chess.WHITE
        )

        board.pop()

        if board.turn == chess.WHITE:

            if value > best_value:

                best_value = value
                best_move = move

        else:

            if value < best_value:

                best_value = value
                best_move = move

    return best_move

# ============================================
# CARGAR CEREBRO
# ============================================

load_brain()

# ============================================
# LOOP PRINCIPAL
# ============================================

for event in client.bots.stream_incoming_events():

    print(event)

    # DESAFÍO

    if event["type"] == "challenge":

        challenge = event["challenge"]

        challenge_id = challenge["id"]

        print("DESAFÍO RECIBIDO")

        client.bots.accept_challenge(
            challenge_id
        )

    # PARTIDA

    elif event["type"] == "gameStart":

        game_id = event["game"]["id"]

        print("PARTIDA INICIADA")

        board = chess.Board()

        bot_color = None

        for game_event in client.bots.stream_game_state(game_id):

            print(game_event)

            # INFORMACIÓN COMPLETA

            if game_event["type"] == "gameFull":

                white_id = game_event["white"].get("id", "")
                black_id = game_event["black"].get("id", "")

                my_id = client.account.get()["id"]

                if my_id == white_id:
                    bot_color = chess.WHITE
                else:
                    bot_color = chess.BLACK

                moves = game_event["state"]["moves"]

            # ESTADO NORMAL

            elif game_event["type"] == "gameState":

                moves = game_event["moves"]

                status = game_event.get("status")

                if status != "started":

                    print("PARTIDA TERMINADA")

                    winner = game_event.get("winner")

                    if winner == "white":
                        result = "1-0"

                    elif winner == "black":
                        result = "0-1"

                    else:
                        result = "1/2-1/2"

                    print("RESULTADO:", result)

                    learn(result)

                    break

            else:
                continue

            # RECONSTRUIR TABLERO

            board.reset()

            if moves != "":

                for move in moves.split():

                    board.push_uci(move)

            # TURNO DEL BOT

            if board.turn != bot_color:
                continue

            print("IA PENSANDO...")

            move = get_best_move(board, 3)

            if move:

                print("BOT JUEGA:", move)

                try:

                    client.bots.make_move(
                        game_id,
                        move.uci()
                    )

                except Exception as e:

                    print("ERROR:")
                    print(e)

                    while True:

                        try:

                            print("REINTENTANDO...")

                            client.bots.make_move(
                                game_id,
                                move.uci()
                            )

                            print("REINTENTO EXITOSO")
                            break

                        

                        except Exception as e2:

                            print("SIGUE FALLANDO:")
                            print(e2)

                            time.sleep(5)
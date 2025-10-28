"""
eval.py
Very small evaluation: material balance with simple piece values.
Expand to include mobility, king safety, pawns, piece-square tables, etc.
"""

import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate(board: chess.Board) -> float:
    """
    Return evaluation from side-to-move's perspective (positive = advantage).
    Uses simple material balance.
    """
    white_score = 0
    black_score = 0
    for piece_type in PIECE_VALUES:
        value = PIECE_VALUES[piece_type]
        white_score += len(board.pieces(piece_type, chess.WHITE)) * value
        black_score += len(board.pieces(piece_type, chess.BLACK)) * value

    score = white_score - black_score
    # If it's black to move, invert so value is always from side-to-move perspective
    return score if board.turn == chess.WHITE else -score

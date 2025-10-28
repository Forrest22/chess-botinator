"""
search.py
Contains Search class with a simple negamax alpha-beta implementation and iterative deepening.
See https://www.chessprogramming.org/Negamax
"""

import time
import math
import chess

from eval import evaluate

class Search:
    def __init__(self):
        self.nodes = 0

    def clear(self):
        self.nodes = 0

    def find_best_move(self, board: chess.Board, time_budget: float = 0.1, max_depth: int = None, stop_event=None):
        """
        Iterative deepening loop up to max_depth or until time_budget elapsed.
        Returns a chess.Move (from python-chess) or None.
        """
        start_time = time.time()
        best_move = None
        # Set a safe max depth if not provided
        if max_depth is None:
            global_max_depth = 4
        else:
            global_max_depth = max_depth

        for depth in range(1, global_max_depth + 1):
            self.nodes = 0
            try:
                score, move = self._negamax_root(board, depth, start_time, time_budget, stop_event)
                if move is not None:
                    best_move = move
            except TimeoutError:
                break
            if stop_event and stop_event.is_set():
                break
            # small time check
            if time.time() - start_time > time_budget:
                break
        return best_move

    def _negamax_root(self, board, depth, start_time, time_budget, stop_event):
        best_score = -math.inf
        best_move = None
        alpha = -math.inf
        beta = math.inf
        for move in board.legal_moves:
            if stop_event and stop_event.is_set():
                raise TimeoutError()
            board.push(move)
            score = -self._negamax(board, depth - 1, -beta, -alpha, start_time, time_budget, stop_event)
            board.pop()
            if score > best_score:
                best_score = score
                best_move = move
            if score > alpha:
                alpha = score
            # time check
            if time.time() - start_time > time_budget:
                raise TimeoutError()
        return best_score, best_move

    def _negamax(self, board, depth, alpha, beta, start_time, time_budget, stop_event):
        if stop_event and stop_event.is_set():
            raise TimeoutError()
        self.nodes += 1
        if depth == 0 or board.is_game_over():
            return evaluate(board)

        max_eval = -math.inf
        for move in board.legal_moves:
            if time.time() - start_time > time_budget:
                raise TimeoutError()
            board.push(move)
            val = -self._negamax(board, depth - 1, -beta, -alpha, start_time, time_budget, stop_event)
            board.pop()
            if val > max_eval:
                max_eval = val
            if val > alpha:
                alpha = val
            if alpha >= beta:
                break  # beta cutoff
        return max_eval

#!/usr/bin/env python3
"""
engine.py
Simple UCI-compatible entrypoint. Talks UCI with the frontend (lichess-bot expects a UCI engine).
Relies on python-chess for board representation and move legality.
"""

import sys
import time
import threading

import chess

from search import Search

ENGINE_NAME = "chess-botinator"
ENGINE_AUTHOR = "Forrest22"

class UCIEngine:
    def __init__(self):
        self.board = chess.Board()
        self.search = Search()
        self.ponder = False
        self.stop_event = threading.Event()

    def loop(self):
        """Main UCI loop reading stdin lines and responding on stdout."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.strip()
                if line == "":
                    continue
                parts = line.split()
                cmd = parts[0]

                if cmd == "uci":
                    self.id()
                    print("uciok", flush=True)

                elif cmd == "isready":
                    print("readyok", flush=True)

                elif cmd == "ucinewgame":
                    self.board.reset()
                    # Reset internal search state if needed
                    self.search.clear()

                elif cmd == "position":
                    # position [fen <fenstring> | startpos ]  moves <move1> ... <moveN>
                    self._handle_position(parts[1:])

                elif cmd == "go":
                    args = parts[1:]
                    self._handle_go(args)

                elif cmd == "stop":
                    self.stop_event.set()

                elif cmd == "quit" or cmd == "exit":
                    return

                elif cmd == "d":
                    # debug print board for human
                    print("Command: ", cmd)
                    print(self.board, flush=True)

                else:
                    # unsupported commands are ignored with no crash
                    print("Command not supported")
                    pass

            except Exception as e:
                # Keep engine alive for debugging; log to stderr
                print(f"info string exception: {e}", file=sys.stderr, flush=True)

    def id(self):
        print(f"id name {ENGINE_NAME}", flush=True)
        print(f"id author {ENGINE_AUTHOR}", flush=True)

    def _handle_position(self, tokens):
        # tokens start after 'position'
        idx = 0
        if tokens[0] == "startpos":
            self.board.reset()
            idx = 1
        elif tokens[0] == "fen":
            # read fen until 'moves' or end
            fen_parts = []
            idx = 1
            while idx < len(tokens) and tokens[idx] != "moves":
                fen_parts.append(tokens[idx])
                idx += 1
            fen = " ".join(fen_parts)
            self.board.set_fen(fen)
        else:
            # unknown, ignore
            return

        # apply moves if present
        if idx < len(tokens) and tokens[idx] == "moves":
            idx += 1
            while idx < len(tokens):
                mv = tokens[idx]
                try:
                    move = self.board.parse_uci(mv)
                    self.board.push(move)
                except ValueError:
                    # illegal move string - ignore but report
                    print(f"info string illegal move ignored: {mv}", file=sys.stderr, flush=True)
                idx += 1

    def _handle_go(self, args):
        # Very small parsing: support 'movetime <ms>' and 'wtime/btime <ms>' optionally 'depth <d>'
        movetime = None
        wtime = None
        btime = None
        depth = None

        i = 0
        while i < len(args):
            if args[i] == "movetime" and i + 1 < len(args):
                movetime = int(args[i + 1])
                i += 2
            elif args[i] == "wtime" and i + 1 < len(args):
                wtime = int(args[i + 1])
                i += 2
            elif args[i] == "btime" and i + 1 < len(args):
                btime = int(args[i + 1])
                i += 2
            elif args[i] == "depth" and i + 1 < len(args):
                depth = int(args[i + 1])
                i += 2
            else:
                i += 1

        # Determine a time budget in seconds (simple heuristic)
        if movetime is not None:
            time_budget = movetime / 1000.0
        else:
            # if no movetime, allocate a small default or based on clock
            if (self.board.turn == chess.WHITE and wtime is not None) or (self.board.turn == chess.BLACK and btime is not None):
                # naive: use 0.5% of remaining time + 0.05s
                remaining = wtime if self.board.turn == chess.WHITE else btime
                time_budget = max(0.05, remaining / 1000.0 * 0.005)
            else:
                time_budget = 0.1

        # Start search in separate thread so 'stop' can set event (UCI expects stop to work)
        self.stop_event.clear()
        search_thread = threading.Thread(target=self._run_search, args=(time_budget, depth))
        search_thread.start()
        # We don't join here; UCI expects engine to print bestmove when ready. We will join to ensure output delivered before function returns
        search_thread.join()

    def _run_search(self, time_budget, depth):
        start = time.time()
        best_move = None
        try:
            best_move = self.search.find_best_move(self.board, time_budget=time_budget, max_depth=depth, stop_event=self.stop_event)
        except Exception as e:
            print(f"info string search error: {e}", file=sys.stderr, flush=True)
        if best_move is None:
            # fallback: choose any legal move (shouldn't happen)
            legal = list(self.board.legal_moves)
            if legal:
                best_move = legal[0]
        if best_move is None:
            print("bestmove 0000", flush=True)
        else:
            print(f"bestmove {best_move.uci()}", flush=True)


if __name__ == "__main__":
    engine = UCIEngine()
    engine.loop()

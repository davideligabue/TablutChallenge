from board import *
import numpy as np
import unittest


'''
Tests for class Board
'''


class TestBoard(unittest.TestCase):
    def setUp(self):
        # Initialize a standard board setup
        self.state = {
            'turn': 'WHITE',
            'board': np.array([
                ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
                ['BLACK', 'BLACK', 'WHITE', 'WHITE', 'KING', 'WHITE', 'WHITE', 'BLACK', 'BLACK'],
                ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'BLACK', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY']
            ])
        }
        self.board = Board(self.state)
    
    def test_valid_move_king_escape(self):
        # Move the King to an escape tile and check if it results in White's win
        move = Move((4, 4), (0, 1), KING)
        self.assertTrue(self.board.is_valid_move(move))
        self.board.apply_moves([move])
        self.assertTrue(self.board.is_king_escaped())

    def test_capture_white_piece(self):
        # Simulate a Black piece surrounding a White piece and capturing it
        move = Move((3, 0), (3, 4), BLACK)  # Move Black to capture White
        self.board.apply_moves([move])
        capture_result = self.board.is_a_capture_move(move)
        self.assertTrue(capture_result[0])
        self.assertEqual(self.board.get_cell((3, 4)), EMPTY)  # White piece should be captured

    def test_king_capture_in_castle(self):
        # Surround the King in the castle to simulate a capture
        self.board.apply_moves([
            Move((3, 4), (4, 3), BLACK),  # Move Black around King
            Move((4, 5), (4, 6), BLACK),
            Move((5, 4), (4, 5), BLACK),
            Move((4, 2), (4, 3), BLACK)
        ])
        self.assertTrue(self.board.is_king_captured())

# Uncomment the following line to run tests
unittest.main()

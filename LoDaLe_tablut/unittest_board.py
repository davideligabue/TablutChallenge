from board import *
import numpy as np
import unittest


'''
Tests for class Board
'''


class TestBoard(unittest.TestCase):

    def initialize_Board(self) -> Board:
        state = {
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
        return Board(state)
    
    def initialize_Board_simple_case(self) -> Board:
        state = {
            'turn': 'WHITE',
            'board': np.array([
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'KING', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY']
            ])
        }
        return Board(state)# 4,5 -> 1,5 white | 8,5 -> 2,5  black 
    
    def test_king_position(self):
        board = self.initialize_Board()
        self.assertEqual(board.king, CASTLE, "Bad king initializazion in starting position")
        board = self.initialize_Board_simple_case()
        self.assertEqual(board.king, (2,3), "Bad king initialization in different position")

    def test_performing_checks(self):
        board = self.initialize_Board()
        # is_orthogonal and is_within_bounds check
        self.assertRaises(Exception, lambda: Move((0,3),(12,3),BLACK), "Should throw exception because out of bound move")
        self.assertRaises(Exception, lambda: Move((0,3),(1,2),BLACK), "Should throw exception because not orthogonal")
        self.assertRaises(Exception, lambda: Move((0,3),(1,3),"wrong piece"), "Should throw exception because 'piece' is incorrect")
        self.assertIsInstance(Move((0,3),(2,3),BLACK), Move, "A correct Move initialization")
        # get_cell check
        self.assertRaises(Exception, lambda: board.get_cell((9,7)), "Should throw exception because checks a cell out of bounds")
        self.assertEqual(board.get_cell((3,8)), BLACK, "Incorrect value returned by get_cell")
        # is_adjacent check
        self.assertTrue(board.is_adjacent((5,6),(4,6)), "is_adjacent should have returned True")
        self.assertFalse(board.is_adjacent((5,6),(4,7)), "is_adjacent should have returned False")
        # is_valid_move check
        board = self.initialize_Board_simple_case()
        self.assertTrue(board.is_valid_move(Move((0,5),(0,3),BLACK)), "Black piece must be able to move in camps if already inside")
        self.assertTrue(board.is_valid_move(Move(board.king,CASTLE,KING)), "King should be able to move in CASTLE")
        self.assertFalse(board.is_valid_move(Move((4,2),(4,1),BLACK)), "Black can't move in camps it was outside")
        self.assertFalse(board.is_valid_move(Move((4,5),(3,5),BLACK)), "If move.piece is Black you cannot move a white piece")
        self.assertFalse(board.is_valid_move(Move((4,5),CASTLE,WHITE)), "Only king should be able to move in CASTLE")


    def test_initial_ring_occupation(self):
        board = self.initialize_Board()
        occupation_obj = {
            "str":"WEWEWEWE",
            "cells" : [(4,3),(5,3),(5,4),(5,5),(4,5),(3,5),(3,4),(3,3)]
        }
        self.assertDictEqual(occupation_obj, board.ring_occupation((4,4), 1), "Error object ring occupation")
        occupation_str = "EEEWWKWWEEEEBBBE"
        self.assertEqual(occupation_str, board.ring_occupation((2,4), 2)["str"], "Error string of ring (n=2) occupation")

    def test_move_pieces_around(self):
        board = self.initialize_Board_simple_case()
        # 4,5 -> 1,5 white | 8,5 -> 2,5  black 
        move_seq = board.apply_moves([Move((4,5),(1,5),WHITE), Move((8,5),(2,5),BLACK)])
        self.assertEqual(len(move_seq), 3, "Wrong sequence of moves returned by apply_moves when capturing a checker")
        new_state = np.array([
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'KING', 'EMPTY', 'WHITE', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['BLACK', 'EMPTY', 'BLACK', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY'],
                ['EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY']
            ])
        print(board.board)
        self.assertTrue(np.array_equiv(new_state, board.board), "Wrong expected state after moves and checker capture")
        


    

    

unittest.main()

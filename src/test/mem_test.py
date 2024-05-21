from src.memory.board import Board
from src.profiles.profile_WWII import CountryProfileList

board = Board(CountryProfileList)

r = board.output_rels()
# print(r)

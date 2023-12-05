from board import Board

new_board = Board("702406003060000041004187600600020009053004280200010005001862504030000020500903007")
#new_board.enter()
new_board.show()
print()
new_board.update()
new_board.show_possibles()
print()
new_board.cells[40].set_value(9)
new_board.update()
new_board.show()
print()
new_board.show_possibles()

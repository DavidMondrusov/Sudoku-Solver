class Solver:
    numRec = 0

    def recursions(self):
        temp = int(self.numRec)
        self.numRec = 0
        return temp

    def solve(self, table, row, col):
        self.numRec = self.numRec + 1
        if table[row][col] == 0:
            for val in range(1, 10):
                if self.constraints(table, row, col, val):
                    table[row][col] = val
                    if col == 8:
                        if row == 8:
                            return True
                        elif self.solve(table, row + 1, 0):
                            return True
                    elif self.solve(table, row, col + 1):
                        return True
            table[row][col] = 0
            return False
        else:
            if col == 8:
                if row == 8:
                    return True
                elif self.solve(table, row + 1, 0):
                    return True
            elif self.solve(table, row, col + 1):
                return True
        return False

    def constraints(self, table, row, col, val):
        for thisRow in range(0, 9):
            if thisRow != row and table[thisRow][col] == val:
                return False
        for thisCol in range(0, 9):
            if thisCol != col and table[row][thisCol] == val:
                return False
        boxX, boxY = 3 * (col // 3), 3 * (row // 3)
        for thisRow in range(boxY, boxY + 3):
            for thisCol in range(boxX, boxX + 3):
                if (thisRow != row or thisCol != col) and table[thisRow][
                    thisCol
                ] == val:
                    return False
        return True

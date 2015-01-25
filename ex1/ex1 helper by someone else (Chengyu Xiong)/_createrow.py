# My improved version of the Task._createrow method in ex1.py
# Written by Xiuqi (Rex) Xia

def _createrow(self, columns):
    """(Task, list of str) -> str
    Create and return a formatted table row using the data in columns.
    The entry for each column is padded with spaces to len(self).
    Each column is separated by ' | '
    """
    # Each cell is a column padded to len(self)
    cells = []
    
    for col in columns:
        # left-justify and pad to len(self)
        cells.append(col.ljust(len(self)))
    
    # Join all the cells into one row str, with ' | ' as the separator
    return ' | '.join(cells)
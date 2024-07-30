import numpy as np
from object import Object


class ObstacleRow:
    def __init__(self, obstacle_row: list[Object]):
        self.__obstacles: list[Object] = obstacle_row
    
    def append(self, obstacle: Object):
        self.__obstacles.append(obstacle)

    def at(self, index: int) -> Object:
        return self.__obstacles[index]

    def length(self) -> int:
        return len(self.__obstacles)


class ObstacleMatrix:
    """
    A non-checking structure which keeps track of top-most and right-most
    parts of an obstacle formation (assumes all obstacles in a col have the
    same x, and all obstacles in a row have the same y).
    """
    def __init__(self, obstacle_rows: list[ObstacleRow]):
        self.__obstacles: list[ObstacleRow] = obstacle_rows
    
    def highest_row(self) -> ObstacleRow:
        "Returns the highest non-empty row of obstacles."
        for row in self.__obstacles:
            if row.length() == 0:
                continue
            return row
    
    def lowest_row(self) -> ObstacleRow:
        "Returns the lowest non-empty row of obstacles."
        rev_obs = reversed(self.__obstacles)
        for row in rev_obs:
            if row.length() == 0:
                continue
            return row

    def top(self) -> int:
        "Returns the top component of the first obstacle in the highest row."
        return self.highest_row().at(0).get_rect().top
    
    def right(self) -> int:
        "Returns the right component of the furthest right obstacle in the lowest row."
        b_row: ObstacleRow = self.lowest_row()
        return b_row.at(b_row.length()-1).get_rect().right
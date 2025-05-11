from dependency_injection.terrain.terrain import Terrain

class RectangleTerrain(Terrain):
    def __init__(self, length: float, width: float):
        self.length = length
        self.width = width

    def get_area(self) -> float:
        return self.length * self.width
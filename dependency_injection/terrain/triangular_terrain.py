from dependency_injection.terrain.terrain import Terrain

class TriangularTerrain(Terrain):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def get_area(self) -> float:
        return 0.5 * self.base * self.height
from dependency_injection.terrain.terrain import Terrain

class TerrainPricer:
    def __init__(self, terrain: Terrain, price_per_square_meter: float):
        self.terrain = terrain
        self.price_per_square_meter = price_per_square_meter

    def calculate_price(self) -> float:
        area = self.terrain.get_area()
        return area * self.price_per_square_meter
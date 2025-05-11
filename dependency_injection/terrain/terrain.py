from abc import ABC, abstractmethod

class Terrain(ABC):
    @abstractmethod
    def get_area(self) -> float:
        """
        Calculate the area of the terrain.
        
        Returns:
            float: The area of the terrain in square meters.
        """
        pass
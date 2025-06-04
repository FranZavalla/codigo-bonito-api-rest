from abc import ABC, abstractmethod


class DollarConnector(ABC):
    @abstractmethod
    def get_price(self) -> float:
        """
        Retrieves the current price of the dollar.

        Returns:
          float: The current price of the dollar.
        """
        pass  # pragma: no cover

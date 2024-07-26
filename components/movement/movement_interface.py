from abc import ABC, abstractmethod

class MovementComponent(ABC):
    """Classe abstrata para componentes de movimento.

    Define a interface que todos componentes de movimento devem implementar.
    """

    @abstractmethod
    def handle_movements(self):
        pass

    def limits_movements(self, left_boundary: int, right_boundary: int):
        pass
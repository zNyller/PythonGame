from abc import ABC, abstractmethod

class AnimationComponent(ABC):
    """Classe abstrata para componentes de animação."""

    IDLE_STATE = 'idle'

    def __init__(self) -> None:
        self.animation_state = self.IDLE_STATE
        self.current_frame_index = 0 
        self.frame_counter = 0

    @abstractmethod
    def update(self, delta_time: float):
        pass
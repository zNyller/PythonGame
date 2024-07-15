from abc import ABC, abstractmethod

class AnimationComponent(ABC):

    IDLE_STATE = 'idle'

    def __init__(self) -> None:
        self.animation_state = self.IDLE_STATE
        self.current_frame_index = 0 
        self.frame_counter = 0


    @abstractmethod
    def update(self, delta_time):
        pass


    @abstractmethod
    def reset(self):
        pass
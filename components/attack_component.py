from abc import ABC, abstractmethod

class AttackComponent(ABC):
    """
    Classe abstrata para componentes de ataque.
    Define a interface que todos os componentes de ataque devem implementar.
    """

    @abstractmethod
    def attack(self):
        pass


    @abstractmethod
    def update(self, target_sprites):
        pass


    @abstractmethod
    def perform_attack(self, target_sprites):
        pass


    @abstractmethod
    def inflict_damage(self, target):
        pass
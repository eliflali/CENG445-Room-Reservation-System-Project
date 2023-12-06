from abc import ABC, abstractmethod
import uuid

class CRUD(ABC): # Inherit from ABC(Abstract base class)
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def get(self) -> dict:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @abstractmethod
    def delete(self) -> None:
        pass



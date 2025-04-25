# agents/base_agent.py
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """Abstract base class for all agents in PatientGPT."""

    @abstractmethod
    def run(self, *args, **kwargs):
        """Each agent implements its core function here."""
        pass

    def name(self):
        return self.__class__.__name__

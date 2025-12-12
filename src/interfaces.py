from abc import ABC, abstractmethod

class ObstacleStrategy(ABC):
    @abstractmethod
    def check_path(self):
        """
        Analyze the environment.
        Returns tuple: (is_safe, front_dist, left_dist, right_dist)
        """
        pass
    
    @abstractmethod
    def stop(self):
        """Release resources (close serial ports, cameras, etc.)"""
        pass
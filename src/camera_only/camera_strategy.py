from src.interfaces import ObstacleStrategy


class CameraStrategy(ObstacleStrategy):
    def check_path(self):
        return True, 0.0, 0.0, 0.0 
    def stop(self):
        pass

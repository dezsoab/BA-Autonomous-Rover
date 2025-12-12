from src.interfaces import ObstacleStrategy


class FusionStrategy(ObstacleStrategy):
    def check_path(self):
        # Combine strategies
        is_safe, front_dist, left_dist, right_dist = super().check_path()
        return is_safe, front_dist, left_dist, right_dist

    def stop(self):
        super().stop()  
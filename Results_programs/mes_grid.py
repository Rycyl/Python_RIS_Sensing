import math

class PointGrid:
    def __init__(self, start_x, start_y, dx, dy, rows, cols):
        """
        Initializes the grid structure.
        
        :param start_x: X coordinate of the first point (bottom left)
        :param start_y: Y coordinate of the first point (bottom left)
        :param dx: Horizontal distance between columns
        :param dy: Vertical distance between rows
        :param rows: Number of rows in the grid
        :param cols: Number of columns in the grid
        """
        self.start_x = start_x
        self.start_y = start_y
        self.dx = dx
        self.dy = dy
        self.rows = rows
        self.cols = cols
        self.total_points = rows * cols

    def get_cartesian(self, index):
        """Returns the (x, y) coordinates for a given 1-based index."""
        if not (1 <= index <= self.total_points):
            raise ValueError(f"Index {index} is out of bounds. Must be between 1 and {self.total_points}.")

        # Convert 1-based index to 0-based for math operations
        idx = index - 1

        # Calculate the current column and row based on column-major ordering
        col = idx // self.rows
        row = idx % self.rows

        # Calculate actual X and Y coordinates
        x = self.start_x + (col * self.dx)
        y = self.start_y + (row * self.dy)

        return x, y

    def get_polar(self, index):
        """
        Returns the polar coordinates (v, alpha) for a given index.
        v = distance from origin (0,0)
        alpha = angle in degrees measured clockwise from the Y-axis.
        """
        x, y = self.get_cartesian(index)

        # Calculate the vector magnitude (distance from origin)
        v = math.hypot(x, y)

        # Calculate the angle from the Y-axis. 
        # Using atan2(x, y) instead of atan2(y, x) shifts the reference axis to Y.
        alpha_rad = math.atan2(x, y)
        alpha_deg = math.degrees(alpha_rad)

        # Optional: Normalize the angle to be strictly between 0 and 360 degrees
        if alpha_deg < 0:
            alpha_deg += 360

        return v, alpha_deg


if __name__ == "__main__":
    grid = PointGrid(start_x=0, start_y=240, dx=122, dy=122, rows=3, cols=6)

    # Test Point 1 (Should be v = 240, alpha = 0)
    v1, alpha1 = grid.get_polar(1)
    print(f"Point 1 -> v: {v1:.2f}, alpha: {alpha1:.2f}°")

    # Test Point 4 (Should be v = ~269.23, alpha = ~26.95)
    v4, alpha4 = grid.get_polar(4)
    print(f"Point 4 -> v: {v4:.2f}, alpha: {alpha4:.2f}°")

    v18, alpha18 = grid.get_polar(18)
    print(f"Point 4 -> v: {v18:.2f}, alpha: {alpha18:.2f}°")
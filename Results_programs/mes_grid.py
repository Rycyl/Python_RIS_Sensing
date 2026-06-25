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
        alpha_rad = math.atan2(x, y)
        alpha_deg = math.degrees(alpha_rad)

        # Normalize the angle to be strictly between 0 and 360 degrees
        if alpha_deg < 0:
            alpha_deg += 360

        return v, alpha_deg

    def get_distance_from_y_axis_point(self, index, y_virtual):
        """
        Calculates the distance from a virtual point on the Y-axis (0, y_virtual)
        to the grid point specified by the index.
        
        :param index: The 1-based index of the target grid point.
        :param y_virtual: The Y-coordinate of the virtual point.
        """
        x, y = self.get_cartesian(index)
        
        # Calculate the distance. 
        # Since the virtual point's X is 0, the delta X is just 'x - 0' or simply 'x'.
        # The delta Y is 'y - y_virtual'.
        distance = math.hypot(x, y - y_virtual)
        
        return distance

# ==========================================
# Example Usage
# ==========================================
if __name__ == "__main__":
    # Defining the same grid starting at (0, 240)
    grid = PointGrid(start_x=0, start_y=240, dx=122, dy=10, rows=3, cols=2)

    # --- Existing Tests ---
    v1, alpha1 = grid.get_polar(1)
    print(f"Point 1 -> v: {v1:.2f}, alpha: {alpha1:.2f}°")

    v4, alpha4 = grid.get_polar(4)
    print(f"Point 4 -> v: {v4:.2f}, alpha: {alpha4:.2f}°")
    
    print("-" * 30)

    # --- New Feature Tests ---
    # Let's place a virtual point at Y = 100 (so the point is 0, 100)
    virtual_y = 698
    
    # Distance to Point 1 (which is at 0, 240) 
    # Math: sqrt(0^2 + (240 - 100)^2) = 140
    dist1 = grid.get_distance_from_y_axis_point(1, virtual_y)
    print(f"Distance from (0, {virtual_y}) to Point 1: {dist1:.2f}")

    # Distance to Point 4 (which is at 122, 240)
    # Math: sqrt(122^2 + (240 - 100)^2) = sqrt(14884 + 19600) = ~185.70
    dist4 = grid.get_distance_from_y_axis_point(4, virtual_y)
    print(f"Distance from (0, {virtual_y}) to Point 4: {dist4:.2f}")
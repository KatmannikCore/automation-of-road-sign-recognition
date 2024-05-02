class Frame:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.name_sign = ""
        self.latitude = 0
        self.longitude = 0
        self.number_frame = 0
        self.number_sign = 0
        self.text_on_sign = ''
    @staticmethod
    def overlap_area( square1, square2):
        """
        Calculates the overlap area between two squares.

        Args:
          square1: A list of four numbers [x1, y1, width1, height1] representing
            the coordinates of the top-right corner and the width and height of the
            first square.
          square2: A list of four numbers [x2, y2, width2, height2] representing
            the coordinates of the top-right corner and the width and height of the
            second square.

        Returns:
          The overlap area between the two squares.
        """

        # Calculate the intersection of the two squares.
        intersection = [
            max(square1[0], square2[0]),
            max(square1[1], square2[1]),
            min(square1[0] + square1[2], square2[0] + square2[2]) - max(square1[0], square2[0]),
            min(square1[1] + square1[3], square2[1] + square2[3]) - max(square1[1], square2[1])
        ]

        # Calculate the overlap area.
        if intersection[2] > 0 and intersection[3] > 0:
            overlap_area = intersection[2] * intersection[3]
        else:
            overlap_area = 0

        # Calculate the percentage overlap.
        overlap_percentage = overlap_area / (square1[2] * square1[3]) * 100

        return overlap_percentage

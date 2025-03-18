class MapData():
    def __init__(self, width, height, numRooms, roomSize, circularity, squarelike):
        self.width = width
        self.height = height
        self.numRooms = numRooms
        self.roomSize = roomSize
        self.circularity = circularity
        self.squarelike = squarelike

    def get_numRooms(self):
        return self.numRooms

    def get_circularity(self):
        return self.circularity

    def get_roomSize(self):
        return self.roomSize

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height


# Config data!
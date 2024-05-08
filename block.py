class Block:
    def __init__(self, shape, position=[-1, 0], rotation=0, fixed=False):
        self.shape = shape
        self.rotation = rotation
        self.position = position
        self.fixed = fixed

    def translate(self):
        result = []

        rotation = abs(self.rotation) % 4

        if rotation == 0:
            result = [
                [
                    [self.position[0] + rowPos, self.position[1] + colPos, cell]
                    for colPos, cell in enumerate(row)
                ]
                for rowPos, row in enumerate(self.shape)
            ]
        elif rotation == 3:
            result = [
                [
                    [self.position[0] + colPos, self.position[1] + rowPos, self.shape[-(rowPos + 1)][colPos]]
                    for rowPos in range(len(self.shape))
                ]
                for colPos in range(len(self.shape[0]))
            ]
        elif rotation == 2:
            result = [
                [
                    [self.position[0] + rowPos, self.position[1] + colPos, cell]
                    for colPos, cell in enumerate(reversed(row))
                ]
                for rowPos, row in enumerate(reversed(self.shape))
            ]
        elif rotation == 1:
            result = [
                [
                    [self.position[0] + colPos, self.position[1] + rowPos, self.shape[rowPos][-(colPos + 1)]]
                    for rowPos in range(len(self.shape))
                ]
                for colPos in range(len(self.shape[0]) - 1, -1, -1)
            ]

        return result

    def draw(self):
        translated = self.translate()
        return "\n".join("".join(cell[2] if cell else '⬜' for cell in row) for row in translated)

    def toJSON(self):
        return {
            'shape': self.shape,
            'position': self.position,
            'rotation': self.rotation,
            'fixed': self.fixed
        }

    @staticmethod
    def fromJSON(json):
        return Block(json['shape'], json['position'], json['rotation'], json['fixed'])

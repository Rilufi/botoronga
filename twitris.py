import random
import numpy as np
from PIL import Image, ImageDraw

class Color:
    """Defines colors for Tetris blocks."""
    I = (0, 255, 255)    # Cyan
    O = (255, 255, 0)    # Yellow
    S = (0, 255, 0)      # Green
    Z = (255, 0, 0)      # Red
    T = (128, 0, 128)    # Purple
    J = (0, 0, 255)      # Blue
    L = (255, 128, 0)    # Orange
    Blank = (255, 255, 255)  # White (for blank space)

class Block:
    def __init__(self, shape):
        self.shape = np.array(shape)
        self.color = self.get_color_by_shape()
        self.rotation = 0
        self.position = [0, self.get_center_x()]

    def get_color_by_shape(self):
        shape_array = self.shape.tolist()  # Convert shape to nested list
        for color_name, color_tuple in Color.__dict__.items():
            if isinstance(color_tuple, tuple) and color_tuple in shape_array:
                return color_tuple
        return Color.Blank  # Default to white if color not found

    def get_center_x(self):
        return self.shape.shape[1] // 2

    def translate(self):
        rotations = [self.shape] * 4
        for i in range(1, 4):
            rotations[i] = np.rot90(rotations[i-1])
        return [(pos[0], pos[1], self.color) for pos in np.argwhere(rotations[self.rotation % 4]) + self.position]

class Game:
    def __init__(self, width=10, height=18):
        self.width = width
        self.height = height
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.current_block = self.new_block()

    def new_block(self):
        shapes = [
            [[1, 1, 1, 1]],       # I-shape
            [[1, 1], [1, 1]],     # O-shape
            [[1, 1, 0], [0, 1, 1]],  # S-shape
            [[0, 1, 1], [1, 1, 0]],  # Z-shape
            [[1, 1, 1], [0, 1, 0]],  # T-shape
            [[1, 1, 0], [0, 1, 1]],  # J-shape
            [[0, 1, 0], [1, 1, 1]]   # L-shape
        ]
        shape = random.choice(shapes)
        return Block(shape)

    def draw(self, filename):
        image = Image.new('RGB', (self.width * 20, self.height * 20), color='white')
        draw = ImageDraw.Draw(image)

        for y in range(self.height):
            for x in range(self.width):
                color = self.board[y][x]
                if color != ' ':
                    draw.rectangle([x * 20, y * 20, (x + 1) * 20, (y + 1) * 20], fill=color, outline='black')

        image.save(filename)
        print("Imagem do tabuleiro salva com sucesso.")

def main():
    game = Game()
    game.draw('imagens/tetris_board.png')

if __name__ == "__main__":
    main()

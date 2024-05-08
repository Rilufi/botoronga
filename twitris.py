import random
import numpy as np
from PIL import Image, ImageDraw

class Block:
    def __init__(self, shape):
        self.shape = np.array(shape)

    def translate(self, position):
        return [(pos[0], pos[1]) for pos in np.argwhere(self.shape) + position]

class Game:
    def __init__(self, width=10, height=18):
        self.width = width
        self.height = height
        self.board = [[' ' for _ in range(width)] for _ in range(height)]
        self.current_block = self.new_block()

    def new_block(self):
        shapes = [
            [[1, 1, 1, 1]],             # I-shape
            [[1, 1], [1, 1]],           # O-shape
            [[1, 1, 0], [0, 1, 1]],     # S-shape
            [[0, 1, 1], [1, 1, 0]],     # Z-shape
            [[1, 1, 1], [0, 1, 0]],     # T-shape
            [[1, 1, 0], [0, 1, 1]],     # J-shape
            [[0, 1, 0], [1, 1, 1]]      # L-shape
        ]
        shape = random.choice(shapes)
        position = [0, self.width // 2 - len(shape[0]) // 2]
        return Block(shape)

    def draw(self, filename):
        board_with_block = [row[:] for row in self.board]
        positions = self.current_block.translate([0, self.width // 2 - len(self.current_block.shape[0]) // 2])
        for x, y in positions:
            if 0 <= x < self.height and 0 <= y < self.width:
                board_with_block[x][y] = '#'

        image = Image.new('RGB', (self.width * 20, self.height * 20), color='white')
        draw = ImageDraw.Draw(image)
        for y in range(self.height):
            for x in range(self.width):
                color = 'black' if board_with_block[y][x] == '#' else 'white'
                draw.rectangle([x * 20, y * 20, (x + 1) * 20, (y + 1) * 20], fill=color, outline='black')

        image.save(filename)

def main():
    game = Game()

    # Gerar e salvar a imagem estática do tabuleiro
    game.draw('tetris_board.png')
    print("Imagem do tabuleiro salva com sucesso.")

if __name__ == "__main__":
    main()

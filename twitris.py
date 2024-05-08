import os
import json
import random
import time

import numpy as np
import pygame
from tweepy import OAuthHandler, API

# Replace with your Twitter API keys
consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token_key = "YOUR_ACCESS_TOKEN_KEY"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

screen_name = "botoronga"

class Twitter:
  def __init__(self):
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    self.api = API(auth)

  def tweet_image(self, image_path, status):
    media = self.api.media_upload(image_path)
    self.api.update_status(status=status, media_ids=[media.media_id])

  def get_last_tweet(self):
    tweets = self.api.user_timeline(screen_name=screen_name, count=1)
    return tweets[0] if tweets else None

  def get_replies(self, tweet_id):
    replies = []
    for tweet in self.api.mentions_timeline(since_id=tweet_id, count=200):
      if tweet.in_reply_to_status_id == tweet_id:
        replies.append(tweet)
        replies.extend(self.get_replies(tweet.id))
    return replies

  def filter_replies(self, commands, replies):
    return [reply for reply in replies if any(cmd.lower() in reply.text.lower() for cmd in commands)]

class Block:
  def __init__(self, shape, position=(0, 0), rotation=0):
    self.shape = shape
    self.rotation = rotation
    self.position = position

  def translate(self):
    rotations = [self.shape] * 4
    for i in range(1, 4):
      rotations[i] = np.rot90(rotations[i-1])
    return rotations[self.rotation % 4] + self.position

  def draw(self, board):
    board[self.translate().T.tolist()] = "🟦"
    return board

  def to_json(self):
    return {"shape": self.shape.tolist(), "position": list(self.position), "rotation": self.rotation}

  @staticmethod
  def from_json(data):
    return Block(np.array(data["shape"]), data["position"], data["rotation"])

class Game:
  def __init__(self, width=10, height=18):
    self.width = width
    self.height = height
    self.board = np.zeros((height, width), dtype=str)
    self.blocks = []
    self.twitter = Twitter()
    self.score = 0
    self.font = pygame.font.SysFont(None, 32)  # Initialize font here

  def start(self):
    self.board = np.zeros((self.height, width), dtype=str)
    self.blocks = []
    self.score = 0
    self.generate_board()
    self.tweet_game_state()

  def generate_board(self):
    shapes = [
      [[None, "🟦", None], ["🟦", "🟦", "🟦"]],
      [[ "🟥", "🟥", "🟥"], [None, None, None]],
      [[ "🟨", "🟨"], ["🟨", "🟨"]],
      ["🟧", "🟧", "🟧", "🟧"],
      [[None, "🟪", None], [None, "🟪", "🟪"]],
      [[ "🟩", "🟩", None], [None, "🟩", "🟩"]],
      [[None, "🟫", "🟫"], ["🟫", "🟫", None]],
    ]
    for i in range(5):
      block = Block(np.array(random.choice(shapes)))
      while not self.is_valid_position(block):
        block = Block(np.array(random.choice(shapes)))
      block.position = np.array([self.height - block.translate().shape[0] + 1, self.width // 2 - block.translate().shape[1] // 2])
      self.blocks.append(block)

  def tweet_game_state(self):
    surface = pygame.display.set_mode((self.width * 25, self.height * 25))  # Create a visible window
    surface.fill((0, 0, 0))
    grid = self.board * 25
    pygame.draw.rect(surface, (255, 255, 255), (0, 0, self.width * 25, self.height * 25), 1)
    for y, row in enumerate(grid):
      for x, cell in enumerate(row):
        if cell != " ":
          pygame.draw.rect(surface, (0, 255, 0), (x * 25, y * 25, 25, 25))
    text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
    surface.blit(text, (10, 10))
    pygame.display.flip()  # Update the display
    pygame.image.save(f"tetris_board_{time.time()}.png", surface)  # Generate unique filename
    self.twitter.tweet_image(f"tetris_board_{time.time()}.png", "Current Tetris Board!")  # Tweet with image
    os.remove(f"tetris_board_{time.time()}.png")  # Clean up temporary image

  def is_valid_position(self, block):
    return (0 <= block.position[0] < self.height and 0 <= block.position[1] < self.width and
            not (block.translate() + block.position).T.tolist().count(None) < block.translate().T.size)

  def get_move_from_replies(self):
    last_tweet = self.twitter.get_last_tweet()
    if last_tweet:
      replies = self.twitter.get_replies(last_tweet.id)
      commands = ["left", "right"]
      move = self.twitter.filter_replies(commands, replies)
      return move[0] if move else None
    return None

  def move_block(self, direction):
    if direction == "left":
      for block in self.blocks:
        new_position = block.position + np.array([0, -1])
        if self.is_valid_position(block):
          block.position = new_position
          self.board = block.draw(self.board.copy())  # Avoid modifying board directly
    elif direction == "right":
      for block in self.blocks:
        new_position = block.position + np.array([0, 1])
        if self.is_valid_position(block):
          block.position = new_position
          self.board = block.draw(self.board.copy())

  def run(self):
    pygame.init()
    self.start()

    while True:
      move = self.get_move_from_replies()
      if move:
        self.move_block(move)
        self.tweet_game_state()
      pygame.display.flip()  # Update the display for every loop
      time.sleep(5)  # Check for replies every 5 seconds

if __name__ == "__main__":
  game = Game()
  game.run()

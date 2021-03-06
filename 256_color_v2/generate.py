import chess
import chess.svg
import chess.pgn
import numpy as np
import random
import os, sys, io
import cairosvg
import PIL
import time
import random


def parse_games1(fn):
  pgn = open(fn, encoding="ISO-8859-1")
  while True:
    g = chess.pgn.read_game(pgn)
    if g is None:
      break
    yield g
  del pgn


def random_position(g):
  b = g.board()
  moves = list(g.mainline_moves())
  if len(moves) <= 1:
      return None
  pick = random.randint(0, len(moves) - 1)
  for i, move in enumerate(moves):
    if i == pick:
      return b
    b.push(move)


def board_to_png(b):
  return cairosvg.svg2png(bytestring=chess.svg.board(b, size=256, coordinates=False, flipped=(random.random() < 0.5)))


def file_to_rgb_numpy(fn):
  return np.array(PIL.Image.open(fn).convert('RGB'))


def board_to_rgb_numpy(b):
  png = board_to_png(b)
  buf = io.BytesIO()
  buf.write(png)
  buf.seek(0)
  return file_to_rgb_numpy(buf)


def pgn_to_unique_positions(fn, limit=None):
  already = set()
  row = 0
  mod = 1
  for i, g in enumerate(parse_games1(fn)):
    row += 1
    if row % mod == 0:
      print('row: ', row)
      mod *= 2
      if mod > 512:
        mod = 512
    b = random_position(g)
    if b is None:
      continue
    fen = b.fen()
    simple = fen.split(' ')[0]
    if simple in already:
      continue
    yield board_to_rgb_numpy(b)
    if limit is not None and i >= limit:
      break



N = None
dir = '.'
t1 = time.time()
for i, ar in enumerate(pgn_to_unique_positions("all.pgn", N)):
    np.savez_compressed('{}/{:06d}.npz'.format(dir, i), ar)
t2 = time.time()
print('dt: ', t2-t1)

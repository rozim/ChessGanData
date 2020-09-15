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

SIZE = 256


def parse_games1(fn):
  pgn = open(fn, encoding="ISO-8859-1")
  while True:
    g = chess.pgn.read_game(pgn)
    if g is None:
      break
    yield g
  del pgn


def all_positions(g):
  b = g.board()
  for move in g.mainline_moves():
    b.push(move)
    yield b


def board_to_png(b):
  return cairosvg.svg2png(bytestring=chess.svg.board(b, size=SIZE, coordinates=False, flipped=False))


def file_to_rgb_numpy(fn):
  return np.array(PIL.Image.open(fn).convert('RGB'))

def file_to_gray_numpy(fn):
  return np.array(PIL.Image.open(fn).convert('L')) #  .resize((SIZE, SIZE)))


def board_to_rgb_numpy(b):
  png = board_to_png(b)
  buf = io.BytesIO()
  buf.write(png)
  buf.seek(0)
  return file_to_rgb_numpy(buf)


def board_to_gray_numpy(b):
  png = board_to_png(b)
  buf = io.BytesIO()
  buf.write(png)
  buf.seek(0)
  return file_to_gray_numpy(buf)



limit = None
games = 0
dir = 'out'
t1 = time.time()
already = set()
row = 0
mod = 1
dups = 0
for g in parse_games1('all.pgn'):
  games += 1
  for b in all_positions(g):
    fen = b.fen()
    simple = fen.split(' ')[0]
    if simple in already:
      dups += 1
      continue
    already.add(simple)

    fn = '{}/{:016x}.png'.format('out', abs(hash(simple)))

    with open(fn, 'wb') as fp:
      png = board_to_png(b)
      buf = io.BytesIO()
      buf.write(png)
      PIL.Image.open(buf).convert('L').save(fp, 'PNG')


    if limit is not None and row >= limit:
      t2 = time.time()
      print('dt: ', t2-t1)
      sys.exit(0)

    row += 1
    if row % mod == 0:
      print('row: {}/{} dups={} pos={} games={} dt={:.1f}s'.format(row, limit, dups, len(already), games, time.time() - t1))
      mod *= 2
      if mod > 1024:
        mod = 1024

t2 = time.time()
print('dt: ', t2-t1)

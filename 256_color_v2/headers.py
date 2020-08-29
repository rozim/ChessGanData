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





pgn = open('all.pgn', encoding="ISO-8859-1")
n = 0
bad = 0
while True:
  g = chess.pgn.read_game(pgn)
  if g is None:
      break
  if ('Variant' in g.headers or
      'FEN' in g.headers or
      'Variant' in g.headers):
      print(g.headers)
      bad += 1
  n += 1

print(n, bad)

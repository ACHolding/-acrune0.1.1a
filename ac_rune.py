#!/usr/bin/env python3
# =============================================================================
#   AC RUNE 0.1  (2026)  [C] AC HOLDING  --  a Team Flames / Samsoft joint
#   -------------------------------------------------------------------------
#   An ORIGINAAL dark-world AU RPG in one file. files = off. 60 fps. speed = 1.0.
#   Custom OST — Undertale Yellow style (original leitmotifs, Toby Fox timbre).
#   files = off. 14 tracks, procedural NES synth, zero asset files.
#
#   CAST
#     AC      - a quiet blue cat. the vessel. (hero)
#     RYEN    - a time traveller with cracked goggles. (rude one)
#     LASSE   - a soft-spoken fox. joins in CH3. (healer)
#     PLOMBO  - a laid-back mustachioed plumber OC. judges you in CH5.
#     WRENCHARD - the Pipe Knight. plumber-armor OC. opens the fountains.
#     BECCA   - runs the house. worries. (mom energy)
#     JOSEPH  - classmate. grows sunflowers. (big warm guy)
#
#   CHAPTERS
#     CH1 SCHOOL OF STATIC   CH2 NEON HARBOR   CH3 BOARDWALK VHS
#     CH4 THE HOLLOW CHOIR   CH5 PIPEWORKS
#
#   OST — custom AC RUNE soundtrack (Undertale Yellow approach, files = off):
#     a_cat's_morning / field_of_static / neon_harbor / boardwalk_vhs
#     hollow_choir / pipeworks / rude_rumble / PREFECT! / CIRCUIT CROWN
#     JESTER STATIC / WARDEN'S HYMN / KNIGHT OF PIPES / plombo's_theme
#     a_cat's_tomorrow
#   Shared "meow leitmotif" weaves through every track (AABB + ostinato).
#
#   CONTROLS:  Arrows move - Z confirm - X cancel - M mute - ESC quit
#   RUN:       python3 ac_rune.py          (python 3.10+ incl. 3.14)
# =============================================================================
import os, sys, math, random, array

SMOKE = "--smoke" in sys.argv
if SMOKE:
    os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
    os.environ.setdefault("SDL_AUDIODRIVER", "dummy")

import pygame

# ---------------------------------------------------------------- constants
FILES  = False                   # files = off — one python file, no asset folder
W, H   = 640, 480
FPS    = 60
SPEED  = 1.0                     # 1.0x at 60fps (deltarune-turbo timing, not 2x)
SOUL_SPD = 2.0 * SPEED           # DR global.sp=4 @30fps → 2.0 px/frame @60fps
OW_SPD   = 2.5 * SPEED           # overworld walk, scaled to match
SR     = 44100                   # cleaner NES-style pulse rendering
BLUE   = (51, 204, 255)          # electric flames-blue
WHITE  = (240, 240, 240)
BLACK  = (6, 6, 10)
YELLOW = (255, 230, 90)
RED    = (255, 70, 90)
GREEN  = (90, 230, 130)
ORANGE = (255, 170, 60)
PURPLE = (200, 120, 255)
GRAY   = (120, 120, 140)
BOX    = pygame.Rect(170, 238, 300, 162)

CH_TITLES = ["CH1: SCHOOL OF STATIC", "CH2: NEON HARBOR", "CH3: BOARDWALK VHS",
             "CH4: THE HOLLOW CHOIR", "CH5: PIPEWORKS"]
CH_PAL = [((18,18,30),(40,40,70)), ((6,20,34),(10,60,90)), ((26,10,30),(70,20,80)),
          ((14,14,14),(60,50,30)), ((8,24,16),(20,80,50))]

CH_TITLES.append("LAST BREATH: PHASE 1")
CH_PAL.append(((0,0,0),(40,40,60)))
# ---------------------------------------------------------------- last breath phase 1 sprites (base64, files = off)
import base64 as _lb_b64
import io as _lb_io

SANS_ANIMS_B64 = {
    "idle_0": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABeklEQVR42u3bQQqDMBRFUZfjDrqNLsfdp3baQUUSY148FzIpauEfhEbpskiSJEmSJEmSJEmS9JhKw0wzBApcMBa0QCxoYVDggrGgAYMFDRa0GbCgAYMFDBgwYMCAAQPWDOx7yL/V4XwBAwYMGLAmYNvPZx3OlzsMGDBgwIABAxb7aOoshEdTwIABAwZsJDSvV4ABS0KjEoRGoxLtaAN8dsGa6C6jEIRm+iFwph2EZspBaKZ70Lq+Ss2qrfb7gQEDBgzYvGBXD+4usGl/xAADBgwYsGZgdwcMGDBgwIABAwYMGDBgNs42zsCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMBy8mcIYMCAAQMGDBgwYMCAAbu5bd9sjrwEDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYCGdfeXf+3oCBgwYMAEDBgyYgAEDBkzAgAEDBgwYMGDAgAEDBgwYMGCPgnpvpWZdfT0BAwYMmIABAyZJ0sB9AOHBOS62Iv5hAAAAAElFTkSuQmCC",
    "idle_1": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABeUlEQVR42u3bQQ6CMBRFUZbDDtyGy+nuq04dSEhLy6vnJp0YwOSfkFiI2yZJkiRJkiRJkiRJkiR1qHbMNEOgwAVjQQvEghYGBS4YCxowWNBgQVsBCxowWMCAAQMGDBgwYN3APof8WgPOFzBgwIAB6wJWvj4bcL7cYcCAAQMGDBiw2EdTZyE8mgIGDBgwYHdC83oFGLAkNCpBaDQa0Y42wGcXrIXuMgpBaKYfAmfaQWimHIRmugft+6O2rNZavx8YMGDAgK0LdvXgZoEt+yMGGDBgwIB1A5sdMGDAgAEDBgwYMGDAgNk42zgDAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgwIABy8mfIYABAwYMGDBgwIABAwZscuW92bzzEjBgwIABAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgwICFdPaV/+jrCRgwYMAEDBgwYAIGDBgwAQMGDBgwYMCAAQMGDBgwYMCA/RXUs9SWdfX1BAwYMGACBgyYpMZebDg5Ln2rOlkAAAAASUVORK5CYII=",
    "clenched": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABfklEQVR42u3b0Q3CIBRAUcbpBq7hON0edQMqUHh95yZ8GTHhJBUwliJJkiRJkiRJkiRJUprqwKxmEChwgbGgBcSCFgwKXGAsaMBgQYMF7QlY0IDBAgYMGDBgwIABAwYM2PZgv5dbxqz3AwMGDBgwYDYdwIABAwYMWPsGBRgwAQMGbNSCR914AAMWH2xXtNTfQdHOZOk3DaPma73Q/eeiN8XOEFhysNWPRueojoUAFQzsLjQ3FYMXBdZCsON41Z7RW+/nAwMGDBgwYNHAHrOJAQYMGDBg08BWBwwYMGDAgAEDBgwYMGAOzg7OwDKDXQ0YMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBiz5nyGAAQMGDBgwYMCAAQNW0nd+D5s7DwEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgxYkK7+5H/3fAIGDBgwAQMGDJiAAQMGTMCAAQMGDBgwYMCAAQMGDBgwYKmg3mftGbPnEzBgwIAJGDBgkiRt3AfYw1TVGAzpKQAAAABJRU5ErkJggg==",
    "fatal": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABdElEQVR42u3b0Q3CIBRA0Y7DBq7hOB3WXah++WkrUHhwbvK+TGvCSQitcdskSZIkSZIkSZIkSVqqXDGrGQQKXGAsaAGxoAWDAhcYCxowWNBgQZsBCxowWMCAAQMGDBgwYMCAAQMGDNjSYJ+Pz0yr64EBsyXaEoEBAwYMWHSwKwcJYMCAAQMGbIWDBx1g0GBBg1UL7ewL3X9e9MICBs1WCA5UNDSrHAjN6v4opUcumdJKvx8YMGDAgM0L1nrheoFNe4gBBgwYMGDVwHoHDBgwYMCAAQMGrFavlLL5DjBgHpw9OAMDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAFrkT9DAAMGDBgwYMCAAQMGDFjn9vfD5sgjYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQvS1Z/8776fgAEDBkzAgAEDJmDAgAETMGDAgAEDBgwYMGDAgAEDBgzYUlDPPZdM6/sJGDBgwAQMGDBJkgbtAMU02uYC/t+sAAAAAElFTkSuQmCC",
    "glow_0": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABj0lEQVR42u3b0Q2CMBRAUcZxHMdxA9dwHIZwlxr/DD/YtPX12XOTforknQSBxm2TJEmSJEmSJEmSJGmZSsdMMwkUuMRY0BJiQUsGBS4xFjRgsKDBgvYPWNCAwQIGDBiwRcCepewRCxiwtcDOLlm1AGefBwYMGDBgwIABAwYMGDBgwIABi3819T7U5/JqCph6bq8cwWyvAFNvNBuYwIBlQos4X2iDBgfsy0Ecby5qV6+hAQOW9zczw00GsGC4Wc7N3eOgIQELQpvtnKYb/vV2Ly2rtdbvX+4BGRgwYMAWAhs9OGDAgAEDBmxWsOiAAQMGDBgwYMCAAQMGzIOzB2dgwIABAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgefJnCGDAgAEDBgwYMGDAgAGL7bKXMvPaBAwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGBJqt3y//XxBAwYMGACBgwYMAEDBgyYgAEDBgwYMGDAgAEDBgwYMGDAloJ67KVljT6egAEDBkzAgAGTJGniXrz5bunWHo+vAAAAAElFTkSuQmCC",
    "glow_1": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABj0lEQVR42u3b0Q2CMBRAUcZxHMdxA9dwHIZwlxr/DD/YtPX12XOTforknQSBxm2TJEmSJEmSJEmSJEmas9Ix00wCBS4xFrSEWNCSQYFLjAUNGCxosKD9AxY0YLCAAQMGbBGwZyl7xAIGbC2ws0tWLcDZ54EBAwYMGDBgwIABAwYMGDBgwOJfTb0P9bm8mgKmntsrRzDbK8DUG80GJjBgmdAizhfaoMEB+3IQx5uL2tVraMCA5f3NzHCTASwYbpZzc/c4aEjAgtBmO6fphn+93UvLaq31+5d7QAYGDBiwhcBGDw4YMGDAgAGbFSw6YMCAAQMGDBgwYMCAAfPg7MEZGDBgwIABAwYMGDBgwIABAwYMGDBgwIABAwYMWJ78GQIYMGDAgAEDBgwYMGDAYrvspcy8NgEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgxYkmq3/H99PAEDBgyYgAEDBkzAgAEDJmDAgAEDBgwYMGDAgAEDBgwYsKWgHntpWaOPJ2DAgAETMGDAJGmtXhucbulcevnjAAAAAElFTkSuQmCC",
    "shrug": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABkUlEQVR42u3d0Q2CMBRAUcZhA9dwHLav8ZcEpdDS9+DcpD9GNOVILJDoNEmSJEmSJEmSJEmS9JhKw+zNJFDgEmNBS4gFLRkUuMRY0IDBggYL2h2woAGDBQwYMGDAgAED1gzs+5Rf44LtBQwYMGDAmoAtq8cu2F6OMGDAgAEDBgxY2ktTtRAuTQEDBgwYsEhobq8AKxA2dkhUrMfAHploxCML2J+JHj0Brh2tP0TAgnxvAdsx0UiLDGAVE42wGgRWOdHRS3dgByY68jwL2Kp5flWNs/V6P2DAgAEDBgwYMGDAgAHLCjY6YMCAAQMGbKvei4rei5LpaQEDBgwYsN1g0U6cgQEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGCJWkoJPQQMGDBgwIABAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgSRr1Vxy3/xk9YAIGDBgwAQMGDJiAAQMGTMCAAQMmYMCAAQMGDBgwYMCOQL2Xcmb0fj0BAwYMmIABAyZJUuA+xrfT4T+ukWAAAAAASUVORK5CYII=",
    "point": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABeUlEQVR42u3b4Q2CMBCA0Y7DBq7hOGxf4wbFUnrnvS/pLyOSeyYW1NYkSZIkSZIkSZIkSSpTvzHTTAIFLjEWtIRY0JJBgUuMBQ0YLGiwoP0DFjRgsIABAwYMGDBgwIABAxYe7PvwyFr1fGDAgAEDBsymAxgwYMCAARvfoAADJmDAgFXfeNABBm0HljdIy/XLX2CDgxi9ofvLjd4rQwMGLO9nZoZNBrDNcFHOze5x0ZCAbUKLdk7hhn8crz6zZpt9/XIXyMCAAQNWCGz14IABAwYMGLCoYLsDBgwYMGDAgAEDBgwYMBfOLpyBAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCA5cmfIYABAwYMGDBgwIABAwZsc2fvoZeAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGLElXv/J/+ngCBgwYMAEDBgyYgAEDBkzAgAEDBgwYMGDAgAEDBgwYMGCloN5nn1mrjydgwIABEzBgwCRJCtwH5Bm2V5F2Ru4AAAAASUVORK5CYII=",
    "dodge_l": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABeUlEQVR42u3bQQ6CMBRFUZbDDtyGy+nuq04dSEhLy6vnJp0YwOSfkFiI2yZJkiRJkiRJkiRJUny1Y6YZAgUuGAtaIBa0MChwwVjQgMGCBgvaCljQgMECBgwYMGDAgAHrBvY55NcacL6AAQMGDFgXsPL12YDz5Q4DBgwYMGDAgMU+mjoL4dEUMGDAgAG7E5rXK8CAJaFRCUKj0Yh2tAE+u2AtdJdRCEIz/RA40w5CM+UgNNM9aN8ftWW11vr9wIABAwZsXbCrBzcLbNkfMcCAAQMGrBvY7IABAwYMGDBgwIABAwbMxtnGGRgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDFhO/gwBDBgwYMCAAQMGDBgwYJMr783mnZeAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGLKSzr/xHX0/AgAEDJmDAgAETMGDAgAkYMGDAgAEDBgwYMGDAgAEDBuyvoJ6ltqyrrydgwIABEzBgwCRJWqAX0VA5Lgq8xxoAAAAASUVORK5CYII=",
    "dodge_r": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABeUlEQVR42u3bQQqDMBRFUZfjDrqNLsfdp3bqoBISjS89FzIpauEfhEbpskiSJEmSJEmSJEmSpEOlY6YZAgUuGAtaIBa0MChwwVjQgMGCBgvaDFjQgMECBgwYMGDAgAHrBvY95Ne64XwBAwYMGLAuYNvhsxvOlzsMGDBgwIABAxb7aKoWwqMpYMCAAQP2JDSvV4ABS0KjEoRGoxHtbANcu2BNdJdRCEIz/RA40w5CM+UgNNM9aV1fpWW11vr9wIABAwZsXrCrBzcKbNofMcCAAQMGrBvY6IABAwYMGDBgwIABAwbMxtnGGRgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDFhO/gwBDBgwYMCAAQMGDBgwYIPb9s3mk5eAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGLKTaV/53X0/AgAEDJmDAgAETMGDAgAkYMGDAgAEDBgwYMGDAgAEDBuyvoN5baVlXX0/AgAEDJmDAgEmSNKAP8jI5Lu05uHwAAAAASUVORK5CYII=",
    "blaster": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABmklEQVR42u3c0Q2CMBRAUcZxHMdxA9dwnA7hEGxQ45/hQ9K0pH3tucn7FAlHUSCwbZIkSZIkSZIkSZIkLVNumK0ZBApcYCxoAbGgBYMCFxgLGjBY0GBBmwELGjBYwIABA7YI2Dvn1GOAAVsL7GyXVQpw9npgwIABAwYMGDBgwIABAwYMGLD+p6a+i/odp6aAqeXllSOYyyvA1BrNBUxgwCKhUQmERqMR2vHPRelcjbXcBwZYwG/4yLvCtO/53yy9Sx7xNwvYAGgl6wOsM1rpuiwHdn88c83UVvv+wIABAwZsXrCrNxwwYMBmBlv2jDuwScB6BwwYMGDAgAEDBgwYMGAOnB04AwMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAYtT9JshgAEDBgwYMGDAgAEDBix6t5TzyLMJGDBgwIABAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgwILU+mHGwz4cGRgwYAIGDBgwAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMAiQL1SrpmrlydgwIABEzBgwCRJGrgPqA8ylxS23PgAAAAASUVORK5CYII=",
    "serious": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABaElEQVR42u3b0Q2DIBRAUcdxA9foOG6POkFpAeHBuQlfRk04iQGN2yZJkiRJkiRJkiRJ0jKlipnNIFDgAmNBC4gFLRgUuMBY0IDBggYL2gxY0IDBAgYMGDBgwIABAwYM2PBgz+Gc0ep8YMCAAQMGzKIDGDBgwIABy1+gAAMmYMCArb7woAMMGixosGqh5b7Q/edFLyxg0DwKwYGKhmaWA6GZ3S/t+5FKRmml9wcGDBgwYPOCtZ64XmDTLmKAAQMGDFg1sN4BAwYMGDBgwIABAwYMmI2zjTMwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBiwOPkZAhgwYMCAAQMGDBgwYMA6d96bzZGHgAEDBgwYMGDAgAEDBgwYMGDAgAEDBgwYMGDAgAEDBixIv37yf/t6AgYMGDABAwYMmIABAwZMwIABAwYMGDBgwIABAwYMGDBgS0F9zlQyWl9PwIABAyZgwIBJkjRwF9d2/3a0U64hAAAAAElFTkSuQmCC",
    "laugh": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABe0lEQVR42u3b4Q3CIBCA0Y7TDVzDcbo96gS2uaP04H0Jv0xrwksIYNw2SZIkSZIkSZIkSZKWqSVmNotAgSuMBa0gFrRiUOAKY0EDBgsaLGgzYEEDBgsYMGDAgAEDBgwYMGDAgAFbGuz38ZnR63lgwCyJlkRgwIABA1Yd7MpGAhgwYMCAAVth40EH2BpoZ6+ZMq6jYN14r5gFRiOIlrWZcOELTCOXRLOfBNcbzGwX2vKb5UJoZvdP+/5qkREt+v3AgAEDBmxesN4TNwps2k0MMGDAgAFLAxsdMGDAgAEDBgwYMGDAgDk4OzgDAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgwIABq5M/QwADBgwYMGDAgAEDBgzY4I7vYfPJQ8CAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQNWpKs/+d/9PgEDBgyYgAEDBkzAgAEDJmDAgAEDBgwYMGDAgAEDBgwYsKWg3keLjN7vEzBgwIAJGDBgkiQ9uA+jTc+mgGRxtQAAAABJRU5ErkJggg==",
    "hurt": "iVBORw0KGgoAAAANSUhEUgAAAGwAAACSCAYAAACg/i+kAAABjUlEQVR42u3bwRHCIBBA0ZRDB7ZhOSnWXqLevDnIErPs+zMcgyPvEMBx2yRJkiRJkiRJkiRJKtMRmNVMAgUuMRa0hFjQkkGBS4wFDRgsaLCgrYAFDRgsYMCAAQMGDBgwYNXAHq11jejngQEDBsw7DBgwYMCAAQMGDNhSYO+pPgcwYAIGDFjUgmfdeAADlh+sc56hUf79FfnlrwRWftMQNd+vm4qe5+zygK0L9m3O2WDOUQMLcSaYg2/Qgpyx6XBTEbwoM8FcLX0Ba+12jIzRRj8fGDBgwIABywa2zJUWMGDAgAGbBvbvgAEDBgwYMGDAgAEDBszB2cEZWGWw3oABAwYMGDBgwIABAwYMGDBgwIABAwYMGDBgwIr/GQIYMGDAgAEDBgwYMGBb+fbXYfPKQ8CAAQMGDBgwYMCAAQMGDBgwYMCAAQMGDBgwYMCAAQOWpN6f/M+eT8CAAQMmYMCAARMwYMCACRgwYMCAAQMGDBgwYMCAAQMGrBTUfT9Gxuz5BAwYMGACBgyYJEkX7gkCWTGtOcV2pwAAAABJRU5ErkJggg==",
}

GASTER_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAFAAAAByCAYAAADEdVaQAAABVklEQVR4nO3QwWkDAAzF0Ow/WYfoLik9+tZ8haoFPfDRYOvxSJIkSZIkSZIkyY89X/S98u4Zbvg7CggVECogVECogFABoQJCBYQKCBUQKiBUQKiAUAGhl69/wcfz+flXp4AFLGABC1jAAhawgAUsYAEL+Kve9vw72DEWdrPDjrGwmx12jIXd7LBjLOxmhx1jYTc77BgLu9lhx1jYzQ47xsJudtgxFnazw46xsJsddoyF3eywYyzsZocdY2E3O+wYC7vZYcdY2M0OO8bCbnbYMRZ2s8OOsbCbHXaMhd3ssGMs7GaHHWNhNzvsGAu72WHHWNjNDjvGwm72FoWACggVECogVECogFABoQJCBYQKCBUQKiBUQKiAUAGhAkIFhAoIFRAqIFRAqIBQAaECQgWECggVECogVECogFABoQJCBYQKCBUQKiBUQKiAUAGhAkIFhAoI/feAXxhfwE9l8piGAAAAAElFTkSuQmCC"
)


class LBSansAnimator:
    POSES = (
        "idle_0", "idle_1", "clenched", "fatal", "glow_0", "glow_1",
        "shrug", "point", "dodge_l", "dodge_r", "blaster", "serious", "laugh", "hurt",
    )

    def __init__(self):
        self.frames = {n: LBSprites._from_b64(SANS_ANIMS_B64[n]) for n in self.POSES}
        self.pose = "shrug"
        self.tick = 0
        self.flash_pose = None
        self.flash_timer = 0

    def flash(self, pose, frames):
        self.flash_pose = pose
        self.flash_timer = frames

    def update(self, state, turn_timer, attack_pattern, blasters_firing, player_hit):
        if self.flash_timer > 0:
            self.flash_timer -= 1
            if self.flash_timer == 0:
                self.flash_pose = None
            return
        self.tick += 1
        if state == "INTRO":
            self.pose = "shrug"
        elif state == "MENU":
            self.pose = "idle_0" if (self.tick // 18) % 2 == 0 else "idle_1"
        elif state == "SANS_TURN":
            if player_hit:
                self.flash("dodge_r" if (self.tick % 2) else "dodge_l", 12)
            elif blasters_firing:
                self.pose = "glow_0" if (self.tick // 8) % 2 == 0 else "glow_1"
            elif attack_pattern == 0:
                self.pose = "point" if turn_timer > 30 else "clenched"
            elif attack_pattern == 1:
                self.pose = "blaster" if turn_timer > 20 else "serious"
            else:
                self.pose = "idle_0" if (self.tick // 18) % 2 == 0 else "idle_1"
            if turn_timer > 330:
                self.pose = "laugh"
        elif state == "GAME_OVER":
            self.pose = "fatal"

    def surface(self):
        return self.frames.get(self.flash_pose or self.pose, self.frames["idle_0"])


class LBSprites:
    _bank = None

    @staticmethod
    def _from_bytes(data):
        return pygame.image.load(_lb_io.BytesIO(data)).convert_alpha()

    @classmethod
    def _from_b64(cls, b64):
        return cls._from_bytes(_lb_b64.b64decode(b64))

    @classmethod
    def get(cls):
        if cls._bank is None:
            cls._bank = cls()
        return cls._bank

    def __init__(self):
        self.blaster = self._from_b64(GASTER_B64)
        self.sans_anim = LBSansAnimator()


def lb_sprites():
    return LBSprites.get()

LB_CH = 5  # last breath phase 1 chapter index


# ---------------------------------------------------------------- audio synth
NAMES = {'C':-9,'C#':-8,'Db':-8,'D':-7,'D#':-6,'Eb':-6,'E':-5,'F':-4,'F#':-3,
         'Gb':-3,'G':-2,'G#':-1,'Ab':-1,'A':0,'A#':1,'Bb':1,'B':2}
def nfreq(name):
    octv = int(name[-1]); key = name[:-1]
    return 440.0 * (2 ** ((NAMES[key] + (octv - 4) * 12) / 12))

def osc(w, f, t, duty=0.5):
    p = (t * f) % 1.0
    if w in ('sq', 'pulse'): return 1.0 if p < duty else -1.0
    if w == 'thin':  return 1.0 if p < 0.125 else -1.0
    if w == 'mid':   return 1.0 if p < 0.25 else -1.0
    if w == 'fat':   return 1.0 if p < 0.75 else -1.0
    if w == 'saw':   return 2.0 * p - 1.0
    if w == 'tri':   return 4.0 * abs(p - 0.5) - 1.0
    return random.uniform(-1.0, 1.0)

def vib(f, t, depth=0.018, rate=5.5):
    return f * (1.0 + depth * math.sin(t * rate * math.tau))

def _pcm(buf):
    """float mono buffer → pygame Sound (files = off, no wav)"""
    peak = max(abs(s) for s in buf) or 1.0
    a = array.array('h', (int(max(-1.0, min(1.0, s * 0.85 / peak)) * 28000) for s in buf))
    return pygame.mixer.Sound(a)

def _kick(buf, pos, vol=0.32):
  """tonal NES kick — not white noise"""
  L = min(380, len(buf) - pos)
  for j in range(L):
    t = j / SR
    f = 195.0 * (0.992 ** j)
    env = (1.0 - j / L) ** 2.2
    buf[pos + j] += math.sin(t * f * math.tau) * vol * env

def _snare(buf, pos, vol=0.10):
  L = min(220, len(buf) - pos)
  for j in range(L):
    env = (1.0 - j / L) ** 1.6
    tone = math.sin(j / SR * 185 * math.tau) * 0.35
    nz = (random.random() * 2.0 - 1.0) * 0.65
    buf[pos + j] += (tone + nz) * vol * env

def _hat(buf, pos, vol=0.025):
  L = min(90, len(buf) - pos)
  for j in range(L):
    buf[pos + j] += (random.random() * 2.0 - 1.0) * vol * (1.0 - j / L)

DUTY = {'sq': 0.5, 'thin': 0.125, 'mid': 0.25, 'fat': 0.75}

def _m(seq):
    """compact 'N:d N:d ...' → [(note, beats), ...]"""
    out = []
    for tok in seq.split():
        if tok == 'R':
            out.append(('R', 1))
        elif ':' in tok:
            n, d = tok.split(':'); out.append((n, float(d)))
    return out

# --- AC RUNE custom OST (Undertale Yellow style — leitmotif + AABB, files = off) -
# The "meow leitmotif" — 8-note hook reused in every track (like Yellow's main motif)
LEIT = _m("A3:0.5 C4:0.5 E4:0.5 A4:0.5 G4:0.5 E4:0.5 C4:0.5 A3:0.5")

# a_cat's_morning — title, 82 BPM, A minor, gentle AABB
MEL_AM = _m("A3:1.5 C4:0.5 E4:1 D4:1 C4:1 B3:1 A3:2 E3:1 A3:1 C4:2 B3:1 A3:1 "
            "F3:1 A3:1 C4:1 E4:1 D4:2 C4:2 B3:1 C4:1 D4:1 E4:1 A4:4 "
            "A3:1.5 C4:0.5 E4:1 D4:1 C4:1 B3:1 A3:2 E3:1 A3:1 C4:2 B3:1 A3:1 "
            "G3:1 B3:1 D4:1 G4:1 E4:2 D4:2 C4:1 B3:1 A3:1 E3:1 A3:4")
BAS_AM = _m("A2:2 E2:2 A2:2 E2:2 F2:2 C3:2 G2:2 E2:2 A2:4")

# field_of_static — CH1 field, 118 BPM, bouncy ostinato intro
MEL_FS = _m("A3:0.25 C4:0.25 E4:0.25 A4:0.25 G4:0.25 E4:0.25 C4:0.25 A3:0.25 "
            "C4:0.25 E4:0.25 G4:0.25 C5:0.25 A4:0.25 G4:0.25 E4:0.25 C4:0.25 "
            "D4:0.5 F4:0.5 A4:0.5 D5:0.5 C5:0.5 A4:0.5 F4:0.5 D4:0.5 "
            "A3:0.25 C4:0.25 E4:0.25 A4:0.25 G4:0.25 F4:0.25 E4:0.25 D4:0.25 "
            "E4:0.5 G4:0.5 B4:0.5 E5:0.5 D5:0.5 B4:0.5 G4:0.5 E4:0.5 "
            "A3:0.25 C4:0.25 E4:0.25 A4:0.25 G4:0.25 E4:0.25 C4:0.25 A3:0.25 A3:2")
BAS_FS = _m("A2:0.5 E2:0.5 A2:0.5 E2:0.5 D2:0.5 A2:0.5 D2:0.5 A2:0.5")

# neon_harbor — CH2, 124 BPM, leitmotif +2 semitones (B major energy)
MEL_NH = _m("B3:0.25 D4:0.25 F#4:0.25 B4:0.25 A4:0.25 F#4:0.25 D4:0.25 B3:0.25 "
            "D4:0.5 F#4:0.5 A4:0.5 D5:0.5 C#5:0.5 A4:0.5 F#4:0.5 D4:0.5 "
            "E4:0.5 G4:0.5 B4:0.5 E5:0.5 D5:0.5 B4:0.5 G4:0.5 E4:0.5 "
            "B3:0.25 D4:0.25 F#4:0.25 B4:0.25 A4:0.25 G4:0.25 F#4:0.25 E4:0.25 "
            "F#4:0.5 A4:0.5 C#5:0.5 F#5:0.5 E5:0.5 C#5:0.5 A4:0.5 F#4:0.5 B3:2")
BAS_NH = _m("B2:0.5 F#2:0.5 B2:0.5 F#2:0.5 E2:0.5 B2:0.5 E2:0.5 B2:0.5")

# boardwalk_vhs — CH3, 112 BPM, detuned wobble
MEL_BV = _m("G3:0.5 Bb3:0.5 D4:0.5 G4:0.5 F4:0.5 D4:0.5 Bb3:0.5 G3:0.5 "
            "A3:0.5 C4:0.5 E4:0.5 A4:0.5 G4:0.5 E4:0.5 C4:0.5 A3:0.5 "
            "Bb3:0.25 D4:0.25 F4:0.25 Bb4:0.25 Ab4:0.25 F4:0.25 D4:0.25 Bb3:0.25 "
            "C4:0.5 Eb4:0.5 G4:0.5 C5:0.5 Bb4:0.5 G4:0.5 Eb4:0.5 C4:0.5 "
            "G3:0.5 Bb3:0.5 D4:0.5 G4:0.5 F4:0.5 Eb4:0.5 D4:0.5 C4:0.5 G3:2")
BAS_BV = _m("G2:0.5 D3:0.5 G2:0.5 D3:0.5 C3:0.5 G2:0.5 C3:0.5 G2:0.5")

# hollow_choir — CH4, 100 BPM, minor leitmotif, choral
MEL_HC = _m("A3:1 C4:1 E4:1 A4:1 G4:0.5 E4:0.5 C4:1 A3:1 "
            "F3:1 A3:1 C4:1 F4:1 E4:0.5 C4:0.5 A3:1 G3:1 "
            "A3:0.5 C4:0.5 E4:0.5 G4:0.5 A4:0.5 G4:0.5 E4:0.5 C4:0.5 "
            "B3:0.5 D4:0.5 F4:0.5 A4:0.5 G4:0.5 F4:0.5 D4:0.5 B3:0.5 "
            "A3:1 C4:1 E4:1 A4:1 G4:0.5 E4:0.5 C4:1 A3:2")
BAS_HC = _m("A2:2 E2:2 D2:2 A2:2 C3:2 G2:2 A2:4")

# pipeworks — CH5, 128 BPM, plumbing groove
MEL_PW = _m("D4:0.5 F4:0.5 A4:0.5 D5:0.5 C5:0.5 A4:0.5 F4:0.5 D4:0.5 "
            "G3:0.5 B3:0.5 D4:0.5 G4:0.5 F4:0.5 D4:0.5 B3:0.5 G3:0.5 "
            "A3:0.5 C4:0.5 E4:0.5 A4:0.5 G4:0.5 E4:0.5 C4:0.5 A3:0.5 "
            "D4:0.25 F4:0.25 A4:0.25 D5:0.25 F5:0.25 D5:0.25 A4:0.25 F4:0.25 "
            "G3:0.5 B3:0.5 D4:0.5 G4:0.5 A3:0.5 C4:0.5 E4:0.5 A4:0.5 D4:2")
BAS_PW = _m("D2:0.5 A2:0.5 D3:0.5 A2:0.5 G2:0.5 D3:0.5 G2:0.5 D2:0.5")

# rude_rumble — battle, 140 BPM, aggressive leitmotif + arpeggios
MEL_RR = _m("A3:0.25 C4:0.25 E4:0.25 A4:0.25 G4:0.25 E4:0.25 C4:0.25 A3:0.25 "
            "B3:0.25 D4:0.25 F#4:0.25 B4:0.25 A4:0.25 F#4:0.25 D4:0.25 B3:0.25 "
            "C4:0.25 E4:0.25 G4:0.25 C5:0.25 B4:0.25 G4:0.25 E4:0.25 C4:0.25 "
            "A3:0.25 C4:0.25 E4:0.25 A4:0.25 C5:0.25 A4:0.25 E4:0.25 C4:0.25 "
            "D4:0.5 F4:0.5 A4:0.5 D5:0.5 C5:0.5 A4:0.5 F4:0.5 D4:0.5")
BAS_RR = _m("A2:0.5 A2:0.5 E2:0.5 E2:0.5 D2:0.5 D2:0.5 A2:0.5 A2:0.5")
ARP_RR = [('A3','C4','E4','A4'),('B3','D4','F#4','B4'),('C4','E4','G4','C5'),('D4','F#4','A4','D5')]

# PREFECT! — boss CH1, 152 BPM
MEL_PF = _m("A3:0.25 C4:0.25 Eb4:0.25 G4:0.25 A4:0.25 G4:0.25 Eb4:0.25 C4:0.25 "
            "B3:0.25 D4:0.25 F4:0.25 A4:0.25 Ab4:0.25 F4:0.25 D4:0.25 B3:0.25 "
            "A4:0.5 G4:0.5 F4:0.5 Eb4:0.5 D4:0.5 C4:0.5 B3:0.5 A3:0.5 "
            "A3:0.25 C4:0.25 E4:0.25 A4:0.25 G4:0.25 E4:0.25 C4:0.25 A3:0.25 A3:2")
BAS_PF = _m("A2:0.5 A2:0.5 G2:0.5 F2:0.5 E2:0.5 E2:0.5 A2:0.5 A2:0.5")
ARP_PF = [('A3','C4','Eb4','A4'),('G3','B3','D4','G4'),('F3','A3','C4','F4'),('E3','G3','B3','E4')]

# CIRCUIT CROWN — boss CH2, 156 BPM
MEL_CC = _m("B3:0.25 D4:0.25 F#4:0.25 B4:0.25 A4:0.25 F#4:0.25 D4:0.25 B3:0.25 "
            "C4:0.25 E4:0.25 G4:0.25 C5:0.25 B4:0.25 G4:0.25 E4:0.25 C4:0.25 "
            "B4:0.5 A4:0.5 G4:0.5 F#4:0.5 E4:0.5 D4:0.5 C#4:0.5 B3:0.5 "
            "B3:0.25 D4:0.25 F#4:0.25 B4:0.25 C#5:0.25 B4:0.25 F#4:0.25 D4:0.25 B3:2")
BAS_CC = _m("B2:0.5 B2:0.5 F#2:0.5 F#2:0.5 E2:0.5 E2:0.5 B2:0.5 B2:0.5")
ARP_CC = [('B3','D4','F#4','B4'),('C4','E4','G4','C5'),('A3','C4','E4','A4'),('G3','B3','D4','G4')]

# JESTER STATIC — boss CH3, 158 BPM, chromatic chaos
MEL_JS = _m("G3:0.25 Bb3:0.25 Db4:0.25 F4:0.25 G4:0.25 F4:0.25 Db4:0.25 Bb3:0.25 "
            "A3:0.25 C4:0.25 Eb4:0.25 G4:0.25 Ab4:0.25 G4:0.25 Eb4:0.25 C4:0.25 "
            "G4:0.5 F4:0.5 Eb4:0.5 D4:0.5 C4:0.5 Bb3:0.5 A3:0.5 G3:0.5 "
            "G3:0.25 Bb3:0.25 D4:0.25 G4:0.25 F4:0.25 D4:0.25 Bb3:0.25 G3:0.25 G3:2")
BAS_JS = _m("G2:0.5 G2:0.5 D3:0.5 D3:0.5 C3:0.5 C3:0.5 G2:0.5 G2:0.5")
ARP_JS = [('G3','Bb3','D4','G4'),('A3','C4','Eb4','A4'),('Bb3','D4','F4','Bb4'),('C4','Eb4','G4','C5')]

# WARDEN'S HYMN — boss CH4, 146 BPM, choral boss
MEL_WH = _m("E4:0.5 G4:0.5 B4:0.5 E5:0.5 D5:0.5 B4:0.5 G4:0.5 E4:0.5 "
            "C4:0.5 E4:0.5 G4:0.5 C5:0.5 B4:0.5 G4:0.5 E4:0.5 C4:0.5 "
            "A3:0.5 C4:0.5 E4:0.5 A4:0.5 G4:0.5 E4:0.5 C4:0.5 A3:0.5 "
            "E4:0.25 G4:0.25 B4:0.25 E5:0.25 D5:0.25 B4:0.25 G4:0.25 E4:0.25 E4:2")
BAS_WH = _m("E2:0.5 B2:0.5 E2:0.5 B2:0.5 C3:0.5 G2:0.5 C3:0.5 G2:0.5")

# KNIGHT OF PIPES — final boss, 106 BPM, solemn march
MEL_KP = _m("D4:1 F4:1 A4:1 D5:1 C5:0.5 A4:0.5 G4:1 F4:1 "
            "E4:1 G4:1 A4:2 F4:1 D4:1 "
            "A3:1 C4:1 E4:1 A4:1 G4:0.5 E4:0.5 C4:1 A3:1 "
            "D4:0.5 F4:0.5 A4:0.5 C5:0.5 D5:1 C5:1 A4:1 G4:1 F#4:0.5 E4:0.5 D4:3")
BAS_KP = _m("D2:2 D2:2 A2:2 A2:2 G2:2 D2:2 A2:4")

# plombo's_theme — NPC, 142 BPM, laid-back plumber shuffle
MEL_PL = _m("C4:0.5 E4:0.5 G4:0.5 C5:0.5 B4:0.5 A4:0.5 G4:0.5 E4:0.5 "
            "F4:0.5 A4:0.5 C5:0.5 F5:0.5 E5:0.5 C5:0.5 A4:0.5 F4:0.5 "
            "G4:0.5 B4:0.5 D5:0.5 G5:0.5 F5:0.5 D5:0.5 B4:0.5 G4:0.5 "
            "C4:0.5 E4:0.5 G4:0.5 C5:0.5 A4:0.5 G4:0.5 E4:0.5 C4:0.5 C4:2")
BAS_PL = _m("C3:0.5 G2:0.5 C3:0.5 G2:0.5 F2:0.5 C3:0.5 F2:0.5 C3:0.5")

# a_cat's_tomorrow — credits, 90 BPM, leitmotif resolved in major
MEL_AT = _m("A3:1 C4:1 E4:1 A4:1 G4:0.5 E4:0.5 C4:1 A3:1 "
            "F3:1 A3:1 C4:1 F4:1 E4:0.5 C4:0.5 A3:1 G3:1 "
            "A3:1.5 C4:0.5 E4:1 D4:1 C4:1 B3:1 A3:2 "
            "C4:1 E4:1 A4:1 E5:1 D5:0.5 C5:0.5 B4:0.5 A4:0.5 A4:4")
BAS_AT = _m("A2:2 E2:2 F2:2 C3:2 G2:2 D3:2 A2:4")

# (melody, bass, bpm, lead, tr, name, arp, harm, strings, drums, leit, piano)
SONGS = {
 'title':  (MEL_AM, BAS_AM,  82,'mid',  0,"a_cat's_morning",    None,   True,  False,'soft',  True, True),
 'world0': (MEL_FS, BAS_FS, 118,'sq',   0,"field_of_static",    None,   True,  True, 'bounce', True, True),
 'world1': (MEL_NH, BAS_NH, 124,'sq',   0,"neon_harbor",        None,   True,  True, 'bounce', True, False),
 'world2': (MEL_BV, BAS_BV, 112,'mid',  0,"boardwalk_vhs",      None,   True,  False,'bounce', True, False),
 'world3': (MEL_HC, BAS_HC, 100,'thin', 0,"hollow_choir",       None,   True,  True, 'soft',   True, True),
 'world4': (MEL_PW, BAS_PW, 128,'sq',   0,"pipeworks",          None,   True,  False,'bounce', True, False),
 'battle': (MEL_RR, BAS_RR, 140,'thin', 0,"rude_rumble",        ARP_RR, True,  False,'rude',   True, False),
 'boss0':  (MEL_PF, BAS_PF, 152,'thin', 0,"PREFECT!",           ARP_PF, True,  False,'boss',   True, False),
 'boss1':  (MEL_CC, BAS_CC, 156,'thin', 0,"CIRCUIT CROWN",      ARP_CC, True,  False,'boss',   True, False),
 'boss2':  (MEL_JS, BAS_JS, 158,'mid',  0,"JESTER STATIC",      ARP_JS, True,  False,'boss',   True, False),
 'boss3':  (MEL_WH, BAS_WH, 146,'thin', 0,"WARDEN'S HYMN",      None,   True,  True, 'boss',   True, True),
 'final':  (MEL_KP, BAS_KP, 106,'mid',  0,"KNIGHT OF PIPES",    None,   True,  False,'soft',   True, True),
 'plombo': (MEL_PL, BAS_PL, 142,'fat',  0,"plombo's_theme",     None,   False, False,'bounce', False,False),
 'end':    (MEL_AT, BAS_AT,  90,'mid',  0,"a_cat's_tomorrow",   None,   True,  True, 'soft',   True, True),
}

class Music:
    def __init__(self, ok):
        self.ok = ok; self.cache = {}; self.cur = None; self.snd = None
        self.mute = False; self.now = ""
    def build(self, key):
        mel, bas, bpm, wave, tr, name, arp, harm, strings, drums, leit, piano = SONGS[key]
        spb = 60.0 / bpm
        total = sum(b for _, b in mel)
        n = int(total * spb * SR)
        buf = [0.0] * n
        duty = DUTY.get(wave, 0.5)
        # leitmotif bed — quiet, no extra triangle (bass handles low end)
        if leit:
            lpos = 0; li = 0; bar = int(spb * SR * 2)
            while lpos < n:
                nt, b = LEIT[li % len(LEIT)]; li += 1
                ns = min(int(b * spb * SR), bar, n - lpos)
                if nt != 'R':
                    f = nfreq(nt) * (2 ** (tr / 12))
                    for i in range(ns):
                        env = min(1.0, i / 80.0) * (1.0 if i < ns - 300 else (ns - i) / 300.0)
                        buf[lpos + i] += osc('thin', f, (lpos + i) / SR) * 0.03 * env
                lpos += bar
        # lead — pulse + vibrato
        pos = 0
        for nt, b in mel:
            ns = int(b * spb * SR)
            if nt != 'R':
                f = nfreq(nt) * (2 ** (tr / 12))
                for i in range(ns):
                    t = (pos + i) / SR
                    env = min(1.0, i / 100.0) * (1.0 if i < ns - 500 else (ns - i) / 500.0)
                    buf[pos + i] += osc('pulse', vib(f, t), t, duty) * 0.22 * env
            pos += ns
        # piano stabs
        if piano:
            beat = int(spb * SR); i = 0
            while i < n:
                f = nfreq('A3') * (2 ** (tr / 12))
                for j in range(min(900, n - i)):
                    env = max(0.0, 1.0 - j / 900) ** 1.5
                    buf[i + j] += osc('sq', f, (i + j) / SR) * 0.06 * env
                i += beat * 2
        # harmony — 12.5% pulse octave down
        if harm:
            pos = 0
            for nt, b in mel:
                ns = int(b * spb * SR)
                if nt != 'R':
                    f = nfreq(nt) * (2 ** ((tr - 12) / 12))
                    for i in range(ns):
                        t = (pos + i) / SR
                        env = min(1.0, i / 140.0) * (1.0 if i < ns - 700 else (ns - i) / 700.0)
                        buf[pos + i] += osc('thin', vib(f, t, 0.010, 4.0), t) * 0.07 * env
                pos += ns
        # string pad
        if strings:
            pos = 0
            for nt, b in mel:
                ns = int(b * spb * SR)
                if nt != 'R':
                    f = nfreq(nt) * (2 ** ((tr + 12) / 12))
                    for i in range(ns):
                        t = (pos + i) / SR
                        env = min(1.0, i / 250.0) * (1.0 if i < ns - 900 else (ns - i) / 900.0)
                        v = osc('thin', vib(f, t, 0.006, 3.2), t)
                        buf[pos + i] += v * 0.025 * env
                pos += ns
        # arpeggio
        if arp:
            sixteenth = max(1, int(spb * SR / 4))
            ai = 0; ti = 0
            for i in range(0, n, sixteenth):
                chord = arp[ai % len(arp)]
                nt = chord[ti % len(chord)]
                f = nfreq(nt) * (2 ** (tr / 12))
                for j in range(min(sixteenth, n - i)):
                    env = 1.0 if j < sixteenth - 100 else (sixteenth - j) / 100.0
                    buf[i + j] += osc('mid', f, (i + j) / SR) * 0.08 * env
                ti += 1
                if ti % len(chord) == 0: ai += 1
        # bass — triangle
        pos = 0; bi = 0
        while pos < n:
            nt, b = bas[bi % len(bas)]; bi += 1
            ns = min(int(b * spb * SR), n - pos)
            f = nfreq(nt) * (2 ** (tr / 12))
            for i in range(ns):
                t = (pos + i) / SR
                env = 1.0 if i < ns - 400 else (ns - i) / 400.0
                buf[pos + i] += osc('tri', f, t) * 0.18 * env
            pos += ns
        # drums — tonal kick/snare/hat (NOT full-band white noise)
        beat = int(spb * SR); half = max(1, beat // 2); i = 0; beat_n = 0
        while i < n:
            if drums in ('bounce', 'rude', 'boss'):
                if beat_n % 4 in (0, 2):
                    _kick(buf, i, 0.34 if drums == 'rude' else 0.28)
                if beat_n % 4 in (1, 3):
                    _snare(buf, i, 0.12 if drums == 'boss' else 0.09)
            if drums in ('bounce', 'rude', 'boss', 'soft'):
                nh = 2 if drums != 'soft' else 1
                for h in range(nh):
                    _hat(buf, i + h * half, 0.03 if drums == 'rude' else 0.02)
            i += beat; beat_n += 1
        # light echo on dry signal only
        delay = int(0.12 * SR); fb = 0.20
        echo = [0.0] * n; out = [0.0] * n
        for i in range(n):
            tap = echo[i - delay] if i >= delay else 0.0
            out[i] = buf[i] + tap * fb
            echo[i] = out[i]
        return _pcm(out), name
    def play(self, key):
        if not self.ok or key == self.cur: return
        if self.snd: self.snd.stop()
        if key not in self.cache:
            try: self.cache[key] = self.build(key)
            except Exception: self.ok = False; return
        self.snd, self.now = self.cache[key]
        self.cur = key
        if not self.mute: self.snd.play(-1)
    def toggle(self):
        self.mute = not self.mute
        if self.snd: self.snd.stop() if self.mute else self.snd.play(-1)

def tone(freq, dur, wave='sq', vol=0.3, slide=0.0):
    n = int(dur * SR); buf = [0.0] * n
    for i in range(n):
        f = freq + slide * (i / n)
        env = 1 - i / n
        buf[i] = osc(wave, f, i / SR) * vol * env
    return _pcm(buf)

# ---------------------------------------------------------------- helpers
def txt(surf, s, x, y, size=18, col=WHITE, center=False, font=[None]*80):
    if font[size] is None: font[size] = pygame.font.Font(None, size + 6)
    img = font[size].render(s, False, col)
    r = img.get_rect()
    if center: r.center = (x, y)
    else: r.topleft = (x, y)
    surf.blit(img, r); return r

def draw_actor(s, x, y, who, f=0, scale=1.0):
    bob = int(math.sin(f * 0.15) * 2)
    x, y = int(x), int(y + bob)
    sz = int(22 * scale)
    if who == 'AC':      # blue cat
        pygame.draw.rect(s, BLUE, (x - sz//2, y - sz, sz, sz), border_radius=4)
        pygame.draw.polygon(s, BLUE, [(x - sz//2, y - sz), (x - sz//2 + 6, y - sz - 9), (x - sz//2 + 10, y - sz)])
        pygame.draw.polygon(s, BLUE, [(x + sz//2, y - sz), (x + sz//2 - 6, y - sz - 9), (x + sz//2 - 10, y - sz)])
        pygame.draw.line(s, BLUE, (x + sz//2, y - 6), (x + sz//2 + 9, y - 14), 3)
        pygame.draw.rect(s, BLACK, (x - 6, y - sz + 7, 3, 3)); pygame.draw.rect(s, BLACK, (x + 3, y - sz + 7, 3, 3))
    elif who == 'RYEN':  # time traveller
        pygame.draw.rect(s, PURPLE, (x - sz//2, y - sz, sz, sz), border_radius=3)
        pygame.draw.rect(s, (255,255,180), (x - sz//2 + 2, y - sz + 4, sz - 4, 6))  # goggles
        pygame.draw.line(s, (255,255,180), (x, y - 2), (x, y - sz//2), 2)           # clock hand
    elif who == 'LASSE': # fox
        pygame.draw.rect(s, ORANGE, (x - sz//2, y - sz, sz, sz), border_radius=5)
        pygame.draw.polygon(s, ORANGE, [(x - sz//2, y - sz), (x - sz//2 + 4, y - sz - 11), (x - sz//2 + 9, y - sz)])
        pygame.draw.polygon(s, ORANGE, [(x + sz//2, y - sz), (x + sz//2 - 4, y - sz - 11), (x + sz//2 - 9, y - sz)])
        pygame.draw.circle(s, WHITE, (x + sz//2 + 7, y - 8), 5)                      # fluffy tail tip
        pygame.draw.rect(s, BLACK, (x - 6, y - sz + 8, 3, 3)); pygame.draw.rect(s, BLACK, (x + 3, y - sz + 8, 3, 3))
    elif who == 'PLOMBO':
        pygame.draw.rect(s, (230, 60, 60), (x - 12, y - 24, 24, 12))
        pygame.draw.rect(s, (60, 60, 230), (x - 12, y - 12, 24, 12))
        pygame.draw.rect(s, (40, 30, 20), (x - 8, y - 15, 16, 4))  # mustache
    elif who == 'BECCA':
        pygame.draw.rect(s, (240, 200, 220), (x - 11, y - 26, 22, 26), border_radius=6)
    elif who == 'JOSEPH':
        pygame.draw.rect(s, (250, 210, 90), (x - 13, y - 28, 26, 28), border_radius=6)
        pygame.draw.circle(s, (180, 120, 30), (x, y - 30), 6)

SPEAKER_COL = {'AC': BLUE, 'RYEN': PURPLE, 'LASSE': ORANGE, 'PLOMBO': RED,
               'BECCA': (240,200,220), 'JOSEPH': (250,210,90),
               'WRENCHARD': GREEN, '': GRAY}

# ---------------------------------------------------------------- game data
def make_party():
    return [
        {'name': 'AC',    'hp': 90,  'mx': 90,  'atk': 10, 'col': BLUE,
         'spell': ('MEOW', 10, 'mercy')},
        {'name': 'RYEN',  'hp': 110, 'mx': 110, 'atk': 14, 'col': PURPLE,
         'spell': ('REWIND', 32, 'healall')},
        {'name': 'LASSE', 'hp': 75,  'mx': 75,  'atk': 7,  'col': ORANGE,
         'spell': ('FOXFIRE', 20, 'damage')},
    ]

ITEMS = {'ChocCone': 60, 'CatTea': 45, 'PipeSoda': 80, 'DustBun': 30}

MINIONS = [
 {'name':'DUSTLING','hp':60,'atk':4,'pat':'rain','col':GRAY,
  'quotes':['* Dustling drifts in a small circle.','* Smells like an old chalkboard.'],
  'acts':[('SWEEP',45,'* You sweep gently. Dustling feels organized.'),
          ('SNEEZE',30,'* You sneeze. Dustling relates deeply.')]},
 {'name':'SPARKFISH','hp':70,'atk':5,'pat':'aim','col':(120,220,255),
  'quotes':['* Sparkfish swims through pure signal.','* It hums at 60hz.'],
  'acts':[('UNPLUG',45,'* You mime unplugging it. Sparkfish calms down.'),
          ('SPLASH',30,'* You splash imaginary water. Refreshing!')]},
 {'name':'TAPE GHOST','hp':80,'atk':6,'pat':'wave','col':(220,220,255),
  'quotes':['* Tape Ghost rewinds itself nervously.','* Please be kind. Rewind.'],
  'acts':[('REWIND',45,'* You rewind it carefully. It sighs in stereo.'),
          ('LABEL',30,'* You write a nice label. It feels remembered.')]},
 {'name':'HYMNLING','hp':90,'atk':6,'pat':'notes','col':(255,240,170),
  'quotes':['* Hymnling holds a very long note.','* The echo has an echo.'],
  'acts':[('HARMONIZE',45,'* You hum a third above. Beautiful.'),
          ('CONDUCT',30,'* You wave your paws. It follows tempo.')]},
 {'name':'PIPELING','hp':100,'atk':7,'pat':'pipes','col':GREEN,
  'quotes':['* Pipeling gurgles menacingly.','* Water pressure rising.'],
  'acts':[('TIGHTEN',45,'* You tighten its valve. Much less drippy.'),
          ('KNOCK',30,'* You knock twice. It knocks back. Friends?')]},
]

BOSSES = [
 {'name':'CARD PREFECT','hp':260,'atk':5,'pat':'cards','col':(255,120,120),'song':'boss0',
  'quotes':['* The Prefect checks your hall pass.','* "RUNNING IN THE HALLS?!"','* Detention slips flutter.'],
  'acts':[('APOLOGIZE',35,'* You apologize for existing. Accepted, barely.'),
          ('HALLPASS',40,'* You present a hall pass drawn in crayon. ...It works?!'),
          ('MEOW',25,'* You meow. The Prefect softens 3%.')],
  'intro':[('','* A towering playing card in a school uniform blocks the exit!'),
           ('RYEN',"Great. Middle management."),('AC','...meow.')]},
 {'name':'CIRCUIT QUEEN','hp':300,'atk':6,'pat':'grid','col':(120,255,220),'song':'boss1',
  'quotes':['* The Queen boots up a grand speech.','* "PING me later, darlings."','* Royal firmware updating...'],
  'acts':[('REBOOT',35,'* You suggest turning her off and on. She is FLATTERED.'),
          ('CURTSY',40,'* You curtsy at 60fps. Impeccable frame timing.'),
          ('MEOW',25,'* Meow.exe executed successfully.')],
  'intro':[('','* The Circuit Queen descends on a throne of routers!'),
           ('RYEN',"I've seen the future. She monologues."),('AC','mrow.')]},
 {'name':'STATIC JESTER','hp':340,'atk':7,'pat':'spiral','col':(255,160,255),'song':'boss2',
  'quotes':['* The Jester laughs on channel 3.','* "STAY TUNED!!"','* Signal integrity: comedic.'],
  'acts':[('LAUGH',35,'* You laugh politely. It DEMANDS a real laugh.'),
          ('CHANGE CH.',40,'* You change the channel. It chases the remote.'),
          ('MEOW',25,'* The meow gets great ratings.')],
  'intro':[('','* A jester made of broadcast static tumbles out of the screen!'),
           ('LASSE',"O-oh no. I hate live television."),('RYEN',"Then let's cancel him.")]},
 {'name':'CHOIR WARDEN','hp':380,'atk':7,'pat':'notes2','col':(255,230,150),'song':'boss3',
  'quotes':['* The Warden demands PERFECT pitch.','* "FROM THE TOP."','* A thousand-year rehearsal continues.'],
  'acts':[('SING',35,'* You sing your heart out. Slightly flat. He weeps anyway.'),
          ('METRONOME',40,'* You become the metronome. Tick. Tock. Respect.'),
          ('MEOW',25,'* A meow in G major.')],
  'intro':[('','* The Choir Warden raises a baton the size of a lamppost!'),
           ('LASSE',"Everyone... sing like your HP depends on it."),('RYEN',"It literally does.")]},
 {'name':'WRENCHARD','hp':440,'atk':8,'pat':'knight','col':GREEN,'song':'final',
  'quotes':['* The Pipe Knight says nothing.','* Water drips from ancient valves.','* The fountain howls behind him.'],
  'acts':[('PLEAD',30,'* You plead for the surface world. His wrench trembles.'),
          ('REMEMBER',40,'* You remind him fountains were for WISHES once.'),
          ('MEOW',30,'* Even knights cannot resist the meow.')],
  'intro':[('','* WRENCHARD, THE PIPE KNIGHT, bars the final fountain.'),
           ('WRENCHARD','...'),('RYEN',"All this time. A PLUMBER?!"),
           ('LASSE',"Everyone... together!"),('AC','MEOW!!')]},
]

SANS_LB = {
 'name': 'SANS', 'hp': 1, 'atk': 5, 'pat': 'lb_phase1', 'col': WHITE, 'song': 'battle', 'lb': True,
 'quotes': [
     "* you're going to have a bad time.",
     "* keeps dodging.",
     "* guess you really hate bad puns.",
 ],
 'acts': [
     ('CHECK', 15, '* SANS — 1 ATK 1 DEF. The easiest enemy.'),
     ('JOKE', 30, '* You tell a pun. Sans groans.'),
     ('FLIRT', 20, '* You wink. Sans pretends not to notice.'),
 ],
 'intro': [
     ('', '* LAST BREATH — PHASE 1'),
     ('', '* "you\'re not gonna give up, huh."'),
     ('', '* "on days like these, kids like you..."'),
     ('', '* "should be burning in hell."'),
     ('RYEN', '...we should leave.'),
     ('AC', 'meow.'),
 ],
}

CH_INTRO = [
 [('BECCA',"AC, sweetie! You'll be late for class. Take Ryen with you."),
  ('RYEN',"I'm from the year 3026 and even I can't fix your bedhead."),
  ('',"* The supply closet floor gives way... into the STATIC WORLD."),
  ('RYEN',"Okay. New timeline. Rules: I punch, you meow."),
  ('AC',"...meow.")],
 [('',"* CH2. The dark water glows with neon signage."),
  ('RYEN',"A whole harbor made of wifi. My era invented this, you're welcome."),
  ('AC',"mrrp?"),
  ('RYEN',"No, you can't fish in it. ...Okay, ONE fish.")],
 [('',"* CH3. A boardwalk flickers between channels."),
  ('LASSE',"U-um! AC! Ryen! I fell through my TV and I— is that a battle box?!"),
  ('RYEN',"Welcome aboard, fox. You're the healer now. Congrats on the promotion."),
  ('LASSE',"I didn't apply for this...!")],
 [('',"* CH4. A choir hums beneath the floorboards of the world."),
  ('LASSE',"The music is... kind of beautiful?"),
  ('RYEN',"It's a boss theme, Lasse. It's ALWAYS a boss theme."),
  ('AC',"meow. (agreement)")],
 [('',"* CH5. Pipes. Endless pipes. All roads flow down."),
  ('JOSEPH',"Oh hey little buddies! I planted sunflowers in the drainage. Be safe down there!"),
  ('RYEN',"The final fountain is below. I've seen how this ends. ...Actually, no. I haven't."),
  ('LASSE',"Then we write it ourselves."),
  ('AC',"...meow. (resolve)")],
 [('', '* Judgment Hall. The air smells like bones.'),
  ('', '* A skeleton in a blue hoodie watches you approach.'),
  ('RYEN', "That's... Sans. Last Breath Phase 1. Don't die."),
  ('AC', '...meow.')],
]

CH_OUTRO = [
 [('',"* The Static Fountain is sealed. The classroom rebuilds itself around you."),
  ('BECCA',"There you two are! Dinner's ready. ...Why are you covered in chalk?")],
 [('',"* The Neon Fountain dims to a gentle glow. The harbor sleeps."),
  ('RYEN',"Two down. My future self says hi, by the way. He's proud. Weird.")],
 [('',"* The VHS Fountain rewinds itself shut. Roll credits? Not yet."),
  ('LASSE',"I... I helped! I actually helped!")],
 [('',"* The Choir Fountain resolves on a perfect final chord."),
  ('RYEN',"One fountain left. The big one. Bring snacks.")],
 [('',"* The last fountain closes. Light pours through every pipe."),
  ('WRENCHARD',"...thank you."),
  ('JOSEPH',"GROUP HUG! I brought sunflowers!"),
  ('BECCA',"You're all grounded. Lovingly."),
  ('',"* AC RUNE 0.1 — THE END (for now) — [C] 2026 AC HOLDING"),
  ('',"* thank you for playing. meow.")],
 [('', '* PHASE 1 complete. Sans vanishes into a pun.'),
  ('RYEN', "We lived. That's canon enough."),
  ('AC', 'meow. (shaken)')],
]

PLOMBO_SCENE = [
 ('',"* A figure leans against the last doorway, spinning a pipe wrench."),
 ('PLOMBO',"heya. it's-a me. the guy before the guy."),
 ('PLOMBO',"five fountains. zero rage-quits. not bad, little cat."),
 ('PLOMBO',"my brother wrenchard is through that door. he's... complicated."),
 ('PLOMBO',"be rude to him and you'll have a bad tuesday. capisce?"),
 ('RYEN',"Is EVERYONE in this world a plumber?!"),
 ('PLOMBO',"union's strong down here, kid. go get 'em."),
]

# ---------------------------------------------------------------- the game
class Game:
    def __init__(self):
        pygame.mixer.pre_init(SR, -16, 1, 2048)
        pygame.init()
        audio_ok = True
        try: pygame.mixer.init(SR, -16, 1, 2048)
        except Exception: audio_ok = False
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption("AC RUNE 0.1 — [C] 2026 AC HOLDING")
        self.clock = pygame.time.Clock()
        self.music = Music(audio_ok)
        self.sfx = {}
        if audio_ok:
            try:
                self.sfx = {'blip': tone(880,.045,'sq',.2), 'ok': tone(660,.08,'sq',.25,660),
                            'no': tone(220,.12,'saw',.25,-80), 'hurt': tone(180,.16,'saw',.3,-120),
                            'heal': tone(520,.14,'tri',.25,520), 'slash': tone(120,.08,'saw',.2,-60),
                            'graze': tone(1200,.03,'tri',.12), 'win': tone(440,.3,'sq',.25,440)}
            except Exception: pass
        self.state = 'title'; self.frame = 0
        self.progress = 0                       # chapters cleared
        self.sel = 0
        self.party = make_party()
        self.inv = ['ChocCone', 'CatTea']
        self.tp = 0
        self.ch = 0
        self.dlg = []; self.dlg_i = 0; self.dlg_t = 0; self.dlg_next = 'title'
        self.toast = ""; self.toast_t = 0
        self.flash = 0
        # overworld
        self.px = 60.0; self.trail = []
        self.fought = False
        # battle
        self.b = None

    # ---------------- util
    def play_sfx(self, k):
        s = self.sfx.get(k)
        if s and not self.music.mute: s.play()
    def song(self, key):
        self.music.play(key)
        if self.music.ok:
            self.toast = "♪ " + SONGS[key][5]; self.toast_t = 150
    def say(self, lines, nxt):
        self.dlg = lines; self.dlg_i = 0; self.dlg_t = 0
        self.dlg_next = nxt; self.state = 'dialog'

    def active_party(self):
        n = 3 if self.ch >= 2 else 2
        return self.party[:n]

    # ---------------- chapter flow
    def begin_chapter(self, ch):
        self.ch = ch
        self.px = 60.0; self.trail = []; self.fought = False
        for m in self.party: m['hp'] = m['mx']
        self.tp = 20
        for it in ('ChocCone', 'CatTea', 'PipeSoda'):
            if len(self.inv) < 6: self.inv.append(it)
        if ch == LB_CH:
            lb_sprites()
            self.say(CH_INTRO[ch], 'lb_start')
            self.song('battle')
        else:
            self.say(CH_INTRO[ch], 'over')
            self.song('world%d' % ch)

    def end_chapter(self):
        self.progress = max(self.progress, self.ch + 1)
        if self.ch == 4:
            self.say(CH_OUTRO[4], 'credits'); self.song('end')
        else:
            self.say(CH_OUTRO[self.ch], 'select'); self.song('title')

    # ---------------- battle setup
    def start_battle(self, boss):
        if boss and self.ch == LB_CH:
            e = dict(SANS_LB)
        elif boss:
            e = dict(BOSSES[self.ch])
        else:
            e = dict(MINIONS[self.ch])
        e['mx'] = e['hp']; e['mercy'] = 0; e['boss'] = boss
        self.b = {'e': e, 'phase': 'intro' if boss else 'menu', 'mi': 0, 'sel': 0,
                  'msg': '', 'turn': 0, 'bullets': [], 't': 0, 'soul': [BOX.centerx, BOX.centery],
                  'inv_sel': 0, 'bar': 0.0, 'bardir': 1, 'dmg_pop': [], 'iframes': 0,
                  'quote': random.choice(e['quotes']), 'blasters': [],
                  'lb_pat': random.randint(0, 1), 'lb_hit': False}
        self.state = 'battle'
        self.song(e['song'] if boss else 'battle')
        if boss:
            if e.get('lb'):
                lb_sprites().sans_anim.pose = 'shrug'
            self.say(e['intro'], 'battle')

    # ---------------- battle logic
    def next_member(self):
        b = self.b; ap = self.active_party()
        b['mi'] += 1
        while b['mi'] < len(ap) and ap[b['mi']]['hp'] <= 0: b['mi'] += 1
        if b['mi'] >= len(ap):
            b['phase'] = 'dodge'; b['t'] = 0; b['bullets'] = []
            b['soul'] = [BOX.centerx, BOX.centery]
            b['quote'] = random.choice(b['e']['quotes'])
        else:
            b['phase'] = 'menu'; b['sel'] = 0

    def apply_damage(self, dmg):
        b = self.b; e = b['e']
        if e.get('lb'):
            lb_sprites().sans_anim.flash('dodge_r' if random.random() > 0.5 else 'dodge_l', 12)
            b['msg'] = "* Sans dodges!"
            b['phase'] = 'text'
            self.play_sfx('graze')
            return
        e['hp'] -= dmg; self.play_sfx('slash'); self.flash = 6
        b['dmg_pop'].append([320, 150, str(dmg), 40, RED])
        if e['hp'] <= 0:
            e['hp'] = 0; b['phase'] = 'win'
            b['msg'] = "* You won! %s was defeated." % e['name']
            self.play_sfx('win')

    def try_spare(self):
        b = self.b; e = b['e']
        need = 80 if e.get('lb') else 100
        if e['mercy'] >= need:
            b['phase'] = 'win'
            if e.get('lb'):
                b['msg'] = "* PHASE 1 complete. Sans lets you go... for now."
            else:
                b['msg'] = "* You won! %s was SPARED." % e['name']
            self.play_sfx('win')
        else:
            b['msg'] = "* %s isn't ready to be spared. (mercy %d%%)" % (e['name'], e['mercy'])
            b['phase'] = 'text'

    def cast(self, m):
        b = self.b; name, cost, kind = m['spell']
        if self.tp < cost:
            b['msg'] = "* Not enough TP! (%d needed)" % cost; b['phase'] = 'text'; return
        self.tp -= cost
        if kind == 'mercy':
            b['e']['mercy'] = min(100, b['e']['mercy'] + 20)
            b['msg'] = "* AC meows with maximum sincerity. Mercy +20%!"
            self.play_sfx('heal')
        elif kind == 'healall':
            for p in self.active_party(): p['hp'] = min(p['mx'], p['hp'] + 45)
            b['msg'] = "* RYEN rewinds everyone's bruises. Party healed 45!"
            self.play_sfx('heal')
        else:
            b['msg'] = "* LASSE unleashes FOXFIRE!"
            self.apply_damage(random.randint(46, 58))
        if b['phase'] != 'win': b['phase'] = 'text'

    def spawn_bullets(self):
        b = self.b; t = b['t']; e = b['e']; ch = self.ch
        sp = (1.6 + ch * 0.28) * SPEED
        pat = e['pat']
        def add(x, y, vx, vy, r=5, col=None, w=0, h=0):
            b['bullets'].append({'x':x,'y':y,'vx':vx,'vy':vy,'r':r,'c':col or e['col'],'w':w,'h':h,'g':False})
        if pat == 'rain':
            if t % 13 == 0: add(random.randint(BOX.left+8, BOX.right-8), BOX.top-8, 0, sp)
        elif pat == 'aim':
            if t % 34 == 0:
                sx, sy = random.choice([(BOX.left-6,BOX.top-6),(BOX.right+6,BOX.top-6)])
                dx, dy = b['soul'][0]-sx, b['soul'][1]-sy; d = math.hypot(dx,dy) or 1
                add(sx, sy, dx/d*sp*1.4, dy/d*sp*1.4, 6)
        elif pat == 'wave':
            if t % 11 == 0:
                add(BOX.right+8, BOX.centery + math.sin(t*0.08)*60, -sp*1.3, 0, 5)
        elif pat == 'notes':
            if t % 16 == 0:
                y0 = random.randint(BOX.top+10, BOX.bottom-10)
                add(BOX.right+8, y0, -sp, math.sin(t)*0.6, 6, (255,240,170))
        elif pat == 'pipes':
            if t % 55 == 0:
                gap = random.randint(BOX.top+30, BOX.bottom-50)
                add(BOX.right+12, BOX.top, -sp, 0, 0, GREEN, 14, gap-BOX.top)
                add(BOX.right+12, gap+44, -sp, 0, 0, GREEN, 14, BOX.bottom-(gap+44))
        elif pat == 'cards':
            if t % 20 == 0:
                y0 = BOX.top + 14 + ((t//20) % 5) * 28
                side = -1 if (t//20) % 2 else 1
                add(BOX.centerx + side*170, y0, -side*sp*1.2, 0, 0, (255,120,120), 18, 10)
        elif pat == 'grid':
            if t % 26 == 0:
                add(random.randint(BOX.left+8,BOX.right-8), BOX.top-8, 0, sp, 5, (120,255,220))
                add(BOX.left-8, random.randint(BOX.top+8,BOX.bottom-8), sp, 0, 5, (120,255,220))
        elif pat == 'spiral':
            if t % 7 == 0:
                a = t * 0.19
                add(BOX.centerx, BOX.top+10, math.cos(a)*sp, abs(math.sin(a))*sp+0.6, 5, (255,160,255))
        elif pat == 'notes2':
            if t % 12 == 0:
                add(BOX.right+8, BOX.top+15+((t//12)%6)*24, -sp*1.15, math.sin(t*0.5)*0.4, 6, (255,230,150))
            if t % 50 == 0: add(random.randint(BOX.left+8,BOX.right-8), BOX.top-8, 0, sp*0.9)
        elif pat == 'knight':
            ph = (b['turn']) % 3
            if ph == 0 and t % 45 == 0:
                gap = random.randint(BOX.top+30, BOX.bottom-56)
                add(BOX.right+12, BOX.top, -sp*1.1, 0, 0, GREEN, 14, gap-BOX.top)
                add(BOX.right+12, gap+50, -sp*1.1, 0, 0, GREEN, 14, BOX.bottom-(gap+50))
            elif ph == 1 and t % 6 == 0:
                a = t * 0.23
                add(BOX.centerx, BOX.top+10, math.cos(a)*sp*1.1, abs(math.sin(a))*sp+0.7, 5, GREEN)
            elif ph == 2 and t % 26 == 0:
                sx = random.choice([BOX.left-6, BOX.right+6])
                dx, dy = b['soul'][0]-sx, b['soul'][1]-BOX.top; d = math.hypot(dx,dy) or 1
                add(sx, BOX.top-6, dx/d*sp*1.5, dy/d*sp*1.5, 6, GREEN)
        elif pat == 'lb_phase1':
            lp = b.get('lb_pat', 0)
            if lp == 0 and t % 20 == 0:
                y0 = random.randint(BOX.top, BOX.bottom - 10)
                add(BOX.right + 8, y0, -sp * 1.3, 0, 0, WHITE, 18, 10)
            elif lp == 1 and t % 60 == 0:
                sx = random.choice([BOX.left - 20, BOX.right + 20])
                sy = random.choice([BOX.top - 20, BOX.bottom + 20])
                angle = math.atan2(b['soul'][1] - sy, b['soul'][0] - sx)
                b.setdefault('blasters', []).append(
                    {'x': sx, 'y': sy, 'angle': angle, 'timer': 0, 'firing': False})

    def _update_lb_blasters(self, b):
        s = b['soul']
        for gb in b.get('blasters', [])[:]:
            gb['timer'] += 1
            if gb['timer'] == 30:
                gb['firing'] = True
            if gb.get('firing') and b['iframes'] == 0:
                angle_to_p = math.atan2(s[1] - gb['y'], s[0] - gb['x'])
                if abs(math.degrees(angle_to_p - gb['angle'])) < 5:
                    b['iframes'] = 45
                    self.play_sfx('hurt')
                    self.flash = 5
                    b['lb_hit'] = True
                    lb_sprites().sans_anim.flash('dodge_l', 10)
                    alive = [p for p in self.active_party() if p['hp'] > 0]
                    victim = random.choice(alive) if alive else None
                    if victim:
                        victim['hp'] = max(0, victim['hp'] - (b['e']['atk'] + self.ch))
                        b['dmg_pop'].append([120 + 130 * self.party.index(victim), 430,
                                             "-%d" % (b['e']['atk'] + self.ch), 35, RED])
                    alive = [p for p in self.active_party() if p['hp'] > 0]
                    if not alive:
                        self.state = 'gameover'
                        return
            if gb['timer'] > 90:
                gb['firing'] = False
                b['blasters'].remove(gb)

    def _draw_lb_blasters(self, s, b):
        for gb in b.get('blasters', []):
            dist = 40
            bx = gb['x'] + math.cos(gb['angle']) * dist
            by = gb['y'] + math.sin(gb['angle']) * dist
            bl = lb_sprites().blaster
            rot = pygame.transform.rotate(bl, -math.degrees(gb['angle']) - 90)
            s.blit(rot, rot.get_rect(center=(int(bx), int(by))))
            if gb.get('firing'):
                beam = pygame.Surface((800, 20), pygame.SRCALPHA)
                beam.fill((255, 255, 255, 200))
                rbeam = pygame.transform.rotate(beam, -math.degrees(gb['angle']))
                s.blit(rbeam, rbeam.get_rect(center=(bx, by)))

    def _update_lb_sans_anim(self, b):
        ph = b['phase']
        if ph == 'dodge':
            lb_state = 'SANS_TURN'
        elif ph == 'menu':
            lb_state = 'MENU'
        else:
            lb_state = 'INTRO'
        bl_on = any(g.get('firing') for g in b.get('blasters', []))
        lb_sprites().sans_anim.update(
            lb_state, b['t'], b.get('lb_pat', 0), bl_on, b.get('lb_hit', False))
        if ph != 'dodge':
            b['lb_hit'] = False

    def update_dodge(self, keys):
        b = self.b; s = b['soul']; spd = SOUL_SPD
        if keys[pygame.K_LEFT]:  s[0] -= spd
        if keys[pygame.K_RIGHT]: s[0] += spd
        if keys[pygame.K_UP]:    s[1] -= spd
        if keys[pygame.K_DOWN]:  s[1] += spd
        s[0] = max(BOX.left+7, min(BOX.right-7, s[0]))
        s[1] = max(BOX.top+7, min(BOX.bottom-7, s[1]))
        self.spawn_bullets()
        if b['e'].get('lb'):
            self._update_lb_blasters(b)
        if b['iframes'] > 0: b['iframes'] -= 1
        alive = [p for p in self.active_party() if p['hp'] > 0]
        for bl in b['bullets'][:]:
            bl['x'] += bl['vx']; bl['y'] += bl['vy']
            if bl['x'] < BOX.left-40 or bl['x'] > BOX.right+40 or bl['y'] > BOX.bottom+40 or bl['y'] < BOX.top-60:
                b['bullets'].remove(bl); continue
            if bl['w']:  # rect bullet
                r = pygame.Rect(bl['x'], bl['y'], bl['w'], bl['h'])
                hit = r.collidepoint(s[0], s[1])
                near = r.inflate(22, 22).collidepoint(s[0], s[1])
            else:
                d = math.hypot(bl['x']-s[0], bl['y']-s[1])
                hit = d < bl['r'] + 6; near = d < bl['r'] + 20
            if near and not bl['g'] and not hit:
                bl['g'] = True; self.tp = min(100, self.tp + 2); self.play_sfx('graze')
            if hit and b['iframes'] == 0:
                b['iframes'] = 45; self.play_sfx('hurt'); self.flash = 5
                if b['e'].get('lb'):
                    lb_sprites().sans_anim.flash('hurt', 8)
                victim = random.choice(alive) if alive else None
                if victim:
                    victim['hp'] = max(0, victim['hp'] - (b['e']['atk'] + self.ch))
                    b['dmg_pop'].append([120 + 130*self.party.index(victim), 430,
                                         "-%d" % (b['e']['atk']+self.ch), 35, RED])
                alive = [p for p in self.active_party() if p['hp'] > 0]
                if not alive:
                    self.state = 'gameover'; return
        b['t'] += 1
        dur = 290 + self.ch * 35 + (60 if b['e']['boss'] else 0)
        if b['t'] > dur:
            b['e']['mercy'] = min(100, b['e']['mercy'] + (6 if b['e']['boss'] else 10))
            if b['e'].get('lb'):
                b['lb_pat'] = (b.get('lb_pat', 0) + 1) % 2
                b['blasters'] = []
                b['lb_hit'] = False
            b['turn'] += 1; b['mi'] = -1; self.next_member()
            b['mi'] = 0
            while self.active_party()[b['mi']]['hp'] <= 0: b['mi'] += 1
            b['phase'] = 'menu'; b['sel'] = 0

    # ---------------- events
    def handle_key(self, k):
        st = self.state
        if k == pygame.K_m: self.music.toggle(); return
        if st == 'title':
            if k in (pygame.K_z, pygame.K_RETURN): self.play_sfx('ok'); self.state = 'select'
        elif st == 'select':
            if k == pygame.K_UP:   self.sel = (self.sel - 1) % len(CH_TITLES); self.play_sfx('blip')
            if k == pygame.K_DOWN: self.sel = (self.sel + 1) % len(CH_TITLES); self.play_sfx('blip')
            if k in (pygame.K_z, pygame.K_RETURN):
                if self.sel <= self.progress or self.sel == LB_CH:
                    self.play_sfx('ok'); self.begin_chapter(self.sel)
                else: self.play_sfx('no')
            if k == pygame.K_x: self.state = 'title'
        elif st == 'dialog':
            if k in (pygame.K_z, pygame.K_RETURN):
                sp, tx_ = self.dlg[self.dlg_i]
                if self.dlg_t < len(tx_): self.dlg_t = len(tx_)
                else:
                    self.dlg_i += 1; self.dlg_t = 0; self.play_sfx('blip')
                    if self.dlg_i >= len(self.dlg):
                        self.state = self.dlg_next
                        if self.dlg_next == 'lb_start':
                            self.start_battle(True)
                        elif self.dlg_next == 'battle' and self.b:
                            self.b['phase'] = 'menu'
        elif st == 'battle':
            self.battle_key(k)
        elif st == 'gameover':
            if k in (pygame.K_z, pygame.K_RETURN):
                for m in self.party: m['hp'] = m['mx'] // 2 + 10
                boss = self.b['e']['boss']
                self.say([('RYEN', "Nope. Rewinding THAT one. Nobody dies on my watch.")], 'battle')
                self.start_battle(boss)
        elif st == 'credits':
            if k in (pygame.K_z, pygame.K_RETURN): self.state = 'select'; self.song('title')

    def battle_key(self, k):
        b = self.b; ap = self.active_party(); m = ap[b['mi']] if b['mi'] < len(ap) else ap[0]
        ph = b['phase']
        if ph == 'menu':
            opts = 5
            if k == pygame.K_LEFT:  b['sel'] = (b['sel'] - 1) % opts; self.play_sfx('blip')
            if k == pygame.K_RIGHT: b['sel'] = (b['sel'] + 1) % opts; self.play_sfx('blip')
            if k in (pygame.K_z, pygame.K_RETURN):
                self.play_sfx('ok')
                c = ['FIGHT','ACT','MAGIC','ITEM','SPARE'][b['sel']]
                if c == 'FIGHT': b['phase'] = 'fight'; b['bar'] = 0.0; b['bardir'] = 1
                elif c == 'ACT': b['phase'] = 'act'; b['sel2'] = 0
                elif c == 'MAGIC': self.cast(m)
                elif c == 'ITEM':
                    if self.inv: b['phase'] = 'item'; b['sel2'] = 0
                    else: b['msg'] = "* Your pockets contain one (1) crumb."; b['phase'] = 'text'
                elif c == 'SPARE': self.try_spare()
        elif ph == 'act':
            acts = b['e']['acts']
            if k == pygame.K_UP:   b['sel2'] = (b['sel2'] - 1) % len(acts); self.play_sfx('blip')
            if k == pygame.K_DOWN: b['sel2'] = (b['sel2'] + 1) % len(acts); self.play_sfx('blip')
            if k == pygame.K_x: b['phase'] = 'menu'
            if k in (pygame.K_z, pygame.K_RETURN):
                nm, mc, txt_ = acts[b['sel2']]
                b['e']['mercy'] = min(100, b['e']['mercy'] + mc)
                b['msg'] = txt_ + "  (mercy +%d%%)" % mc
                b['phase'] = 'text'; self.play_sfx('heal')
        elif ph == 'item':
            if k == pygame.K_UP:   b['sel2'] = (b['sel2'] - 1) % len(self.inv); self.play_sfx('blip')
            if k == pygame.K_DOWN: b['sel2'] = (b['sel2'] + 1) % len(self.inv); self.play_sfx('blip')
            if k == pygame.K_x: b['phase'] = 'menu'
            if k in (pygame.K_z, pygame.K_RETURN):
                it = self.inv.pop(b['sel2'])
                heal = ITEMS[it]
                m['hp'] = min(m['mx'], m['hp'] + heal)
                b['msg'] = "* %s ate the %s. Recovered %d HP!" % (m['name'], it, heal)
                b['phase'] = 'text'; self.play_sfx('heal')
        elif ph == 'fight':
            if k in (pygame.K_z, pygame.K_RETURN):
                acc = 1.25 - 2.2 * abs(b['bar'] - 0.5)
                dmg = max(3, int(m['atk'] * max(0.15, acc) * random.uniform(0.9, 1.15) * 2.2))
                self.apply_damage(dmg)
                if b['phase'] != 'win': b['phase'] = 'text'; b['msg'] = "* %s attacks! %d damage!" % (m['name'], dmg)
        elif ph == 'text':
            if k in (pygame.K_z, pygame.K_RETURN): self.next_member()
        elif ph == 'win':
            if k in (pygame.K_z, pygame.K_RETURN):
                boss = b['e']['boss']; self.b = None
                self.tp = min(100, self.tp + 15)
                if boss and self.ch == LB_CH:
                    self.say(CH_OUTRO[LB_CH], 'select'); self.song('title')
                elif boss:
                    self.say([('', "* You reach the DARK FOUNTAIN."),
                              ('AC', "meow. (sealing sounds)"),
                              ('', "* The fountain closes gently.")], 'chend')
                else:
                    self.state = 'over'; self.song('world%d' % self.ch)

    # ---------------- update / draw
    def update(self):
        self.frame += 1
        if self.toast_t > 0: self.toast_t -= 1
        if self.flash > 0: self.flash -= 1
        keys = pygame.key.get_pressed()
        if self.state == 'over':
            spd = OW_SPD
            moved = False
            if keys[pygame.K_RIGHT]: self.px += spd; moved = True
            if keys[pygame.K_LEFT]:  self.px = max(40, self.px - spd); moved = True
            room = 1500 + self.ch * 200
            self.trail.append(self.px)
            if len(self.trail) > 40: self.trail.pop(0)
            if not self.fought and self.px > room * 0.45:
                self.fought = True
                self.say([('', "* %s draws near!" % MINIONS[self.ch]['name'])], 'over')
                self.start_battle(False)
            if self.px > room - 80:
                self.start_battle(True)
        elif self.state == 'battle':
            b = self.b
            if b and b['e'].get('lb'):
                self._update_lb_sans_anim(b)
            if b['phase'] == 'fight':
                b['bar'] += 0.022 * b['bardir']
                if b['bar'] >= 1: b['bar'], b['bardir'] = 1, -1
                if b['bar'] <= 0: b['bar'], b['bardir'] = 0, 1
            elif b['phase'] == 'dodge':
                self.update_dodge(keys)
            for p in b['dmg_pop'][:] if b else []:
                p[1] -= 0.7; p[3] -= 1
                if p[3] <= 0: b['dmg_pop'].remove(p)
        elif self.state == 'dialog':
            sp, tx_ = self.dlg[self.dlg_i]
            if self.dlg_t < len(tx_):
                self.dlg_t += 1
                if self.dlg_t % 3 == 0: self.play_sfx('blip')
        elif self.state == 'chend':
            pass

    def draw_dialog_box(self):
        s = self.screen
        r = pygame.Rect(30, 350, W - 60, 110)
        pygame.draw.rect(s, BLACK, r); pygame.draw.rect(s, WHITE, r, 3)
        sp, tx_ = self.dlg[self.dlg_i]
        shown = tx_[:self.dlg_t]
        if sp:
            txt(s, sp, r.x + 14, r.y + 8, 18, SPEAKER_COL.get(sp, WHITE))
            draw_actor(s, r.x + 40, r.y + 95, sp, self.frame)
            x0 = r.x + 80
        else:
            x0 = r.x + 16
        # word wrap
        words = shown.split(' '); line = ''; y = r.y + (32 if sp else 16)
        for wd in words:
            if len(line + wd) > (52 if not sp else 44):
                txt(s, line, x0, y, 17); y += 22; line = ''
            line += wd + ' '
        txt(s, line, x0, y, 17)
        txt(s, "[Z]", r.right - 40, r.bottom - 24, 14, GRAY)

    def draw(self):
        s = self.screen; st = self.state
        bg, ac = CH_PAL[self.ch]
        s.fill(BLACK if st in ('title', 'select', 'gameover', 'credits') else bg)

        if st == 'title':
            for i in range(24):  # static specks
                s.set_at((random.randrange(W), random.randrange(H)), (30, 30, 45))
            txt(s, "A C   R U N E", W//2, 130, 54, BLUE, True)
            txt(s, "0.1  —  2026  —  [C] AC HOLDING", W//2, 185, 18, WHITE, True)
            txt(s, "files = off  |  60 fps  |  speed = 1.0", W//2, 208, 14, GRAY, True)
            txt(s, "a Team Flames / Samsoft original AU", W//2, 228, 15, GRAY, True)
            if (self.frame // 30) % 2: txt(s, "[ PRESS Z ]", W//2, 300, 22, YELLOW, True)
            draw_actor(s, W//2 - 60, 380, 'AC', self.frame, 1.6)
            draw_actor(s, W//2, 380, 'RYEN', self.frame + 10, 1.6)
            draw_actor(s, W//2 + 60, 380, 'LASSE', self.frame + 20, 1.6)
            txt(s, "Z confirm   X cancel   M mute", W//2, 440, 14, GRAY, True)
        elif st == 'select':
            txt(s, "SELECT CHAPTER", W//2, 60, 30, BLUE, True)
            for i, t in enumerate(CH_TITLES):
                locked = i > self.progress and i != LB_CH
                col = GRAY if locked else (YELLOW if i == self.sel else WHITE)
                pre = "> " if i == self.sel else "  "
                suf = "  [LOCKED]" if locked else ("  * CLEAR *" if i < self.progress else "")
                txt(s, pre + t + suf, 120, 130 + i * 46, 21, col)
            txt(s, "meow through them in order. nya.", W//2, 420, 15, GRAY, True)
        elif st in ('over', 'dialog', 'chend') and self.b is None:
            room = 1500 + self.ch * 200
            cam = max(0, min(self.px - W//2, room - W))
            # parallax stripes
            for i in range(10):
                y = 60 + i * 20
                pygame.draw.line(s, ac, (0, y + int(math.sin(self.frame*0.02 + i)*4)), (W, y), 1)
            pygame.draw.rect(s, ac, (0, 330, W, 6))
            pygame.draw.rect(s, (bg[0]+8, bg[1]+8, bg[2]+8), (0, 336, W, H-336))
            # signposts + door
            for sx, label in ((300, CH_TITLES[self.ch]), (room//2 - 120, "battle zone ahead. stretch first."),):
                x = sx - cam
                if -50 < x < W + 50:
                    pygame.draw.rect(s, GRAY, (x, 290, 6, 40))
                    pygame.draw.rect(s, GRAY, (x - 40, 272, 86, 22))
                    txt(s, label[:20], x + 3, 276, 12, BLACK, True)
            dx = room - 60 - cam
            pygame.draw.rect(s, ac, (dx, 250, 44, 80)); pygame.draw.rect(s, YELLOW, (dx, 250, 44, 80), 2)
            txt(s, "BOSS", dx + 22, 240, 14, YELLOW, True)
            # party
            ap = self.active_party()
            draw_actor(s, self.px - cam, 330, 'AC', self.frame)
            if len(self.trail) > 12 and len(ap) > 1:
                draw_actor(s, self.trail[-12] - cam, 330, 'RYEN', self.frame + 8)
            if len(self.trail) > 24 and len(ap) > 2:
                draw_actor(s, self.trail[-24] - cam, 330, 'LASSE', self.frame + 16)
            txt(s, CH_TITLES[self.ch], 12, 10, 16, BLUE)
            txt(s, "→ walk right", W - 110, 10, 14, GRAY)
            if st == 'chend':
                pygame.draw.circle(s, WHITE, (W//2, 200), 30 + (self.frame % 60))
                self.end_chapter()
        elif st == 'battle' or (st in ('dialog',) and self.b):
            b = self.b; e = b['e']
            ex, ey = 320, 120 + int(math.sin(self.frame * 0.06) * 6)
            if e.get('lb'):
                sans = lb_sprites().sans_anim.surface()
                sr = sans.get_rect(center=(ex, ey))
                self.screen.blit(sans, sr)
                hp_bar = pygame.Rect(ex - 60, ey + sr.height // 2 + 8, 120, 15)
                pygame.draw.rect(self.screen, RED, hp_bar)
                pygame.draw.rect(self.screen, YELLOW, hp_bar, 2)
            else:
                pygame.draw.rect(self.screen, e['col'], (ex - 34, ey - 34, 68, 68), border_radius=10)
                pygame.draw.rect(self.screen, WHITE, (ex - 34, ey - 34, 68, 68), 2, border_radius=10)
                if e['name'] == 'WRENCHARD':
                    pygame.draw.rect(self.screen, (200,200,200), (ex - 6, ey - 60, 12, 30))
            s = self.screen
            txt(s, e['name'], ex, ey - 55, 20, YELLOW if e['mercy'] >= 80 and e.get('lb') else (YELLOW if e['mercy'] >= 100 else WHITE), True)
            # hp+mercy
            pygame.draw.rect(s, (60,0,0), (ex - 60, ey + 44, 120, 8))
            pygame.draw.rect(s, RED, (ex - 60, ey + 44, int(120 * e['hp'] / e['mx']), 8))
            txt(s, "mercy %d%%" % e['mercy'], ex, ey + 62, 14, YELLOW, True)
            # box
            pygame.draw.rect(s, BLACK, BOX); pygame.draw.rect(s, WHITE, BOX, 3)
            ph = b['phase']
            if ph == 'dodge':
                if b['e'].get('lb'):
                    self._draw_lb_blasters(s, b)
                for bl in b['bullets']:
                    if bl['w']: pygame.draw.rect(s, bl['c'], (bl['x'], bl['y'], bl['w'], bl['h']))
                    else: pygame.draw.circle(s, bl['c'], (int(bl['x']), int(bl['y'])), bl['r'])
                if b['iframes'] % 8 < 5:
                    x0, y0 = int(b['soul'][0]), int(b['soul'][1])
                    pygame.draw.polygon(s, RED, [(x0, y0+7), (x0-7, y0-2), (x0-3, y0-7),
                                                 (x0, y0-3), (x0+3, y0-7), (x0+7, y0-2)])
                txt(s, b['quote'], W//2, 218, 15, GRAY, True)
            elif ph == 'fight':
                bar = pygame.Rect(BOX.x + 20, BOX.centery - 14, BOX.w - 40, 28)
                pygame.draw.rect(s, (40,40,40), bar); pygame.draw.rect(s, WHITE, bar, 2)
                pygame.draw.rect(s, GREEN, (bar.centerx - 7, bar.y, 14, bar.h), 2)
                cx = bar.x + int(b['bar'] * bar.w)
                pygame.draw.rect(s, YELLOW, (cx - 2, bar.y - 4, 4, bar.h + 8))
                txt(s, "press Z in the center!", W//2, 218, 15, GRAY, True)
            elif ph in ('text', 'win', 'intro'):
                words = b['msg'].split(' '); line = ''; y = BOX.y + 18
                for wd in words:
                    if len(line + wd) > 36: txt(s, line, BOX.x + 14, y, 16); y += 22; line = ''
                    line += wd + ' '
                txt(s, line, BOX.x + 14, y, 16)
                txt(s, "[Z]", BOX.right - 36, BOX.bottom - 24, 14, GRAY)
            elif ph == 'menu':
                txt(s, b['quote'], BOX.x + 14, BOX.y + 12, 15, GRAY)
                ap = self.active_party()
                txt(s, "%s's move" % ap[b['mi']]['name'], BOX.x + 14, BOX.y + 40, 17, ap[b['mi']]['col'])
                for i, o in enumerate(['FIGHT','ACT','MAGIC','ITEM','SPARE']):
                    col = YELLOW if i == b['sel'] else WHITE
                    if o == 'SPARE' and (e['mercy'] >= 100 or (e.get('lb') and e['mercy'] >= 80)):
                        col = YELLOW if i == b['sel'] else GREEN
                    txt(s, o, BOX.x + 20 + i * 56, BOX.bottom - 34, 15, col)
            elif ph in ('act', 'item'):
                lst = [a[0] for a in e['acts']] if ph == 'act' else self.inv
                for i, o in enumerate(lst):
                    txt(s, ("> " if i == b['sel2'] else "  ") + o, BOX.x + 24, BOX.y + 16 + i * 24,
                        16, YELLOW if i == b['sel2'] else WHITE)
                txt(s, "[X back]", BOX.right - 70, BOX.bottom - 24, 13, GRAY)
            # party hud
            ap = self.active_party()
            for i, p in enumerate(ap):
                x0 = 90 + i * 170
                col = p['col'] if p['hp'] > 0 else GRAY
                txt(s, p['name'], x0, 412, 15, col)
                pygame.draw.rect(s, (60,0,0), (x0, 432, 100, 10))
                pygame.draw.rect(s, GREEN if p['hp'] > p['mx']//4 else RED,
                                 (x0, 432, int(100 * p['hp'] / p['mx']), 10))
                txt(s, "%d/%d" % (p['hp'], p['mx']), x0 + 104, 428, 13)
            pygame.draw.rect(s, (40,20,0), (16, 240, 14, 160))
            pygame.draw.rect(s, ORANGE, (16, 400 - int(160 * self.tp / 100), 14, int(160 * self.tp / 100)))
            txt(s, "TP", 23, 408, 13, ORANGE, True)
            for p in b['dmg_pop']:
                txt(s, p[2], int(p[0]), int(p[1]), 20, p[4], True)
        elif st == 'gameover':
            txt(s, "SOUL SHATTERED", W//2, 180, 40, RED, True)
            txt(s, "...but somewhere, a clock ticks backwards.", W//2, 240, 17, GRAY, True)
            txt(s, "[Z] let Ryen rewind", W//2, 300, 18, YELLOW, True)
        elif st == 'credits':
            txt(s, "AC RUNE 0.1", W//2, 70, 36, BLUE, True)
            lines = ["directed by catsan  //  Team Flames", "engine: one (1) python file. files = off.",
                     "60 fps  //  speed = 1.0  //  soul spd = DR-accurate",
                     "", "AC ... a cat", "RYEN ... a time traveller", "LASSE ... a fox",
                     "PLOMBO & WRENCHARD ... union plumbers", "BECCA ... mom energy", "JOSEPH ... sunflower guy",
                     "", "OST: 14 custom tracks (Undertale Yellow style)",
                     "toby-adjacent NES synth, files = off @ %d hz" % SR,
                     "", "[C] 2026 AC HOLDING   —   meow."]
            for i, l in enumerate(lines):
                txt(s, l, W//2, 130 + i * 22, 16, WHITE if l else GRAY, True)
            txt(s, "[Z] back to chapter select", W//2, 452, 14, YELLOW, True)

        if st == 'dialog': self.draw_dialog_box()
        if self.toast_t > 0:
            txt(s, self.toast, W - 8, H - 20, 14, BLUE)
            r = txt(s, self.toast, 0, -100, 14)  # measure offscreen
            txt(s, self.toast, W - r.w - 10, H - 22, 14, BLUE)
        if self.flash: pygame.draw.rect(s, WHITE, (0, 0, W, H), 6)
        pygame.display.flip()

    # ---------------- main loop
    def run(self):
        self.song('title')
        smoke_t = 0
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT: pygame.quit(); return
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE: pygame.quit(); return
                    self.handle_key(ev.key)
            self.update()
            self.draw()
            self.clock.tick(FPS)
            if SMOKE:
                smoke_t += 1
                if smoke_t == 20: self.state = 'select'
                if smoke_t == 40: self.begin_chapter(0); self.state = 'over'
                if smoke_t == 60: self.start_battle(False); self.b['phase'] = 'menu'
                if smoke_t == 80: self.b['phase'] = 'dodge'; self.b['t'] = 0
                if smoke_t == 200: self.b['phase'] = 'fight'
                if smoke_t == 220: self.battle_key(pygame.K_z)
                if smoke_t == 240 and self.b: self.next_member()
                if smoke_t == 400:
                    print("SMOKE OK — states exercised, no crash. meow.")
                    pygame.quit(); return

if __name__ == '__main__':
    Game().run()

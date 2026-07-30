import os, io, base64, threading, json, math
from datetime import datetime

from kivy.app import App
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.graphics import Color, Rectangle, Ellipse, Line, RoundedRectangle, Mesh
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, NumericProperty, ObjectProperty, ListProperty, BooleanProperty, DictProperty
from kivy.utils import get_color_from_hex

import crop_advisory_engine
import market_advisory_engine
import plant_db
import ann_model
import localization as l10n
from gemini_client import GeminiClient
from offline_vlm import OfflineVLM

try:
    from plyer import filechooser, camera
    PLYER_OK = True
except:
    PLYER_OK = False

# ─── COLORS ─────────────────────────────────────────────────────
DARK_BG    = "#0f172a"
DARK_CARD  = "#1e293b"
DARK_CARD2 = "#334155"
ACCENT     = "#3b82f6"
FG         = "#f1f5f9"
FG_DIM     = "#94a3b8"
CLR_SUCCESS= "#22c55e"
CLR_WARN   = "#eab308"
CLR_DANGER = "#ef4444"
BORDER     = "#475569"

# ─── LOCALIZATION WRAPPER ────────────────────────────────────────
def tr(s):
    return l10n.tr(s)

# ─── CROP-SPECIFIC PLANT DRAWING ────────────────────────────────
# All functions accept (canvas_ctx, w, h, gy, prog) where
# gy = ground y (0..h), prog = 0..1

def draw_maize(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-6, gy-4), size=(12, 4)))
        return
    sh = 10 + prog * (h * 0.58)
    st = gy - sh
    sw = max(2, int(3 + prog * 8))
    segs = int(5 + prog * 5)
    for s in range(segs):
        f = s / segs
        y1 = gy - f * sh
        y2 = gy - (f + 1/segs) * sh
        x1 = mx + int(3 * math.sin(math.radians(f * 120)))
        x2 = mx + int(3 * math.sin(math.radians((f+0.5) * 120)))
        shade = f"#{int(35+15*f):02x}{int(95+20*f):02x}{int(20+10*f):02x}"
        ctx.add(Color(*get_color_from_hex(shade)))
        ctx.add(Line(points=[x1, y1, x2, y2], width=sw))
    # leaves
    for i in range(int(2 + prog * 7)):
        side = 1 if i % 2 == 0 else -1
        f = (i + 1) / (3 + int(prog * 6))
        ly = gy - f * sh * 0.92
        lw = 8 + prog * 32
        lh = 3 + prog * 6
        gc = f"#{int(30+i*10):02x}{int(95+i*8):02x}{int(20):02x}"
            ctx.add(Color(*get_color_from_hex(gc)))
        pts = [mx+side*2, ly, mx+side*int(lw*0.2), ly-lh, mx+side*int(lw*0.6), ly, mx+side*int(lw*0.2), ly+lh]
        ctx.add(Mesh(vertices=pts, indices=range(4), mode="triangle_fan"))
        ctx.add(Color(*get_color_from_hex("#7cb342")))
        ctx.add(Line(points=[mx+side*2, ly, mx+side*int(lw*0.7), ly-int(lh*0.2)], width=1))
    # tassel
    if prog > 0.35:
        branches = 6 + int(prog * 8)
        for ti in range(branches):
            a = ti * (360 / branches)
            r = 8 + prog * 20
            tx = mx + int(r * math.cos(math.radians(a)))
            ty = st - 6 + int(r * math.sin(math.radians(a)) * 0.4)
            ctx.add(Color(*get_color_from_hex("#9e9e24")))
            ctx.add(Line(points=[mx, st-2, tx, ty], width=1))
            ctx.add(Color(*get_color_from_hex("#facc15")))
            ctx.add(Ellipse(pos=(tx-1, ty-1), size=(2, 2)))
    # ears
    if prog > 0.42:
        for ei in range(2):
            side = 1 if ei == 0 else -1
            ey = gy - sh * (0.3 + 0.2 * ei)
            ew, eh = 4+prog*10, 5+prog*12
            ctx.add(Color(*get_color_from_hex("#4caf50")))
            ctx.add(Ellipse(pos=(mx+side*3, ey-eh), size=(ew+8, eh*2), angle_start=0 if side>0 else 180, angle_end=160))
            si_count = 4 + int(prog * 6)
            for sii in range(si_count):
                sx = mx + side * ew
                sy = ey + (sii-2)*1
                ctx.add(Color(*get_color_from_hex("#c8a84e")))
                ctx.add(Line(points=[sx, sy, sx+side*int(8+prog*10), sy-int(2+prog*4)], width=1))

def draw_cereal(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-4, gy-3), size=(8, 3)))
        return
    nt = int(2 + prog * 4)
    for t in range(nt):
        ox = (t - (nt-1)/2) * 8
        sh = 6 + prog * (h * 0.40 + t * 2)
        st = gy - sh
        ctx.add(Color(*get_color_from_hex("#5a7a4a")))
        ctx.add(Line(points=[mx+ox, gy, mx+ox+int(2*math.sin(t*2)), st], width=2))
        for i in range(int(1 + prog * 5)):
            side = 1 if i % 2 == 0 else -1
            f = (i + 1) / 6
            ly = gy - f * sh * 0.85
            ll = 3 + prog * 15
            ctx.add(Line(points=[mx+ox+side*1, ly, mx+ox+side*ll, ly-1], width=2))
        if prog > 0.45:
            hh = 5 + prog * 22
            hw = 2 + prog * 4
            ctx.add(Color(*get_color_from_hex("#c8a84e")))
            ctx.add(Rectangle(pos=(mx+ox-hw, st-hh), size=(hw*2, hh)))
            for ai in range(5):
                ax = mx+ox + (ai-2)*2
                ctx.add(Color(*get_color_from_hex("#d4a843")))
                ctx.add(Line(points=[ax, st-hh, ax, st-hh-6], width=1))

def draw_rice(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-5, gy-2), size=(10, 2)))
        return
    ctx.add(Color(*get_color_from_hex("#1a3a4a")))
    ctx.add(Rectangle(pos=(0, gy), size=(w, 6)))
    nt = int(3 + prog * 3)
    for t in range(nt):
        ox = (t - 1) * 8
        sh = 5 + prog * (h * 0.38)
        st = gy - sh
        ctx.add(Color(*get_color_from_hex("#5a8a4a")))
        ctx.add(Line(points=[mx+ox, gy, mx+ox, st], width=2))
        for i in range(int(1 + prog * 5)):
            side = 1 if i % 2 == 0 else -1
            f = (i + 1) / 6
            ly = gy - f * sh * 0.8
            ll = 3 + prog * 10
            ctx.add(Line(points=[mx+ox+side*2, ly, mx+ox+side*ll, ly-1], width=2))
        if prog > 0.5:
            for pi in range(5 + int(prog * 5)):
                a = 160 + pi * 8
                r = 3 + prog * 14
                px = mx+ox + int(r * math.cos(math.radians(a)))
                py = st + int(r * math.sin(math.radians(a)) * 0.3)
                ctx.add(Color(*get_color_from_hex("#c8a84e")))
                ctx.add(Line(points=[mx+ox, st, px, py], width=1))
                ctx.add(Color(*get_color_from_hex("#d4a843")))
                ctx.add(Ellipse(pos=(px-1, py-1), size=(2, 2)))

def draw_cassava(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-5, gy-3), size=(10, 3)))
        return
    sh = 6 + prog * (h * 0.38)
    st = gy - sh
    sw = max(2, int(3 + prog * 7))
    ctx.add(Color(*get_color_from_hex("#5d4037")))
    ctx.add(Line(points=[mx, gy, mx, st], width=sw))
    for bi in range(int(1 + prog * 4)):
        side = 1 if bi % 2 == 0 else -1
        f = (bi + 1) / 5
        by = gy - f * sh
        bl = 6 + prog * 22
        ctx.add(Color(*get_color_from_hex("#5d4037")))
        ctx.add(Line(points=[mx, by, mx+side*bl, by-12], width=max(2, int(2+prog*3))))
        if prog > 0.2:
            lx, ly2 = mx+side*bl, by-12
            for li in range(7):
                a = -70 + li * (140 / 6)
                rad = 4 + prog * 16
                fx = lx + int(rad * math.cos(math.radians(a)))
                fy = ly2 + int(rad * math.sin(math.radians(a)))
                lc = f"#{int(35+li*8):02x}{int(105+li*5):02x}{int(25):02x}"
                ctx.add(Color(*get_color_from_hex(lc)))
                ctx.add(Line(points=[lx, ly2, fx, fy], width=2))
                ctx.add(Color(*get_color_from_hex("#2e5a1e")))
                ctx.add(Line(points=[lx, ly2, fx, fy], width=1))
    if prog > 0.5:
        for ri in range(3 + int(prog * 2)):
            rx = mx + (ri - 1) * 12
            rl = 6 + prog * 18
            rr = 2 + prog * 5
            ctx.add(Color(*get_color_from_hex("#8B6914")))
            ctx.add(Line(points=[rx, gy, rx-int(5+ri*3), gy+rl], width=rr))
            ctx.add(Color(*get_color_from_hex("#a0724a")))
            ctx.add(Ellipse(pos=(rx-rr, gy+rl-rr), size=(rr*2, rr*2)))

def draw_groundnuts(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-6, gy-3), size=(12, 3)))
        return
    bh = 4 + prog * (h * 0.18)
    bt = gy - bh
    ctx.add(Color(*get_color_from_hex("#2e7d32")))
    ctx.add(Line(points=[mx, gy, mx, bt], width=max(2, int(2+prog*3))))
    for bi in range(int(3 + prog * 6)):
        side = 1 if bi % 2 == 0 else -1
        f = 0.1 + (bi // 2) * 0.2
        bx = mx + side * (4 + bi * 8)
        by = gy - f * bh
        ctx.add(Color(*get_color_from_hex("#2e7d32")))
        ctx.add(Line(points=[mx, gy-f*bh*0.8, bx, by], width=2))
        if prog > 0.2:
            lc = f"#{int(40+bi*8):02x}{int(100+bi*6):02x}{int(25):02x}"
            ctx.add(Color(*get_color_from_hex(lc)))
            for lii in range(4):
                xx = bx + (lii-1)*3
                ctx.add(Ellipse(pos=(xx-2, by-2), size=(4,4)))
    if 0.35 < prog < 0.65:
        for fi in range(int(1 + prog * 3)):
            side = 1 if fi % 2 == 0 else -1
            fy = gy - bh * (0.3 + 0.2 * fi)
            fx = mx + side * (8 + fi * 6)
            ctx.add(Color(*get_color_from_hex("#facc15")))
            ctx.add(Ellipse(pos=(fx-3, fy-3), size=(6,6)))
    if prog > 0.45:
        for pi in range(3 + int(prog * 2)):
            side = 1 if pi % 2 == 0 else -1
            px = mx + side * (6 + pi * 5)
            ctx.add(Color(*get_color_from_hex("#8B4513")))
            ctx.add(Line(points=[px, gy-2, px-1, gy+4+pi*3], width=2))
            ctx.add(Color(*get_color_from_hex("#8B6914")))
            ctx.add(Ellipse(pos=(px-3, gy+4+pi*3), size=(4,4)))

def draw_legume(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-4, gy-3), size=(8,3)))
        return
    bh = 4 + prog * (h * 0.22)
    bt = gy - bh
    ctx.add(Color(*get_color_from_hex("#2e7d32")))
    ctx.add(Line(points=[mx, gy, mx, bt], width=max(2, int(2+prog*4))))
    for i in range(int(2 + prog * 5)):
        side = 1 if i % 2 == 0 else -1
        f = (i + 1) / (3 + int(prog * 4))
        ly = gy - f * bh
        ll = 5 + prog * 14
        lc = f"#{int(40+i*10):02x}{int(105+i*8):02x}{int(25):02x}"
        ctx.add(Color(*get_color_from_hex(lc)))
        ctx.add(Ellipse(pos=(mx+side*2, ly-3), size=(ll, 6)))
        ctx.add(Ellipse(pos=(mx+side*(ll//2)-3, ly-4), size=(4,6)))
        ctx.add(Ellipse(pos=(mx+side*(ll//2), ly-1), size=(ll-2,5)))
    if prog > 0.4:
        for pi in range(int(1 + prog * 3)):
            side = 1 if pi % 2 == 0 else -1
            py = gy - bh * (0.3 + 0.25 * pi)
            ctx.add(Color(*get_color_from_hex("#7cb342")))
            ctx.add(Ellipse(pos=(mx+side*3, py-4), size=(11, 8), angle_start=0 if side>0 else 180, angle_end=180))

def draw_vine(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-5, gy-3), size=(10,3)))
        return
    for vi in range(int(2 + prog * 4)):
        side = 1 if vi % 2 == 0 else -1
        vx = mx + side * (6 + vi * 18)
        vy = gy - 1
        ctx.add(Color(*get_color_from_hex("#2e7d32")))
        ctx.add(Line(points=[mx, vy, vx, vy-2-vi*2], width=3))
        ctx.add(Line(points=[vx, vy-2-vi*2, vx+side*28, vy+2+vi*2], width=2))
        if prog > 0.15 and vi < 4:
            lx, ly2 = vx-3, vy-5-vi*3
            ls = 5 + prog * 15
            lc = f"#{int(35+vi*15):02x}{int(105+vi*8):02x}{int(25):02x}"
            ctx.add(Color(*get_color_from_hex(lc)))
            pts = [lx, ly2, lx-ls//2, ly2-ls//3, lx+ls//2, ly2+ls//3, lx+ls//3, ly2-ls//3]
            ctx.add(Mesh(vertices=pts, indices=range(4), mode="triangle_fan"))
    if prog > 0.45:
        for fi in range(int(prog * 2)):
            side = 1 if fi % 2 == 0 else -1
            fx = mx + side * (12 + fi * 30)
            fy = gy + 3 + fi * 5
            fs = 4 + prog * 8
            ctx.add(Color(*get_color_from_hex("#f4a460")))
            ctx.add(Ellipse(pos=(fx-fs, fy-fs//2), size=(fs*2, fs)))
            ctx.add(Color(*get_color_from_hex("#facc15")))
            ctx.add(Ellipse(pos=(fx-fs+2, fy-fs//2+1), size=(fs*2-4, fs-2)))

def draw_cotton(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-4, gy-3), size=(8,3)))
        return
    sh = 6 + prog * (h * 0.34)
    st = gy - sh
    sw = max(2, int(2 + prog * 6))
    ctx.add(Color(*get_color_from_hex("#5d4037")))
    ctx.add(Line(points=[mx, gy, mx, st], width=sw))
    for bi in range(int(1 + prog * 3)):
        side = 1 if bi % 2 == 0 else -1
        f = (bi + 1) / 4
        by = gy - f * sh
        bl = 6 + prog * 18
        ctx.add(Color(*get_color_from_hex("#5d4037")))
        ctx.add(Line(points=[mx, by, mx+side*bl, by-8], width=max(2, int(2+prog*2))))
        if prog > 0.2:
            lx, ly2 = mx+side*bl, by-8
            lobe = 3 + prog * 12
            lc = f"#{int(40+bi*12):02x}{int(110+bi*6):02x}{int(30):02x}"
            ctx.add(Color(*get_color_from_hex(lc)))
            pts = [lx, ly2, lx-side*lobe, ly2-lobe, lx+side*lobe, ly2-lobe, lx, ly2+lobe//2]
            ctx.add(Mesh(vertices=pts, indices=range(4), mode="triangle_fan"))
    if prog > 0.45:
        for bi in range(int(1 + prog * 2)):
            side = 1 if bi % 2 == 0 else -1
            by = gy - sh * (0.35 + 0.3 * bi)
            bx = mx + side * (4 + bi * 18)
            bs = 4 + prog * 10
            ctx.add(Color(*get_color_from_hex("#f5f5f5")))
            ctx.add(Ellipse(pos=(bx-bs, by-bs), size=(bs*2, bs*2)))
            ctx.add(Color(*get_color_from_hex("#ffffff")))
            ctx.add(Ellipse(pos=(bx-bs+2, by-bs+2), size=(bs*2-4, bs*2-4)))

def draw_sunflower(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-5, gy-3), size=(10,3)))
        return
    sh = 8 + prog * (h * 0.52)
    st = gy - sh
    sw = max(2, int(3 + prog * 9))
    ctx.add(Color(*get_color_from_hex("#3d6b35")))
    ctx.add(Line(points=[mx, gy, mx, st], width=sw))
    for i in range(int(1 + prog * 5)):
        side = 1 if i % 2 == 0 else -1
        f = (i + 1) / 6
        ly = gy - f * sh * 0.85
        ll = 6 + prog * 24
        lh = 4 + prog * 8
        lc = f"#{int(40+i*12):02x}{int(115+i*8):02x}{int(30):02x}"
        ctx.add(Color(*get_color_from_hex(lc)))
        pts = [mx, ly, mx+side*ll, ly-lh, mx+side*(ll-3), ly+lh]
        from kivy.graphics import Mesh
        ctx.add(Mesh(vertices=pts, indices=range(3), mode="triangle_fan"))
    if prog > 0.45:
        fs = 8 + prog * 22
        for pi in range(24):
            a = pi * 15
            rad = fs + 4
            px = mx + int(rad * math.cos(math.radians(a)))
            py = st + int(rad * math.sin(math.radians(a)))
            ctx.add(Color(*get_color_from_hex("#facc15")))
            ctx.add(Line(points=[mx+int((fs-3)*math.cos(math.radians(a))),
                                st+int((fs-3)*math.sin(math.radians(a))),
                                px, py], width=3))
        ctx.add(Color(*get_color_from_hex("#5d4037")))
        ctx.add(Ellipse(pos=(mx-fs+4, st-fs+4), size=((fs-4)*2, (fs-4)*2)))
        for si in range(15):
            a2 = si * 24
            r2 = 2 + prog * 8
            sx = mx + int(r2 * math.cos(math.radians(a2)))
            sy = st + int(r2 * math.sin(math.radians(a2)))
            ctx.add(Color(*get_color_from_hex("#3e2723")))
            ctx.add(Ellipse(pos=(sx-1, sy-1), size=(2,2)))

def draw_shrub(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-4, gy-3), size=(8,3)))
        return
    sh = 6 + prog * (h * 0.36)
    st = gy - sh
    sw = max(2, int(2 + prog * 6))
    ctx.add(Color(*get_color_from_hex("#5d4037")))
    ctx.add(Line(points=[mx, gy, mx, st], width=sw))
    for bi in range(int(1 + prog * 4)):
        side = 1 if bi % 2 == 0 else -1
        f = (bi + 1) / 5
        by = gy - f * sh
        bl = 6 + prog * 20
        ctx.add(Color(*get_color_from_hex("#5d4037")))
        ctx.add(Line(points=[mx, by, mx+side*bl, by-12], width=max(2, int(2+prog*2))))
        if prog > 0.2:
            for li in range(2):
                lo = li * 6
                lc = f"#{int(45+li*12):02x}{int(110+li*8):02x}{int(30):02x}"
                ctx.add(Color(*get_color_from_hex(lc)))
                ctx.add(Ellipse(pos=(mx+side*bl-3-lo, by-14-lo), size=(8+lo*2, 10+lo*2)))
    if prog > 0.5:
        for fi in range(int(1 + prog * 2)):
            side = 1 if fi % 2 == 0 else -1
            fy = gy - sh * (0.25 + 0.3 * fi)
            fx = mx + side * (4 + fi * 14)
            fs = 3 + prog * 7
            ctx.add(Color(*get_color_from_hex("#f44336")))
            ctx.add(Ellipse(pos=(fx-fs//2, fy-fs//2), size=(fs, fs)))

def draw_rosette(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-6, gy-3), size=(12,3)))
        return
    size = 5 + prog * (h * 0.11)
    for i in range(int(3 + prog * 12)):
        a = i * (360 / (3 + int(prog * 10)))
        rad = size * (0.25 + 0.75 * (i % 3) / 3)
        lx = mx + int(rad * math.cos(math.radians(a)))
        ly = gy - int(rad * math.sin(math.radians(a)))
        lc = f"#{int(30+i*7):02x}{int(115+i*4):02x}{int(25+i*2):02x}"
        ctx.add(Color(*get_color_from_hex(lc)))
        ctx.add(Ellipse(pos=(lx-size//3, ly-size//6), size=(size*2//3, size//3)))

def draw_root_crop(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-5, gy-3), size=(10,3)))
        return
    for i in range(int(3 + prog * 8)):
        side = 1 if i % 2 == 0 else -1
        f = (i + 1) / (4 + int(prog * 6))
        ly = gy - 3 - f * (8 + prog * 32)
        ll = 3 + prog * 16
        lc = f"#{int(35+i*8):02x}{int(110+i*6):02x}{int(25):02x}"
        ctx.add(Color(*get_color_from_hex(lc)))
        ctx.add(Line(points=[mx, ly, mx+side*ll, ly], width=2))
    if prog > 0.3:
        rs = 3 + prog * 14
        for ri in range(int(1 + prog * 2)):
            rx = mx + (ri - 1) * 12
            ctx.add(Color(*get_color_from_hex("#f4a460")))
            ctx.add(Ellipse(pos=(rx-rs//2, gy+2), size=(rs, rs+ri*5)))
            ctx.add(Color(*get_color_from_hex("#8d6e63")))
            ctx.add(Line(points=[rx, gy+rs+ri*5, rx, gy+rs+ri*5+5], width=1))

def draw_banana(ctx, w, h, gy, prog):
    mx = w * 0.5
    if prog < 0.04:
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(RoundedRectangle(pos=(mx-6, gy-3), size=(12,3)))
        return
    sh = 10 + prog * (h * 0.48)
    st = gy - sh
    sw = max(4, int(4 + prog * 12))
    for la in range(3):
        lw = sw - la * 3
        ox = (la - 1) * 3
        ctx.add(Color(*get_color_from_hex(f"#{int(45+la*10):02x}{int(105+la*15):02x}{int(30-la*5):02x}")))
        ctx.add(Line(points=[mx+ox, gy, mx+ox, st], width=max(2, lw)))
    for i in range(int(1 + prog * 5)):
        side = 1 if i % 2 == 0 else -1
        f = (i + 1) / 6
        ly = gy - f * sh * 0.9
        ll = 10 + prog * 38
        lh = 5 + prog * 10
        lc = f"#{int(30+i*10):02x}{int(105+i*6):02x}{int(22):02x}"
        ctx.add(Color(*get_color_from_hex(lc)))
        ctx.add(Ellipse(pos=(mx+side*3, ly-lh), size=(ll, lh*2), angle_start=0 if side>0 else 180, angle_end=130))
        ctx.add(Color(*get_color_from_hex("#2e5a1e")))
        ctx.add(Line(points=[mx+side*3, ly, mx+side*(ll-5), ly], width=2))
    if prog > 0.35:
        bud_h = 6 + prog * 18
        ctx.add(Color(*get_color_from_hex("#8B4513")))
        pts = [mx-4, st, mx+4, st, mx+7, st+bud_h, mx-7, st+bud_h]
        from kivy.graphics import Mesh
        ctx.add(Mesh(vertices=pts, indices=range(4), mode="triangle_fan"))
    if prog > 0.5:
        for bi in range(3 + int(prog * 3)):
            side = 1 if bi % 2 == 0 else -1
            by = st + bud_h * 0.4 + bi * 9
            ctx.add(Color(*get_color_from_hex("#facc15")))
            ctx.add(Ellipse(pos=(mx+side*4, by-3), size=(18, 6), angle_start=0 if side>0 else 180, angle_end=120))
            ctx.add(Color(*get_color_from_hex("#fde047")))
            ctx.add(Ellipse(pos=(mx+side*5, by-1), size=(14, 2), angle_start=0 if side>0 else 180, angle_end=120))

DRAWER_MAP = {
    "maize": draw_maize, "sorghum": draw_maize, "millet": draw_maize,
    "wheat": draw_cereal, "rice": draw_rice, "sugarcane": draw_cereal,
    "cassava": draw_cassava, "sweet_potato": draw_vine, "potato": draw_root_crop,
    "groundnuts": draw_groundnuts, "soybean": draw_legume, "beans": draw_legume,
    "cowpea": draw_legume, "pigeon_pea": draw_shrub, "bambara": draw_groundnuts,
    "cotton": draw_cotton, "tobacco": draw_shrub, "sunflower": draw_sunflower,
    "coffee": draw_shrub, "banana": draw_banana,
    "tomato": draw_shrub, "pumpkin": draw_vine, "cucumber": draw_vine,
    "watermelon": draw_vine,
    "cabbage": draw_rosette, "lettuce": draw_rosette, "kale": draw_rosette,
    "onion": draw_root_crop, "carrot": draw_root_crop, "beetroot": draw_root_crop,
}

# ─── REUSABLE WIDGETS ───────────────────────────────────────────
class Card(BoxLayout):
    pass

class NavButton(Button):
    pass

# ─── KV LANGUAGE UI ─────────────────────────────────────────────
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<Card>:
    orientation: 'vertical'
    padding: dp(10)
    size_hint_y: None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: get_color_from_hex('#1e293b')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(6)]

<NavButton>:
    size_hint_y: None
    height: dp(48)
    background_normal: ''
    background_color: 0,0,0,0
    color: get_color_from_hex('#94a3b8')
    font_size: sp(11)
    markup: True

BoxLayout:
    orientation: 'vertical'
    ScreenManager:
        id: sm
        Screen:
            name: 'live'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(8)
                spacing: dp(6)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#0f172a')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: '[color=f1f5f9]Live Diagnosis[/color]'
                    markup: True
                    size_hint_y: None
                    height: dp(30)
                    font_size: sp(16)
                RelativeLayout:
                    size_hint_y: 0.45
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex('#1e293b')
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(8)]
                    Image:
                        id: live_preview
                        source: ''
                        allow_stretch: True
                        keep_ratio: True
                        center: self.parent.center
                    Label:
                        text: 'No Camera'
                        color: get_color_from_hex('#475569')
                        font_size: sp(14)
                        center: self.parent.center
                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(8)
                    Button:
                        text: 'Capture'
                        background_color: get_color_from_hex('#3b82f6')
                        color: get_color_from_hex('#f1f5f9')
                        on_press: app.capture_live()
                    Button:
                        text: 'Diagnose'
                        background_color: get_color_from_hex('#22c55e')
                        color: get_color_from_hex('#f1f5f9')
                        on_press: app.diagnose_live()
                ScrollView:
                    Card:
                        id: live_result_box
                        Label:
                            id: live_result
                            text: 'Capture an image to diagnose'
                            color: get_color_from_hex('#94a3b8')
                            font_size: sp(12)
                            text_size: self.width, None
                            size_hint_y: None
                            height: self.texture_size[1]

        Screen:
            name: 'offline'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(8)
                spacing: dp(6)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#0f172a')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: '[color=f1f5f9]Offline Analysis[/color]'
                    markup: True
                    size_hint_y: None
                    height: dp(30)
                    font_size: sp(16)
                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(8)
                    Button:
                        text: 'Select Image'
                        background_color: get_color_from_hex('#3b82f6')
                        color: get_color_from_hex('#f1f5f9')
                        on_press: app.pick_image()
                    Button:
                        text: 'Analyze'
                        background_color: get_color_from_hex('#22c55e')
                        color: get_color_from_hex('#f1f5f9')
                        on_press: app.analyze_offline()
                RelativeLayout:
                    size_hint_y: 0.35
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex('#1e293b')
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(8)]
                    Image:
                        id: off_preview
                        source: ''
                        allow_stretch: True
                        keep_ratio: True
                        center: self.parent.center
                    Label:
                        id: off_placeholder
                        text: 'No image selected'
                        color: get_color_from_hex('#475569')
                        font_size: sp(14)
                        center: self.parent.center
                ScrollView:
                    Card:
                        id: off_result_box
                        Label:
                            id: off_result
                            text: 'Select an image and analyze'
                            color: get_color_from_hex('#94a3b8')
                            font_size: sp(12)
                            text_size: self.width, None
                            size_hint_y: None
                            height: self.texture_size[1]

        Screen:
            name: 'advisory'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(8)
                spacing: dp(4)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#0f172a')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: '[color=f1f5f9]Crop Advisory[/color]'
                    markup: True
                    size_hint_y: None
                    height: dp(28)
                    font_size: sp(16)
                ScrollView:
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(4)
                        Card:
                            Label:
                                text: 'Climate & Soil'
                                color: get_color_from_hex('#3b82f6')
                                font_size: sp(13)
                                size_hint_y: None
                                height: dp(20)
                            GridLayout:
                                cols: 2
                                spacing: dp(4)
                                size_hint_y: None
                                height: dp(150)
                                Label:
                                    text: 'Climate'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                Spinner:
                                    id: adv_climate
                                    text: 'tropical'
                                    values: ['tropical','subtropical','temperate','semi-arid','highland']
                                    size_hint_x: 0.6
                                Label:
                                    text: 'Soil Type'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                Spinner:
                                    id: adv_soil
                                    text: 'loamy'
                                    values: ['loamy','sandy','clay','silt','laterite']
                                    size_hint_x: 0.6
                                Label:
                                    text: 'pH: 6.5'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                BoxLayout:
                                    Slider:
                                        id: adv_ph
                                        min: 3.0
                                        max: 9.0
                                        value: 6.5
                                        cursor_size: dp(20)
                                        on_value: setattr(app, '_adv_ph_val', args[1])
                                Label:
                                    text: 'Rainfall: 800mm'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                BoxLayout:
                                    Slider:
                                        id: adv_rain
                                        min: 200
                                        max: 2500
                                        value: 800
                                        on_value: setattr(app, '_adv_rain_val', args[1])
                        Card:
                            Label:
                                text: 'Temperature'
                                color: get_color_from_hex('#3b82f6')
                                font_size: sp(13)
                                size_hint_y: None
                                height: dp(20)
                            GridLayout:
                                cols: 3
                                spacing: dp(4)
                                size_hint_y: None
                                height: dp(60)
                                Label:
                                    text: 'Min'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                TextInput:
                                    id: adv_tmin
                                    text: '18'
                                    input_filter: 'int'
                                    size_hint_x: 0.3
                                Label:
                                    text: chr(176)+'C'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                Label:
                                    text: 'Max'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                                TextInput:
                                    id: adv_tmax
                                    text: '32'
                                    input_filter: 'int'
                                    size_hint_x: 0.3
                                Label:
                                    text: chr(176)+'C'
                                    color: get_color_from_hex('#94a3b8')
                                    font_size: sp(11)
                        BoxLayout:
                            size_hint_y: None
                            height: dp(40)
                            spacing: dp(8)
                            Button:
                                text: 'Get Recommendations'
                                background_color: get_color_from_hex('#22c55e')
                                color: get_color_from_hex('#f1f5f9')
                                on_press: app.get_recommendations()
                        Label:
                            id: adv_results_header
                            text: ''
                            color: get_color_from_hex('#3b82f6')
                            font_size: sp(13)
                            size_hint_y: None
                            height: dp(20)
                        BoxLayout:
                            id: adv_results
                            orientation: 'vertical'
                            size_hint_y: None
                            height: self.minimum_height

        Screen:
            name: 'market'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(8)
                spacing: dp(4)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#0f172a')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: '[color=f1f5f9]Market Advisory[/color]'
                    markup: True
                    size_hint_y: None
                    height: dp(28)
                    font_size: sp(16)
                Card:
                    size_hint_y: None
                    height: dp(130)
                    GridLayout:
                        cols: 2
                        spacing: dp(4)
                        size_hint_y: None
                        height: dp(120)
                        Label:
                            text: 'Min Demand'
                            color: get_color_from_hex('#94a3b8')
                            font_size: sp(11)
                        BoxLayout:
                            Slider:
                                id: mkt_demand
                                min: 0
                                max: 10
                                value: 6.0
                        Label:
                            text: 'Max Price (K)'
                            color: get_color_from_hex('#94a3b8')
                            font_size: sp(11)
                        BoxLayout:
                            Slider:
                                id: mkt_price
                                min: 5
                                max: 70
                                value: 70
                        Label:
                            text: 'Min Margin %'
                            color: get_color_from_hex('#94a3b8')
                            font_size: sp(11)
                        BoxLayout:
                            Slider:
                                id: mkt_margin
                                min: 0
                                max: 80
                                value: 0
                Button:
                    text: 'Refresh'
                    size_hint_y: None
                    height: dp(40)
                    background_color: get_color_from_hex('#3b82f6')
                    color: get_color_from_hex('#f1f5f9')
                    on_press: app.refresh_market()
                ScrollView:
                    BoxLayout:
                        id: mkt_results
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(4)

        Screen:
            name: 'simulator'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(6)
                spacing: dp(4)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#0f172a')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: '[color=f1f5f9]Crop Simulator[/color]'
                    markup: True
                    size_hint_y: None
                    height: dp(28)
                    font_size: sp(16)
                RelativeLayout:
                    size_hint_y: 0.4
                    canvas.before:
                        Color:
                            rgba: get_color_from_hex('#1a2a1a')
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [dp(6)]
                    Widget:
                        id: sim_canvas
                BoxLayout:
                    size_hint_y: None
                    height: dp(40)
                    spacing: dp(4)
                    Spinner:
                        id: sim_crop
                        text: 'maize'
                        values: ['maize','sorghum','millet','wheat','rice','cassava','sweet_potato','groundnuts','soybean','beans','cotton','sunflower','banana','tomato','cabbage','carrot']
                        size_hint_x: 0.4
                    Label:
                        id: sim_day
                        text: 'Day 0'
                        color: get_color_from_hex('#3b82f6')
                        font_size: sp(11)
                        size_hint_x: 0.2
                    ProgressBar:
                        id: sim_prog
                        max: 100
                        value: 0
                        size_hint_x: 0.3
                    Button:
                        id: sim_play
                        text: chr(9654)
                        background_color: get_color_from_hex('#22c55e')
                        color: get_color_from_hex('#f1f5f9')
                        size_hint_x: 0.1
                        on_press: app.toggle_sim()
                    Button:
                        text: chr(8634)
                        background_color: get_color_from_hex('#475569')
                        color: get_color_from_hex('#f1f5f9')
                        size_hint_x: 0.1
                        on_press: app.reset_sim()
                ScrollView:
                    BoxLayout:
                        id: sim_stages
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: dp(2)

        Screen:
            name: 'trainer'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(8)
                spacing: dp(6)
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#0f172a')
                    Rectangle:
                        pos: self.pos
                        size: self.size
                Label:
                    text: '[color=f1f5f9]Model Trainer[/color]'
                    markup: True
                    size_hint_y: None
                    height: dp(30)
                    font_size: sp(16)
                Card:
                    size_hint_y: None
                    height: dp(120)
                    Label:
                        text: 'Train a neural network model\\non your crop data'
                        color: get_color_from_hex('#94a3b8')
                        font_size: sp(12)
                        text_size: self.width, None
                        size_hint_y: None
                        height: dp(40)
                    Button:
                        text: 'Select CSV Data'
                        size_hint_y: None
                        height: dp(40)
                        background_color: get_color_from_hex('#3b82f6')
                        color: get_color_from_hex('#f1f5f9')
                        on_press: app.pick_training_data()
                    Button:
                        text: 'Start Training'
                        size_hint_y: None
                        height: dp(40)
                        background_color: get_color_from_hex('#22c55e')
                        color: get_color_from_hex('#f1f5f9')
                        on_press: app.start_training()
                ScrollView:
                    Card:
                        Label:
                            id: train_log
                            text: 'Ready'
                            color: get_color_from_hex('#94a3b8')
                            font_size: sp(11)
                            text_size: self.width, None
                            size_hint_y: None
                            height: self.texture_size[1]

    BoxLayout:
        size_hint_y: None
        height: dp(52)
        canvas.before:
            Color:
                rgba: get_color_from_hex('#1e293b')
            Rectangle:
                pos: self.pos
                size: self.size
        Button:
            text: '[b]\\U0001F3A5[/b]\\nLive'
            markup: True
            on_press: sm.current = 'live'
        Button:
            text: '[b]\\U0001F4C4[/b]\\nOffline'
            markup: True
            on_press: sm.current = 'offline'
        Button:
            text: '[b]\\U0001F33E[/b]\\nAdvisory'
            markup: True
            on_press: sm.current = 'advisory'
        Button:
            text: '[b]\\U0001F4CA[/b]\\nMarket'
            markup: True
            on_press: sm.current = 'market'
        Button:
            text: '[b]\\U0001F9EA[/b]\\nSimulator'
            markup: True
            on_press: sm.current = 'simulator'
        Button:
            text: '[b]\\U0001F916[/b]\\nTrainer'
            markup: True
            on_press: sm.current = 'trainer'
'''

# ─── APP CLASS ──────────────────────────────────────────────────
class AgriEyeMobile(App):
    _sim_playing = False
    _sim_day = 0
    _sim_crop = "maize"
    _captured_path = None
    _offline_path = None
    _train_data_path = None

    def build(self):
        self.title = "Agri-Eye AI Diagnostics"
        return Builder.load_string(KV)

    def on_start(self):
        # Load simulator
        sm = self.root.ids.sm
        Clock.schedule_interval(self._sim_tick, 0.3)

    # ─── LIVE DIAGNOSIS ───────────────────────────────────────────
    def capture_live(self):
        if PLYER_OK:
            try:
                camera.take_picture(self._on_captured, on_complete=self._on_cap_done)
            except:
                self._toast("Camera not available")
        else:
            self._toast("Camera module not available")

    def _on_captured(self, path):
        self._captured_path = path
        img = self.root.ids.live_preview
        img.source = path
        img.reload()

    def _on_cap_done(self, *a):
        pass

    def diagnose_live(self):
        if not self._captured_path:
            self._toast("Capture an image first")
            return
        lbl = self.root.ids.live_result
        lbl.text = "Analyzing..."
        threading.Thread(target=self._do_diagnose, daemon=True).start()

    def _do_diagnose(self):
        try:
            from PIL import Image
            img = Image.open(self._captured_path)
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            client = GeminiClient()
            result = client.analyze_image(b64)
            txt = f"[color=f1f5f9][b]Result:[/b][/color]\n"
            if result:
                txt += f"   {result[:500]}"
            else:
                txt += "   No diagnosis returned"
        except Exception as e:
            txt = f"[color=ef4444]Error: {e}[/color]"
        Clock.schedule_once(lambda dt: self._set_live_result(txt))

    @mainthread
    def _set_live_result(self, txt):
        self.root.ids.live_result.text = txt

    # ─── OFFLINE ANALYSIS ─────────────────────────────────────────
    def pick_image(self):
        if PLYER_OK:
            try:
                filechooser.open_file(on_selection=self._on_file_picked)
            except:
                self._toast("File chooser not available")
        else:
            self._toast("File chooser not available")

    def _on_file_picked(self, selection):
        if selection:
            self._offline_path = selection[0]
            img = self.root.ids.off_preview
            img.source = self._offline_path
            img.reload()
            self.root.ids.off_placeholder.text = ""

    def analyze_offline(self):
        if not self._offline_path:
            self._toast("Select an image first")
            return
        lbl = self.root.ids.off_result
        lbl.text = "Analyzing..."
        threading.Thread(target=self._do_offline, daemon=True).start()

    def _do_offline(self):
        try:
            from PIL import Image
            img = Image.open(self._offline_path)
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            b64 = base64.b64encode(buf.getvalue()).decode()
            vlm = OfflineVLM()
            result = vlm.analyze(b64)
            txt = f"[color=f1f5f9][b]Analysis:[/b][/color]\n"
            if result:
                txt += f"   {result[:500]}"
            else:
                txt += "   No analysis returned"
        except Exception as e:
            txt = f"[color=ef4444]Error: {e}[/color]"
        Clock.schedule_once(lambda dt: self._set_off_result(txt))

    @mainthread
    def _set_off_result(self, txt):
        self.root.ids.off_result.text = txt

    # ─── CROP ADVISORY ────────────────────────────────────────────
    def get_recommendations(self):
        ids = self.root.ids
        inputs = {
            "climate": ids.adv_climate.text,
            "soil_type": ids.adv_soil.text,
            "soil_ph": float(ids.adv_ph.value),
            "rainfall": float(ids.adv_rain.value),
            "temp_min": int(ids.adv_tmin.text or "18"),
            "temp_max": int(ids.adv_tmax.text or "32"),
        }
        results = crop_advisory_engine.calculate_advisory(inputs)
        box = ids.adv_results
        box.clear_widgets()
        ids.adv_results_header.text = f"[color=f1f5f9]Top Recommendations[/color]"
        for r in results[:10]:
            crop = r["crop"]
            score = r["total_score"]
            bg = "#22c55e" if score >= 75 else "#eab308" if score >= 50 else "#ef4444"
            card = Card()
            card.add_widget(Label(
                text=f"[color=f1f5f9][b]{crop['name']}[/b] ({crop['zambian_name']})[/color]",
                markup=True, font_size=sp(12), size_hint_y=None, height=dp(22),
                text_size=(self.root.width - dp(60), None), halign="left"))
            card.add_widget(Label(
                text=f"[color={bg}]Score: {score}%[/color]  [color=94a3b8]pH {crop['min_ph']}-{crop['max_ph']}  {crop['growth_days']}days[/color]",
                markup=True, font_size=sp(11), size_hint_y=None, height=dp(18)))
            box.add_widget(card)

    # ─── MARKET ADVISORY ──────────────────────────────────────────
    def refresh_market(self):
        ids = self.root.ids
        min_demand = float(ids.mkt_demand.value)
        max_price = float(ids.mkt_price.value)
        min_margin = int(ids.mkt_margin.value)
        items = market_advisory_engine.get_market_data()
        filtered = [i for i in items if i.get("demand", 0) >= min_demand
                    and i.get("price_zk_kg", 0) <= max_price
                    and i.get("margin", 0) >= min_margin]
        box = ids.mkt_results
        box.clear_widgets()
        for i in filtered[:15]:
            card = Card()
            card.add_widget(Label(
                text=f"[color=f1f5f9][b]{i['name']}[/b][/color]",
                markup=True, font_size=sp(12), size_hint_y=None, height=dp(22)))
            card.add_widget(Label(
                text=f"[color=22c55e]K{i['price_zk_kg']}/kg[/color]  Demand: {i['demand']}/10  Margin: {i['margin']}%",
                markup=True, font_size=sp(11), size_hint_y=None, height=dp(18)))
            box.add_widget(card)
        if not filtered:
            box.add_widget(Label(text="No matching crops", color=get_color_from_hex("#94a3b8"), font_size=sp(12)))

    # ─── SIMULATOR ─────────────────────────────────────────────────
    def toggle_sim(self):
        self._sim_playing = not self._sim_playing
        self.root.ids.sim_play.text = chr(9632) if self._sim_playing else chr(9654)

    def reset_sim(self):
        self._sim_playing = False
        self._sim_day = 0
        self.root.ids.sim_play.text = chr(9654)
        self._draw_plant()

    def _sim_tick(self, dt):
        if self._sim_playing:
            crop_id = self.root.ids.sim_crop.text or "maize"
            crop = crop_advisory_engine.get_or_create_crop_data(crop_id)
            stages = crop.get("stages", [])
            total = sum(s[1] for s in stages) or 120
            if self._sim_day <= total:
                self._sim_day += 1
            self._update_sim_display()
        elif self._sim_day == 0:
            self._update_sim_display()

    def _update_sim_display(self):
        ids = self.root.ids
        crop_id = ids.sim_crop.text or "maize"
        crop = crop_advisory_engine.get_or_create_crop_data(crop_id)
        stages = crop.get("stages", [])
        total = sum(s[1] for s in stages) or 120
        day = self._sim_day
        prog = min(1.0, day / total)
        ids.sim_day.text = f"Day {min(day, total)}/{total}"
        ids.sim_prog.value = prog * 100
        self._draw_plant()
        # stage cards
        box = ids.sim_stages
        box.clear_widgets()
        cumulative = 0
        for s in stages:
            start = cumulative
            end = cumulative + s[1]
            in_stage = start <= day < end
            past = day >= end
            pct = min(100, max(0, (day - start) / s[1] * 100)) if s[1] > 0 else 0
            cumulative += s[1]
            bg = "#334155" if in_stage else "#22c55e" if past else "#1e293b"
            fg = "#3b82f6" if in_stage else "#22c55e" if past else "#94a3b8"
            icon = chr(9654) if in_stage else chr(10003) if past else "  "
            card = Card()
            card.add_widget(Label(
                text=f"[color={fg}]{icon} {s[0]} ({s[1]}d)[/color]",
                markup=True, font_size=sp(11), size_hint_y=None, height=dp(20)))
            if in_stage:
                card.add_widget(Label(
                    text=f"[color=22c55e]{'|'*int(pct//10)}{'.'*(10-int(pct//10))} {pct:.0f}%[/color]",
                    markup=True, font_size=sp(10), size_hint_y=None, height=dp(16)))
            box.add_widget(card)
        if day >= total:
            box.add_widget(Label(
                text=f"[color=22c55e][b]READY FOR HARVEST[/b][/color]",
                markup=True, font_size=sp(13), size_hint_y=None, height=dp(24)))

    def _draw_plant(self):
        canvas_widget = self.root.ids.sim_canvas
        canvas_widget.canvas.clear()
        ctx = canvas_widget.canvas
        w = canvas_widget.width or 300
        h = canvas_widget.height or 200
        if w < 10:
            return
        crop_id = self.root.ids.sim_crop.text or "maize"
        crop = crop_advisory_engine.get_or_create_crop_data(crop_id)
        stages = crop.get("stages", [])
        total = sum(s[1] for s in stages) or 120
        prog = min(1.0, self._sim_day / total) if total > 0 else 0
        gy = int(h * 0.8)
        # sky
        sky_c = f"#{int(15+40*prog):02x}{int(25+60*prog):02x}{int(35+50*prog):02x}"
        ctx.add(Color(*get_color_from_hex(sky_c)))
        ctx.add(Rectangle(pos=(0, 0), size=(w, h)))
        # ground
        ctx.add(Color(*get_color_from_hex("#3d2b1f")))
        ctx.add(Rectangle(pos=(0, gy), size=(w, h - gy)))
        ctx.add(Color(*get_color_from_hex("#5a3d2b")))
        ctx.add(Rectangle(pos=(0, gy), size=(w, 5)))
        # sun
        sx, sy = w - 50, h - 45
        sr = 25 + int(10 * prog)
        ctx.add(Color(*get_color_from_hex("#facc15")))
        ctx.add(Ellipse(pos=(sx-sr, sy-sr), size=(sr*2, sr*2)))
        ctx.add(Color(*get_color_from_hex("#fde047")))
        ctx.add(Ellipse(pos=(sx-sr+5, sy-sr+5), size=((sr-5)*2, (sr-5)*2)))
        # clouds
        for i in range(int(2 + prog * 3)):
            cx = 40 + i * 110 + int(20 * (prog % 1))
            cy = h - 35 - i * 22
            shade = f"#{int(50+40*i):02x}{int(50+40*i):02x}{int(55+40*i):02x}"
            ctx.add(Color(*get_color_from_hex(shade)))
            ctx.add(Ellipse(pos=(cx, cy), size=(40, 16)))
            ctx.add(Ellipse(pos=(cx+15, cy-6), size=(33, 14)))
        # crop-specific drawing
        crop_id = self.root.ids.sim_crop.text or "maize"
        drawer = DRAWER_MAP.get(crop_id, draw_maize)
        drawer(ctx, w, h, gy, prog)

    # ─── MODEL TRAINER ────────────────────────────────────────────
    def pick_training_data(self):
        if PLYER_OK:
            try:
                filechooser.open_file(on_selection=self._on_train_file, filters=["*.csv"])
            except:
                self._toast("File chooser not available")
        else:
            self._toast("File chooser not available")

    def _on_train_file(self, selection):
        if selection:
            self._train_data_path = selection[0]
            self._log(f"Selected: {self._train_data_path}")

    def start_training(self):
        if not self._train_data_path:
            self._toast("Select training data first")
            return
        self._log("Training started...")
        threading.Thread(target=self._do_train, daemon=True).start()

    def _do_train(self):
        try:
            import numpy as np
            import csv
            rows = []
            with open(self._train_data_path) as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row:
                        rows.append([float(x) for x in row if x.strip()])
            if len(rows) < 5:
                raise ValueError("Need at least 5 data rows")
            arr = np.array(rows)
            X = arr[:, :-1]
            y = arr[:, -1]
            model = ann_model.AnnModel(input_dim=X.shape[1])
            model.train(X, y, epochs=20)
            self._log(f"Training complete! Model saved.")
        except Exception as e:
            self._log(f"Error: {e}")

    @mainthread
    def _log(self, msg):
        lbl = self.root.ids.train_log
        lbl.text = lbl.text + f"\n{msg}" if lbl.text != "Ready" else msg

    def _toast(self, msg):
        self._log(msg)

if __name__ == "__main__":
    AgriEyeMobile().run()

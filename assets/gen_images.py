from PIL import Image, ImageDraw, ImageFont
import os

OUTPUT = os.path.dirname(os.path.abspath(__file__))

def hex_to_rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def draw_gradient(draw, w, h, c1, c2, vertical=True):
    for i in range(h if vertical else w):
        t = i / (h - 1 if vertical else w - 1)
        r = int(c1[0] + (c2[0] - c1[0]) * t)
        g = int(c1[1] + (c2[1] - c1[1]) * t)
        b = int(c1[2] + (c2[2] - c1[2]) * t)
        if vertical:
            draw.line([(0, i), (w, i)], fill=(r, g, b))
        else:
            draw.line([(i, 0), (i, h)], fill=(r, g, b))

def rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + 2*radius, y1 + 2*radius], fill=fill)
    draw.ellipse([x2 - 2*radius, y1, x2, y1 + 2*radius], fill=fill)
    draw.ellipse([x1, y2 - 2*radius, x1 + 2*radius, y2], fill=fill)
    draw.ellipse([x2 - 2*radius, y2 - 2*radius, x2, y2], fill=fill)

def try_font(size):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFPro.ttf",
        "/Library/Fonts/Arial Bold.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

def try_font_regular(size):
    paths = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFPro.ttf",
    ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            pass
    return ImageFont.load_default()

# ── Banner: Anushka Nair profile header ──────────────────────────────────────
def make_banner():
    W, H = 1400, 320
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, W, H, hex_to_rgb("#0B1020"), hex_to_rgb("#0D2137"), vertical=True)

    # accent line top
    draw.rectangle([0, 0, W, 4], fill=hex_to_rgb("#0EA5E9"))

    # Grid dots pattern (subtle)
    for x in range(0, W, 40):
        for y in range(0, H, 40):
            draw.ellipse([x-1, y-1, x+1, y+1], fill=(255,255,255,30))

    # Name
    f_name  = try_font(72)
    f_sub   = try_font_regular(26)
    f_small = try_font_regular(20)

    name = "Anushka Nair"
    bbox = draw.textbbox((0,0), name, font=f_name)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw)//2, 60), name, font=f_name, fill=hex_to_rgb("#FFFFFF"))

    sub = "Software Engineering  |  ML  |  Generative AI  |  Full-Stack  |  Web3"
    bbox2 = draw.textbbox((0,0), sub, font=f_sub)
    tw2 = bbox2[2] - bbox2[0]
    draw.text(((W - tw2)//2, 152), sub, font=f_sub, fill=hex_to_rgb("#38BDF8"))

    tagline = "CSE @ VIT Vellore  •  CGPA 9.44  •  IEEE Published  •  Open to SDE Internships"
    bbox3 = draw.textbbox((0,0), tagline, font=f_small)
    tw3 = bbox3[2] - bbox3[0]
    draw.text(((W - tw3)//2, 205), tagline, font=f_small, fill=hex_to_rgb("#94A3B8"))

    # bottom accent line
    draw.rectangle([0, H-4, W, H], fill=hex_to_rgb("#22C55E"))

    img.save(os.path.join(OUTPUT, "banner.png"))
    print("banner.png saved")

# ── Project card ─────────────────────────────────────────────────────────────
def make_project_card(filename, title, subtitle, stack_tags, accent, icon_char):
    W, H = 900, 200
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, W, H, hex_to_rgb("#0F172A"), hex_to_rgb("#1E293B"), vertical=False)

    acc = hex_to_rgb(accent)

    # left accent bar
    draw.rectangle([0, 0, 5, H], fill=acc)

    # icon circle
    cx, cy, r = 52, H//2, 30
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=acc)
    f_icon = try_font(28)
    ib = draw.textbbox((0,0), icon_char, font=f_icon)
    iw, ih = ib[2]-ib[0], ib[3]-ib[1]
    draw.text((cx - iw//2, cy - ih//2 - 2), icon_char, font=f_icon, fill=(255,255,255))

    # title
    f_title = try_font(32)
    f_sub   = try_font_regular(19)
    f_tag   = try_font_regular(16)

    draw.text((100, 30), title, font=f_title, fill=(255,255,255))
    draw.text((100, 74), subtitle, font=f_sub, fill=hex_to_rgb("#94A3B8"))

    # tags
    tx = 100
    ty = 130
    pad = 10
    for tag in stack_tags:
        tb = draw.textbbox((0,0), tag, font=f_tag)
        tw = tb[2] - tb[0] + pad*2
        th = tb[3] - tb[1] + 6
        rounded_rect(draw, [tx, ty, tx+tw, ty+th], 6, hex_to_rgb("#1E3A5F"))
        draw.text((tx+pad, ty+3), tag, font=f_tag, fill=acc)
        tx += tw + 10
        if tx > W - 150:
            break

    img.save(os.path.join(OUTPUT, filename))
    print(f"{filename} saved")

# ── Skills flowchart ─────────────────────────────────────────────────────────
def make_skills_chart():
    W, H = 1100, 420
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    draw_gradient(draw, W, H, hex_to_rgb("#0B1020"), hex_to_rgb("#0F172A"))

    f_cat  = try_font(20)
    f_item = try_font_regular(15)
    f_head = try_font(15)

    categories = [
        ("Languages",    "#38BDF8", ["Python","TypeScript","C++","Java","SQL","R","Solidity"]),
        ("Frontend",     "#22C55E", ["React","Next.js","Tailwind","Vite","Three.js","Framer"]),
        ("Backend",      "#F97316", ["Node.js","Flask","FastAPI","Django","Express","NestJS"]),
        ("AI / ML",      "#A78BFA", ["TensorFlow","PyTorch","scikit-learn","OpenCV","LangChain"]),
        ("Data & Cloud", "#FB923C", ["PostgreSQL","MongoDB","AWS","Supabase","Firebase","Prisma"]),
        ("Web3",         "#34D399", ["Solidity","IPFS","Web3.js","Ethereum","WebAuthn","ZK"]),
    ]

    col_w = W // len(categories)
    box_h = 300
    box_top = 80

    draw.text((W//2 - 120, 20), "Skills & Technologies", font=try_font(28), fill=(255,255,255))

    for i, (cat, color, items) in enumerate(categories):
        x = i * col_w + 14
        acc = hex_to_rgb(color)

        # column header box
        rounded_rect(draw, [x, box_top, x + col_w - 20, box_top + 38], 8, acc)
        cb = draw.textbbox((0,0), cat, font=f_cat)
        cw = cb[2] - cb[0]
        draw.text((x + (col_w - 20 - cw)//2, box_top + 8), cat, font=f_cat, fill=(10,16,32))

        # items
        for j, item in enumerate(items):
            iy = box_top + 52 + j * 34
            if iy + 28 > box_top + box_h:
                break
            rounded_rect(draw, [x, iy, x + col_w - 20, iy + 26], 6, hex_to_rgb("#1E293B"))
            draw.rectangle([x, iy, x+3, iy+26], fill=acc)
            draw.text((x + 10, iy + 5), item, font=f_item, fill=(200,210,225))

    img.save(os.path.join(OUTPUT, "skills_chart.png"))
    print("skills_chart.png saved")

make_banner()
make_project_card(
    "project_ssi.png",
    "NeuralHash SSI",
    "Self-sovereign identity — Ethereum, IPFS, Gemini OCR, WebAuthn, Merkle proofs",
    ["Solidity", "TypeScript", "IPFS", "Gemini API", "WebAuthn", "Ethereum"],
    "#38BDF8", "ID"
)
make_project_card(
    "project_covid.png",
    "COVID DBMS",
    "Public-health platform — React, Flask REST API, PostgreSQL, JWT auth, prediction endpoints",
    ["React", "TypeScript", "Flask", "PostgreSQL", "Supabase", "JWT"],
    "#22C55E", "DB"
)
make_project_card(
    "project_adi.png",
    "Adaptive Dump Intelligence",
    "Smart waste-site monitoring — adaptive analytics, data-driven decision support, sustainability",
    ["TypeScript", "ML", "Data Analytics", "IoT", "Dashboard"],
    "#F97316", "AI"
)
make_skills_chart()

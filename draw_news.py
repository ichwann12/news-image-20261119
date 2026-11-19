#!/usr/bin/env python3
"""Draw the news-image-20261119 entry: a newspaper front page summing up
the world's news of Thursday 19 November 2026.

Renders a 1024x1024 PNG with Pillow. All facts come from the verified
brief for this competition; nothing is invented.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 40
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

NAVY = (20, 33, 61)
RED = (193, 18, 31)
HERO_RED = (155, 27, 48)
INK = (31, 41, 55)
BODY = (55, 65, 81)
RULE = (209, 213, 219)
LIGHT_GREY = (243, 244, 246)
WHITE = (255, 255, 255)


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def wrap(draw, text, fnt, max_width):
    """Wrap text into lines that fit max_width pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, line_h):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += line_h
    return y


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)

    # --- Masthead ---
    d.rectangle([0, 0, W, 92], fill=NAVY)
    f_mast = font("DejaVuSans-Bold.ttf", 54)
    mast = "THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(mast, font=f_mast)) / 2, 16),
           mast, font=f_mast, fill=WHITE)

    # --- Date strip ---
    d.rectangle([0, 92, W, 140], fill=RED)
    f_date = font("DejaVuSans-Bold.ttf", 30)
    date = "THURSDAY  19  NOVEMBER  2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 100),
           date, font=f_date, fill=WHITE)

    # --- Hero: trilateral ---
    y = 154
    f_tag = font("DejaVuSans-Bold.ttf", 20)
    tag = " BREAKING "
    tw = d.textlength(tag, font=f_tag)
    d.rectangle([MARGIN, y, MARGIN + tw + 16, y + 32], fill=RED)
    d.text((MARGIN + 8, y + 4), tag, font=f_tag, fill=WHITE)
    y += 42
    f_hero = font("DejaVuSans-Bold.ttf", 56)
    hero = "TRUMP MEETS XI AND PUTIN"
    d.text((MARGIN, y), hero, font=f_hero, fill=HERO_RED)
    y += 70
    f_body = font("DejaVuSans.ttf", 20)
    hero_body = (
        "An unprecedented trilateral in Shenzhen brings together the leaders "
        "of the world's three largest nuclear powers. Trump presses nuclear "
        "arms control; Beijing resists making it the centrepiece. Xi greeted "
        "Trump at the airport; Trump and Putin shared only a brief handshake."
    )
    y = draw_lines(d, MARGIN, y,
                   wrap(d, hero_body, f_body, W - 2 * MARGIN),
                   f_body, BODY, 28)
    y += 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 16

    # --- Two-column story grid (2 x 2) ---
    col_w = (W - 2 * MARGIN - 36) // 2
    x_left, x_right = MARGIN, MARGIN + col_w + 36
    f_head = font("DejaVuSans-Bold.ttf", 25)
    f_story = font("DejaVuSans.ttf", 19)

    stories = [
        ("KERCH BRIDGE AFTERMATH", (15, 118, 110),
         "The destroyed roadway blocks the Kerch-Yenikale channel; a "
         "270-metre span and an arch collapsed into the strait. Russia hit "
         "Kyiv's bridges overnight \u2014 parts of the city without power "
         "and water. Two killed, all traffic suspended."),
        ("US-IRAN FIRE EXCHANGE", (185, 28, 28),
         "US and Iran traded fire across the Gulf again: the US struck a "
         "missile site on Qeshm Island; Iran widened attacks to a US base "
         "in Kuwait and Bahrain. Ships in the Strait of Hormuz were also "
         "attacked; the US raised its carrier deployment to three."),
        ("FRANCE CONFIRMS TROOPS IN UKRAINE", (109, 40, 217),
         "France confirmed it periodically sends military personnel into "
         "Ukraine for training and maintenance of weaponry. Russia "
         "responded forcefully."),
        ("ISRAELI TANKS CROSS GAZA LINE", (194, 65, 12),
         "Israeli tanks crossed the Gaza ceasefire line, in a new breach "
         "reported live as the truce strains."),
    ]

    def story_block(x, top, title, accent, body):
        tx = x + 18
        text_w = col_w - 18
        title_lines = wrap(d, title, f_head, text_w)
        body_lines = wrap(d, body, f_story, text_w)
        block_h = (len(title_lines) * 29 + 8
                   + len(body_lines) * 26)
        d.rectangle([x, top + 4, x + 7, top + block_h - 6], fill=accent)
        ty = draw_lines(d, tx, top, title_lines, f_head, INK, 29)
        draw_lines(d, tx, ty + 8, body_lines, f_story, BODY, 26)
        return top + block_h

    row1_end = max(
        story_block(x_left, y, stories[0][0], stories[0][1], stories[0][2]),
        story_block(x_right, y, stories[1][0], stories[1][1], stories[1][2]),
    )
    y = row1_end + 10
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=1)
    y += 14
    row2_end = max(
        story_block(x_left, y, stories[2][0], stories[2][1], stories[2][2]),
        story_block(x_right, y, stories[3][0], stories[3][1], stories[3][2]),
    )
    y = row2_end + 12
    d.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=2)
    y += 14

    # --- Full-width story: Berlin ---
    f_head2 = font("DejaVuSans-Bold.ttf", 25)
    berlin_title = "COALITION OF THE WILLING MEETS IN BERLIN"
    berlin_body = (
        "Allies meet in Berlin to discuss burden-sharing and the cost of "
        "military aid. NATO chief Rutte says continued military aid to "
        "Ukraine is essential \u2014 including strikes on logistical nodes."
    )
    berlin_lines = wrap(d, berlin_body, f_story, W - 2 * MARGIN - 18)
    d.rectangle([MARGIN, y + 4, MARGIN + 7, y + 29 + 8 + len(berlin_lines) * 26],
                fill=(21, 128, 61))
    d.text((MARGIN + 18, y), berlin_title, font=f_head2, fill=INK)
    y = draw_lines(d, MARGIN + 18, y + 37, berlin_lines, f_story, BODY, 26)
    y += 12

    # --- Also today strip ---
    strip_h = 92
    d.rectangle([0, y, W, y + strip_h], fill=LIGHT_GREY)
    f_also = font("DejaVuSans-Bold.ttf", 20)
    d.text((MARGIN, y + 8), "ALSO TODAY", font=f_also, fill=INK)
    also = (
        "Trump departs Shenzhen for Washington after the summit  \u00b7  "
        "White House: Ukraine not expected to be raised at the trilateral  "
        "\u00b7  Tensions over reports of Nvidia chips diverted to China "
        "via Southeast Asia"
    )
    draw_lines(d, MARGIN, y + 36,
               wrap(d, also, font("DejaVuSans.ttf", 18), W - 2 * MARGIN),
               font("DejaVuSans.ttf", 18), BODY, 24)
    y += strip_h + 10

    # --- Footer ---
    f_foot = font("DejaVuSans.ttf", 17)
    foot = "Sources: Reuters  \u00b7  AP  \u00b7  AFP"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, H - 28),
           foot, font=f_foot, fill=BODY)

    img.save("entry.png", "PNG")
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()

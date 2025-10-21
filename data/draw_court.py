import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Rectangle, Arc


WOOD_LIGHT = '#f7d7aa'
WOOD_DARK = '#ebc68f'
LINE_COLOR = '#0f172a'
TEAM_ACCENT = '#17408b'  # classic NBA blue accent
PAINT_FILL = '#f5f0e6'
RESTRICTED_FILL = '#fcd34d'
CENTER_FILL = '#fef9c3'
FREE_THROW_DASH = (0, (6, 6))


def draw_court(ax=None, color=LINE_COLOR, lw=1.6, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    # parquet-style background
    for idx, x in enumerate(range(-250, 250, 20)):
        stripe_color = WOOD_LIGHT if idx % 2 == 0 else WOOD_DARK
        plank = Rectangle((x, -47.5), 20, 470, linewidth=0, color=stripe_color, zorder=0)
        ax.add_patch(plank)

    hoop = Circle((0, 0), radius=7.5, linewidth=lw, edgecolor=color, facecolor='none', zorder=5)
    hoop_pad = Circle((0, -5), radius=12, linewidth=0, facecolor=color, alpha=0.25, zorder=4)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, edgecolor=color, facecolor=color, zorder=5)

    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, edgecolor=TEAM_ACCENT, facecolor='none', zorder=3)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, edgecolor=TEAM_ACCENT, facecolor=PAINT_FILL, zorder=2)

    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, edgecolor=TEAM_ACCENT, fill=False, zorder=4)
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, edgecolor=TEAM_ACCENT, linestyle='dashed', zorder=4)

    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, edgecolor=TEAM_ACCENT, zorder=5)
    restricted_fill = Circle((0, 0), radius=40, linewidth=0, facecolor=RESTRICTED_FILL, alpha=0.85, zorder=3)

    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, edgecolor=TEAM_ACCENT, facecolor=TEAM_ACCENT, zorder=4)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, edgecolor=TEAM_ACCENT, facecolor=TEAM_ACCENT, zorder=4)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, edgecolor=TEAM_ACCENT, zorder=4)

    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, edgecolor=TEAM_ACCENT, zorder=4)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, edgecolor=TEAM_ACCENT, zorder=4)
    center_circle = Circle((0, 422.5), radius=60, linewidth=0, facecolor=CENTER_FILL, alpha=0.85, zorder=2)

    free_throw_circle = Circle((0, 142.5), radius=60, linewidth=lw, edgecolor=TEAM_ACCENT, facecolor='none', linestyle=FREE_THROW_DASH, zorder=4)
    lane_hash_left = Line2D([-80, -60], [20, 20], linewidth=lw, color=TEAM_ACCENT, zorder=4)
    lane_hash_right = Line2D([60, 80], [20, 20], linewidth=lw, color=TEAM_ACCENT, zorder=4)
    halfcourt_line = Line2D([-250, 250], [422.5, 422.5], linewidth=lw, color=TEAM_ACCENT, zorder=4)

    court_elements = [
        inner_box, restricted_fill, center_circle,
        free_throw_circle,
        hoop_pad, hoop, backboard, outer_box, top_free_throw, bottom_free_throw,
        restricted, corner_three_a, corner_three_b, three_arc,
        center_outer_arc, center_inner_arc
    ]

    if outer_lines:
        outline = Rectangle((-250, -47.5), 500, 470, linewidth=lw, edgecolor=color, facecolor='none', zorder=4)
        court_elements.append(outline)

    for element in court_elements:
        ax.add_patch(element)

    ax.add_line(lane_hash_left)
    ax.add_line(lane_hash_right)
    ax.add_line(halfcourt_line)

    return ax


def main():
    # Targeting a 500x470px image (matches Vega-Lite width/height) for crisp mapping
    dpi = 100
    fig_w, fig_h = 5.0, 4.7  # inches
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = fig.add_subplot(111)

    # Draw court with darker lines for visibility
    draw_court(ax=ax, color=LINE_COLOR, lw=1.6, outer_lines=True)

    # Half-court extents used by the Vega-Lite spec
    ax.set_xlim(-250, 250)
    ax.set_ylim(-47.5, 422.5)
    ax.set_aspect('equal')
    ax.axis('off')

    # Remove margins so the image fits the exact data extents
    fig.subplots_adjust(0, 0, 1, 1)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')

    out_path = 'court.png'
    fig.savefig(out_path, dpi=dpi, bbox_inches='tight', pad_inches=0)
    print(f"✅ Saved court image to {out_path}")


if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Arc


def draw_court(ax=None, color='#475569', lw=1.6, outer_lines=False):
    if ax is None:
        ax = plt.gca()

    hoop = Circle((0, 0), radius=7.5, linewidth=lw, color=color, fill=False)
    backboard = Rectangle((-30, -7.5), 60, -1, linewidth=lw, color=color)

    outer_box = Rectangle((-80, -47.5), 160, 190, linewidth=lw, color=color, fill=False)
    inner_box = Rectangle((-60, -47.5), 120, 190, linewidth=lw, color=color, fill=False)

    top_free_throw = Arc((0, 142.5), 120, 120, theta1=0, theta2=180, linewidth=lw, color=color, fill=False)
    bottom_free_throw = Arc((0, 142.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color, linestyle='dashed')

    restricted = Arc((0, 0), 80, 80, theta1=0, theta2=180, linewidth=lw, color=color)

    corner_three_a = Rectangle((-220, -47.5), 0, 140, linewidth=lw, color=color)
    corner_three_b = Rectangle((220, -47.5), 0, 140, linewidth=lw, color=color)
    three_arc = Arc((0, 0), 475, 475, theta1=22, theta2=158, linewidth=lw, color=color)

    center_outer_arc = Arc((0, 422.5), 120, 120, theta1=180, theta2=0, linewidth=lw, color=color)
    center_inner_arc = Arc((0, 422.5), 40, 40, theta1=180, theta2=0, linewidth=lw, color=color)

    court_elements = [
        hoop, backboard, outer_box, inner_box, top_free_throw, bottom_free_throw,
        restricted, corner_three_a, corner_three_b, three_arc, center_outer_arc, center_inner_arc
    ]

    if outer_lines:
        outline = Rectangle((-250, -47.5), 500, 470, linewidth=lw, color=color, fill=False)
        court_elements.append(outline)

    for element in court_elements:
        ax.add_patch(element)

    return ax


def main():
    # Targeting a 500x470px image (matches Vega-Lite width/height) for crisp mapping
    dpi = 100
    fig_w, fig_h = 5.0, 4.7  # inches
    fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
    ax = fig.add_subplot(111)

    # Draw court with darker lines for visibility
    draw_court(ax=ax, color="#475569", lw=1.6, outer_lines=True)

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

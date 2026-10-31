"""영문 그림 생성: figures/fig1_en.png (상태도), figures/fig2_en.png (개념도)

사용법: python3 build/figures.py   (matplotlib 필요)
Fig. 1의 선 굵기·모양은 Table 3의 칸 값을 따른다: 굵은 실선 = 큰 확률(●), 가는 파선 = 작지만 0이 아닌 확률(○).
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["mathtext.fontset"] = "dejavusans"

NAVY, GREEN, RED, GREY = "#2c3e50", "#3b5e2b", "#b03a2e", "#7f7f7f"


def box(ax, x, y, w, h, text, ec=NAVY, fc="#f7f9fb", ls="-", fs=10, lw=1.4):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                ec=ec, fc=fc, lw=lw, ls=ls))
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color="black", linespacing=1.25)


def arrow(ax, p, q, color=NAVY, lw=2.2, ls="-", rad=0.0, ms=14):
    ax.add_patch(FancyArrowPatch(p, q, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                                 mutation_scale=ms, lw=lw, ls=ls, color=color, shrinkA=2, shrinkB=2))


def fig1():
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    # regime panels
    ax.add_patch(FancyBboxPatch((0.15, 2.55), 10.7, 1.85, boxstyle="round,pad=0.02,rounding_size=0.15",
                                ec="#9fb0c2", fc="#eaf0f6", lw=1.2))
    ax.text(5.5, 4.18, "Existing regime $R_0$ (weakening resilience)", ha="center", fontsize=11, color=NAVY)
    ax.add_patch(FancyBboxPatch((4.0, 0.15), 6.85, 1.75, boxstyle="round,pad=0.02,rounding_size=0.15",
                                ec="#a8c49a", fc="#eef5ea", lw=1.2))
    ax.text(7.4, 0.3, "New regime $R_1$ (recovering resilience)", ha="center", fontsize=11, color=GREEN)

    w, h, y = 1.75, 0.78, 3.3
    xs = {"B": 1.1, "S0": 3.3, "S1": 5.5, "S2": 7.7, "S3": 9.9}
    labels = {"B": "B\nBaseline stability", "S0": "S0\nPre-contention", "S1": "S1\nContention",
              "S2": "S2\nBoundary", "S3": "S3\nThreshold"}
    for k, x in xs.items():
        box(ax, x, y, w, h, labels[k])
    order = ["B", "S0", "S1", "S2", "S3"]
    for a, b in zip(order, order[1:]):
        # forward (●) above, backward (●) below — both large in Table 3
        arrow(ax, (xs[a] + w / 2, y + 0.15), (xs[b] - w / 2, y + 0.15), lw=2.4, rad=-0.25)
        arrow(ax, (xs[b] - w / 2, y - 0.15), (xs[a] + w / 2, y - 0.15), lw=2.4, rad=-0.25)
    ax.text(2.1, 3.83, "forward", fontsize=8, ha="center", color=NAVY)
    ax.text(2.1, 2.74, "resolution / retreat", fontsize=8, ha="center", color=NAVY)

    yn = 1.05
    xn = {"N": 5.45, "S4": 7.85, "S0p": 9.95}
    box(ax, xn["N"], yn, 2.2, h, "N\nPost-transition\ninstability", ec=GREEN)
    box(ax, xn["S4"], yn, 1.75, h, "S4\nReconfiguration", ec=GREEN)
    box(ax, xn["S0p"], yn, 1.6, h, "S0′\nNew contention\nbased on $R_1$", ec=GREEN, ls="--", fs=9)
    arrow(ax, (xn["N"] + 1.1, yn), (xn["S4"] - 0.875, yn), color=GREEN, lw=2.4)
    arrow(ax, (xn["S4"] + 0.875, yn), (xn["S0p"] - 0.8, yn), color=GREEN, lw=1.2, ls="--")
    ax.text(8.95, 1.45, "re-entry", fontsize=8, ha="center", color=GREEN)

    # E1 regime transition: S3 -> N (●), S2 -> N (○)
    arrow(ax, (xs["S3"] - 0.3, y - h / 2), (xn["N"] + 0.6, yn + h / 2), color=RED, lw=3.4, ms=18)
    ax.text(8.95, 2.2, "E1 regime transition\n(abrupt / gradual)", fontsize=9.5, color=RED, ha="left")
    arrow(ax, (xs["S2"] - 0.2, y - h / 2), (xn["N"] + 0.2, yn + h / 2), color=RED, lw=1.2, ls="--")
    ax.text(6.7, 2.05, "leap (○)", fontsize=8.5, color=RED, ha="center")
    # failure and return N -> R0 (example: to S1)
    arrow(ax, (xn["N"] - 0.5, yn + h / 2), (xs["S1"] - 0.5, y - h / 2), color=GREY, lw=1.2, ls=":")
    ax.text(3.3, 2.0, "failure and return\n(N → $R_0$; target phase\nnot fixed)", fontsize=8, color=GREY, ha="center")

    # legend
    lx, ly = 0.35, 1.55
    ax.plot([lx, lx + 0.5], [ly, ly], color=NAVY, lw=2.4)
    ax.text(lx + 0.6, ly, "large probability (●)", va="center", fontsize=8.5)
    ax.plot([lx, lx + 0.5], [ly - 0.35, ly - 0.35], color=NAVY, lw=1.2, ls="--")
    ax.text(lx + 0.6, ly - 0.35, "small but nonzero (○)", va="center", fontsize=8.5)
    ax.plot([lx, lx + 0.5], [ly - 0.7, ly - 0.7], color=GREY, lw=1.2, ls=":")
    ax.text(lx + 0.6, ly - 0.7, "return to $R_0$", va="center", fontsize=8.5)
    fig.savefig(ROOT / "figures" / "fig1_en.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    # phases in R0
    ax.add_patch(FancyBboxPatch((0.15, 4.0), 6.55, 1.05, boxstyle="round,pad=0.02,rounding_size=0.12",
                                ec="#9fb0c2", fc="white", lw=1.0))
    ax.text(3.42, 4.85, "Phases within existing regime $R_0$ (phase-specific transition probabilities)",
            ha="center", fontsize=9, color=NAVY)
    px = [0.95, 2.55, 4.15, 5.75]
    pt = ["Misfit accumulates\nB → S0", "Contention active\nS1", "Resilience weakens\nS2", "Threshold conditions\nS3"]
    for x, s in zip(px, pt):
        box(ax, x, 4.35, 1.45, 0.55, s, fs=7.5)
    for a, b in zip(px, px[1:]):
        arrow(ax, (a + 0.725, 4.35), (b - 0.725, 4.35), lw=1.4, ms=10)

    # drivers
    ax.add_patch(FancyBboxPatch((2.25, 2.45), 6.75, 1.2, boxstyle="round,pad=0.02,rounding_size=0.12",
                                ec="#9fb0c2", fc="white", lw=1.0))
    ax.text(5.62, 3.47, "Drivers of transition risk (measured independently)", ha="center", fontsize=9, color=NAVY)
    dx = [3.1, 4.75, 6.4, 8.05]
    dt = ["Maintenance cost $C_m$\nrework, delay,\nrole conflict", "Transition cost $C_t$\nlearning, loss,\nuncertainty",
          "Inertia $\\alpha$\ncusp splitting\nfactor", "Trigger × readiness\napproval, training,\nminor events"]
    for x, s in zip(dx, dt):
        box(ax, x, 2.9, 1.55, 0.75, s, fs=7.5)
    box(ax, 10.2, 2.9, 1.55, 0.75, "Higher-level context\nteam/organization\nprocedures, authority,\nresources", ec=GREY, ls="--", fs=7.5)
    arrow(ax, (9.42, 3.1), (9.0, 3.1), color=GREY, lw=1.1, ls="--", ms=10)
    ax.text(10.2, 3.4, "forced transition", fontsize=7, color=GREY, ha="center")

    # hazard
    box(ax, 5.5, 1.55, 4.3, 0.62,
        "Transition hazard $h(t)$\nlogit $h(t) = \\beta_0(t) + \\beta_1 \\ln C_m + \\beta_2 \\ln C_t + \\beta_3 \\ln \\alpha$",
        ec=RED, fc="#fdf2e6", fs=8.5)
    signs = ["+", "−", "−", "+ (steeper in S3)"]
    for x, s in zip(dx, signs):
        arrow(ax, (x, 2.52), (5.5 + (x - 5.5) * 0.45, 1.88), lw=1.1, ms=9)
        ax.text(x + (0.12 if s != "+ (steeper in S3)" else -0.1), 2.25 if s != "+ (steeper in S3)" else 1.98, s, fontsize=8, color=NAVY)
    # readiness condition from S3: routed around the right side of the driver panel
    ax.plot([6.53, 9.25, 9.25], [4.35, 4.35, 1.55], color=RED, lw=1.3)
    arrow(ax, (9.25, 1.55), (7.68, 1.55), color=RED, lw=1.3, ms=10)
    ax.text(7.9, 4.45, "readiness condition (from S3)", fontsize=7.5, color=RED, ha="center")

    # after transition
    yb = 0.4
    box(ax, 1.5, yb, 2.5, 0.55, "E1 regime transition\nbehavior, role, structure, relation", ec=RED, fc="#fbe9e7", fs=7.8)
    box(ax, 4.2, yb, 2.3, 0.55, "N instability\ndual operation, learning load", ec=NAVY, fs=7.8)
    box(ax, 6.9, yb, 2.4, 0.55, "S4 reconfiguration\nrepetition, alignment, resilience", ec=NAVY, fs=7.8)
    box(ax, 9.6, yb, 2.2, 0.55, "Separate outcomes\nperformance, desirability,\nburnout, turnover", ec=GREY, ls="--", fs=7.5)
    arrow(ax, (3.35, 1.3), (1.9, yb + 0.29), color=RED, lw=2.2, ms=12)
    arrow(ax, (2.75, yb), (3.05, yb), lw=1.4, ms=10)
    arrow(ax, (5.35, yb), (5.7, yb), lw=1.4, ms=10)
    arrow(ax, (8.1, yb), (8.5, yb), color=GREY, lw=1.1, ls="--", ms=10)
    fig.savefig(ROOT / "figures" / "fig2_en.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    print("ok")

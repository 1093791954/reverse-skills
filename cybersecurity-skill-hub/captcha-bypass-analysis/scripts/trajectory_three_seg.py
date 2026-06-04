"""
trajectory_three_seg.py - 三段式（加速 - 匀速 - 减速）鼠标轨迹（教学 demo）
========================================================================
配套 SKILL.md Path 4。

阶段 1（30%~40%）：a₁ ∈ [800, 1500] px/s²
阶段 2（20%~30%）：恒速 ~600 px/s
阶段 3（30%~40%）：a₂ ∈ [-1000, -1800] px/s²
末端可选过冲。
"""

import random
from typing import List, Tuple


def three_segment_trajectory(
    distance: float,
    dt_ms: int = 16,
) -> List[Tuple[float, float, int]]:
    """
    返回 [(x, y, t_ms)] 列表（y 为微抖动，主要 X 方向运动）。
    """
    # 阶段比例
    seg1_ratio = random.uniform(0.30, 0.40)
    seg3_ratio = random.uniform(0.30, 0.40)
    seg2_ratio = 1 - seg1_ratio - seg3_ratio

    seg1_dist = distance * seg1_ratio
    seg2_dist = distance * seg2_ratio
    seg3_dist = distance * seg3_ratio

    a1 = random.uniform(800, 1500)
    v_cruise = random.uniform(500, 700)
    a3 = -random.uniform(1000, 1800)

    pts = []
    x, t_ms = 0.0, 0
    v = 0.0

    # 阶段 1：加速
    while x < seg1_dist:
        dt = dt_ms + random.randint(-3, 3)
        v += a1 * (dt / 1000)
        x += v * (dt / 1000)
        t_ms += dt
        pts.append((x, random.gauss(0, 0.8), t_ms))
        if v >= v_cruise:
            v = v_cruise
            break

    # 阶段 2：匀速
    target2 = seg1_dist + seg2_dist
    while x < target2:
        dt = dt_ms + random.randint(-3, 3)
        x += v_cruise * (dt / 1000)
        t_ms += dt
        pts.append((x, random.gauss(0, 0.8), t_ms))

    # 阶段 3：减速
    while x < distance and v > 0:
        dt = dt_ms + random.randint(-3, 3)
        v += a3 * (dt / 1000)
        if v < 0:
            v = 0
        x += v * (dt / 1000)
        t_ms += dt
        pts.append((x, random.gauss(0, 0.8), t_ms))

    return pts


if __name__ == "__main__":
    traj = three_segment_trajectory(distance=200.0)
    print(f"共 {len(traj)} 点 / 总耗时 {traj[-1][2]} ms")
    for x, y, t in traj[::5]:
        print(f"{t:>5d}ms  ({x:>6.2f}, {y:>5.2f})")

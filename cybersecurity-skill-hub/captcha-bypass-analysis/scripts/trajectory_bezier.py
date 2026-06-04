"""
trajectory_bezier.py - 贝塞尔曲线鼠标轨迹（教学 demo）
====================================================
配套 SKILL.md Path 4。

依赖：仅 numpy
"""

import numpy as np
import random
from typing import List, Tuple


def bezier_trajectory(
    start: Tuple[float, float],
    end: Tuple[float, float],
    n_points: int = 60,
    jitter: float = 8.0,
) -> List[Tuple[float, float, int]]:
    """
    生成从 start 到 end 的三阶贝塞尔轨迹。
    返回 [(x, y, t_ms), ...]，t_ms 为相对起点的毫秒时间戳。

    控制点策略：
        P0 = start
        P1 = start + 25%~40% 距离 + Y 方向随机扰动
        P2 = end - 15%~25% 距离 + Y 方向随机扰动
        P3 = end
    时间间隔 ~16ms ± 5ms（模拟 60fps 抖动）。
    """
    sx, sy = start
    ex, ey = end
    dx, dy = ex - sx, ey - sy
    dist = (dx ** 2 + dy ** 2) ** 0.5

    # 随机控制点
    p1 = (sx + dx * random.uniform(0.25, 0.4),
          sy + dy * random.uniform(0.25, 0.4) + random.uniform(-jitter, jitter))
    p2 = (ex - dx * random.uniform(0.15, 0.25),
          ey - dy * random.uniform(0.15, 0.25) + random.uniform(-jitter, jitter))

    pts = []
    t_ms = 0
    for i in range(n_points):
        t = i / (n_points - 1)
        # 三阶贝塞尔：B(t) = (1-t)^3 P0 + 3(1-t)^2 t P1 + 3(1-t) t^2 P2 + t^3 P3
        b = (1 - t) ** 3
        c = 3 * (1 - t) ** 2 * t
        d = 3 * (1 - t) * t ** 2
        e = t ** 3
        x = b * sx + c * p1[0] + d * p2[0] + e * ex
        y = b * sy + c * p1[1] + d * p2[1] + e * ey
        # 微抖动 + 时间戳不等距
        x += random.gauss(0, 0.5)
        y += random.gauss(0, 0.5)
        t_ms += int(random.gauss(16, 3))
        pts.append((x, y, t_ms))
    return pts


def add_overshoot(pts, overshoot_px: int = 10) -> list:
    """模拟"过冲再回退"：末端先冲过去 overshoot_px，再两点拉回。"""
    last_x, last_y, last_t = pts[-1]
    direction = 1 if pts[-1][0] > pts[0][0] else -1
    pts.append((last_x + direction * overshoot_px, last_y + random.gauss(0, 1), last_t + 22))
    pts.append((last_x + direction * overshoot_px / 2, last_y, last_t + 45))
    pts.append((last_x, last_y, last_t + 75))
    return pts


if __name__ == "__main__":
    # 模拟"从 (50, 200) 滑动到 (250, 200) 的滑块轨迹"
    traj = bezier_trajectory((50, 200), (250, 200), n_points=50)
    traj = add_overshoot(traj, overshoot_px=8)
    for x, y, t in traj:
        print(f"{t:>5d}ms  ({x:>6.1f}, {y:>6.1f})")

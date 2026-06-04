"""
opencv_slider_gap.py - 滑块缺口距离识别（教学用 demo）
======================================================

合规边界：本脚本仅作为 OpenCV 模板匹配教学示例，与 D:\\tmp\\SKILLS\\captcha-bypass-analysis\\SKILL.md
Path 3 配套。**不**针对任何商业风控产品做生产级 bypass。

依赖：
    pip install opencv-python numpy

输入：
    bg_path  — 背景大图（含缺口）
    tile_path — 滑块小图（凸出形状，通常带 alpha 通道）

输出：
    缺口起点的 x 坐标（px）

算法：
    1. 读图，灰度化
    2. Canny 边缘
    3. cv2.matchTemplate(method=TM_CCOEFF_NORMED)
    4. minMaxLoc 找最大相关位置，返回 x 坐标
"""

import cv2
import numpy as np
import sys


def find_gap_x(bg_path: str, tile_path: str, debug: bool = False) -> int:
    """返回缺口的 x 坐标（相对背景大图左上角的 px）。"""
    bg = cv2.imread(bg_path)
    tile = cv2.imread(tile_path, cv2.IMREAD_UNCHANGED)
    if bg is None or tile is None:
        raise FileNotFoundError(f"读图失败：bg={bg_path} tile={tile_path}")

    # 1. 处理 tile 的 alpha 通道：用 alpha 当 mask，避免 padding 干扰相关性
    if tile.shape[2] == 4:
        alpha = tile[:, :, 3]
        tile_rgb = tile[:, :, :3]
        # 仅保留非透明像素的边缘
        tile_gray = cv2.cvtColor(tile_rgb, cv2.COLOR_BGR2GRAY)
        tile_gray = cv2.bitwise_and(tile_gray, tile_gray, mask=alpha)
    else:
        tile_gray = cv2.cvtColor(tile, cv2.COLOR_BGR2GRAY)

    bg_gray = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)

    # 2. Canny 边缘（缺口与滑块都是边缘形状信息）
    bg_edge = cv2.Canny(bg_gray, 100, 200)
    tile_edge = cv2.Canny(tile_gray, 100, 200)

    # 3. 模板匹配
    res = cv2.matchTemplate(bg_edge, tile_edge, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    x = max_loc[0]

    if debug:
        h, w = tile_edge.shape
        cv2.rectangle(bg, (x, max_loc[1]), (x + w, max_loc[1] + h), (0, 0, 255), 2)
        cv2.imwrite("_debug_match.png", bg)
        print(f"[debug] 相关度={max_val:.3f} x={x}")

    return x


# 进阶：Sobel 梯度（应对 Canny 把图块和缺口都"边缘化"导致的伪相关）
def find_gap_x_sobel(bg_path: str, tile_path: str) -> int:
    bg = cv2.imread(bg_path, cv2.IMREAD_GRAYSCALE)
    tile = cv2.imread(tile_path, cv2.IMREAD_GRAYSCALE)
    bg_sx = cv2.Sobel(bg, cv2.CV_32F, 1, 0)
    tile_sx = cv2.Sobel(tile, cv2.CV_32F, 1, 0)
    res = cv2.matchTemplate(bg_sx, tile_sx, cv2.TM_CCOEFF_NORMED)
    _, _, _, max_loc = cv2.minMaxLoc(res)
    return max_loc[0]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python opencv_slider_gap.py <bg.png> <tile.png>")
        sys.exit(1)
    x = find_gap_x(sys.argv[1], sys.argv[2], debug=True)
    print(f"缺口 x 坐标 = {x} px")

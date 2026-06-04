"""
ddddocr_demo.py - ddddocr 调用示例（教学 demo）
==============================================
配套 SKILL.md Path 3 / Path 5。

ddddocr 是一个开源的通用验证码识别库（github.com/sml2h3/ddddocr），
支持：纯文字 OCR、滑块距离识别、目标检测点选。

依赖：
    pip install ddddocr

合规边界：仅作 OCR 模型调用教学；不绑定任何具体目标站点。
"""

import ddddocr


def ocr_text(image_path: str) -> str:
    """识别图片验证码中的文字。"""
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(image_path, "rb") as f:
        return ocr.classification(f.read())


def slide_match_distance(bg_path: str, tile_path: str) -> int:
    """识别滑块缺口的 x 坐标。"""
    det = ddddocr.DdddOcr(det=False, ocr=False, show_ad=False)
    with open(bg_path, "rb") as fb, open(tile_path, "rb") as ft:
        res = det.slide_match(ft.read(), fb.read(), simple_target=True)
    # 返回 {'target_y': int, 'target': [x1, y1, x2, y2]}
    return res["target"][0]


def click_detect(image_path: str):
    """点选题目标检测：返回 [(x1,y1,x2,y2), ...]。"""
    det = ddddocr.DdddOcr(det=True, show_ad=False)
    with open(image_path, "rb") as f:
        return det.detection(f.read())


if __name__ == "__main__":
    print("=== 文字 OCR ===")
    # print(ocr_text("captcha.png"))
    print("=== 滑块距离 ===")
    # print(slide_match_distance("bg.png", "tile.png"))
    print("=== 点选检测 ===")
    # print(click_detect("click.png"))
    print("（取消注释并提供本地样本图片即可运行）")

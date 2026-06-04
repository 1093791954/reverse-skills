# 旋转还原 / 3D 旋转（Rotate Image / 3D Rotation）

## 1. 题型描述
- 经典 2D 旋转：一张被旋转一定角度的图，要求拖动滑块/旋转盘把图转回正向。
  - 代表：极验 v4 旋转、顶象旋转、网易易盾旋转、百度旋转。
- 3D 旋转：一个 3D 物体（动物/卡车/立方体），把方向调到指定方向。
  - 代表：FunCaptcha 3D rotation、Arkose roller。
- 立方体方向：选 6 个方向之一。

## 2. 检测维度
- 旋转角度精度（2D 容忍 ±5°）。
- 旋转过程的轨迹（不能瞬时跳到目标）。
- 提交参数加密。
- 指纹与行为（同样要补环境）。

## 3. 解题思路
**2D 旋转**：
- **图像方向回归（Regression）**：ResNet18/EfficientNet 输入图返回 0~360°；训练数据可从原始图生成（自监督，旋转任意角度做标签）。
- **矩阵正向 / 标杆**：图中如果有水平线/天空，可用 Hough 直线检测预估角度。
- **DeepRotate / RotNet**：开源 RotNet 项目，迁移训练即可。

**3D 旋转 / FunCaptcha**：
- 题目 game_data 是有限候选 image set（多为 5~10 帧）。
- 每帧角度对应 0~360 中的若干离散值。
- 等价于「N 选 1 分类」：训练 ResNet18 多头分类，输入候选 + 标签 → 输出 index。
- 立方体方向：6 类分类，CNN 即可。
- 卡车/动物方向：识别正面朝向（front/side/back），加上颜色/纹理可以更稳。

## 4. 已公开研究
- CSDN「FunCaptcha 旋转」相关文章（CSDN 全部 30 篇结果）。
- CSDN「探索未来验证码：Funcaptcha 的强大与便捷」(139404538)：题型综述。
- CSDN「快速定位 FunCaptcha sitekey 参数」(155098149)。
- CSDN「FunCaptcha 与其他验证码的技术对比分析」(155192657)。
- GitHub `noahcoolboy/funcaptcha-challenger`：题型分类 + ONNX。
- arxiv「Self-Supervised Image Rotation Recovery」论文。
- 极验 v4 旋转：CSDN/吾爱多篇逆向，配合 ResNet 角度回归。
- 网易易盾旋转题：CSDN 中文笔记若干。

## 5. 防御性分析步骤
1. 收集旋转题样本（合法授权）。
2. 标注：2D 用自监督（自旋转任意角度做标签）；3D 用题型分类标签。
3. 训练 + 评估 MAE（角度误差）/ Top-1 准确率。
4. 端到端联通：识别 → 拖滑块 → 提交。
5. 注意拖动轨迹要带"过冲 + 微调"。

## 6. 缓解 / 趋势
- 加干扰：背景纹理、阴影、模糊。
- 多帧候选：图像有微妙差异，分类难度上升。
- 噪声水印对抗 ResNet 训练。
- 3D 题图渲染随机化（光照、视角微扰）。

## 7. 待研究
- ViT vs ResNet 在小样本旋转回归任务上的优劣。
- FunCaptcha 各 game_variant 的题型 ID 完整列表。
- 自监督预训练（DINO）在旋转题上的迁移效果。

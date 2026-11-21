# -*- coding: utf-8 -*-
"""生成关键业务流程图 PNG：学生求职与岗位匹配主流程（跨学生端/数据支撑/高校管理端）。"""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 1660, 1150
img = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(img)

FB = "C:/Windows/Fonts/msyhbd.ttc"   # 微软雅黑 粗
FR = "C:/Windows/Fonts/msyh.ttc"     # 微软雅黑 常规
f_title = ImageFont.truetype(FB, 30)
f_sub = ImageFont.truetype(FR, 16)
f_lane = ImageFont.truetype(FB, 21)
f_node = ImageFont.truetype(FB, 17)
f_desc = ImageFont.truetype(FR, 13)
f_num = ImageFont.truetype(FB, 14)
f_foot = ImageFont.truetype(FR, 14)

NAVY = "#17324D"
GREY = "#5B6B7B"
LANE_BG = ["#EAF3FB", "#EDF7EF", "#FDF3E7"]
LANE_LINE = ["#B9D6EE", "#BFE3C6", "#F2D7AC"]
LANE_TITLE = ["#1F6FB2", "#2E8B4E", "#C67C1A"]
NODE_FILL = "#FFFFFF"

# ---------- 标题 ----------
d.text((W // 2, 34), "关键业务流程图 · 学生求职与岗位匹配主流程",
       font=f_title, fill=NAVY, anchor="mm")
d.text((W // 2, 70),
       "从学生发起测评到拿到岗位推荐与面试反馈的跨模块全过程",
       font=f_sub, fill=GREY, anchor="mm")

# ---------- 泳道 ----------
lanes = [(40, 560, "学生端"), (570, 1090, "数据支撑"), (1100, 1620, "高校管理端")]
lane_top, lane_bottom = 100, 1105
for i, (x0, x1, name) in enumerate(lanes):
    d.rounded_rectangle([x0, lane_top, x1, lane_bottom], radius=12,
                        fill=LANE_BG[i], outline=LANE_LINE[i], width=2)
    d.rounded_rectangle([x0, lane_top, x1, lane_top + 46], radius=12,
                        fill=LANE_TITLE[i])
    d.rectangle([x0, lane_top + 30, x1, lane_top + 46], fill=LANE_TITLE[i])
    d.text(((x0 + x1) // 2, lane_top + 23), name, font=f_lane,
           fill="white", anchor="mm")

CENTERS = [(l[0] + l[1]) // 2 for l in lanes]  # 300, 830, 1360
NW = 470   # 节点宽
NH = 84    # 节点高

# (泳道, 中心y, 编号, 标题, 描述)
steps = [
    (0, 205, 1, "学生发起求职", "完成职业测评 / 设定求职与成长目标"),
    (1, 325, 2, "生成能力画像", "汇集测评、课程、经历数据，输出技能画像"),
    (0, 445, 3, "导入并生成简历", "录入经历，系统校验字段，缺项提示补充"),
    (1, 565, 4, "岗位能力匹配", "岗位信息库＋技能标签库，计算岗位匹配度"),
    (0, 685, 5, "定制简历＋模拟面试", "一键生成针对性简历，语音面试获反馈"),
    (0, 805, 6, "检索筛选并投递", "按匹配结果检索、收藏、投递目标职位"),
    (2, 925, 7, "就业指导与帮扶", "老师查看画像与投递数据，定向帮扶困难生"),
    (0, 1045, 8, "拿到结果与反馈", "收到岗位推荐、面试反馈，回流能力画像"),
]

def node_box(lane, cy):
    cx = CENTERS[lane]
    return [cx - NW // 2, cy - NH // 2, cx + NW // 2, cy + NH // 2]

# ---------- 节点 ----------
for lane, cy, num, title, desc in steps:
    box = node_box(lane, cy)
    # 阴影
    d.rounded_rectangle([box[0]+3, box[1]+4, box[2]+3, box[3]+4], radius=10,
                        fill="#D9E1E8")
    d.rounded_rectangle(box, radius=10, fill=NODE_FILL,
                        outline=LANE_TITLE[lane], width=2)
    # 编号圆
    ncx, ncy = box[0] + 30, cy
    d.ellipse([ncx-16, ncy-16, ncx+16, ncy+16], fill=LANE_TITLE[lane])
    d.text((ncx, ncy), str(num), font=f_num, fill="white", anchor="mm")
    # 标题与描述
    d.text((box[0] + 60, cy - 14), title, font=f_node, fill=NAVY, anchor="lm")
    d.text((box[0] + 60, cy + 14), desc, font=f_desc, fill=GREY, anchor="lm")

# ---------- 箭头 ----------
def arrow(p1, p2, color="#37474F", width=3):
    x1, y1 = p1
    x2, y2 = p2
    d.line([x1, y1, x2, y2], fill=color, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    L = 13
    for a in (ang + 2.6, ang - 2.6):
        d.line([x2, y2, x2 + L * math.cos(a), y2 + L * math.sin(a)],
               fill=color, width=width)

for i in range(len(steps) - 1):
    lane_a, cy_a, *_ = steps[i]
    lane_b, cy_b, *_ = steps[i+1]
    box_a, box_b = node_box(lane_a, cy_a), node_box(lane_b, cy_b)
    start = ((box_a[0] + box_a[2]) // 2, box_a[3] + 3)
    end = ((box_b[0] + box_b[2]) // 2, box_b[1] - 3)
    cross = lane_a != lane_b
    arrow(start, end, color="#C0392B" if cross else "#37474F",
          width=3 if not cross else 3)

# ---------- 页脚 ----------
d.text((40, 1128), "绘制人：钟弦峰    |    跨模块流程：学生端 → 数据支撑 → 高校管理端 → 学生端（闭环）",
       font=f_foot, fill=GREY, anchor="lm")
d.text((1620, 1128), "注：红色箭头为跨泳道（跨模块）数据/结果流转",
       font=f_foot, fill="#C0392B", anchor="rm")

out = "D:/基地/平台功能需求梳理_钟弦峰/钟弦峰_学生求职与岗位匹配主流程图.png"
img.save(out)
print("saved:", out, img.size)

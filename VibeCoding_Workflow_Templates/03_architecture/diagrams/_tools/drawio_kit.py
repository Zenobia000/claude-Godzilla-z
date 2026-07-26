#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
drawio_kit — 架構圖程式化生成引擎（通用）
=========================================
AI 或人不直接手寫 drawio XML（必疊線、必亂版面），而是寫一份「宣告式 spec」
（Python 函式：擺 node、拉 edge、放 legend），由本引擎負責 style 與 XML。

用法（spec 檔範例見 ../_examples/acme_solution_overview.py）：

    from drawio_kit import *

    def my_diagram():
        c = [title("t1", "圖標題")]
        c.append(node("sys", "本系統", 520, 350, 340, 120, rrect("blue")))
        c.append(node("ext", "外部系統", 1100, 350, 220, 70, rect("gray")))
        c.append(edge("e1", "sys", "ext", "呼叫語意", E_SOLID))
        c += legend("p", 40, 700, [("fill", "blue", "本系統"), ("edge", E_SOLID, "同步呼叫")])
        return ("page1", "分頁名稱", c)

    write_drawio([my_diagram()], "out.drawio")

驗收：python3 analyze_layout.py <path> —— 量測連線交叉與穿越節點，不合格調座標重生。
鐵律：絕不手改生成出的 .drawio（重生會覆蓋）；styles 依 ../README.md 視覺規範。
"""

import html

# ---------------------------------------------------------------------------
# 語意配色（README §4.1）— (fill, stroke)
# ---------------------------------------------------------------------------
FILL = {
    "red":    ("#F8CECC", "#B85450"),   # 即時／關鍵熱路徑
    "blue":   ("#DAE8FC", "#6C8EBF"),   # 營運／後台面
    "green":  ("#D5E8D4", "#82B366"),   # 平台共用服務
    "teal":   ("#B0E3E6", "#0E8088"),   # 獨立子系統
    "orange": ("#FFE6CC", "#D79B00"),   # AI／能力資產
    "yellow": ("#FFF2CC", "#D6B656"),   # 設計態／設定／DSL
    "gray":   ("#F5F5F5", "#666666"),   # 外部實體／actor
    "purple": ("#E1D5E7", "#9673A6"),   # Data Store
    "white":  ("#FFFFFF", "#666666"),   # 中性容器／圖例
}

# ---------------------------------------------------------------------------
# 形狀 style（README §4.2）
# ---------------------------------------------------------------------------
def rrect(color):                       # 元件／程序 = 圓角矩形
    f, s = FILL[color]
    return f"rounded=1;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};"

def rect(color):                        # 外部實體／系統 = 直角矩形
    f, s = FILL[color]
    return f"whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};"

def cyl(color="purple"):                # 資料儲存 = 圓柱
    f, s = FILL[color]
    return (f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;"
            f"backgroundOutline=1;size=12;fillColor={f};strokeColor={s};")

def actor(color="gray"):                # 人／角色 = actor
    f, s = FILL[color]
    return (f"shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;"
            f"html=1;outlineConnect=0;fillColor={f};strokeColor={s};")

def container(color, dashed=False):     # 分層／部署區／子系統 = 群組框（標題置頂）
    f, s = FILL[color]
    d = "dashed=1;" if dashed else ""
    return (f"rounded=1;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};"
            f"verticalAlign=top;fontStyle=1;fontSize=13;container=1;collapsible=0;{d}")

def swim(color, start=40, horizontal=0):  # swimlane（層）
    f, s = FILL[color]
    return (f"swimlane;html=1;whiteSpace=wrap;horizontal={horizontal};startSize={start};"
            f"fillColor={f};strokeColor={s};fontStyle=1;fontSize=13;container=1;collapsible=0;")

def band(color):                        # 標語／註記橫幅
    f, s = FILL[color]
    return f"rounded=0;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};fontStyle=1;"

def arrow_down(color="yellow"):         # 縱向粗箭頭（脊椎）
    f, s = FILL[color]
    return (f"shape=singleArrow;direction=south;whiteSpace=wrap;html=1;"
            f"fillColor={f};strokeColor={s};fontStyle=1;arrowWidth=0.5;arrowSize=0.25;")

def note(color="yellow"):               # 小卡／註記
    f, s = FILL[color]
    return (f"rounded=1;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};"
            f"align=left;verticalAlign=top;fontSize=11;dashed=1;")

def txt(align="left"):                  # 純文字
    return f"text;html=1;strokeColor=none;fillColor=none;align={align};verticalAlign=middle;"

def state_style(color):                 # UML 狀態（狀態圖正典是 lld mermaid；此為簡報級備用）
    f, s = FILL[color]
    return f"rounded=1;arcSize=40;whiteSpace=wrap;html=1;fillColor={f};strokeColor={s};"

# --- Solution Overview（zone 型大圖）專用：白底、淡表頭、低裝飾 ---
def ref_zone(header_fill="#F8FAFC", stroke="#CBD5E1"):
    """L1 責任區。"""
    return (
        "swimlane;html=1;whiteSpace=wrap;horizontal=1;startSize=36;"
        f"fillColor=#FFFFFF;swimlaneFillColor={header_fill};strokeColor={stroke};"
        "fontColor=#0F172A;fontStyle=1;fontSize=12;container=1;collapsible=0;"
    )

def ref_component(stroke="#64748B", fill="#FFFFFF", dashed=False):
    """L2 元件卡：白底加語意色框；dashed=True 表 🔜 目標狀態。"""
    d = "dashed=1;dashPattern=5 4;" if dashed else ""
    return (
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;"
        f"fillColor={fill};strokeColor={stroke};fontColor=#0F172A;"
        f"fontSize=10;spacing=5;{d}"
    )

def ref_store(stroke="#EA580C"):
    """持久化／證據儲存卡。"""
    return (
        "rounded=1;arcSize=8;whiteSpace=wrap;html=1;"
        f"fillColor=#FFF7ED;strokeColor={stroke};fontColor=#7C2D12;"
        "fontSize=9;spacing=4;"
    )

def ref_card(stroke, fill):
    """責任說明卡（align left、細字）。"""
    return (
        "rounded=1;arcSize=6;whiteSpace=wrap;html=1;align=left;verticalAlign=top;"
        f"fillColor={fill};strokeColor={stroke};fontColor=#0F172A;"
        "fontSize=9;spacingTop=7;spacingLeft=8;spacingRight=6;"
    )

# ---------------------------------------------------------------------------
# 線型 style（README §4.3）
# ---------------------------------------------------------------------------
# 一般圖走直線路由（非 orthogonal）：多條線從節點各自角度散開，不被正交繞線疊到
# 同一軌道；節點座標應對「直線穿越」最佳化（用 analyze_layout.py 驗證）。
E_MAIN  = "html=1;strokeWidth=2.5;endArrow=classic;endFill=1;strokeColor=#333333;fontSize=10;"   # 關鍵主鏈
E_SOLID = "html=1;endArrow=classic;endFill=1;strokeColor=#555555;fontSize=10;"                   # 同步呼叫／設計態發布
E_DASH  = "html=1;endArrow=classic;dashed=1;strokeColor=#6C8EBF;fontSize=10;"                    # 非同步／回流（虛線）
E_DOT   = "html=1;endArrow=open;dashed=1;dashPattern=1 4;strokeColor=#999999;fontSize=10;"       # 橫切支撐（點線）
E_STATE = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;endFill=1;"
           "strokeColor=#555555;fontSize=10;")                                                   # 狀態轉移（保留正交）
E_STRAIGHT = "html=1;endArrow=classic;endFill=1;strokeColor=#333333;fontSize=10;"                # 直線（sequence）

# Solution Overview 四條語意資料路徑（solution_overview.md §2.2；正交路由、獨立 lane）
E_REF_INTERACTION = (   # 藍實線：即時互動／同步交易
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
    "html=1;strokeWidth=2.5;endArrow=classic;endFill=1;"
    "strokeColor=#2563EB;fontColor=#1E3A8A;fontSize=9;"
)
E_REF_EVENT = (         # 綠虛線：領域事件／非同步 metadata
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
    "html=1;strokeWidth=2;endArrow=classic;endFill=1;dashed=1;dashPattern=6 4;"
    "strokeColor=#16A34A;fontColor=#166534;fontSize=9;"
)
E_REF_CONTROL = (       # 紫虛線：控制、設定、身分、安全
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
    "html=1;strokeWidth=2;endArrow=open;endFill=0;dashed=1;dashPattern=3 4;"
    "strokeColor=#9333EA;fontColor=#6B21A8;fontSize=9;"
)
E_REF_STORAGE = (       # 橘虛線：持久化、重播與證據
    "edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;"
    "html=1;strokeWidth=2;endArrow=classic;endFill=1;dashed=1;dashPattern=8 4;"
    "strokeColor=#EA580C;fontColor=#9A3412;fontSize=9;"
)

# ---------------------------------------------------------------------------
# 低階建構
# ---------------------------------------------------------------------------
def esc(s):
    return html.escape(str(s), quote=True)

def node(cid, value, x, y, w, h, style, parent="1"):
    return (f'<mxCell id="{cid}" value="{esc(value)}" style="{style}" vertex="1" '
            f'parent="{parent}"><mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" '
            f'as="geometry"/></mxCell>')

def edge(cid, src, tgt, value, style, parent="1", pts=None, exit=None, entry=None):
    st = style
    if exit:
        st += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
    if entry:
        st += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
    if pts:
        arr = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts)
        geo = f'<mxGeometry relative="1" as="geometry"><Array as="points">{arr}</Array></mxGeometry>'
    else:
        geo = '<mxGeometry relative="1" as="geometry"/>'
    return (f'<mxCell id="{cid}" value="{esc(value)}" style="{st}" edge="1" '
            f'parent="{parent}" source="{src}" target="{tgt}">{geo}</mxCell>')

def free_edge(cid, x1, y1, x2, y2, value, style, parent="1", dash=False):
    st = style + ("dashed=1;" if dash else "")
    return (f'<mxCell id="{cid}" value="{esc(value)}" style="{st}" edge="1" parent="{parent}">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/></mxGeometry></mxCell>')

def title(cid, text, x=40, y=8, w=760):
    return node(cid, text, x, y, w, 30,
                "text;html=1;strokeColor=none;fillColor=none;align=left;"
                "verticalAlign=middle;fontStyle=1;fontSize=17;")

def subtitle(cid, text, x=40, y=36, w=900):
    return node(cid, text, x, y, w, 22,
                "text;html=1;strokeColor=none;fillColor=none;align=left;"
                "verticalAlign=middle;fontSize=11;fontColor=#666666;")

def legend(prefix, x, y, items, w=250, ttl="圖例 Legend"):
    """items: list of (kind, val, text).
    kind='fill' → val=色票 key，畫色塊；
    kind='line' → val=色票 key，畫實心細線；
    kind='edge' → val=完整 edge style 字串，畫真實線型 swatch（粗實／實／虛／點）。
    """
    cells = []
    row_h = 22
    h = 30 + row_h * len(items) + 6
    gid = f"{prefix}_lg"
    cells.append(node(gid, ttl, x, y, w, h,
                      "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#666666;"
                      "verticalAlign=top;fontStyle=1;fontSize=11;container=1;collapsible=0;"))
    yy = 28
    for i, (kind, val, text) in enumerate(items):
        if kind == "edge":
            # 用絕對座標畫真實線型 swatch（避免容器內 edge 座標歧義）
            sw = val.replace("edgeStyle=orthogonalEdgeStyle;", "")  # swatch 走直線
            cells.append(
                f'<mxCell id="{gid}_s{i}" value="" style="{sw}" edge="1" parent="1">'
                f'<mxGeometry relative="1" as="geometry">'
                f'<mxPoint x="{x + 8}" y="{y + yy + 11}" as="sourcePoint"/>'
                f'<mxPoint x="{x + 38}" y="{y + yy + 11}" as="targetPoint"/></mxGeometry></mxCell>')
        else:
            f, s = FILL[val]
            if kind == "fill":
                cells.append(node(f"{gid}_s{i}", "", 10, yy + 3, 26, 14,
                                  f"rounded=1;html=1;fillColor={f};strokeColor={s};", parent=gid))
            else:  # 'line'
                cells.append(node(f"{gid}_s{i}", "", 10, yy + 8, 26, 4,
                                  f"html=1;fillColor={s};strokeColor={s};", parent=gid))
        cells.append(node(f"{gid}_t{i}", text, 42, yy, w - 50, row_h,
                          "text;html=1;align=left;verticalAlign=middle;fontSize=10;", parent=gid))
        yy += row_h
    return cells

# ---------------------------------------------------------------------------
# 輸出
# ---------------------------------------------------------------------------
def wrap_mxfile(diagrams, page_w=1700, page_h=1200):
    """diagrams: list of (diagram_id, page_name, cells)。"""
    parts = ['<mxfile host="app.diagrams.net" agent="drawio_kit" version="24.7.17">']
    for did, name, cells in diagrams:
        parts.append(f'<diagram id="{did}" name="{esc(name)}">')
        parts.append(f'<mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" '
                     f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
                     f'pageWidth="{page_w}" pageHeight="{page_h}" math="0" shadow="0"><root>'
                     '<mxCell id="0"/><mxCell id="1" parent="0"/>')
        parts.append("".join(cells))
        parts.append('</root></mxGraphModel></diagram>')
    parts.append('</mxfile>')
    return "\n".join(parts)

def write_drawio(diagrams, path, page_w=1700, page_h=1200):
    """把多張圖寫成單一多分頁 .drawio；一張圖就傳一個元素的 list。"""
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(wrap_mxfile(diagrams, page_w, page_h))
    print(f"  ✓ {path}")

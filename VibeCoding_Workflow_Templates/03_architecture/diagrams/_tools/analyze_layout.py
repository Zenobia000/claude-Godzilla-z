#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Layout analyzer — 量測 .drawio 的連線交錯程度，供「減少交錯」迭代驗證（通用）。

偵測：
  (A) edge–edge 交叉  : 兩條不共端點的連線，其實際 waypoint 線段相交
  (B) edge 穿越節點   : 任一實際線段穿過「非其端點」的節點方框
有 waypoint 時依實際折線量測；無 waypoint 時以端點中心直線作代理。

用法：python3 analyze_layout.py [檔案或目錄 ...] [-v]
      不給路徑時掃當前目錄（遞迴 **/*.drawio）。
驗收基準：score（cross+pierce）應為 0；>0 時回 spec 調座標或 waypoint 重生。
"""
import xml.etree.ElementTree as ET
import glob
import os
import sys


def abs_geom(cells_by_id, cid):
    """回傳節點絕對 (x,y,w,h)；沿 parent 鏈累加位移。"""
    x = y = 0.0
    w = h = None
    seen = set()
    cur = cid
    first = True
    while cur and cur in cells_by_id and cur not in seen:
        seen.add(cur)
        c = cells_by_id[cur]
        g = c["geom"]
        if g is None:
            break
        if first:
            w, h = g["w"], g["h"]
            first = False
        x += g["x"]
        y += g["y"]
        cur = c["parent"]
    return (x, y, w, h)


def center(cells_by_id, cid):
    x, y, w, h = abs_geom(cells_by_id, cid)
    if w is None:
        return None
    return (x + w / 2.0, y + h / 2.0)


def seg_intersect(p1, p2, p3, p4):
    def ccw(a, b, c):
        return (c[1]-a[1])*(b[0]-a[0]) - (b[1]-a[1])*(c[0]-a[0])
    d1 = ccw(p3, p4, p1); d2 = ccw(p3, p4, p2)
    d3 = ccw(p1, p2, p3); d4 = ccw(p1, p2, p4)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
        return True
    return False


def seg_rect(p1, p2, rect):
    """線段是否與矩形相交（含穿越）。"""
    rx, ry, rw, rh = rect
    for px, py in (p1, p2):
        if rx <= px <= rx+rw and ry <= py <= ry+rh:
            return True
    corners = [(rx, ry), (rx+rw, ry), (rx+rw, ry+rh), (rx, ry+rh)]
    edges = [(corners[i], corners[(i+1) % 4]) for i in range(4)]
    for a, b in edges:
        if seg_intersect(p1, p2, a, b):
            return True
    return False


def analyze(path):
    tree = ET.parse(path)
    results = []
    for diagram in tree.getroot().iter("diagram"):
        cells = {}
        vertices = []
        edges = []
        for c in diagram.iter("mxCell"):
            cid = c.get("id")
            if not cid:
                continue
            g = c.find("mxGeometry")
            geom = None
            if g is not None and g.get("width"):
                geom = {"x": float(g.get("x", 0)), "y": float(g.get("y", 0)),
                        "w": float(g.get("width")), "h": float(g.get("height"))}
            cells[cid] = {"parent": c.get("parent"), "geom": geom,
                          "edge": c.get("edge"), "vertex": c.get("vertex"),
                          "source": c.get("source"), "target": c.get("target"),
                          "points": [
                              (float(p.get("x", 0)), float(p.get("y", 0)))
                              for p in (
                                  g.findall("Array[@as='points']/mxPoint")
                                  if g is not None else []
                              )
                          ]}
        for cid, c in cells.items():
            if c["vertex"] == "1" and c["geom"] is not None:
                vertices.append(cid)
            if c["edge"] == "1" and c.get("source") and c.get("target"):
                edges.append(cid)

        # 端點中心 + 明示 waypoint；未明示時維持中心直線代理。
        segs = []
        for e in edges:
            s, t = cells[e]["source"], cells[e]["target"]
            if s == t:
                continue
            cs, ct = center(cells, s), center(cells, t)
            if cs and ct:
                segs.append((e, s, t, [cs, *cells[e]["points"], ct]))

        # (A) edge-edge 交叉
        cross = 0
        cross_pairs = []
        for i in range(len(segs)):
            for j in range(i+1, len(segs)):
                e1, s1, t1, path1 = segs[i]
                e2, s2, t2, path2 = segs[j]
                if {s1, t1} & {s2, t2}:      # 共端點不算交錯
                    continue
                if any(
                    seg_intersect(path1[a], path1[a + 1], path2[b], path2[b + 1])
                    for a in range(len(path1) - 1)
                    for b in range(len(path2) - 1)
                ):
                    cross += 1
                    cross_pairs.append((e1, e2))

        # (B) edge 穿越非端點節點
        pierce = 0
        pierce_list = []
        # 只把「葉節點」當障礙物：容器／群組被連線穿過是預期的，不計。
        parents = {c["parent"] for c in cells.values() if c["parent"]}
        leaf = []
        for v in vertices:
            if v in parents:                 # 是別人的 parent → 容器，不計
                continue
            x, y, w, h = abs_geom(cells, v)
            if w is None:
                continue
            leaf.append((v, (x, y, w, h)))

        def is_desc(node_id, anc):
            cur = cells.get(node_id, {}).get("parent")
            seen = set()
            while cur and cur not in seen:
                if cur == anc:
                    return True
                seen.add(cur)
                cur = cells.get(cur, {}).get("parent")
            return False

        for e, s, t, seg_path in segs:
            for v, r in leaf:
                if v in (s, t):
                    continue
                if is_desc(v, s) or is_desc(v, t):   # 箭頭進容器命中其子節點=預期
                    continue
                # 收縮矩形避免僅擦邊
                rx, ry, rw, rh = r
                shrink = (rx+6, ry+6, max(rw-12, 1), max(rh-12, 1))
                if any(
                    seg_rect(seg_path[index], seg_path[index + 1], shrink)
                    for index in range(len(seg_path) - 1)
                ):
                    pierce += 1
                    pierce_list.append((e, v))

        results.append((diagram.get("name"), len(segs), cross, pierce,
                        cross_pairs, pierce_list))
    return results


def collect(paths):
    files = []
    for p in paths:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "**", "*.drawio"), recursive=True))
        else:
            files.append(p)
    return files


def main():
    args = [a for a in sys.argv[1:] if a != "-v"]
    verbose = "-v" in sys.argv[1:]
    files = collect(args or ["."])
    if not files:
        print("no .drawio found")
        return
    total_c = total_p = 0
    rows = []
    for f in files:
        for name, ne, cross, pierce, cp, pl in analyze(f):
            rows.append((name, ne, cross, pierce))
            total_c += cross
            total_p += pierce
            if verbose and (cross or pierce):
                print(f"\n### {name}  edges={ne} cross={cross} pierce={pierce}")
                if cp:
                    print("   cross:", cp[:20])
                if pl:
                    print("   pierce:", pl[:20])
    rows.sort(key=lambda r: (r[2]+r[3]), reverse=True)
    print(f"\n{'diagram':40s} {'edges':>5} {'cross':>6} {'pierce':>7} {'score':>6}")
    print("-"*68)
    for name, ne, cross, pierce in rows:
        print(f"{name:40s} {ne:5d} {cross:6d} {pierce:7d} {cross+pierce:6d}")
    print("-"*68)
    print(f"{'TOTAL':40s} {'':5} {total_c:6d} {total_p:7d} {total_c+total_p:6d}")


if __name__ == "__main__":
    main()

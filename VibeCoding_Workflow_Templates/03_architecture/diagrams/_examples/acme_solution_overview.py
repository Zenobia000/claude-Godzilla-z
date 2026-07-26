#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Worked example — ACME Field Service（虛構專案）Solution Architecture Overview
==========================================================================
對應模板：../solution_overview.md；引擎：../_tools/drawio_kit.py。
示範「模板 §2 生成 prompt → 宣告式 spec → .drawio」的完整鏈路：
5 個 L1 Zone、底部橫切治理帶、四條語意資料路徑、圖例與 metadata banner。

版面心法（讓 analyze_layout score=0 的三個手段）：
  1. 長距離連線走專用通道：上方 lane（y36/46/56，錯開高度）、右側外緣（x1600）。
  2. 同通道的線共用端點（共端點不計交叉）；不共端點的線分不同高度。
  3. zone 內用行列擺位讓相鄰流向（服務→儲存）成為短水平線，消除長垂直線。

執行：  python3 acme_solution_overview.py
驗收：  python3 ../_tools/analyze_layout.py . -v   （目標 score=0）
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_tools"))
from drawio_kit import (  # noqa: E402
    E_REF_CONTROL, E_REF_EVENT, E_REF_INTERACTION, E_REF_STORAGE,
    actor, container, edge, legend, node, note, rect, ref_component,
    ref_store, ref_zone, title, write_drawio,
)

ZY, ZH, ZW = 70, 600, 296
ZX = [40, 352, 664, 976, 1288]          # 五個 zone 的 x（間距 312，留 16px 縫）


def overview():
    c = [title("t", "ACME Field Service — 高階端到端參考架構（虛構示例）", w=760)]

    # ── L1 Zones ──────────────────────────────────────────────────────────
    zones = [
        ("z1", "Z1 Actors & Inbound Signals"),
        ("z2", "Z2 Channel & AI Runtime"),
        ("z3", "Z3 Interaction & Event Distribution"),
        ("z4", "Z4 Domain Services & Data"),
        ("z5", "Z5 Applications & External Systems"),
    ]
    for (zid, name), x in zip(zones, ZX):
        c.append(node(zid, name, x, ZY, ZW, ZH, ref_zone()))

    # ── Zone 內元件（座標相對 zone；zone 表頭高 36）──────────────────────
    # Z1：外部角色
    c.append(node("a_cust", "客戶\n(Web / LINE 聊天)", 118, 60, 60, 90, actor(), parent="z1"))
    c.append(node("a_ops", "營運人員\n(後台)", 118, 200, 60, 90, actor(), parent="z1"))
    c.append(node("a_field", "外勤技師\n(App → REST API)", 118, 340, 60, 90, actor(), parent="z1"))

    # Z2：通道與 AI Runtime
    c.append(node("c_gw", "Chat Gateway\n（webhook 驗簽／去重）", 30, 70, 236, 60,
                  ref_component("#2563EB"), parent="z2"))
    c.append(node("c_ai", "Assistant Runtime\n（對話編排／工具白名單）", 30, 180, 236, 70,
                  ref_component("#D79B00"), parent="z2"))
    c.append(node("c_llm", "Model Gateway\n（供應商無關路由\n→ 外部 LLM）", 24, 300, 130, 70,
                  ref_component("#D79B00"), parent="z2"))
    c.append(node("c_kb", "Knowledge Store\n(vector)", 166, 300, 106, 70,
                  ref_store(), parent="z2"))

    # Z3：互動與事件分發
    c.append(node("d_api", "REST API / ACL\n（認證·租戶·授權守衛）", 30, 70, 236, 60,
                  ref_component("#2563EB"), parent="z3"))
    c.append(node("d_obx", "Outbox Relay", 30, 180, 236, 50,
                  ref_component("#16A34A"), parent="z3"))
    c.append(node("d_bus", "Event Bus 🔜\n（AsyncAPI topics）", 30, 290, 236, 60,
                  ref_component("#16A34A", dashed=True), parent="z3"))
    c.append(node("d_ws", "Realtime Hub (WS)", 30, 420, 236, 50,
                  ref_component("#2563EB"), parent="z3"))

    # Z4：領域服務與資料（服務→儲存水平相鄰，垂直長線歸零）
    c.append(node("s_ord", "Order Service\n（工單／派工真相）", 24, 70, 130, 60,
                  ref_component("#64748B"), parent="z4"))
    c.append(node("s_db", "Domain DB\n(SQL·outbox)", 176, 70, 96, 60,
                  ref_store(), parent="z4"))
    c.append(node("s_bil", "Billing Service", 24, 180, 130, 60,
                  ref_component("#64748B"), parent="z4"))
    c.append(node("s_obj", "Evidence\nObject Store\n（Order Service 寫入）", 176, 300, 96, 60,
                  ref_store(), parent="z4"))

    # Z5：應用與外部系統
    c.append(node("p_portal", "Ops Portal\n（營運後台）", 30, 70, 236, 60,
                  ref_component("#2563EB"), parent="z5"))
    c.append(node("p_pay", "Payment Provider（外部）", 30, 180, 236, 50, rect("gray"), parent="z5"))
    c.append(node("p_cloud", "Cloud Platform\n（部署／密鑰／DB 託管）", 30, 300, 236, 60,
                  rect("gray"), parent="z5"))

    # ── 橫切治理帶（位置即語意：支撐所有 zone，不畫連線）──────────────────
    c.append(node("z6", "Cross-Cutting Management（控制面 · 設定 · 身分 · 安全 · 可觀測）",
                  40, 700, 1544, 110, container("white")))
    cards = ["Control Plane\n租戶 provisioning", "Configuration\nfeature flag / 設定",
             "Identity & Access\nOIDC / RBAC", "Security & Governance\n稽核 / 秘密管理",
             "Observability\nmetrics / trace / log"]
    for i, v in enumerate(cards):
        c.append(node(f"x{i}", v, 20 + i * 300, 45, 280, 50,
                      ref_component("#9333EA"), parent="z6"))

    # ── 四條語意資料路徑 ─────────────────────────────────────────────────
    # 藍：即時互動／同步交易
    c.append(edge("e1", "a_cust", "c_gw", "訊息 / webhook (HTTPS)", E_REF_INTERACTION))
    c.append(edge("e2", "c_gw", "c_ai", "normalized turn", E_REF_INTERACTION))
    c.append(edge("e3", "c_ai", "d_api", "工具呼叫 (REST)", E_REF_INTERACTION))
    c.append(edge("e4", "d_api", "s_ord", "下單／派工 command", E_REF_INTERACTION))
    c.append(edge("e5", "a_ops", "p_portal", "HTTPS（OIDC 登入）", E_REF_INTERACTION,
                  pts=[(84, 315), (84, 36), (1400, 36)]))
    c.append(edge("e6", "p_portal", "d_api", "REST 查詢／操作", E_REF_INTERACTION,
                  pts=[(1436, 56), (812, 56)]))
    c.append(edge("e7", "c_ai", "c_llm", "模型呼叫", E_REF_INTERACTION))
    c.append(edge("e8", "d_ws", "p_portal", "即時更新推送 (WS)", E_REF_INTERACTION,
                  pts=[(1600, 515), (1600, 170)]))
    c.append(edge("e9", "s_bil", "p_pay", "請款 (API)", E_REF_INTERACTION))

    # 綠：領域事件／非同步 metadata
    c.append(edge("g1", "s_db", "d_obx", "outbox 輪詢", E_REF_EVENT,
                  pts=[(1200, 230)]))
    c.append(edge("g2", "d_obx", "d_bus", "publish 🔜", E_REF_EVENT))
    c.append(edge("g3", "d_bus", "s_bil", "order.completed 🔜", E_REF_EVENT))

    # 紫：控制、設定、身分、安全（身分／稽核由底部治理帶承載，不畫長線）
    c.append(edge("p1", "p_portal", "d_api", "租戶設定 / feature flag 下發", E_REF_CONTROL,
                  pts=[(1436, 46), (812, 46)]))

    # 橘：持久化、重播與證據
    c.append(edge("o1", "s_ord", "s_db", "SQL/JSONB · outbox insert", E_REF_STORAGE))
    c.append(edge("o3", "c_ai", "c_kb", "RAG 查詢 (vector)", E_REF_STORAGE))

    # ── metadata banner 與圖例 ────────────────────────────────────────────
    c.append(node("meta", "受眾：主管／客戶／新人 onboarding\n"
                          "回答的問題：系統端到端由哪些責任區組成？資料以哪幾種語意流動？\n"
                          "正典來源：sad.md §1／§6–7（本圖為虛構示例）｜最後校驗：2026-07-26",
                  420, 840, 560, 70, note("yellow")))
    c += legend("ov", 40, 840, [
        ("edge", E_REF_INTERACTION, "藍實線＝即時互動／同步交易"),
        ("edge", E_REF_EVENT, "綠虛線＝領域事件／非同步"),
        ("edge", E_REF_CONTROL, "紫虛線＝控制／設定／身分"),
        ("edge", E_REF_STORAGE, "橘虛線＝持久化／證據"),
        ("fill", "gray", "灰＝外部系統"),
        ("line", "purple", "🔜＝目標狀態（虛框）"),
    ], w=340)
    return ("acme_ov", "ACME Solution Overview（示例）", c)


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    write_drawio([overview()], os.path.join(base, "acme-one-platform-overview.drawio"))

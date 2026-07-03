# EA_SYSTEM Execution Model

---

# 1. Purpose

本ファイルはEA_SYSTEMにおける「判断から実行までの流れ」を定義する。

---

# 2. Core Flow

EAの基本フローは以下：

monitoring → market data → decision → risk check → safety check → execution

---

# 3. Step Definition

## 3.1 Monitoring
- 市場データ収集
- 異常検知
- 状態更新

---

## 3.2 Market Processing
- 価格データ整形
- レジーム判定
- ノイズ除去

---

## 3.3 Decision Layer
- エントリー判断
- ロジック選択
- シグナル生成

---

## 3.4 Risk Layer
- ロット計算
- 損失許容確認
- ポジションサイズ制御

---

## 3.5 Safety Layer
- safety_orchestration参照
- Level判定
- 必要なら停止・制限

---

## 3.6 Execution Layer
- 注文実行
- ポジション管理
- 約定確認

---

# 4. Control Priority

優先順位：

1. safety_orchestration（最優先）
2. risk_rules
3. decision logic
4. execution

---

# 5. Failure Handling

- execution失敗 → retry or rollback
- risk超過 → execution停止
- safety発動 → 全停止

---

# 6. System Principle

- executionは単独判断しない
- 必ずriskとsafetyを通過する
- decisionは実行を直接行わない

---

# 7. Design Rule

- 判断と実行を分離する
- 安全層は常に上書き可能
- フローは一方向（逆流禁止）

---

END
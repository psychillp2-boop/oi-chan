# EA_SYSTEM Safety Orchestration

---

# 1. Purpose

本ファイルはEA_SYSTEMにおける「動的安全制御レイヤー」を定義する。

execution_modelおよびrisk_policyを監視し、
異常時に即時介入・制御・停止を行う。

---

# 2. Core Role

- リアルタイム安全判断
- executionの上書き制御
- リスク急変時の即時対応

---

# 3. Control Priority

最優先順位：

1. safety_orchestration（最優先）
2. risk_policy
3. execution_model
4. decision logic

---

# 4. Trigger Conditions

以下で発動：

- 急激な損失拡大
- スプレッド異常
- ボラティリティ急上昇
- 連敗増加
- 約定異常
- システム遅延

---

# 5. Safety Levels

## Level 1: Normal
- 通常運用

## Level 2: Caution
- ロット制限
- 新規エントリー抑制

## Level 3: Risk Mode
- 新規停止
- ポジション縮小

## Level 4: Emergency Stop
- 全execution停止
- ポジション保護優先

---

# 6. Execution Override Rules

- safetyはexecutionを強制停止できる
- risk_policyより優先される
- decisionより常に上位制御

---

# 7. System Behavior

- 異常検知 → 即評価
- 状態更新 → レベル決定
- レベルに応じて制御実行

---

# 8. Integration Rules

- monitoring → データ供給
- risk_policy → 静的制御
- execution_model → 実行フロー
- safety → 最終判断

---

# 9. Design Principle

- 安全は常に後付けではなく先制的
- システムは壊れる前に止まる
- 判断よりも保護を優先

---

END
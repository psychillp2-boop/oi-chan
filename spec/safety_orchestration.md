# Safety Orchestration (EA_SYSTEM)

---

# 1. Purpose

本ファイルはEA_SYSTEM全体の「動的安全制御レイヤー」を定義する。

役割は以下：

- 市場状態に応じたシステム制御
- リスク増大時の自動制限
- executionの安全停止判断
- monitoringとriskの統合制御

---

# 2. Core Principle

- rulesは静的ルール
- safety_orchestrationは動的判断
- executionより常に優先される

---

# 3. Data Flow

monitoring → risk → safety_orchestration → execution

---

# 4. Trigger Conditions

以下のいずれかで制御発動：

- スプレッド異常拡大
- ボラティリティ急上昇
- 連続損失発生
- モデル異常検知
- 実行エラー増加

---

# 5. Safety Levels

## Level 1: Normal
- 通常運用
- フィルタなし

## Level 2: Caution
- エントリー制限
- ロット縮小

## Level 3: Risk Control
- 新規エントリー制限
- ポジション縮小

## Level 4: Emergency Stop
- execution停止
- 全ポジション保護優先

---

# 6. Execution Control Rules

- safetyがexecutionを上書きする
- risk判断より安全判断が優先
- 異常時は即停止可能構造とする

---

# 7. Integration Rules

- monitoringはデータ供給のみ
- riskは数値評価
- safetyは意思決定層
- executionは実行のみ

---

# 8. Design Principle

- 判断は一箇所に集約する
- ルールと制御を混在させない
- 必ず段階的制御を行う

---

END

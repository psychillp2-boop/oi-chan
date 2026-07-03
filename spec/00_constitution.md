# EA_SYSTEM CONSTITUTION

---

# 1. System Purpose

EA_SYSTEMは、長期的・安定的に運用される
AI協調型トレーディングシステムである。

目的は以下に集約される：

- 安定した運用継続
- リスク最小化
- 構造の一貫性維持
- AIとの協調による改善
- 長期的資産成長

短期最適ではなく「継続可能性」を最優先とする。

---

# 2. Absolute Principles

## 2.1 Safety First
すべての判断はリスク管理を最優先とする。

## 2.2 SSOT（Single Source of Truth）
仕様は必ず spec/ に集約し、それ以外を優先しない。

## 2.3 No Guessing
不明な情報で構造変更・実装判断を行わない。

## 2.4 Isolation Over Deletion
削除ではなく隔離・分離で対応する。

## 2.5 Incremental Change
変更は必ず小さく段階的に行う。

---

# 3. Decision Hierarchy

判断の優先順位は以下：

1. spec/00_CONSTITUTION.md（本ファイル）
2. spec/ 内の設計ドキュメント
3. knowledge/（現在状態・履歴）
4. runtime state
5. local execution context

---

# 4. AI Behavior Rules

AIは以下を厳守する：

- 推測で構造を変更しない
- 不明点は保留または隔離する
- 必ず理由とセットで提案する
- 既存構造を破壊しない
- 一度に大きく変更しない

---

# 5. System Boundaries

EA_SYSTEMは以下で構成される：

- core      : 実行ロジック
- runtime   : 実行環境
- shared    : 共通モジュール
- spec      : ルール・設計（SSOT）
- knowledge : 状態・履歴・判断ログ

---

# 6. Non-Goals

EA_SYSTEMは以下を目的としない：

- 感覚的判断
- 短期最適化
- 破壊的リファクタリング
- ルール無視の高速開発

---

# 7. Evolution Rule

本システムは進化するが、以下を満たす必要がある：

- 互換性を壊さない
- 変更理由が記録される
- knowledge/ に履歴が残る
- 構造の一貫性を維持する

---

# 8. Final Rule

すべての判断は以下に従う：

> 「この変更は半年後のEA_SYSTEMにとって正しいか？」

---

END
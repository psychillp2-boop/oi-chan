# Refactoring TODO

## Rule

- 動作するコードはすぐに変更しない
- Phase完了後に整理する
- SSOTを維持する
- Additive Changes Only
- リファクタリング前に必ずテストを実施する
- 新しい改善候補が見つかったら、このファイルへ追加する

---

## R-001 Order Sendの重複

状態：未対応

内容：

Executor と OrderSender の両方で
mt5.order_send() を実行している。

現状

Runtime
    ↓
Executor
    ↓
MT5

理想

Runtime
    ↓
Executor
    ↓
OrderSender
    ↓
MT5

対応

- ExecutorからMT5直接呼び出しを削除
- OrderSender.send()へ一本化

優先度：★★★★★

---

## R-002 PositionManagerの命名整理

状態：調査中

対象

core/risk/position_manager.py

runtime/execution/position_manager.py

内容

同じ PositionManager という名前だが、
責務が異なる。

対応候補

- RiskPositionManager
- ExecutionPositionManager

または責務に合った名称へ変更する。

優先度：★★★★☆

---

## R-003 Runtime → Broker の依存整理

状態：未対応

内容

Runtime は Broker を保持しているが、
Executor が直接 MT5 を呼び出している。

理想

Runtime
    ↓
Executor
    ↓
Broker
    ↓
MT5

対応

Broker を唯一の MT5 窓口にする。

優先度：★★★★☆

---

## R-004 tests フォルダ整理

状態：保留

内容

tests フォルダの役割を整理する。

候補

tests/
│
├── broker/
├── runtime/
├── integration/
├── scenarios/
└── stress/

目的

・テストの種類を明確化
・重複テスト防止
・保守性向上

優先度：★★★☆☆

---

## R-005 Executor と OrderSender の責務整理

状態：未対応

内容

Executor と OrderSender の両方が
注文リクエスト作成・送信に関わっている。

対応

・Executorは実行フロー管理
・OrderSenderは注文送信専用
・MT5 API を呼ぶのは Broker 層のみ

優先度：★★★★☆

---

## R-006 MT5設定値のCONFIG集約

状態：保留

内容

固定値が複数箇所に存在する。

対象

- magic
- deviation
- comment
- type_filling
- type_time

対応

CONFIGへ集約し、
SSOTを徹底する。

優先度：★★★☆☆

---

## R-007 PerformanceTrackerの命名整理

状態：調査中

対象

core/analytics/performance_tracker.py

runtime/performance_tracker.py

内容

同名ファイルだが役割が異なる。

対応候補

- AnalyticsPerformanceTracker
- RuntimePerformanceTracker

または責務に合わせて配置・名称を見直す。

優先度：★★★☆☆

---

## R-008 market / monitoring の役割明文化

状態：確認のみ

対象

core/market
runtime/market

runtime/monitoring
tools/monitoring

内容

フォルダ名は重複して見えるが、
役割は異なる。

役割

core/market
    ↓
市場分析・AI・インジケータ

runtime/market
    ↓
Runtime専用の市場状態

runtime/monitoring
    ↓
Runtime実行中の監視

tools/monitoring
    ↓
運用・保守ツール

対応

README または Architecture 文書へ役割を明記する。

優先度：★★☆☆☆
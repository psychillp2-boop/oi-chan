\# Core Layer Rules



\## 1. 役割



coreはEA\_SYSTEMの意思決定・判断ロジックを担当する中枢層



\---



\## 2. 構成（固定）



\- ai: 学習・判断

\- risk: リスク制御

\- execution: 実行判断

\- monitoring: 状態監視

\- market: 市場情報処理



\---



\## 3. 禁止事項



\- core内で直接UI処理をしない

\- core内でログ保存を単独で設計しない

\- coreからbrokerを直接操作しすぎない（必ずexecution経由）



\---



\## 4. 設計原則



\- 判断（AI）

\- 制御（risk）

\- 実行指示（execution）

\- 観測（monitoring）



この4つを分離する


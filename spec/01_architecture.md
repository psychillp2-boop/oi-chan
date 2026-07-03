\# EA\_SYSTEM Architecture



\## 1. 全体構造



EA\_SYSTEMは3層構造で構成される



\- spec（設計層）

\- runtime（実行層）

\- shared（共通層）



\---



\## 2. runtime（実行層）



実際に動作するシステム本体



構成：

\- core: AI / risk / execution / monitoring

\- broker: MT5連携

\- dashboard: 可視化

\- strategies: 売買ロジック

\- logs: 実行ログ



\---



\## 3. spec（設計層）



システムのルールと構造定義



役割：

\- モジュール構造の定義

\- 禁止ルール

\- アーキテクチャ管理



\---



\## 4. shared（共通層）



全モジュールで共通利用する部品



例：

\- logger

\- config

\- utils



\---



\## 5. 原則



\- runtimeは直接壊さない

\- 仕様変更はspecで管理

\- 共通処理はsharedへ移動


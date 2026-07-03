\# Shared Layer Rules



\## 1. 役割



sharedは全モジュール共通の機能を提供する層



\---



\## 2. 絶対ルール



\- runtimeに重複コードを置かない

\- 共通処理は必ずsharedへ移動

\- 変更は影響範囲を確認してから実施



\---



\## 3. 禁止事項



\- strategiesやcoreで独自loggerを作る

\- configを各モジュールで分散管理する



\---



\## 4. 原則



共通化できるものはすべてsharedに集約する


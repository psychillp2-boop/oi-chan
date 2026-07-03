\# Runtime Rules



\## 1. runtimeの役割



runtimeは「実行専用領域」であり、設計判断は禁止



\---



\## 2. 変更ルール



\- runtime内の構造変更は必ずspec承認後

\- コード修正は最小単位で行う

\- 削除ではなく修正・置換を優先



\---



\## 3. 責務分離



\- core: ロジック

\- broker: 外部接続

\- strategies: 売買ロジック

\- logs: 出力のみ



\---



\## 4. 原則



runtimeは「動くもの」、specは「決めるもの」


\# Safety Orchestration Rules (Monitoring × Risk)



\## 1. 役割



monitoringとriskは連携してEA\_SYSTEM全体の安全性を維持する



\- monitoring：異常検知

\- risk：停止判断・制御



\---



\## 2. 連携フロー



1\. monitoringが異常を検知

2\. riskにシグナル送信

3\. riskが評価

4\. 必要に応じてexecution停止



\---



\## 3. 異常トリガー



以下のいずれかで発動：



\- 連続エラー増加

\- ドローダウン急増

\- 注文失敗率上昇

\- プロセス停止

\- データ欠損



\---



\## 4. アクションレベル



\### Level 1（警告）

\- ログ記録のみ

\- 通常運用継続



\### Level 2（注意）

\- 新規エントリー制限

\- risk強化モード



\### Level 3（危険）

\- 新規注文停止

\- 監視強化



\### Level 4（緊急停止）

\- 全注文停止

\- executionフリーズ

\- 手動復旧待ち



\---



\## 5. 復旧ルール



\- monitoringが正常復帰を確認

\- riskが安全状態を再評価

\- executionを段階的に再開



\---



\## 6. 原則



「止める判断は速く、戻す判断は慎重に」


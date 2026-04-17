# HANDOFF

## 現在の状況
- Phase 1 ほぼ完了（D-U-N-S申請のみ Apple側の問題で詰まり中）
- 屋号「P3 Craft」: 確定
- **事業所住所確定**: 〒150-0043 東京都渋谷区道玄坂1-10-8 渋谷道玄坂東急ビル2F-C（バーチャルオフィス検討は終了）
- **税務署受理済の届出書PDF**: `提出書類/P3 Craft.pdf`（屋号・住所行に赤線、本体＋受理メール詳細を1ファイルに結合）
- ドメイン: p3craft.com 取得済み（Cloudflare）
- メール: info@p3craft.com 稼働中
- Webサイト: Cloudflare Pagesにデプロイ済み（SEO対策込み）
- ロゴ: 仮ロゴ使用中

## D-U-N-S番号（2026-04-17 確認済み）
**D-U-N-S番号: 699016309** ✅
- 2026-04-15 東京商工リサーチから申請
- 2026-04-17 Apple公式lookupで確認済み（自動入力スクリプトで検索）

**注意**: 以前誤って送信されたP3, K.K.のD-U-N-S番号は使わないこと。

## 次のアクション（4/21 月曜 9:00以降）
1. **Apple Developerサポートに電話: 0120-9333-88**（月〜金 9:00〜17:00）
   - 伝えること:
     - 「個人事業主だが、D-U-N-S番号を取得済み。組織として登録したい」
     - D-U-N-S番号: 699016309
     - 屋号: P3 Craft
     - ドメインメール: info@p3craft.com
     - Webサイト: p3craft.com
   - 追加書類を求められる可能性あり:
     - 開業届PDF: `提出書類/P3 Craft.pdf`
     - 身分証明書（運転免許証 or マイナンバーカード）
   - 参考事例: https://qiita.com/GoHiromi/items/890de3fe5811d357e4bc
2. Apple Developer承認後 → Google Play Developer 登録

## 保留事項
- ロゴデザイン: ユーザーが手書きスケッチを準備してから再検討
- Thunderbird設定: メールが必要になったタイミングで

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- Wrangler CLI でデプロイ可能: `npx wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true`
- GitHubリポジトリ: nock-in-mook/P3-Craft

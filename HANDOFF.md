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

## D-U-N-S申請の状況（2026-04-15）
**東京商工リサーチ（D&B Japan）がD&Bへ申請送信** ✅
- 2026-04-15 東京商工リサーチから「本日D&Bへ申請を出した」と連絡
- D-U-N-S番号発行 → D&B本体DB反映 → Apple側lookup同期 の流れを待つ

**注意**: 以前誤って送信されたP3, K.K.のD-U-N-S番号は使わないこと。

## 次のアクション
1. **D-U-N-S番号の発行連絡を待つ**
2. 番号到着後、Apple公式lookup（https://developer.apple.com/enroll/duns-lookup/ ）で引けるか確認
   - 検索条件: 会社名=P3 Craft（英語表記）/ 国=Japan / 住所=申請時の住所
   - Apple lookup で引けることが Apple Developer 申請の前提
3. 引けたら Phase 2（Apple Developer / Google Play 登録）へ

## 保留事項
- ロゴデザイン: ユーザーが手書きスケッチを準備してから再検討
- Thunderbird設定: メールが必要になったタイミングで

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- Wrangler CLI でデプロイ可能: `npx wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true`
- GitHubリポジトリ: nock-in-mook/P3-Craft

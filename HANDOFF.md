# HANDOFF

## 現在の状況
- Phase 1 完了、Phase 2 進行中（Apple Developer承認済み・支払い完了）
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

## Apple Developer Program（2026-04-22 承認・支払い完了）
- **審査通過** ✅
- **$99 支払い完了** ✅
- 組織アカウントとして登録済み

## Google Play Developer 登録状況（2026-04-22）
- **アカウント作成・$25支払い完了** ✅
- アカウントID: 9069423254862487158
- 本人確認: 身分証明書アップロード済み → **審査待ち**（数日かかる）
- ウェブサイト確認: Google Search Consoleでp3craft.comの所有権確認が必要
- 電話番号確認: 本人確認完了後に対応可能
- デベロッパープロフィール: アイコン・紹介テキスト等を充実させる（後で対応）

## 次のアクション
1. **Google Play 本人確認の結果を待つ** → 通ったら電話番号確認・ウェブサイト確認
2. デベロッパープロフィールの充実（アイコン・紹介テキスト）
3. アプリ開発開始（Phase 3）
4. W-8BEN-E / W-8BEN 納税フォーム提出（リリース前までに・税理士に相談）

## 保留事項
- ロゴデザイン: ユーザーが手書きスケッチを準備してから再検討
- Thunderbird設定: メールが必要になったタイミングで

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- Wrangler CLI でデプロイ可能: `npx wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true`
- GitHubリポジトリ: nock-in-mook/P3-Craft

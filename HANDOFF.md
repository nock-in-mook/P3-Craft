# HANDOFF

## 現在の状況
- Phase 1 ほぼ完了（D-U-N-S申請のみ保留）
- 屋号準備: 完了（届出書PDF、赤丸付きセット版あり docs/）
- ドメイン: p3craft.com 取得済み（Cloudflare）
- メール: info@p3craft.com 稼働中（iCloud+カスタムドメイン）
- Webサイト: Cloudflare Pagesにデプロイ済み（SEO対策込み）
- Google Search Console: 登録済み、サイトマップ送信済み
- ロゴ: 仮ロゴ使用中、スケッチベースで後日再検討

## 保留事項
- **D-U-N-S番号申請**: バーチャルオフィスの要否を税理士に確認中（ストア公開住所と納税地の使い分け）
- **ロゴデザイン**: ユーザーが手書きスケッチを準備してから再検討
- **Thunderbird設定**: メールが必要になったタイミングで

## 次のアクション
1. 税理士の回答を受けてD-U-N-S申請（バーチャルオフィス要否で住所が変わる）
2. ロゴのスケッチ → ChatGPT等で生成 → 確定
3. D-U-N-S番号取得後 → Phase 2（Apple Developer / Google Play 登録）へ

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- Wrangler CLI でデプロイ可能: `npx wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true`
- GitHubリポジトリ: nock-in-mook/P3-Craft
- git global config 設定済み（nock-in-mook / noreply）

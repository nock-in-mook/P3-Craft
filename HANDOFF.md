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
- **D-U-N-S番号申請**: 税理士に追加質問中（開業届の事業所欄にバーチャルオフィス住所を追記してよいか）。返答待ち
  - 納税地は自宅のままでOK（一人一か所）
  - App Store公開住所 = D-U-N-S登録住所なので、自宅を載せたくなければバーチャルオフィスが必要
  - バーチャルオフィス住所が記載された公的書類（開業届等）が必要
- **ロゴデザイン**: ユーザーが手書きスケッチを準備してから再検討
- **Thunderbird設定**: メールが必要になったタイミングで

## 次のアクション
1. **税理士の返答を待つ** → 開業届にバーチャルオフィス住所追記OKなら、届出提出→D-U-N-S申請
2. ロゴのスケッチ → ChatGPT等で生成 → 確定
3. D-U-N-S番号取得後 → Phase 2（Apple Developer / Google Play 登録）へ

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- Wrangler CLI でデプロイ可能: `npx wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true`
- GitHubリポジトリ: nock-in-mook/P3-Craft
- git global config 設定済み（nock-in-mook / noreply）

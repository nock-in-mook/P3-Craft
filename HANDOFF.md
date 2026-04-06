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

## D-U-N-S申請の状況（2026-04-06）
**Apple経由の申請ルートで詰まった**。経緯：
1. https://developer.apple.com/enroll/duns-lookup/ で `P3 Craft` を検索
2. D&Bの先頭プレフィックス・マッチで八王子の無関係な「**P3, K.K.**（株式会社P3）」がヒット
3. 「該当しない」を選ぶ導線が無く、検索フォームの値がそのまま申請の法人名としてロックされる仕様
4. 検索を回避するハック（記号入りのダミー名）を試したが、ダミー名のまま登録されてしまうため使えず
5. 試しに `P3 Craft` で「続ける」を押したところ、即座に **P3, K.K. のD-U-N-S番号がメールで送信されてしまった**（番号: メール参照、`info@p3craft.com` 受信）

**重要**: メールで届いたD-U-N-S番号は **絶対に使わない**（他社のものなので、Apple Developer登録時に本人確認で弾かれる、かつ法的に問題）。

**Appleサポートに問い合わせ済（このセッション内で送信）**。返信待ち。

## 次のアクション
1. **Appleサポートからの返信を待つ** → 手動でD-U-N-S取得対応してもらえる可能性
2. ダメなら **D&B Japan（東京商工リサーチ）に直接申請**: https://www.tsr-net.co.jp/duns/
   - 個人事業主無料、約30営業日
3. D-U-N-S取得後 → Phase 2（Apple Developer / Google Play 登録）へ

## 保留事項
- ロゴデザイン: ユーザーが手書きスケッチを準備してから再検討
- Thunderbird設定: メールが必要になったタイミングで

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- Wrangler CLI でデプロイ可能: `npx wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true`
- GitHubリポジトリ: nock-in-mook/P3-Craft

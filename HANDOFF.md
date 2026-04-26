# HANDOFF

## 現在の状況
- **Phase 2 完全完了** + 屋号スローガン確定 + X アカウント開設まで完了（2026-04-27）
- 屋号「P3 Craft」: 確定
- **屋号スローガン**: 日「最小の操作で、最大の便利さを。」/ 英「Minimum effort. Maximum ease.」
- **事業所住所確定**: 〒150-0043 東京都渋谷区道玄坂1-10-8 渋谷道玄坂東急ビル2F-C
- **税務署受理済の届出書PDF**: `提出書類/P3 Craft.pdf`
- ドメイン: p3craft.com 取得済み（Cloudflare）
- メール: info@p3craft.com 稼働中
- Webサイト: スローガン入りバージョンを Cloudflare Pages にデプロイ済み（業務説明・読み方は削除しフッターに統合、ヒーローはロゴ＋スローガンのみのミニマル構成）
- **ロゴ確定**: `icons_generated/favorites/p3craft_logo_final.png`
- サイト用ロゴ `site/logo.png`: 透過済み（白角丸ロゴのみくりぬき）

## D-U-N-S番号
**D-U-N-S番号: 699016309** ✅

## Apple Developer Program ✅ 全完了
- 審査通過・$99支払い完了・有料アプリ契約署名・銀行口座追加・W-8BEN-E提出（源泉徴収0%）・EU DSA対応

## Google Play Developer ✅ 全完了
- アカウントID: 9069423254862487158
- アカウント作成・$25支払い・本人確認・お支払いプロファイル作成・W-8BEN提出・ウェブサイト確認・電話番号確認・15%手数料プログラム登録
- **デベロッパープロフィール**: アイコン＋ヘッダー画像 Play Console にアップ済み

## X (Twitter) アカウント ✅ 開設完了
- ハンドル: **@p3_craft**
- 名前: P3 Craft
- メアド: 個人 Gmail（プラスアドレス `yagukyou+x@gmail.com`）
- プロフィール画像: 確定ロゴ1.4倍拡大版（X 円形マスク対応）
- ヘッダー画像: スローガンテキスト版（アイコンとロゴ重複を避けるため、中央にダークネイビーの英語スローガン）
- Bio: 日英バイリンガル、Website設定、メアド検索オフ済み

## 提出書類フォルダの素材
- `提出書類/P3 Craft.pdf` — 税務署受理済の開業届
- `提出書類/google_play_developer_icon.png` — 512x512、Play Console アップ済み
- `提出書類/google_play_developer_header.jpg` — 4096x2304、Play Console アップ済み
- `提出書類/x_avatar.png` — 400x400、X アップ済み（円形対応版）
- `提出書類/x_header.jpg` — 1500x500、X アップ済み（スローガンテキスト版）

## 次のアクション
1. **アプリ開発（Phase 3）の本格化** ← 本命
   - 実体は別プロジェクト: `_Apps2026/Memolette-Flutter/`, `_Apps2026/Reminder_Flutter/`
   - P3 Craft プロジェクトでの追加作業はほぼなし
2. **ROADMAP 土台3点で残り**: 投稿テンプレ準備、ASO 準備調査
3. （後回しOK）デベロッパープロフィール充実、X 投稿開始

## SEO対策状況
- ピースリークラフト/P3クラフト等のカタカナ表記を title/description/keywords/JSON-LD/本文/フッターに追加
- Search Console でURL検査→インデックス登録リクエスト済み、サイトマップ送信済み

## 保留事項
- Thunderbird設定: メールが必要になったタイミングで
- フォント Inter ExtraBold のローカル導入（X ヘッダーのテキストフォントをロゴと統一したい時、現在は Arial Bold で代用）

## Drive 同期事故対策（重要）
- 別 PC 作業後の Drive 同期で `.git/` が巻き戻る事故が再発（今セッション #13 でも発生）
- CLAUDE.md に対策ルール（Step 0: fetch → status -sb → behind なら pull/reset）が追加された
- 今セッション内でも `git reset --hard origin/main` で対応
- ローカルに残ってる `_(1)_` 付き重複ファイル（`icons_generated (1)/`, `site/logo (1).png`, `tools/*(1).*`）は Drive 同期コンフリクトの残骸 → **次セッションで手動削除可**

## 技術メモ
- Cloudflare Pages プロジェクト名: p3craft
- デプロイ: `wrangler pages deploy site --project-name p3craft --branch main --commit-dirty=true` （要 `CLOUDFLARE_API_TOKEN`、`shared-env` から source）
- GitHubリポジトリ: nock-in-mook/P3-Craft
- Imagen: `imagen-4.0-fast-generate-001` で素材生成。`tools/generate_*.py` 系参照
- Imagen `edit_image` (outpaint) は Vertex AI クライアント専用、API キー認証では使えない（`tools/outpaint_x_header.py` で確認済み）

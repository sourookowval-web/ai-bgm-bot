# 🎵 AI BGM BOT (GitHub Actions完全自動版)

週3回自動で60分の作業用BGM動画を生成し、YouTubeに投稿する完全自動化BOTです。

## ✨ 特徴

- **完全クラウド実行**: Windows PC不要
- **週3回自動投稿**: 月・水・金 9:00 UTC
- **AI生成音楽**: ACE-Step 1.5
- **AI生成背景**: Stable Diffusion XL Turbo
- **完全無料**: GitHub Actions の無料枠で動作

## 🚀 セットアップ手順

### 1. リポジトリ作成

GitHubで新しいリポジトリ `music-feed` を作成

### 2. ファイルをアップロード

以下のファイルをリポジトリにアップロード:
- `.github/workflows/generate-and-upload.yml`
- `scripts/` 内の全Pythonファイル
- `prompts/music_prompts.txt`
- `requirements.txt`
- `README.md`

### 3. GitHub Secrets設定

Settings > Secrets and variables > Actions で以下を設定:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

### 4. Actions有効化

Actions タブで workflows を有効化

### 5. テスト実行

Actions > "Run workflow" で手動実行

## 📊 使用リソース

- GitHub Actions: 月2,000分無料
- すべてクラウドで完結
- PC稼働不要

## 📝 ライセンス

MIT License

---

Made with ❤️ using AI

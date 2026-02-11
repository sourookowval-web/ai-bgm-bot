"""
動画作成スクリプト (ffmpeg)

機能:
    - 音楽WAVファイルと背景画像を合成
    - 60分の動画を作成
    - サムネイル画像も生成
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("output")

def create_video(audio_path, background_path, output_path):
    """
    ffmpegで音楽と背景を合成して動画を作成
    
    Args:
        audio_path: 音楽ファイルパス
        background_path: 背景画像パス
        output_path: 出力動画パス
    """
    print(f"🎬 動画作成開始")
    print(f"🎵 音楽: {audio_path}")
    print(f"🖼️  背景: {background_path}")
    
    try:
        # ffmpegコマンド
        cmd = [
            "ffmpeg",
            "-loop", "1",                          # 画像をループ
            "-i", str(background_path),            # 入力: 背景画像
            "-i", str(audio_path),                 # 入力: 音楽
            "-c:v", "libx264",                     # 動画コーデック
            "-tune", "stillimage",                 # 静止画用の最適化
            "-c:a", "aac",                         # 音声コーデック
            "-b:a", "192k",                        # 音声ビットレート
            "-pix_fmt", "yuv420p",                 # ピクセルフォーマット
            "-shortest",                           # 音声の長さに合わせる
            "-y",                                  # 上書き
            str(output_path)
        ]
        
        print("📹 ffmpeg実行中...")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10分タイムアウト
        )
        
        if result.returncode == 0:
            print(f"✅ 動画作成完了: {output_path}")
            return True
        else:
            print(f"❌ ffmpegエラー: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ タイムアウト: 動画作成に10分以上かかりました")
        return False
    except Exception as e:
        print(f"❌ 動画作成エラー: {e}")
        return False

def create_thumbnail(background_path, title, output_path):
    """
    サムネイル画像を作成
    
    Args:
        background_path: 元の背景画像
        title: 動画タイトル
        output_path: 出力サムネイルパス
    """
    print(f"🖼️  サムネイル作成開始")
    
    try:
        # 背景画像を開く
        img = Image.open(background_path)
        img = img.resize((1280, 720), Image.Resampling.LANCZOS)
        
        # 描画オブジェクト
        draw = ImageDraw.Draw(img)
        
        # 半透明の黒いオーバーレイ
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 150))
        img = img.convert('RGBA')
        img = Image.alpha_composite(img, overlay)
        img = img.convert('RGB')
        
        draw = ImageDraw.Draw(img)
        
        # テキスト描画（フォントが使えない場合はデフォルト）
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 80)
            font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
        except:
            font_title = ImageFont.load_default()
            font_subtitle = ImageFont.load_default()
        
        # タイトルテキスト
        title_text = title.upper()
        
        # テキスト位置（中央）
        bbox = draw.textbbox((0, 0), title_text, font=font_title)
        text_width = bbox[2] - bbox[0]
        text_x = (1280 - text_width) // 2
        text_y = 280
        
        # テキスト描画（影付き）
        shadow_offset = 4
        draw.text((text_x + shadow_offset, text_y + shadow_offset), title_text, 
                 font=font_title, fill=(0, 0, 0, 255))
        draw.text((text_x, text_y), title_text, 
                 font=font_title, fill=(255, 255, 255, 255))
        
        # サブタイトル
        subtitle = "60 MIN • BGM • LOFI CHILL"
        bbox2 = draw.textbbox((0, 0), subtitle, font=font_subtitle)
        text_width2 = bbox2[2] - bbox2[0]
        text_x2 = (1280 - text_width2) // 2
        text_y2 = 400
        
        draw.text((text_x2, text_y2), subtitle, 
                 font=font_subtitle, fill=(200, 200, 200, 255))
        
        # 保存
        img.save(output_path, quality=95)
        print(f"✅ サムネイル作成完了: {output_path}")
        return True
        
    except Exception as e:
        print(f"⚠️  サムネイル作成エラー: {e}")
        print("デフォルトサムネイルを作成します")
        
        # フォールバック: シンプルなサムネイル
        img = Image.new('RGB', (1280, 720), (30, 40, 80))
        img.save(output_path)
        return True

def read_metadata():
    """メタデータから情報を取得"""
    today = datetime.now().strftime('%Y-%m-%d')
    metadata_file = OUTPUT_DIR / f"{today}_metadata.txt"
    
    metadata = {}
    if metadata_file.exists():
        with open(metadata_file, 'r', encoding='utf-8') as f:
            for line in f:
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()
    
    return metadata

def main():
    """メイン処理"""
    print("=" * 60)
    print("🎬 動画作成 & サムネイル生成")
    print("=" * 60)
    
    # ファイルパス
    today = datetime.now().strftime('%Y-%m-%d')
    audio_path = OUTPUT_DIR / f"{today}_bgm.wav"
    background_path = OUTPUT_DIR / f"{today}_background.jpg"
    video_path = OUTPUT_DIR / f"{today}_video.mp4"
    thumbnail_path = OUTPUT_DIR / f"{today}_thumbnail.jpg"
    
    # ファイル存在確認
    if not audio_path.exists():
        print(f"❌ 音楽ファイルが見つかりません: {audio_path}")
        sys.exit(1)
    
    if not background_path.exists():
        print(f"❌ 背景画像が見つかりません: {background_path}")
        sys.exit(1)
    
    # メタデータ取得
    metadata = read_metadata()
    title = metadata.get('prompt', 'Chill BGM')
    
    # 動画作成
    success_video = create_video(audio_path, background_path, video_path)
    
    # サムネイル作成
    success_thumbnail = create_thumbnail(background_path, title, thumbnail_path)
    
    if success_video and success_thumbnail:
        print("")
        print("✅ 全ての処理が完了しました！")
        print(f"📁 動画: {video_path}")
        print(f"📁 サムネイル: {thumbnail_path}")
        print("")
    else:
        print("❌ 一部の処理に失敗しました")
        sys.exit(1)

if __name__ == '__main__':
    main()

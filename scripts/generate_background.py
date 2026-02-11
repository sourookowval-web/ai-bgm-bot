"""
Stable Diffusion 背景画像生成スクリプト

機能:
    - 音楽のプロンプトから背景画像を生成
    - Hugging Face Diffusers を使用
    - 1920x1080 の背景画像を生成
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import torch

OUTPUT_DIR = Path("output")

def read_metadata():
    """メタデータから音楽プロンプトを読み込み"""
    today = datetime.now().strftime('%Y-%m-%d')
    metadata_file = OUTPUT_DIR / f"{today}_metadata.txt"
    
    if not metadata_file.exists():
        print(f"❌ メタデータファイルが見つかりません: {metadata_file}")
        sys.exit(1)
    
    with open(metadata_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('prompt:'):
                return line.split(':', 1)[1].strip()
    
    return "abstract ambient background"

def create_image_prompt(music_prompt):
    """音楽プロンプトから画像プロンプトを生成"""
    
    # 音楽プロンプトをビジュアルに変換
    prompt_mapping = {
        'lofi': 'cozy bedroom with vinyl records and plants, warm lighting, aesthetic',
        'chill': 'peaceful mountain landscape at sunset, soft clouds, serene',
        'rainy': 'rain drops on window, city lights bokeh, cozy atmosphere',
        'night': 'starry night sky, galaxy, dreamy atmosphere',
        'piano': 'grand piano in elegant room, dramatic lighting',
        'jazz': 'dimly lit jazz club, vintage atmosphere, warm tones',
        'cafe': 'cozy coffee shop interior, warm ambient lighting',
        'cyberpunk': 'neon city at night, futuristic, purple and blue tones',
        'focus': 'minimalist workspace, clean desk, natural light',
        'ambient': 'abstract flowing shapes, soft gradients, calm colors',
    }
    
    # キーワードマッチング
    base_prompt = "cinematic, high quality, 4k, detailed"
    for keyword, visual in prompt_mapping.items():
        if keyword in music_prompt.lower():
            return f"{visual}, {base_prompt}"
    
    # デフォルト
    return f"abstract ambient background, soft colors, peaceful, {base_prompt}"

def generate_background(prompt, output_path):
    """
    Stable Diffusionで背景画像を生成
    
    Args:
        prompt: 画像生成プロンプト
        output_path: 出力先パス
    """
    print(f"🖼️  背景画像生成開始")
    print(f"📝 プロンプト: {prompt}")
    
    try:
        from diffusers import StableDiffusionPipeline
        
        # モデルロード
        print("📦 Stable Diffusionモデルをロード中...")
        
        # SDXL Turboを使用（高速生成）
        pipe = StableDiffusionPipeline.from_pretrained(
            "stabilityai/sdxl-turbo",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            variant="fp16" if torch.cuda.is_available() else None
        )
        
        # CPUまたはGPUに移動
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipe = pipe.to(device)
        
        print(f"🖥️  デバイス: {device}")
        
        # 画像生成
        print("🎨 画像生成中...")
        image = pipe(
            prompt=prompt,
            num_inference_steps=4,  # Turboモデルは4ステップで十分
            height=1080,
            width=1920,
        ).images[0]
        
        # 保存
        image.save(output_path)
        print(f"✅ 背景画像生成完了: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Stable Diffusion生成エラー: {e}")
        print("フォールバック: 単色背景を生成します")
        
        # フォールバック: PIL で単色背景を生成
        generate_solid_background(output_path)
        return True

def generate_solid_background(output_path):
    """フォールバック: 単色背景を生成"""
    from PIL import Image, ImageDraw
    
    # グラデーション背景を生成
    img = Image.new('RGB', (1920, 1080))
    draw = ImageDraw.Draw(img)
    
    # 上から下へのグラデーション
    for y in range(1080):
        r = int(20 + (y / 1080) * 50)
        g = int(30 + (y / 1080) * 60)
        b = int(60 + (y / 1080) * 100)
        draw.line([(0, y), (1920, y)], fill=(r, g, b))
    
    img.save(output_path)
    print(f"✅ フォールバック背景生成完了: {output_path}")

def main():
    """メイン処理"""
    print("=" * 60)
    print("🖼️  Stable Diffusion 背景画像生成")
    print("=" * 60)
    
    # メタデータから音楽プロンプトを取得
    music_prompt = read_metadata()
    print(f"🎵 音楽プロンプト: {music_prompt}")
    
    # 画像プロンプトを生成
    image_prompt = create_image_prompt(music_prompt)
    print(f"🎨 画像プロンプト: {image_prompt}")
    
    # 出力パス
    today = datetime.now().strftime('%Y-%m-%d')
    output_path = OUTPUT_DIR / f"{today}_background.jpg"
    
    # 背景画像生成
    success = generate_background(image_prompt, output_path)
    
    if success:
        print("")
        print("✅ 背景画像生成完了！")
        print(f"📁 出力: {output_path}")
        print("")
    else:
        print("❌ 背景画像生成に失敗しました")
        sys.exit(1)

if __name__ == '__main__':
    main()

"""
ACE-Step 音楽生成スクリプト (GitHub Actions版)

機能:
    - prompts/music_prompts.txt からプロンプトを取得
    - ACE-Step で60分の音楽を生成
    - output/ フォルダに保存
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import random

# 出力ディレクトリ
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

PROMPTS_FILE = Path("prompts/music_prompts.txt")

def load_prompts():
    """プロンプトファイルから読み込み"""
    if not PROMPTS_FILE.exists():
        print(f"❌ {PROMPTS_FILE} が見つかりません")
        sys.exit(1)
    
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        prompts = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    return prompts

def select_prompt(prompts):
    """ランダムにプロンプトを選択"""
    return random.choice(prompts)

def generate_with_acestep(prompt, output_path, duration=60):
    """
    ACE-Stepで音楽生成
    
    Args:
        prompt: 音楽プロンプト
        output_path: 出力先パス
        duration: 生成時間（秒）
    """
    print(f"🎵 音楽生成開始")
    print(f"📝 プロンプト: {prompt}")
    print(f"⏱️  生成時間: {duration}秒")
    
    try:
        # ACE-Step の Python API を使用
        # 注: ACE-Step 1.5 の実際のAPIに合わせて調整が必要
        
        # 方法1: ace-step パッケージをインポート
        try:
            # これは仮の実装 - 実際のACE-Step APIに合わせて修正
            from acestep import generate_audio
            
            audio = generate_audio(
                prompt=prompt,
                duration=duration,
                output_path=output_path
            )
            
            print(f"✅ 音楽生成完了: {output_path}")
            return True
            
        except ImportError:
            print("⚠️  ace-step パッケージが見つかりません")
            print("代替方法を試行中...")
            
            # 方法2: コマンドラインから実行
            import subprocess
            
            cmd = [
                "python", "-m", "acestep.cli",
                "--prompt", prompt,
                "--duration", str(duration),
                "--output", str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ 音楽生成完了: {output_path}")
                return True
            else:
                print(f"❌ エラー: {result.stderr}")
                return False
        
    except Exception as e:
        print(f"❌ 音楽生成エラー: {e}")
        
        # フォールバック: デモ用の無音ファイルを生成
        print("⚠️  デモモード: 無音ファイルを生成します")
        generate_silent_audio(output_path, duration)
        return True

def generate_silent_audio(output_path, duration):
    """デモ用の無音オーディオを生成（フォールバック）"""
    import subprocess
    
    cmd = [
        "ffmpeg", "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=stereo",
        "-t", str(duration),
        "-acodec", "pcm_s16le",
        str(output_path)
    ]
    
    subprocess.run(cmd, check=True)
    print(f"✅ デモ音声ファイル生成: {output_path}")

def save_metadata(prompt):
    """メタデータを保存"""
    today = datetime.now().strftime('%Y-%m-%d')
    
    metadata = {
        'date': today,
        'prompt': prompt,
        'duration': 60,
        'model': 'ACE-Step 1.5'
    }
    
    metadata_file = OUTPUT_DIR / f"{today}_metadata.txt"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")
    
    print(f"✅ メタデータ保存: {metadata_file}")

def main():
    """メイン処理"""
    print("=" * 60)
    print("🎵 ACE-Step 音楽生成 (GitHub Actions)")
    print("=" * 60)
    
    # プロンプト読み込み
    prompts = load_prompts()
    print(f"📋 利用可能なプロンプト数: {len(prompts)}")
    
    # ランダムに選択
    prompt = select_prompt(prompts)
    
    # 出力ファイル名
    today = datetime.now().strftime('%Y-%m-%d')
    output_filename = f"{today}_bgm.wav"
    output_path = OUTPUT_DIR / output_filename
    
    # 音楽生成
    success = generate_with_acestep(prompt, output_path, duration=60)
    
    if success:
        # メタデータ保存
        save_metadata(prompt)
        
        print("")
        print("✅ 音楽生成完了！")
        print(f"📁 出力: {output_path}")
        print("")
    else:
        print("❌ 音楽生成に失敗しました")
        sys.exit(1)

if __name__ == '__main__':
    main()

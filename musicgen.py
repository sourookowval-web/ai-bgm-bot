from audiocraft.models import MusicGen
import torchaudio

def generate_music(prompt):
    model = MusicGen.get_pretrained("small")
    model.set_generation_params(duration=600)  # 10分
    wav = model.generate([prompt])[0]
    torchaudio.save("music.wav", wav.unsqueeze(0), 32000)

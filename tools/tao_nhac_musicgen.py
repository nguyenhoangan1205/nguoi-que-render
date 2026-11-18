"""Tạo nhạc nền không lời bằng MusicGen-small (Meta, mã nguồn mở) trên CPU của GitHub Actions.
Đọc phiếu jobs-nhac/<ten>.json: {"ten", "mo_ta" (tiếng Anh), "so_doan" (mỗi đoạn 30 giây), "seed"}.
Các đoạn cùng mô tả, khác seed, nối bằng crossfade 3 giây -> nhac/<ten>.mp3 (chuẩn hoá -20 LUFS, fade vào/ra).
Cách làm theo nature_studio/musicgen.py của repo thien-nhien-hung-vy."""
import json, subprocess, sys, tempfile
from pathlib import Path

import numpy as np
import scipy.io.wavfile
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

job = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
ten, prompt, n, seed = job["ten"], job["mo_ta"], int(job.get("so_doan", 5)), int(job.get("seed", 57))
proc = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
rate = model.config.audio_encoder.sampling_rate
tmp = Path(tempfile.mkdtemp())
files = []
for i in range(n):
    torch.manual_seed(seed + i)
    inp = proc(text=[prompt], padding=True, return_tensors="pt")
    with torch.no_grad():
        a = model.generate(**inp, do_sample=True, guidance_scale=3.0,
                           max_new_tokens=int(30 * model.config.audio_encoder.frame_rate) + 5)
    w = a[0, 0].cpu().numpy()
    w = w / max(1e-6, float(np.abs(w).max())) * 0.9
    f = tmp / f"d{i}.wav"
    scipy.io.wavfile.write(f, rate, (w * 32767).astype(np.int16))
    files.append(f)
    print("đoạn", i + 1, "/", n, flush=True)
# nối crossfade 3 giây
cmd, flt, last = ["ffmpeg", "-v", "error", "-y"], [], "[0:a]"
for f in files:
    cmd += ["-i", str(f)]
for i in range(1, n):
    out = f"[x{i}]"
    flt.append(f"{last}[{i}:a]acrossfade=d=3:c1=tri:c2=tri{out}")
    last = out
total = 30 * n - 3 * (n - 1)
flt.append(f"{last}afade=t=in:d=2,afade=t=out:st={total-4}:d=4,loudnorm=I=-20[o]")
Path("nhac").mkdir(exist_ok=True)
cmd += ["-filter_complex", ";".join(flt), "-map", "[o]", "-ar", "44100", "-c:a", "libmp3lame", "-b:a", "192k", f"nhac/{ten}.mp3"]
subprocess.run(cmd, check=True)
print("xong nhac/%s.mp3, khoảng %d giây" % (ten, total))

"""Render một đoạn khung của một scene trong file .blend ra PNG (Cycles CPU).

blender -b phim.blend --python render_blender_doan.py -- <scene> <khung_dau> <khung_cuoi> <phan_tram> <samples> <thu_muc_ra>
Ảnh ra: <thu_muc_ra>/<scene>/0001.png ... (đánh số theo khung của scene).
Máy quay đổi theo marker trong timeline vẫn giữ nguyên khi render.
"""
import bpy, sys, os
scene, s, e, pct, spp, out = sys.argv[sys.argv.index("--") + 1:]
sc = bpy.data.scenes[scene]
r = sc.render
r.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = int(spp)
sc.cycles.use_denoising = True
try:
    sc.cycles.denoiser = "OPENIMAGEDENOISE"
except Exception:
    pass
r.resolution_percentage = int(pct)
r.use_persistent_data = True
r.image_settings.file_format = "PNG"
r.image_settings.color_mode = "RGB"
sc.frame_start, sc.frame_end = int(s), int(e)
r.filepath = os.path.join(out, scene, "####")
bpy.ops.render.render(animation=True, scene=sc.name)
print("XONG", scene, s, e)

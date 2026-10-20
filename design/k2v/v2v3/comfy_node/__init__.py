"""NC-V2V3 · nút ComfyUI tối thiểu: đọc chuỗi PNG/JPG (JPG q95 chỉ cho khung điều khiển B — vùng giữ được ghép lại từ PNG nguồn sau cùng), ghi PNG không mất mát (khung nguồn, bản đồ độ sâu, cạnh, mặt nạ) — tránh nén video trung gian.
  V2V3LoadFrames(dir, start, count) → IMAGE [N,H,W,3] float 0..1, MASK [N,H,W] (kênh R/255; ô trắng = AI được vẽ)
  V2V3SaveFrames(images, dir)       → PNG 8 bit %05d.png"""
import glob, os
import numpy as np, torch
from PIL import Image


class V2V3LoadFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"dir": ("STRING", {"default": ""}), "start": ("INT", {"default": 0, "min": 0, "max": 100000}), "count": ("INT", {"default": 81, "min": 1, "max": 100000})}}
    RETURN_TYPES = ("IMAGE", "MASK"); FUNCTION = "load"; CATEGORY = "v2v3"

    def load(self, dir, start, count):
        fs = sorted(glob.glob(os.path.join(dir, "*.png")) + glob.glob(os.path.join(dir, "*.jpg")))[start:start + count]
        if not fs: raise ValueError(f"không có PNG trong {dir}")
        a = np.stack([np.asarray(Image.open(f).convert("RGB"), dtype=np.float32) / 255.0 for f in fs])
        t = torch.from_numpy(a); return (t, t[..., 0].clone())


class V2V3SaveFrames:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"images": ("IMAGE",), "dir": ("STRING", {"default": ""})}}
    RETURN_TYPES = (); FUNCTION = "save"; OUTPUT_NODE = True; CATEGORY = "v2v3"

    def save(self, images, dir):
        os.makedirs(dir, exist_ok=True)
        for i, im in enumerate(images.cpu().numpy()):
            Image.fromarray(np.clip(im * 255.0 + 0.5, 0, 255).astype(np.uint8)).save(os.path.join(dir, f"{i:05d}.png"), compress_level=1)
        return {}


NODE_CLASS_MAPPINGS = {"V2V3LoadFrames": V2V3LoadFrames, "V2V3SaveFrames": V2V3SaveFrames}

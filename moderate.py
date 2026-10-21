import os, torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

m = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
p = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

L = {
    "weapon": "a photo of a person holding a gun or knife",
    "violence": "a photo of people fighting",
    "blood": "a photo of blood or injury",
    "smoking": "a photo of a person smoking",
    "alcohol": "a photo of alcoholic drinks",
    "safe": "a normal everyday photo",
}
k, t = list(L), list(L.values())
flags = []

for f in sorted(x for x in os.listdir("frames") if x.endswith(".jpg")):
    im = Image.open(f"frames/{f}")
    x = p(text=t, images=im, return_tensors="pt", padding=True)
    with torch.no_grad():
        s = m(**x).logits_per_image.softmax(1)[0]
    i = s.argmax().item()
    ts = f.split("_")[1][:-4]
    print(f"{ts:>6}  {k[i]:<9} {s[i]*100:.1f}%")
    if k[i] != "safe" and s[i] > 0.5:
        flags.append((ts, k[i]))

print("\nverdict:", "FLAGGED" if flags else "SAFE")
for ts, l in flags:
    print(f"  {ts}  {l}")
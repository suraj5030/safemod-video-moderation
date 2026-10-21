import cv2, os

v = cv2.VideoCapture("/Users/surajchannappanavar/Downloads/7231661-uhd_2160_3840_25fps.mp4")
fps = v.get(cv2.CAP_PROP_FPS)
os.makedirs("frames", exist_ok=True)
i = n = 0

while True:
    ok, f = v.read()
    if not ok: break
    if i % int(fps) == 0:
        cv2.imwrite(f"frames/{n:03d}_{i/fps:.1f}s.jpg", f)
        n += 1
    i += 1

print(f"{n} frames from {i} total")
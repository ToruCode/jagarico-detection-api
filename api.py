from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from ultralytics import YOLO
import cv2
import os
import uuid
import shutil
from collections import Counter

app = FastAPI()
model = YOLO("best.pt")  # あなたの学習済みモデル（.pt）

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# クラスごとの色（BGR形式）
COLOR_MAP = {
    "cheese": (0, 0, 255),       # 赤
    "jaga_butter": (255, 0, 0),  # 青
    "salad": (0, 255, 0)         # 緑
}

@app.post("/predict/jagarico")
async def predict_jagarico(file: UploadFile = File(...)):
    # 一時ファイル名を作成
    file_ext = os.path.splitext(file.filename)[1]
    temp_filename = f"{uuid.uuid4()}{file_ext}"
    input_path = os.path.join(UPLOAD_DIR, temp_filename)

    # ファイルを保存
    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # YOLOで予測
    results = model(input_path)
    result = results[0]

    # クラス名の取得
    names = model.names
    class_ids = [int(box.cls[0]) for box in result.boxes]
    labels = [names[class_id] for class_id in class_ids]
    counts = Counter(labels)

    # 画像読み込み（OpenCV）
    image_np = cv2.imread(input_path)

    # ===============================
    # 上部ラベル（種類と本数）を大きく・色分けして描画
    # ===============================
    text_lines = [f"{label}: {count}" for label, count in counts.items()]
    start_y = 200         # ← 表示開始位置（少し下に）
    line_height = 160    # ← 各行の間隔（重なり防止）

    for i, line in enumerate(text_lines):
        y = start_y + i * line_height
        label = line.split(":")[0]
        color = COLOR_MAP.get(label, (0, 0, 255))  # デフォルト赤
        cv2.putText(image_np, line, (40, y), cv2.FONT_HERSHEY_SIMPLEX,
                    6.0, color, 12)  # サイズ大・太さ太め

    # ===============================
    # バウンディングボックスとラベル（色付き・大きめ）
    # ===============================
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        conf = float(box.conf[0])
        label_name = names[cls_id]
        label = f"{label_name} {conf:.2f}"
        color = COLOR_MAP.get(label_name, (255, 255, 255))  # デフォルト白

        # ボックス＆ラベル描画
        cv2.rectangle(image_np, (x1, y1), (x2, y2), color, 8)
        cv2.putText(image_np, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                    2.0, color, 4)

    # 出力画像の保存
    output_path = os.path.join(OUTPUT_DIR, f"pred_{temp_filename}")
    cv2.imwrite(output_path, image_np)

    # 結果画像を返却
    return FileResponse(output_path, media_type="image/jpeg")

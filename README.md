# じゃがりこ物体検出 API（YOLOv8 × FastAPI）

本プロジェクトは、YOLOv8を用いた物体検出モデルをFastAPIでAPI化したものです。

単にモデルを学習するだけでなく、

- 推論パイプライン設計
- API構築
- 再現性のある環境構築
- エラーハンドリング
- 推論時間計測

までを一貫して実装しています。

---

## 🧠 背景

本プロジェクトは、物体検出モデルを「実運用を想定したAPI」として構築することを目的に作成しました。

データ数は135枚と少規模ですが、

- 少量データでの学習設計
- 過学習への配慮
- 推論速度の可視化
- APIとしての拡張性

を重視しています。

---

## 🛠 使用技術

- Python 3.11
- YOLOv8（Ultralytics）
- PyTorch
- FastAPI
- Uvicorn
- OpenCV
- python-multipart

---

## 📂 データセット

- クラス数：3
  - サラダ味
  - チーズ味
  - じゃがバター味
- 画像数：135枚
- アノテーション形式：Polygon
- 学習環境：Google Colab

---

## 📦 プロジェクト構成
├── api.py

├── requirements.txt

├── .gitignore

├── uploads/

├── output/

---

## 🚀 環境構築

```bash
python -m venv venv
# Windowsの場合
.\venv\Scripts\activate
pip install -r requirements.txt
```

---

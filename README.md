# Image Processing CLI (ImageApp)

このリポジトリは、コマンドラインで画像変換を行う小さなツール群を提供します。OpenCV を使って以下の操作をサポートします。

- リサイズ（任意の幅・高さへ）
- 量子化（K-means による色数削減）
- スケール（縮小して最近傍で拡大するピクセル化効果）
- MMPX 拡大（ドット絵向けのスタイル保持 2x 伸張）
- 一括 MMPX 拡大（フォルダ配下のドット絵をまとめて 2x 化）
- PNG→PDF 変換（アルファを白背景に敷きつめて PDF 化）
- 一括リサイズ（フォルダ構成を維持したまま別ルートへ出力）
- パディング（指定ピクセル分だけ周囲を一定値で埋める）
- 一括パディング（フォルダ配下を丸ごと一定値で囲う）

## 必要要件

- Python 3.8+
- Windows / macOS / Linux（OpenCV がサポートする環境）
- 依存パッケージ: `opencv-python`, `numpy`
	- PNG→PDF を使う場合は `Pillow`

依存関係は `setup.py` の `install_requires` に記載されています。

## インストール

開発中にローカルで試す場合（リポジトリルートで実行）：

```powershell
pip install -e .
```

通常インストール：

```powershell
pip install .
```

これにより、コンソールスクリプト `ImageApp` がインストールされます（`setup.py` の `entry_points` を使用）。

または直接実行する場合：

```powershell
python -m image_app.cli --help
```

## 使い方（コマンドと例）

インストール済みなら `ImageApp` を使います。まだなら `python -m image_app.cli` を使用してください。

- Resize（幅・高さを指定）

```powershell
ImageApp resize input.jpg --width 800 --height 600 --output out_resized.jpg
```

- Quantize（色数を `k` に削減）

```powershell
ImageApp quantize input.jpg --k 8 --output out_quantized.jpg
```

- Scale（スケール値で縮小→最近傍で再拡大）

```powershell
ImageApp scale input.png --scale 4 --output out_scaled.png
```

- MMPX（Morgan McGuire / Mara Gagiu 提案の 2x 拡大フィルタ）

```powershell
ImageApp mmpx sprite.png --output sprite@2x.png
```

ドット絵の輪郭や 45 度・27 度斜線を保ったまま 2 倍化します。アルファチャンネルや元のパレットを保持します。

- Batch MMPX（ドット絵をフォルダ単位で一括拡大）

```powershell
ImageApp batch-mmpx path\to\src path\to\dist --ext .png .bmp
```

`--ext` で対象拡張子を列挙します（省略時は `.png .jpg .jpeg .bmp`）。入力フォルダ基準のサブフォルダ構成を保ったまま 2x の結果を `output_root` に保存します。

- PNG→PDF（ファイルを 1:1 で PDF 化）

```powershell
ImageApp png2pdf input.png --output output.pdf
```

- Batch Resize（指定フォルダ配下をすべてリサイズして別ルートへ保存）

```powershell
ImageApp batch-resize path\to\src path\to\dist --width 1024 --height 1024 --ext .png .jpg
```

`--ext` は処理対象の拡張子を列挙します（省略すると `.png .jpg .jpeg .bmp`）。サブフォルダ構成は入力フォルダを基準にそのまま再現され、出力先の親フォルダのみが変わります。

- Pad（周囲を一定値でパディング）

```powershell
ImageApp pad input.png --padding 1 --value 255 --output padded.png
```

`--padding` で上下左右すべてに追加するピクセル数を指定します。`--value` を省略すると、透過チャネル付き画像では透明 (0,0,0,0)、それ以外は黒で埋めます。値を指定する場合は 0〜255 の範囲になります。

- Batch Pad（フォルダ配下を再帰的にパディングし、構造を保ったまま出力）

```powershell
ImageApp batch-pad path\to\src path\to\dist --padding 1 --value 255 --ext .png .jpg
```

`--ext` の仕様は `batch-resize` と同じです。`--value` を省略すると単体コマンド同様に黒／透明が自動選択されます。指定した場合は 0〜255 にクランプされ、`--padding` は全方向へ同じ幅で追加されます。

各コマンドは `--output` を省略するとデフォルトのファイル名に保存します（`cli.py` に定義）。

## 実装メモ / 注意点

- 入力画像の読み込みに失敗すると `cv2.imread` は `None` を返します。パスが正しいか、ファイルが読み取り可能か確認してください。
- `quantize` の `k` は整数で、通常 `1 <= k <= 256` 程度を指定します。小さい値にすると色情報が大幅に失われます。
- `scale` の `--scale` は整数（例: 2, 3, 4）。`scale` が 1 の場合は効果がありません。非常に大きな値を使うと情報が薄くなるかもしれません。
- 出力画像のフォーマットは指定したファイル拡張子に依存します（OpenCV が対応する形式に保存されます）。

## リポジトリ構成（主なファイル）

- `image_app/cli.py` — CLI 定義とサブコマンドの接続
- `image_app/resize.py` — `resize(input, width, height, output)`
- `image_app/quantize.py` — `quantize(input, k, output)`
- `image_app/resize_scale.py` — `resize_scale(input, scale, output)`
- `image_app/mmpx.py` — `mmpx_scale2x(input, output)`
- `image_app/batch_mmpx.py` — `batch_mmpx(input_dir, output_root, extensions)`
- `image_app/png_to_pdf.py` — `png_to_pdf(input, output)`
- `image_app/batch_resize.py` — `batch_resize(input_dir, output_root, width, height, extensions)`
- `image_app/pad.py` — `pad_image(input, padding, output, value)`
- `image_app/batch_pad.py` — `batch_pad(input_dir, output_root, padding, value, extensions)`
- `setup.py` — インストール設定（コンソールスクリプト登録）

## トラブルシューティング

- OpenCV の読み込みエラーが出た場合は、`pip install opencv-python` を再実行してみてください。環境によっては `opencv-python-headless` を検討します（GUI を使わない場合）。
- 大量の画像を処理する場合はスクリプトをループで呼ぶか、自動化（バッチ）を用意してください。

## ライセンス & 貢献

- 現在ライセンスファイルは含まれていません。適切なライセンスを追加してください。
- バグ修正や機能追加の PR を歓迎します。

---

作成日時: 2025-11-18

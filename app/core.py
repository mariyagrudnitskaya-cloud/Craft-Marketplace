from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import json
import uuid
import os
import math

BASE_STATIC_DIR = "static"

def load_palette(palette_id: str):
    """Загружает JSON-файл палитры по ID"""
    path = os.path.join("app", "palettes", "data", palette_id, "palette.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def rgb_distance(c1, c2):
    """Простая метрика сравнения цветов"""
    return sum((a - b) ** 2 for a, b in zip(c1, c2))

def process_image_to_mosaic(image_bytes, cells_width, cells_height, palette_id="partner_A"):
    """Главная функция: обрабатывает изображение и строит мозаику"""

    # Загружаем палитру
    palette = load_palette(palette_id)

    # Загружаем изображение
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.resize((cells_width, cells_height))

    # Преобразуем в массив numpy
    img_array = np.array(image)
    h, w, _ = img_array.shape

    # Список всех цветов палитры
    palette_rgbs = [tuple(c["rgb"]) for c in palette]
    palette_codes = [c["partner_code"] for c in palette]

    # Матрица для хранения индексов цветов
    color_ids = np.zeros((h, w), dtype=int)

    # Маппинг пикселей под палитру
    for y in range(h):
        for x in range(w):
            pixel = tuple(img_array[y, x])
            best_idx = 0
            best_dist = float("inf")
            for i, rgb in enumerate(palette_rgbs):
                d = rgb_distance(pixel, rgb)
                if d < best_dist:
                    best_dist = d
                    best_idx = i
            color_ids[y, x] = best_idx
            img_array[y, x] = palette_rgbs[best_idx]

    # Считаем количество ячеек каждого цвета
    unique, counts = np.unique(color_ids, return_counts=True)
    color_stats = dict(zip(unique, counts))

    # Создаём таблицу цветов
    colors_table = []
    for i, count in color_stats.items():
        code = palette[i]["partner_code"]
        rgb = palette[i]["rgb"]
        color_item = {
            "symbol": f"C{i+1}",
            "partner_code": code,
            "rgb": rgb,
            "count_cells": int(count),
            "count_with_reserve": math.ceil(count * 1.1)
        }
        colors_table.append(color_item)

    # Генерируем изображения
    uid = str(uuid.uuid4())
    os.makedirs(BASE_STATIC_DIR, exist_ok=True)
    preview_path = os.path.join(BASE_STATIC_DIR, f"{uid}_preview.png")
    grid_path = os.path.join(BASE_STATIC_DIR, f"{uid}_grid.png")

    # Превью мозаики
    preview_image = Image.fromarray(img_array)
    preview_image.save(preview_path)

    # Сетка для печати
    cell_size = 20
    grid_img = Image.new("RGB", (w * cell_size, h * cell_size), "white")
    draw = ImageDraw.Draw(grid_img)
    font = ImageFont.load_default()

    for y in range(h):
        for x in range(w):
            color_idx = color_ids[y, x]
            symbol = f"C{color_idx+1}"
            cx, cy = x * cell_size, y * cell_size
            draw.rectangle([cx, cy, cx + cell_size, cy + cell_size], outline="gray", width=1)
            draw.text((cx + 4, cy + 4), symbol, fill="black", font=font)

    grid_img.save(grid_path)

    # Формируем ответ
    result = {
        "preview_image_url": f"/static/{uid}_preview.png",
        "grid_image_url": f"/static/{uid}_grid.png",
        "colors_table": colors_table,
        "tech_spec": {
            "product_type": "diamond_mosaic",
            "palette_id": palette_id,
            "canvas": {
                "cells_width": cells_width,
                "cells_height": cells_height,
                "size_cm_width": round(cells_width * 0.25, 2),
                "size_cm_height": round(cells_height * 0.25, 2)
            },
            "images": {
                "preview": f"/static/{uid}_preview.png",
                "grid": f"/static/{uid}_grid.png"
            },
            "colors": colors_table
        }
    }

    return result


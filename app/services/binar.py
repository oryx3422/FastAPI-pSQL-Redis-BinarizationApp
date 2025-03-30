import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from fastapi import APIRouter, HTTPException

router = APIRouter()


def bradley_threshold(image_base64: str) -> str:
    # Декодируем изображение из base64
    try:
        image_data = base64.b64decode(image_base64.split(',')[1])
    except IndexError:
        raise HTTPException(status_code=400, detail="Некорректный формат изображения")

    image = Image.open(BytesIO(image_data)).convert('L')
    src = np.array(image)

    height, width = src.shape
    S = width // 8
    s2 = S // 2
    t = 0.15

    # Вычисление интегрального изображения
    integral_image = cv2.integral(src)

    res = np.zeros_like(src, dtype=np.uint8)

    # Поиск локальных областей и вычисление порогов
    for i in range(width):
        for j in range(height):
            x1 = max(0, i - s2)
            x2 = min(width - 1, i + s2)
            y1 = max(0, j - s2)
            y2 = min(height - 1, j + s2)

            count = (x2 - x1) * (y2 - y1)

            sum_val = (
                integral_image[y2 + 1, x2 + 1]
                - integral_image[y1, x2 + 1]
                - integral_image[y2 + 1, x1]
                + integral_image[y1, x1]
            )

            if int(src[j, i]) * count < sum_val * (1.0 - t):  # Исправлено: явное приведение к int
                res[j, i] = 0
            else:
                res[j, i] = 255

    # Преобразование результата в изображение
    result_image = Image.fromarray(res)
    buffered = BytesIO()
    result_image.save(buffered, format="PNG")

    # Кодирование результата в base64
    result_base64 = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')

    return result_base64




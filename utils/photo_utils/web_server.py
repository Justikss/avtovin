from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

from insert_watermark import insert_watermark

# Импортируйте ваш метод insert_watermark из соответствующего файла


app = FastAPI()

class WatermarkRequest(BaseModel):
    photo_list: List[str]

@app.post("/watermark/")
async def watermark_photos(request: WatermarkRequest):
    try:
        # Вызов вашей асинхронной функции insert_watermark
        result_paths = await insert_watermark(request.photo_list)
        return {"file_paths": result_paths}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Если ваша функция не асинхронная, используйте обычный вызов без await

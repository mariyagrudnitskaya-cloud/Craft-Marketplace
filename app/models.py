from pydantic import BaseModel
from typing import List

class ColorItem(BaseModel):
    symbol: str
    partner_code: str
    name: str | None = None
    rgb: List[int]
    count_cells: int
    count_with_reserve: int

class CanvasInfo(BaseModel):
    cells_width: int
    cells_height: int
    size_cm_width: float
    size_cm_height: float

class ImagesInfo(BaseModel):
    preview: str
    grid: str

class TechSpec(BaseModel):
    product_type: str
    palette_id: str
    canvas: CanvasInfo
    images: ImagesInfo
    colors: List[ColorItem]

class MosaicResponse(BaseModel):
    preview_image_url: str
    grid_image_url: str
    colors_table: List[ColorItem]
    tech_spec: TechSpec

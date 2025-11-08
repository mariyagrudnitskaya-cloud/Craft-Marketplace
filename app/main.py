from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Handcraft Kits Core")

class OrderRequest(BaseModel):
    kit_type: str
    size_width_cm: int
    size_height_cm: int
    image_url: Optional[str] = None
    partner_id: Optional[str] = None

@app.get("/")
def root():
    return {"status": "ok", "message": "Core is alive"}

@app.post("/order/create")
def create_order(order: OrderRequest):
    fake_order_id = "ORD-0001"
    return {
        "status": "ok",
        "order_id": fake_order_id,
        "kit_type": order.kit_type,
        "size": {
            "width_cm": order.size_width_cm,
            "height_cm": order.size_height_cm
        },
        "partner_id": order.partner_id,
        "debug_info": "Core stub response. Logic will be implemented later."
    }

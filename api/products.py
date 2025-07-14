from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from database import get_session
from services.inventory_service import InventoryService
from models.product import ProductResponse, ProductCreate, ProductCategory

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(
    category: Optional[ProductCategory] = Query(None),
    brand: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    inventory_service = InventoryService(session)
    
    if search:
        products = await inventory_service.search_products(search)
    elif category:
        products = await inventory_service.get_products_by_category(category)
    elif brand:
        products = await inventory_service.get_products_by_brand(brand)
    else:
        products = await inventory_service.get_all_products()
    
    return products

@router.get("/summary")
async def get_inventory_summary(session: AsyncSession = Depends(get_session)):
    inventory_service = InventoryService(session)
    return await inventory_service.get_inventory_summary()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, session: AsyncSession = Depends(get_session)):
    inventory_service = InventoryService(session)
    product = await inventory_service.get_product_by_id(product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return product

@router.post("/", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    inventory_service = InventoryService(session)
    return await inventory_service.create_product(product)

@router.put("/{product_id}/stock")
async def update_product_stock(
    product_id: int,
    new_stock: int = Query(..., ge=0),
    session: AsyncSession = Depends(get_session)
):
    inventory_service = InventoryService(session)
    product = await inventory_service.update_stock(product_id, new_stock)
    
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {"message": "Stock actualizado", "product_id": product_id, "new_stock": new_stock} 
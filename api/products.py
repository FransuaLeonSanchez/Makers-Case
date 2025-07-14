from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from database import get_session
from models.product import Product, ProductCreate, ProductResponse, ProductCategory, Sale
from services.inventory_service import InventoryService

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

@router.get("/sales/recent")
async def get_recent_sales(
    limit: int = 10,
    session: AsyncSession = Depends(get_session)
):
    """Obtener las ventas más recientes"""
    result = await session.execute(
        select(Sale)
        .order_by(Sale.timestamp.desc())
        .limit(limit)
    )
    sales = result.scalars().all()
    
    return {
        "sales": [
            {
                "id": sale.id,
                "product_name": sale.product_name,
                "product_brand": sale.product_brand,
                "price": sale.price,
                "quantity": sale.quantity,
                "customer_info": sale.customer_info,
                "timestamp": sale.timestamp.isoformat(),
                "status": sale.status
            }
            for sale in sales
        ],
        "total": len(sales)
    }

@router.get("/summary")
async def get_summary(session: AsyncSession = Depends(get_session)):
    """Obtener resumen del inventario"""
    inventory_service = InventoryService(session)
    return await inventory_service.get_inventory_summary()

@router.get("/inventory/summary")
async def get_inventory_summary(session: AsyncSession = Depends(get_session)):
    """Obtener resumen del inventario con métricas"""
    inventory_service = InventoryService(session)
    return await inventory_service.get_inventory_summary()

@router.get("/inventory/summary")
async def get_inventory_summary_alt(session: AsyncSession = Depends(get_session)):
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
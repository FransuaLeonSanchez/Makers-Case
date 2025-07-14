from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from models.product import Product, ProductCategory, ProductCreate
from typing import List, Optional, Dict
import json

class InventoryService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_all_products(self) -> List[Product]:
        result = await self.session.execute(
            select(Product).where(Product.is_active == True)
        )
        return result.scalars().all()
    
    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.session.execute(
            select(Product).where(Product.id == product_id)
        )
        return result.scalar_one_or_none()
    
    async def get_products_by_category(self, category: ProductCategory) -> List[Product]:
        result = await self.session.execute(
            select(Product).where(
                Product.category == category,
                Product.is_active == True
            )
        )
        return result.scalars().all()
    
    async def get_products_by_brand(self, brand: str) -> List[Product]:
        result = await self.session.execute(
            select(Product).where(
                Product.brand == brand,
                Product.is_active == True
            )
        )
        return result.scalars().all()
    
    async def get_inventory_summary(self) -> Dict:
        # Obtener resumen por categoría
        result = await self.session.execute(
            select(
                Product.category,
                func.count(Product.id).label('count'),
                func.sum(Product.stock).label('total_stock')
            ).where(Product.is_active == True)
            .group_by(Product.category)
        )
        
        by_category = []
        total_products = 0
        total_stock = 0
        
        for row in result:
            by_category.append({
                "category": row.category.value,
                "count": row.count,
                "total_stock": row.total_stock or 0
            })
            total_products += row.count
            total_stock += row.total_stock or 0
        
        # Calcular valor total del inventario
        value_result = await self.session.execute(
            select(func.sum(Product.price * Product.stock)).where(Product.is_active == True)
        )
        total_value = value_result.scalar() or 0
        
        # Obtener productos con stock bajo (menos de 5 unidades)
        low_stock_result = await self.session.execute(
            select(Product).where(
                Product.stock < 5,
                Product.is_active == True
            ).order_by(Product.stock)
        )
        low_stock_products = [
            {
                "id": p.id,
                "name": p.name,
                "brand": p.brand,
                "model": p.model,
                "stock": p.stock,
                "price": p.price
            }
            for p in low_stock_result.scalars().all()
        ]
        
        return {
            "by_category": by_category,
            "total_products": total_products,
            "total_stock": total_stock,
            "total_value": float(total_value),
            "low_stock_products": low_stock_products
        }
    
    async def search_products(self, query: str) -> List[Product]:
        search_term = f"%{query}%"
        result = await self.session.execute(
            select(Product).where(
                (Product.name.ilike(search_term)) |
                (Product.brand.ilike(search_term)) |
                (Product.model.ilike(search_term)) |
                (Product.description.ilike(search_term)),
                Product.is_active == True
            )
        )
        return result.scalars().all()
    
    async def create_product(self, product_data: ProductCreate) -> Product:
        product = Product(**product_data.dict())
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product
    
    async def update_stock(self, product_id: int, new_stock: int) -> Optional[Product]:
        product = await self.get_product_by_id(product_id)
        if product:
            product.stock = new_stock
            await self.session.commit()
            await self.session.refresh(product)
        return product
    
    async def init_synthetic_data(self):
        existing = await self.session.execute(select(func.count(Product.id)))
        count = existing.scalar()
        
        if count > 0:
            return
        
        synthetic_products = [
            {
                "name": "Laptop HP Pavilion 15",
                "brand": "HP",
                "model": "15-eh1021la",
                "category": ProductCategory.LAPTOPS,
                "price": 899.99,
                "stock": 5,
                "description": "Laptop HP Pavilion con procesador AMD Ryzen 5, ideal para trabajo y entretenimiento",
                "specifications": json.dumps({
                    "procesador": "AMD Ryzen 5 5500U",
                    "ram": "8GB DDR4",
                    "almacenamiento": "512GB SSD",
                    "pantalla": "15.6 pulgadas Full HD",
                    "sistema_operativo": "Windows 11"
                })
            },
            {
                "name": "Laptop HP ProBook 450",
                "brand": "HP",
                "model": "450 G9",
                "category": ProductCategory.LAPTOPS,
                "price": 1299.99,
                "stock": 3,
                "description": "Laptop profesional HP ProBook con Intel Core i7 de última generación",
                "specifications": json.dumps({
                    "procesador": "Intel Core i7-1255U",
                    "ram": "16GB DDR4",
                    "almacenamiento": "1TB SSD",
                    "pantalla": "15.6 pulgadas Full HD",
                    "sistema_operativo": "Windows 11 Pro"
                })
            },
            {
                "name": "Desktop Dell OptiPlex 3000",
                "brand": "Dell",
                "model": "OptiPlex 3000",
                "category": ProductCategory.COMPUTADORAS,
                "price": 799.99,
                "stock": 2,
                "description": "Computadora de escritorio Dell compacta y potente para oficina",
                "specifications": json.dumps({
                    "procesador": "Intel Core i5-12500",
                    "ram": "8GB DDR4",
                    "almacenamiento": "256GB SSD",
                    "puertos": "USB 3.0, HDMI, DisplayPort",
                    "sistema_operativo": "Windows 11 Pro"
                })
            },
            {
                "name": "MacBook Air M2",
                "brand": "Apple",
                "model": "MacBook Air 2022",
                "category": ProductCategory.LAPTOPS,
                "price": 1499.99,
                "stock": 1,
                "description": "La nueva MacBook Air con chip M2, diseño ultradelgado y batería de larga duración",
                "specifications": json.dumps({
                    "procesador": "Apple M2",
                    "ram": "8GB",
                    "almacenamiento": "256GB SSD",
                    "pantalla": "13.6 pulgadas Liquid Retina",
                    "sistema_operativo": "macOS Ventura"
                })
            },
            {
                "name": "iPad Pro 12.9",
                "brand": "Apple",
                "model": "iPad Pro 6ta Gen",
                "category": ProductCategory.TABLETS,
                "price": 1099.99,
                "stock": 4,
                "description": "iPad Pro con chip M2, pantalla Liquid Retina XDR",
                "specifications": json.dumps({
                    "procesador": "Apple M2",
                    "almacenamiento": "128GB",
                    "pantalla": "12.9 pulgadas Liquid Retina XDR",
                    "conectividad": "Wi-Fi 6E",
                    "camara": "12MP + 10MP"
                })
            },
            {
                "name": "Samsung Galaxy Tab S8",
                "brand": "Samsung",
                "model": "Tab S8",
                "category": ProductCategory.TABLETS,
                "price": 699.99,
                "stock": 6,
                "description": "Tablet Android premium con S Pen incluido",
                "specifications": json.dumps({
                    "procesador": "Snapdragon 8 Gen 1",
                    "ram": "8GB",
                    "almacenamiento": "128GB",
                    "pantalla": "11 pulgadas LTPS TFT",
                    "sistema_operativo": "Android 13"
                })
            },
            {
                "name": "Monitor Dell UltraSharp 27",
                "brand": "Dell",
                "model": "U2723DE",
                "category": ProductCategory.MONITORES,
                "price": 599.99,
                "stock": 8,
                "description": "Monitor profesional 4K con USB-C y ergonomía avanzada",
                "specifications": json.dumps({
                    "tamaño": "27 pulgadas",
                    "resolucion": "3840 x 2160 (4K)",
                    "panel": "IPS",
                    "puertos": "HDMI, DisplayPort, USB-C",
                    "ajustes": "Altura, inclinación, rotación"
                })
            },
            {
                "name": "Mouse Logitech MX Master 3S",
                "brand": "Logitech",
                "model": "MX Master 3S",
                "category": ProductCategory.PERIFERICOS,
                "price": 99.99,
                "stock": 15,
                "description": "Mouse inalámbrico premium con scroll electromagnético",
                "specifications": json.dumps({
                    "conectividad": "Bluetooth, USB receptor",
                    "bateria": "Recargable USB-C",
                    "dpi": "200-8000 DPI",
                    "botones": "7 botones programables"
                })
            },
            {
                "name": "Teclado Mecánico Keychron K2",
                "brand": "Keychron",
                "model": "K2 V2",
                "category": ProductCategory.PERIFERICOS,
                "price": 89.99,
                "stock": 12,
                "description": "Teclado mecánico compacto con retroiluminación RGB",
                "specifications": json.dumps({
                    "switches": "Gateron Brown",
                    "conectividad": "Bluetooth 5.1, USB-C",
                    "layout": "75% (84 teclas)",
                    "compatibilidad": "Windows, Mac, Linux"
                })
            },
            {
                "name": "iPhone 14 Pro",
                "brand": "Apple",
                "model": "iPhone 14 Pro",
                "category": ProductCategory.CELULARES,
                "price": 1299.99,
                "stock": 7,
                "description": "iPhone con Dynamic Island y cámara de 48MP",
                "specifications": json.dumps({
                    "procesador": "A16 Bionic",
                    "almacenamiento": "256GB",
                    "pantalla": "6.1 pulgadas Super Retina XDR",
                    "camara": "48MP principal + 12MP ultra gran angular + 12MP teleobjetivo",
                    "bateria": "Hasta 23 horas de reproducción de video"
                })
            },
            {
                "name": "Samsung Galaxy S23 Ultra",
                "brand": "Samsung",
                "model": "Galaxy S23 Ultra",
                "category": ProductCategory.CELULARES,
                "price": 1199.99,
                "stock": 5,
                "description": "Smartphone Android premium con S Pen integrado",
                "specifications": json.dumps({
                    "procesador": "Snapdragon 8 Gen 2",
                    "ram": "12GB",
                    "almacenamiento": "256GB",
                    "pantalla": "6.8 pulgadas Dynamic AMOLED 2X",
                    "camara": "200MP principal + 12MP + 10MP + 10MP"
                })
            },
            {
                "name": "Impresora HP LaserJet Pro",
                "brand": "HP",
                "model": "M404dn",
                "category": ProductCategory.IMPRESORAS,
                "price": 399.99,
                "stock": 3,
                "description": "Impresora láser monocromática de alta velocidad",
                "specifications": json.dumps({
                    "tipo": "Láser monocromática",
                    "velocidad": "40 ppm",
                    "conectividad": "USB, Ethernet",
                    "duplex": "Automático",
                    "capacidad_papel": "350 hojas"
                })
            },
            {
                "name": "AirPods Pro 2",
                "brand": "Apple",
                "model": "AirPods Pro 2da Gen",
                "category": ProductCategory.ACCESORIOS,
                "price": 249.99,
                "stock": 20,
                "description": "Audífonos inalámbricos con cancelación activa de ruido",
                "specifications": json.dumps({
                    "chip": "H2",
                    "cancelacion_ruido": "Activa adaptable",
                    "bateria": "Hasta 6 horas con ANC",
                    "resistencia": "IPX4",
                    "carga": "USB-C, MagSafe, Qi"
                })
            },
            {
                "name": "Webcam Logitech Brio 4K",
                "brand": "Logitech",
                "model": "Brio",
                "category": ProductCategory.ACCESORIOS,
                "price": 199.99,
                "stock": 10,
                "description": "Webcam profesional 4K con HDR y Windows Hello",
                "specifications": json.dumps({
                    "resolucion": "4K Ultra HD (4096 x 2160)",
                    "fps": "30 fps en 4K, 60 fps en 1080p",
                    "campo_vision": "65°, 78°, 90°",
                    "microfono": "Dual omnidireccional",
                    "conectividad": "USB 3.0"
                })
            }
        ]
        
        for product_data in synthetic_products:
            product = Product(**product_data)
            self.session.add(product)
        
        await self.session.commit() 
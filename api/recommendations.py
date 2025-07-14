from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Dict, Optional
from database import get_session
from services.inventory_service import InventoryService
from models.product import ProductResponse, ProductCategory
import random

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

class UserPreferences(BaseModel):
    budget_max: Optional[float] = None
    budget_min: Optional[float] = 0
    preferred_brands: List[str] = []
    categories_of_interest: List[ProductCategory] = []
    use_case: Optional[str] = None  # "gaming", "office", "creativity", "general"

class RecommendationResponse(BaseModel):
    highly_recommended: List[ProductResponse]
    recommended: List[ProductResponse]
    not_recommended: List[ProductResponse]
    reasoning: Dict[str, str]

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(
    preferences: UserPreferences,
    session: AsyncSession = Depends(get_session)
):
    inventory_service = InventoryService(session)
    all_products = await inventory_service.get_all_products()
    
    if not all_products:
        raise HTTPException(status_code=404, detail="No hay productos disponibles")
    
    highly_recommended = []
    recommended = []
    not_recommended = []
    reasoning = {}
    
    for product in all_products:
        score = 0
        reasons = []
        
        # Scoring por presupuesto
        if preferences.budget_max:
            if product.price <= preferences.budget_max:
                if product.price >= preferences.budget_min:
                    score += 30
                    reasons.append("Dentro del presupuesto")
                else:
                    score += 10
                    reasons.append("Por debajo del presupuesto mínimo")
            else:
                score -= 20
                reasons.append("Excede el presupuesto")
        
        # Scoring por marca preferida
        if preferences.preferred_brands:
            if product.brand in preferences.preferred_brands:
                score += 25
                reasons.append(f"Marca preferida: {product.brand}")
            else:
                score -= 5
                reasons.append("Marca no preferida")
        
        # Scoring por categoría de interés
        if preferences.categories_of_interest:
            if product.category in preferences.categories_of_interest:
                score += 20
                reasons.append(f"Categoría de interés: {product.category.value}")
            else:
                score -= 10
                reasons.append("Categoría no prioritaria")
        
        # Scoring por caso de uso
        use_case_bonus = _get_use_case_score(product, preferences.use_case)
        score += use_case_bonus
        if use_case_bonus > 0:
            reasons.append(f"Adecuado para: {preferences.use_case}")
        
        # Scoring por disponibilidad
        if product.stock > 0:
            score += 15
            reasons.append("Disponible en stock")
        else:
            score -= 30
            reasons.append("Sin stock")
        
        # Categorización
        if score >= 50:
            highly_recommended.append(product)
            reasoning[str(product.id)] = f"Altamente recomendado: {', '.join(reasons)}"
        elif score >= 20:
            recommended.append(product)
            reasoning[str(product.id)] = f"Recomendado: {', '.join(reasons)}"
        else:
            not_recommended.append(product)
            reasoning[str(product.id)] = f"No recomendado: {', '.join(reasons)}"
    
    # Ordenar por precio (más recomendados primero)
    highly_recommended.sort(key=lambda x: x.price)
    recommended.sort(key=lambda x: x.price)
    not_recommended.sort(key=lambda x: x.price, reverse=True)
    
    return RecommendationResponse(
        highly_recommended=highly_recommended,
        recommended=recommended,
        not_recommended=not_recommended,
        reasoning=reasoning
    )

def _get_use_case_score(product, use_case: str) -> int:
    if not use_case:
        return 0
    
    use_case_lower = use_case.lower()
    product_name_lower = product.name.lower()
    category = product.category.value.lower()
    
    # Gaming
    if "gaming" in use_case_lower:
        if any(term in product_name_lower for term in ["gaming", "rtx", "gtx", "ryzen", "intel"]):
            return 15
        if category in ["laptops", "computadoras"]:
            return 10
        return 0
    
    # Office/Trabajo
    elif "office" in use_case_lower or "trabajo" in use_case_lower:
        if any(term in product_name_lower for term in ["pro", "business", "office"]):
            return 15
        if category in ["laptops", "computadoras", "monitores", "perifericos"]:
            return 10
        return 5
    
    # Creatividad
    elif "creativity" in use_case_lower or "creativ" in use_case_lower:
        if "pro" in product_name_lower or "studio" in product_name_lower:
            return 15
        if category in ["laptops", "computadoras", "tablets", "monitores"]:
            return 10
        return 5
    
    # General
    elif "general" in use_case_lower:
        return 5
    
    return 0

@router.get("/use-cases")
async def get_available_use_cases():
    return {
        "use_cases": [
            {"id": "gaming", "name": "Gaming y Entretenimiento"},
            {"id": "office", "name": "Oficina y Trabajo"},
            {"id": "creativity", "name": "Creatividad y Diseño"},
            {"id": "general", "name": "Uso General"}
        ]
    } 
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Dict, Optional
from database import get_session
from services.recommendation_service import RecommendationService
from models.product import ProductResponse, ProductCategory
from models.user_interaction import InteractionRequest

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])

class RecommendedProduct(ProductResponse):
    score: float
    recommendation: str
    reasons: List[str]

@router.get("/")
async def get_recommendations(
    session: AsyncSession = Depends(get_session)
):
    """
    Obtiene recomendaciones personalizadas basadas en el comportamiento global del usuario.
    Las recomendaciones se adaptan automáticamente según todas las interacciones previas
    con el chatbot y el sistema.
    """
    recommendation_service = RecommendationService(session)
    
    try:
        recommendations = await recommendation_service.get_personalized_recommendations()
        
        # Formatear respuesta con scoring y razones
        response = {
            "highly_recommended": [],
            "recommended": [],
            "other_suggestions": []
        }
        
        for category, products in recommendations.items():
            for product in products:
                recommended_product = {
                    **product.__dict__,
                    "score": 85 if category == "highly_recommended" else 65 if category == "recommended" else 40,
                    "recommendation": category.upper().replace("_", " "),
                    "reasons": _get_recommendation_reasons(product, category)
                }
                response[category].append(recommended_product)
        
        await session.commit()
        return response
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al obtener recomendaciones: {str(e)}")

@router.post("/track-interaction")
async def track_interaction(
    interaction: InteractionRequest,
    session: AsyncSession = Depends(get_session)
):
    """Registra una interacción del usuario con el sistema"""
    recommendation_service = RecommendationService(session)
    
    try:
        await recommendation_service.track_interaction(
            interaction_type=interaction.interaction_type,
            product_id=interaction.product_id,
            category=interaction.category_viewed,
            search_query=interaction.search_query
        )
        await session.commit()
        return {"status": "success", "message": "Interacción registrada"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error al registrar interacción: {str(e)}")

@router.get("/related/{product_id}")
async def get_related_products(
    product_id: int,
    limit: int = Query(6, ge=1, le=20),
    session: AsyncSession = Depends(get_session)
):
    """Obtiene productos relacionados a uno específico"""
    recommendation_service = RecommendationService(session)
    
    try:
        related_products = await recommendation_service.get_related_products(
            product_id=product_id,
            limit=limit
        )
        return related_products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos relacionados: {str(e)}")

@router.get("/user-preferences")
async def get_user_preferences(
    session: AsyncSession = Depends(get_session)
):
    """Obtiene las preferencias globales aprendidas del usuario"""
    recommendation_service = RecommendationService(session)
    
    preferences = await recommendation_service.get_user_preferences()
    
    if not preferences:
        return {
            "preferred_categories": [],
            "preferred_brands": [],
            "price_range": {"min": 0, "max": 50000},
            "interaction_count": 0
        }
    
    return {
        "preferred_categories": preferences["preferred_categories"],
        "preferred_brands": preferences["preferred_brands"],
        "price_range": {
            "min": preferences["price_range_min"],
            "max": preferences["price_range_max"]
        },
        "interaction_count": preferences["interaction_count"]
    }

def _get_recommendation_reasons(product, category: str) -> List[str]:
    """Genera razones para la recomendación"""
    reasons = []
    
    if category == "highly_recommended":
        reasons.append("De la categoría que buscaste más recientemente")
        if product.stock > 5:
            reasons.append("Disponibilidad inmediata")
        reasons.append("Producto destacado en su categoría")
    elif category == "recommended":
        reasons.append("De tu penúltima categoría buscada")
        if product.price < 1000:
            reasons.append("Precio accesible")
        if product.stock > 10:
            reasons.append("Amplio stock disponible")
    else:
        reasons.append("Otras opciones que podrían interesarte")
        if hasattr(product, 'brand') and product.brand in ["Apple", "Samsung", "HP", "Dell"]:
            reasons.append("Marca reconocida")
    
    return reasons 
'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaBrain, FaSync, FaHistory, FaLightbulb } from 'react-icons/fa';
import { recommendationAPI, RecommendedProduct, UserPreferences } from '@/lib/api';
import ProductCard from './ProductCard';

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState<{
    highly_recommended: RecommendedProduct[];
    recommended: RecommendedProduct[];
    other_suggestions: RecommendedProduct[];
  }>({
    highly_recommended: [],
    recommended: [],
    other_suggestions: []
  });
  const [userPreferences, setUserPreferences] = useState<UserPreferences | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Cargar recomendaciones al montar el componente
    loadRecommendations();
    loadUserPreferences();
  }, []);

  const loadRecommendations = async () => {
    setLoading(true);
    try {
      const data = await recommendationAPI.getRecommendations();
      setRecommendations(data);
    } catch (error) {
      console.error('Error loading recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadUserPreferences = async () => {
    try {
      const prefs = await recommendationAPI.getUserPreferences();
      setUserPreferences(prefs);
    } catch (error) {
      console.error('Error loading user preferences:', error);
    }
  };

  const handleRefresh = () => {
    loadRecommendations();
    loadUserPreferences();
  };

  const handleProductClick = async (productId: number, category: string) => {
    // Registrar interacción cuando el usuario hace clic en un producto
    try {
      await recommendationAPI.trackInteraction({
        product_id: productId,
        interaction_type: 'recommendation_click',
        category_viewed: category
      });
    } catch (error) {
      console.error('Error tracking interaction:', error);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-3xl font-bold text-gray-900 mb-2 flex items-center gap-3">
              <FaBrain className="text-purple-600" />
              Recomendaciones Inteligentes
            </h2>
            <p className="text-gray-900">
              Basadas en tu comportamiento y preferencias aprendidas
            </p>
          </div>
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            <FaSync className={loading ? 'animate-spin' : ''} />
            Actualizar
          </button>
        </div>

        {userPreferences && userPreferences.interaction_count > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gradient-to-r from-purple-100 to-blue-100 rounded-lg p-6 mb-6"
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <FaLightbulb className="text-yellow-500" />
              Hemos aprendido sobre ti:
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
              <div>
                <p className="font-medium text-gray-900">Categorías preferidas:</p>
                <p className="text-gray-900">
                  {userPreferences.preferred_categories.length > 0 
                    ? userPreferences.preferred_categories.join(', ')
                    : 'Aún aprendiendo...'}
                </p>
              </div>
              <div>
                <p className="font-medium text-gray-900">Marcas favoritas:</p>
                <p className="text-gray-900">
                  {userPreferences.preferred_brands.length > 0
                    ? userPreferences.preferred_brands.join(', ')
                    : 'Aún aprendiendo...'}
                </p>
              </div>
              <div>
                <p className="font-medium text-gray-900">Rango de precio:</p>
                <p className="text-gray-900">
                  ${userPreferences.price_range.min.toFixed(0)} - ${userPreferences.price_range.max.toFixed(0)}
                </p>
              </div>
            </div>
            <div className="mt-3 flex items-center gap-2 text-xs text-gray-900">
              <FaHistory />
              <span>Basado en {userPreferences.interaction_count} interacciones</span>
            </div>
          </motion.div>
        )}
      </motion.div>

      {loading ? (
        <div className="flex flex-col items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mb-4"></div>
          <p className="text-gray-900">Analizando tus preferencias...</p>
        </div>
      ) : (
        <div className="space-y-8">
          {/* Altamente Recomendados */}
          {recommendations.highly_recommended.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
            >
              <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span className="text-green-600">★★★</span> Altamente Recomendados
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.highly_recommended.map(product => (
                  <div
                    key={product.id}
                    onClick={() => handleProductClick(product.id, product.category)}
                  >
                    <ProductCard
                      product={product}
                      recommendation="HIGHLY_RECOMMENDED"
                    />
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Recomendados */}
          {recommendations.recommended.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span className="text-blue-600">★★</span> Recomendados
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.recommended.map(product => (
                  <div
                    key={product.id}
                    onClick={() => handleProductClick(product.id, product.category)}
                  >
                    <ProductCard
                      product={product}
                      recommendation="RECOMMENDED"
                    />
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* No Recomendados */}
          {recommendations.other_suggestions.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
            >
              <h3 className="text-2xl font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span className="text-gray-600">★</span> Otras opciones
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {recommendations.other_suggestions.map(product => (
                  <div
                    key={product.id}
                    onClick={() => handleProductClick(product.id, product.category)}
                  >
                    <ProductCard
                      product={product}
                      recommendation="OTHER_SUGGESTIONS"
                    />
                  </div>
                ))}
              </div>
            </motion.div>
          )}

          {/* Mensaje cuando no hay recomendaciones */}
          {recommendations.highly_recommended.length === 0 && 
           recommendations.recommended.length === 0 && 
           recommendations.other_suggestions.length === 0 && (
            <div className="text-center py-12">
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="inline-block"
              >
                <FaBrain className="text-6xl text-purple-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">
                  ¡Comienza a explorar!
                </h3>
                <p className="text-gray-900 max-w-md mx-auto">
                  Usa nuestro chat para preguntar sobre productos. 
                  Mientras más interactúes, mejores serán nuestras recomendaciones.
                </p>
                <div className="mt-6 space-y-2">
                  <p className="text-sm text-gray-900">Prueba preguntando:</p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {['¿Qué laptops tienen?', '¿Hay tablets disponibles?', 'Busco un celular'].map((suggestion) => (
                      <span
                        key={suggestion}
                        className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm"
                      >
                        "{suggestion}"
                      </span>
                    ))}
                  </div>
                </div>
              </motion.div>
            </div>
          )}
        </div>
      )}
    </div>
  );
} 
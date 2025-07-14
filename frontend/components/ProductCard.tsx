'use client';

import { motion } from 'framer-motion';
import { FaShoppingCart, FaStar } from 'react-icons/fa';
import { Product, RecommendedProduct } from '@/lib/api';

interface ProductCardProps {
  product: Product | RecommendedProduct;
  recommendation?: string;
}

export default function ProductCard({ product, recommendation }: ProductCardProps) {
  const recommendationStyles: Record<string, { border: string; badge: string; text: string }> = {
    HIGHLY_RECOMMENDED: {
      border: 'border-green-500',
      badge: 'bg-green-500',
      text: 'Altamente Recomendado',
    },
    RECOMMENDED: {
      border: 'border-blue-500',
      badge: 'bg-blue-500',
      text: 'Recomendado',
    },
    'OTHER SUGGESTIONS': {
      border: 'border-gray-300',
      badge: 'bg-gray-400',
      text: 'Otras Sugerencias',
    },
    OTHER_SUGGESTIONS: {
      border: 'border-gray-300',
      badge: 'bg-gray-400',
      text: 'Otras Sugerencias',
    },
  };

  const style = recommendation && recommendationStyles[recommendation] ? recommendationStyles[recommendation] : null;

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('es-MX', {
      style: 'currency',
      currency: 'MXN',
    }).format(price);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className={`bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow p-6 relative ${
        style ? `border-2 ${style.border}` : ''
      }`}
    >
      {recommendation && style && (
        <div className={`absolute -top-3 left-4 ${style.badge} text-white px-3 py-1 rounded-full text-xs font-semibold`}>
          {style.text}
        </div>
      )}

      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{product.name}</h3>
        <p className="text-sm text-gray-900">{product.brand} - {product.model}</p>
      </div>

      <div className="mb-4">
        <p className="text-sm text-gray-900 line-clamp-3">{product.description}</p>
      </div>

      <div className="mb-4">
        <p className="text-2xl font-bold text-blue-600">{formatPrice(product.price)}</p>
        <p className="text-sm text-gray-900">
          {product.stock > 0 ? `${product.stock} unidades disponibles` : 'Agotado'}
        </p>
      </div>

      {'score' in product && (
        <div className="mb-4">
          <div className="flex items-center gap-2">
            <div className="flex">
              {[...Array(5)].map((_, i) => (
                <FaStar
                  key={i}
                  className={`${
                    i < Math.round((product as RecommendedProduct).score / 20)
                      ? 'text-yellow-400'
                      : 'text-gray-300'
                  }`}
                  size={16}
                />
              ))}
            </div>
            <span className="text-sm text-gray-900">
              Puntuación: {(product as RecommendedProduct).score}%
            </span>
          </div>
        </div>
      )}

      <div className="flex gap-2">
        <button className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2">
          <FaShoppingCart />
          <span>Agregar al carrito</span>
        </button>
      </div>
    </motion.div>
  );
} 
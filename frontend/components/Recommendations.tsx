'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaFilter, FaSearch } from 'react-icons/fa';
import { recommendationAPI, RecommendedProduct } from '@/lib/api';
import ProductCard from './ProductCard';

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState<RecommendedProduct[]>([]);
  const [loading, setLoading] = useState(false);
  const [filters, setFilters] = useState({
    budget_min: 0,
    budget_max: 50000,
    categories: [] as string[],
    brands: [] as string[],
    use_cases: [] as string[],
  });

  const categories = ['COMPUTADORAS', 'LAPTOPS', 'TABLETS', 'SMARTPHONES', 'ACCESORIOS'];
  const brands = ['Apple', 'Dell', 'HP', 'Lenovo', 'Samsung', 'Logitech'];
  const useCases = ['gaming', 'office', 'creativity', 'general'];

  const handleFilterChange = (key: string, value: any) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  const toggleArrayFilter = (key: 'categories' | 'brands' | 'use_cases', value: string) => {
    setFilters(prev => ({
      ...prev,
      [key]: prev[key].includes(value)
        ? prev[key].filter(item => item !== value)
        : [...prev[key], value],
    }));
  };

  const handleGetRecommendations = async () => {
    setLoading(true);
    try {
      const data = await recommendationAPI.getRecommendations(filters);
      setRecommendations(data);
    } catch (error) {
      console.error('Error getting recommendations:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Recomendaciones Personalizadas
        </h2>
        <p className="text-gray-900">
          Encuentra los productos perfectos basados en tus preferencias
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-1 bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold mb-4 flex items-center gap-2 text-gray-900">
            <FaFilter className="text-blue-600" />
            Filtros
          </h3>

          <div className="space-y-6">
            <div>
              <label className="text-sm font-medium text-gray-900">Presupuesto</label>
              <div className="mt-2 space-y-2">
                <input
                  type="number"
                  placeholder="Mínimo"
                  value={filters.budget_min}
                  onChange={(e) => handleFilterChange('budget_min', Number(e.target.value))}
                  className="w-full px-3 py-2 border rounded-lg text-sm"
                />
                <input
                  type="number"
                  placeholder="Máximo"
                  value={filters.budget_max}
                  onChange={(e) => handleFilterChange('budget_max', Number(e.target.value))}
                  className="w-full px-3 py-2 border rounded-lg text-sm"
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-900">Categorías</label>
              <div className="mt-2 space-y-2">
                {categories.map(category => (
                  <label key={category} className="flex items-center gap-2 text-sm text-gray-900">
                    <input
                      type="checkbox"
                      checked={filters.categories.includes(category)}
                      onChange={() => toggleArrayFilter('categories', category)}
                      className="rounded text-blue-600"
                    />
                    {category}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-900">Marcas</label>
              <div className="mt-2 space-y-2">
                {brands.map(brand => (
                  <label key={brand} className="flex items-center gap-2 text-sm text-gray-900">
                    <input
                      type="checkbox"
                      checked={filters.brands.includes(brand)}
                      onChange={() => toggleArrayFilter('brands', brand)}
                      className="rounded text-blue-600"
                    />
                    {brand}
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="text-sm font-medium text-gray-900">Uso principal</label>
              <div className="mt-2 space-y-2">
                {useCases.map(useCase => (
                  <label key={useCase} className="flex items-center gap-2 text-sm text-gray-900">
                    <input
                      type="checkbox"
                      checked={filters.use_cases.includes(useCase)}
                      onChange={() => toggleArrayFilter('use_cases', useCase)}
                      className="rounded text-blue-600"
                    />
                    {useCase === 'gaming' ? 'Juegos' :
                     useCase === 'office' ? 'Oficina' :
                     useCase === 'creativity' ? 'Creatividad' : 'General'}
                  </label>
                ))}
              </div>
            </div>

            <button
              onClick={handleGetRecommendations}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors flex items-center justify-center gap-2 disabled:opacity-50"
            >
              <FaSearch />
              {loading ? 'Buscando...' : 'Buscar Recomendaciones'}
            </button>
          </div>
        </motion.div>

        <div className="lg:col-span-3">
          {loading ? (
            <div className="flex items-center justify-center h-64">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
          ) : recommendations.length > 0 ? (
            <div className="space-y-6">
              {['HIGHLY_RECOMMENDED', 'RECOMMENDED', 'NOT_RECOMMENDED'].map(level => {
                const products = recommendations.filter(p => p.recommendation === level);
                if (products.length === 0) return null;

                return (
                  <div key={level}>
                    <h4 className="text-lg font-semibold mb-4 text-gray-900">
                      {level === 'HIGHLY_RECOMMENDED' ? 'Altamente Recomendados' :
                       level === 'RECOMMENDED' ? 'Recomendados' : 'No Recomendados'}
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                      {products.map(product => (
                        <ProductCard
                          key={product.id}
                          product={product}
                          recommendation={product.recommendation}
                        />
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          ) : (
            <div className="text-center text-gray-900 mt-12">
              <p className="text-lg">
                Configura tus preferencias y haz clic en "Buscar Recomendaciones"
              </p>
              <p className="text-sm mt-2">
                Obtendrás productos personalizados según tus necesidades
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
} 
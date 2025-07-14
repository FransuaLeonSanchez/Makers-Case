'use client';

import { useState, useEffect } from 'react';
import { productAPI } from '@/lib/api';

interface Product {
  id: number;
  name: string;
  brand: string;
  model: string;
  category: string;
  price: number;
  stock: number;
  description: string;
  specifications: Record<string, any>;
  is_active: boolean;
}

interface ProductsByCategory {
  [category: string]: Product[];
}

export default function Products() {
  const [productsByCategory, setProductsByCategory] = useState<ProductsByCategory>({});
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const products = await productAPI.getAllProducts();
      
      // Organizar productos por categoría
      const organized: ProductsByCategory = {};
      products.forEach((product: Product) => {
        const category = product.category;
        if (!organized[category]) {
          organized[category] = [];
        }
        organized[category].push(product);
      });
      
      setProductsByCategory(organized);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryIcon = (category: string) => {
    const icons: { [key: string]: string } = {
      'CELULARES': '📱',
      'LAPTOPS': '💻',
      'TABLETS': '📲',
      'COMPUTADORAS': '🖥️',
      'MONITORES': '🖥️',
      'PERIFERICOS': '🖱️',
      'ACCESORIOS': '🎧',
      'IMPRESORAS': '🖨️'
    };
    return icons[category] || '📦';
  };

  const getCategoryName = (category: string) => {
    const names: { [key: string]: string } = {
      'CELULARES': 'Celulares',
      'LAPTOPS': 'Laptops',
      'TABLETS': 'Tablets',
      'COMPUTADORAS': 'Computadoras',
      'MONITORES': 'Monitores',
      'PERIFERICOS': 'Periféricos',
      'ACCESORIOS': 'Accesorios',
      'IMPRESORAS': 'Impresoras'
    };
    return names[category] || category;
  };

  const getAllProducts = () => {
    const allProducts: Product[] = [];
    Object.values(productsByCategory).forEach(products => {
      allProducts.push(...products);
    });
    return allProducts;
  };

  const getFilteredProducts = () => {
    const products = selectedCategory === 'all' 
      ? getAllProducts() 
      : productsByCategory[selectedCategory] || [];
    
    if (!searchTerm) return products;
    
    return products.filter(product => 
      product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.brand.toLowerCase().includes(searchTerm.toLowerCase()) ||
      product.description.toLowerCase().includes(searchTerm.toLowerCase())
    );
  };

  const filteredProducts = getFilteredProducts();

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-gray-500">Cargando productos...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Catálogo de Productos</h1>
        <p className="text-gray-600 mt-1">Explora todos nuestros productos organizados por categoría</p>
      </div>

      {/* Filtros */}
      <div className="bg-white rounded-lg shadow-sm p-4 space-y-4">
        {/* Búsqueda */}
        <div className="relative">
          <input
            type="text"
            placeholder="Buscar productos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
          <svg className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </div>

        {/* Categorías */}
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
              selectedCategory === 'all'
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Todos ({getAllProducts().length})
          </button>
          {Object.entries(productsByCategory).map(([category, products]) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors flex items-center gap-1 ${
                selectedCategory === category
                  ? 'bg-purple-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              <span>{getCategoryIcon(category)}</span>
              {getCategoryName(category)} ({products.length})
            </button>
          ))}
        </div>
      </div>

      {/* Resultados */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-lg font-semibold text-gray-900">
            {selectedCategory === 'all' 
              ? `Todos los productos (${filteredProducts.length})`
              : `${getCategoryIcon(selectedCategory)} ${getCategoryName(selectedCategory)} (${filteredProducts.length})`
            }
          </h2>
          {searchTerm && (
            <span className="text-sm text-gray-500">
              Resultados para "{searchTerm}"
            </span>
          )}
        </div>

        {filteredProducts.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-500">No se encontraron productos</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {filteredProducts.map((product) => (
              <div
                key={product.id}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-lg transition-shadow cursor-pointer"
              >
                {/* Categoría Badge */}
                <div className="flex justify-between items-start mb-2">
                  <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                    {getCategoryIcon(product.category)} {getCategoryName(product.category)}
                  </span>
                  {product.stock <= 5 && (
                    <span className="text-xs text-red-600 font-medium">
                      ¡Últimas {product.stock}!
                    </span>
                  )}
                </div>

                {/* Nombre y marca */}
                <h3 className="font-semibold text-gray-900 mb-1 line-clamp-2">
                  {product.name}
                </h3>
                <p className="text-sm text-gray-600 mb-2">{product.brand}</p>

                {/* Descripción */}
                <p className="text-sm text-gray-500 mb-3 line-clamp-2">
                  {product.description}
                </p>

                {/* Precio y stock */}
                <div className="flex justify-between items-end">
                  <div>
                    <p className="text-2xl font-bold text-gray-900">
                      ${product.price.toFixed(2)}
                    </p>
                    <p className="text-xs text-gray-500">
                      {product.stock > 0 ? `${product.stock} disponibles` : 'Agotado'}
                    </p>
                  </div>
                  <button className="bg-purple-600 text-white px-4 py-2 rounded-lg hover:bg-purple-700 transition-colors text-sm">
                    Ver detalles
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 
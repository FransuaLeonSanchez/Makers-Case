'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaBox, FaChartPie, FaDollarSign, FaWarehouse } from 'react-icons/fa';
import { BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { productAPI } from '@/lib/api';

export default function InventoryDashboard() {
  const [inventoryData, setInventoryData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchInventoryData();
  }, []);

  const fetchInventoryData = async () => {
    try {
      const data = await productAPI.getInventorySummary();
      setInventoryData(data);
    } catch (error) {
      console.error('Error fetching inventory:', error);
    } finally {
      setLoading(false);
    }
  };

  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899', '#6366F1', '#14B8A6'];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  const pieData = inventoryData?.by_category?.map((item: any, index: number) => ({
    name: item.category,
    value: item.count,
    color: COLORS[index % COLORS.length],
  })) || [];

  const barData = inventoryData?.by_category?.map((item: any) => ({
    category: item.category,
    stock: item.total_stock,
    productos: item.count,
  })) || [];

  return (
    <div className="max-w-7xl mx-auto p-6">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h2 className="text-3xl font-bold text-gray-800 mb-2">
          Dashboard de Inventario
        </h2>
        <p className="text-gray-600">
          Visualización en tiempo real del estado del inventario
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Total Productos</p>
              <p className="text-2xl font-bold text-gray-800">{inventoryData?.total_products || 0}</p>
            </div>
            <FaBox className="text-blue-600 text-3xl" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Stock Total</p>
              <p className="text-2xl font-bold text-gray-800">{inventoryData?.total_stock || 0}</p>
            </div>
            <FaWarehouse className="text-green-600 text-3xl" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Categorías</p>
              <p className="text-2xl font-bold text-gray-800">{inventoryData?.by_category?.length || 0}</p>
            </div>
            <FaChartPie className="text-purple-600 text-3xl" />
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.4 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600">Valor Total</p>
              <p className="text-2xl font-bold text-gray-800">
                ${(inventoryData?.total_value || 0).toLocaleString('es-MX')}
              </p>
            </div>
            <FaDollarSign className="text-yellow-600 text-3xl" />
          </div>
        </motion.div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold mb-4 text-gray-900">Distribución por Categoría</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={(entry) => `${entry.name}: ${entry.value}`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <h3 className="text-lg font-semibold mb-4 text-gray-900">Stock por Categoría</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="category" angle={-45} textAnchor="end" height={80} tick={{ fontSize: 12 }} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="stock" fill="#3B82F6" name="Stock Total" />
              <Bar dataKey="productos" fill="#10B981" name="Cantidad de Productos" />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
        className="mt-6 bg-white rounded-lg shadow-md p-6"
      >
        <h3 className="text-lg font-semibold mb-4 text-gray-900">Productos con Bajo Stock</h3>
        <div className="space-y-2">
          {inventoryData?.low_stock_products?.map((product: any) => (
            <div key={product.id} className="flex items-center justify-between p-3 bg-red-50 rounded-lg">
              <div>
                <p className="font-medium text-gray-900">{product.name}</p>
                <p className="text-sm text-gray-900">{product.brand} - {product.model}</p>
              </div>
              <div className="text-right">
                <p className="text-red-600 font-semibold">{product.stock} unidades</p>
                <p className="text-sm text-gray-900">${product.price.toLocaleString('es-MX')}</p>
              </div>
            </div>
          ))}
          {(!inventoryData?.low_stock_products || inventoryData.low_stock_products.length === 0) && (
            <p className="text-gray-900 text-center py-4">No hay productos con stock bajo</p>
          )}
        </div>
      </motion.div>
    </div>
  );
} 
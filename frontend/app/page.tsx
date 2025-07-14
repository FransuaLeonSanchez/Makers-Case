'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { FaRobot, FaChartLine, FaBoxes, FaShoppingBag } from 'react-icons/fa';
import Chat from '@/components/Chat';
import Recommendations from '@/components/Recommendations';
import InventoryDashboard from '@/components/InventoryDashboard';
import Products from '@/components/Products';

export default function Home() {
  const [activeTab, setActiveTab] = useState('home');

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-40">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-800">
                Makers Tech
              </h1>
              <span className="ml-2 text-sm text-gray-600">| AI Assistant</span>
            </div>
            
            <div className="flex space-x-8">
              <button
                onClick={() => setActiveTab('home')}
                className={`text-sm font-medium transition-colors ${
                  activeTab === 'home'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                } pb-1`}
              >
                Inicio
              </button>
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`text-sm font-medium transition-colors ${
                  activeTab === 'recommendations'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                } pb-1`}
              >
                Recomendaciones
              </button>
              <button
                onClick={() => setActiveTab('products')}
                className={`text-sm font-medium transition-colors ${
                  activeTab === 'products'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                } pb-1`}
              >
                Productos
              </button>
              <button
                onClick={() => setActiveTab('metrics')}
                className={`text-sm font-medium transition-colors ${
                  activeTab === 'metrics'
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-gray-900'
                } pb-1`}
              >
                Métricas
              </button>
            </div>
          </div>
        </nav>
      </header>

      <main>
        {activeTab === 'home' && (
          <div className="max-w-7xl mx-auto px-4 py-12">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="text-center mb-12"
            >
              <h2 className="text-4xl font-bold text-gray-800 mb-4">
                Bienvenido a Makers Tech
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Tu tienda de tecnología con asistente virtual inteligente. 
                Descubre productos, obtén recomendaciones personalizadas y 
                gestiona tu inventario con IA.
              </p>
            </motion.div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.2 }}
                className="bg-white rounded-lg shadow-lg p-8 text-center hover:shadow-xl transition-shadow"
              >
                <FaRobot className="text-5xl text-blue-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Chat Inteligente</h3>
                <p className="text-gray-600">
                  Pregunta sobre productos, precios y disponibilidad. 
                  Nuestro asistente está aquí para ayudarte 24/7.
                </p>
                <div className="mt-4 text-sm text-gray-500">
                  Haz clic en el icono azul en la esquina inferior derecha
                </div>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.3 }}
                className="bg-white rounded-lg shadow-lg p-8 text-center hover:shadow-xl transition-shadow"
              >
                <FaChartLine className="text-5xl text-green-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Recomendaciones Personalizadas</h3>
                <p className="text-gray-600">
                  Obtén sugerencias basadas en tu presupuesto, 
                  preferencias y necesidades específicas.
                </p>
                <button
                  onClick={() => setActiveTab('recommendations')}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
                >
                  Ver Recomendaciones →
                </button>
              </motion.div>

              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: 0.4 }}
                className="bg-white rounded-lg shadow-lg p-8 text-center hover:shadow-xl transition-shadow"
              >
                <FaBoxes className="text-5xl text-purple-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold mb-2">Dashboard de Métricas</h3>
                <p className="text-gray-600">
                  Visualiza estadísticas de uso, preferencias de usuarios
                  y análisis detallados del comportamiento.
                </p>
                <button
                  onClick={() => setActiveTab('metrics')}
                  className="mt-4 text-blue-600 hover:text-blue-700 font-medium"
                >
                  Ver Métricas →
                </button>
              </motion.div>
            </div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6 }}
              className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg shadow-lg p-12 text-white text-center"
            >
              <h3 className="text-3xl font-bold mb-4">
                Experiencia de Compra del Futuro
              </h3>
              <p className="text-lg mb-8 max-w-2xl mx-auto">
                Combinamos la comodidad del comercio electrónico con 
                la inteligencia artificial para ofrecerte una experiencia 
                de compra única y personalizada.
              </p>
              <div className="flex flex-wrap justify-center gap-8 text-sm">
                <div>
                  <div className="text-3xl font-bold">29+</div>
                  <div>Productos</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">24/7</div>
                  <div>Asistencia</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">100%</div>
                  <div>Personalizado</div>
                </div>
                <div>
                  <div className="text-3xl font-bold">IA</div>
                  <div>Avanzada</div>
                </div>
              </div>
            </motion.div>
          </div>
        )}

        {activeTab === 'recommendations' && <Recommendations />}
        {activeTab === 'products' && <Products />}
        {activeTab === 'metrics' && <InventoryDashboard />}
      </main>

      <Chat />
    </div>
  );
}

'use client';

import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaPaperPlane, FaSpinner, FaTrash } from 'react-icons/fa';
import { BsChat } from 'react-icons/bs';
import { useWebSocket } from '@/hooks/useWebSocket';
import ChatMessage from './ChatMessage';

export default function Chat() {
  const [input, setInput] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const websocketUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000/ws';
    
  const { messages, sendMessage, isConnected, isTyping, clearMessages } = useWebSocket(websocketUrl);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && isConnected) {
      sendMessage(input.trim());
      setInput('');
    }
  };

  const handleClearChat = async () => {
    if (confirm('¿Estás seguro de que quieres limpiar el historial de chat?')) {
      clearMessages();
      // También limpiar en el backend
      try {
        await fetch('/api/chat/clear', { method: 'DELETE' });
      } catch (error) {
        console.error('Error clearing chat history:', error);
      }
    }
  };

  return (
    <>
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            transition={{ duration: 0.3 }}
            className="fixed bottom-20 right-4 w-96 h-[600px] bg-white rounded-lg shadow-2xl flex flex-col z-50"
          >
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-t-lg flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold">Asistente de Makers Tech</h3>
                <p className="text-sm opacity-90">
                  {isConnected ? 'En línea' : 'Conectando...'}
                </p>
              </div>
              {messages.length > 0 && (
                <button
                  onClick={handleClearChat}
                  className="text-white hover:text-gray-200 transition-colors p-1"
                  title="Limpiar historial"
                >
                  <FaTrash size={16} />
                </button>
              )}
            </div>

            <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
              {messages.length === 0 && (
                <div className="text-center text-gray-700 mt-8">
                  <p className="text-lg font-medium mb-2 text-gray-900">¡Hola! 👋</p>
                  <p className="text-sm text-gray-800">
                    Soy tu asistente virtual de Makers Tech. 
                    ¿En qué puedo ayudarte hoy?
                  </p>
                  <div className="mt-4 space-y-2">
                    <p className="text-xs text-gray-600">Puedes preguntarme sobre:</p>
                    <div className="flex flex-wrap gap-2 justify-center">
                      {['Computadoras', 'Laptops', 'Tablets', 'Smartphones'].map((category) => (
                        <button
                          key={category}
                          onClick={() => {
                            setInput(`¿Qué ${category.toLowerCase()} tienen disponibles?`);
                          }}
                          className="text-xs bg-white text-gray-900 px-3 py-1 rounded-full shadow-sm hover:shadow-md transition-shadow"
                        >
                          {category}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {messages.map((msg, index) => (
                <ChatMessage
                  key={index}
                  message={msg.content}
                  isUser={msg.type === 'message'}
                  timestamp={msg.timestamp}
                />
              ))}

              {isTyping && (
                <div className="flex items-center gap-2 text-gray-700 ml-12">
                  <FaSpinner className="animate-spin" size={14} />
                  <span className="text-sm">Escribiendo...</span>
                </div>
              )}

              <div ref={messagesEndRef} />
            </div>

            <form onSubmit={handleSendMessage} className="p-4 border-t">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Escribe tu mensaje..."
                  className="flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm text-gray-900 placeholder-gray-600"
                  disabled={!isConnected}
                />
                <button
                  type="submit"
                  disabled={!isConnected || !input.trim()}
                  className="bg-blue-600 text-white p-2 rounded-full hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <FaPaperPlane size={16} />
                </button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.button
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        onClick={() => setIsOpen(!isOpen)}
        className="fixed bottom-4 right-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-4 rounded-full shadow-lg hover:shadow-xl transition-shadow z-50"
      >
        <BsChat size={24} />
      </motion.button>
    </>
  );
} 
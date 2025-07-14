# Makers Tech Frontend

Frontend moderno para el sistema de ecommerce con chatbot inteligente de Makers Tech.

## Características

- 🤖 **Chat Inteligente**: Asistente virtual con IA para consultas sobre productos
- 📊 **Sistema de Recomendaciones**: Productos personalizados según preferencias
- 📈 **Dashboard de Inventario**: Visualización de métricas en tiempo real
- 🎨 **UI/UX Moderna**: Interfaz atractiva y responsiva con animaciones
- ⚡ **Tiempo Real**: Comunicación WebSocket para respuestas instantáneas

## Tecnologías

- Next.js 14 con App Router
- TypeScript
- Tailwind CSS
- Framer Motion (animaciones)
- Recharts (gráficos)
- Socket.io Client (WebSocket)
- React Icons

## Instalación

1. Asegúrate de que el backend esté ejecutándose en `http://localhost:8000`

2. Instala las dependencias:
```bash
npm install
```

3. Ejecuta el servidor de desarrollo:
```bash
npm run dev
```

4. Abre [http://localhost:3000](http://localhost:3000) en tu navegador

## Estructura del Proyecto

```
frontend/
├── app/                    # Rutas y páginas de Next.js
│   ├── page.tsx           # Página principal
│   └── layout.tsx         # Layout principal
├── components/            # Componentes React
│   ├── Chat.tsx          # Componente de chat
│   ├── ChatMessage.tsx   # Mensajes individuales
│   ├── ProductCard.tsx   # Tarjetas de productos
│   ├── Recommendations.tsx # Sistema de recomendaciones
│   └── InventoryDashboard.tsx # Dashboard de inventario
├── hooks/                # Custom hooks
│   └── useWebSocket.ts   # Hook para WebSocket
└── lib/                  # Utilidades y API
    └── api.ts           # Cliente API

```

## Uso

### Chat
- Haz clic en el botón azul en la esquina inferior derecha
- Escribe preguntas sobre productos, precios o disponibilidad
- El asistente responderá en español con información detallada

### Recomendaciones
- Ve a la pestaña "Recomendaciones"
- Configura tus preferencias (presupuesto, categorías, marcas, uso)
- Haz clic en "Buscar Recomendaciones"
- Los productos se mostrarán categorizados por nivel de recomendación

### Dashboard
- Ve a la pestaña "Inventario"
- Visualiza métricas en tiempo real
- Revisa productos con bajo stock
- Analiza distribución por categorías

## Configuración

Las variables de entorno están en `.env.local`:
- `NEXT_PUBLIC_API_URL`: URL del backend (default: http://localhost:8000)
- `NEXT_PUBLIC_WS_URL`: URL del WebSocket (default: ws://localhost:8000/ws/chat)

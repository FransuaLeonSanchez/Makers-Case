# 🚀 Makers Tech ChatBot

Un sistema inteligente de chatbot para venta de productos tecnológicos con recomendaciones dinámicas y análisis de comportamiento del usuario.

## 📋 Descripción

Makers Tech ChatBot es una aplicación web moderna que combina inteligencia artificial con un sistema completo de e-commerce para productos tecnológicos. El sistema utiliza GPT-4 para proporcionar asistencia personalizada y genera recomendaciones dinámicas basadas en las interacciones del usuario.

## ✨ Características Principales

### 🤖 Chatbot Inteligente
- **IA Conversacional**: Implementado con OpenAI GPT-4 y LangChain
- **Comunicación en Tiempo Real**: WebSocket para respuestas instantáneas
- **Respuestas Múltiples**: Sistema que divide respuestas largas en mensajes naturales
- **Confirmación de Compras**: Proceso de venta con confirmación y recopilación de datos
- **Contexto Persistente**: Historial de conversación guardado en base de datos

### 🎯 Sistema de Recomendaciones
- **Recomendaciones Dinámicas**: Se actualizan automáticamente según categorías mencionadas
- **Preferencias Globales**: Sin sistema de sesiones, un historial único por usuario
- **Algoritmo Inteligente**: 
  - "Altamente recomendados": Productos de la última categoría preguntada
  - "Recomendados": Productos de la penúltima categoría preguntada
- **Actualización Manual**: Sistema sin auto-refresh, actualización por demanda

### 📊 Dashboard de Métricas
- **Comportamiento del Usuario**: Análisis de interacciones y preferencias
- **Estadísticas de Inventario**: Control de stock y productos
- **Ventas Recientes**: Registro y seguimiento de transacciones
- **Métricas Visuales**: Tarjetas con gradientes y datos en tiempo real

### 🛍️ Catálogo de Productos
- **29 Productos**: Distribuidos en 8 categorías tecnológicas
- **Categorías Disponibles**:
  - Smartphones (5 productos)
  - Laptops (6 productos) 
  - Tablets (5 productos)
  - Monitores (4 productos)
  - Periféricos (3 productos)
  - Accesorios (3 productos)
  - Gaming (2 productos)
  - Audio (1 producto)
- **Información Detallada**: Especificaciones, precios, stock y descripciones

### 💰 Sistema de Ventas
- **Proceso de Compra**: Confirmación previa y recopilación de datos del cliente
- **Estados de Venta**: Pendiente, Confirmada, Cancelada
- **Registro Completo**: Historial de ventas con información detallada
- **Integración con Chat**: Compras iniciadas directamente desde el chatbot

## 🏗️ Arquitectura Técnica

### Frontend
- **Next.js 15**: Framework React con SSR y optimizaciones automáticas
- **React + TypeScript**: Componentes tipados y reutilizables
- **Tailwind CSS**: Diseño responsive y moderno
- **Framer Motion**: Animaciones fluidas
- **WebSocket Client**: Comunicación bidireccional en tiempo real

### Backend
- **FastAPI**: API REST moderna y rápida con Python
- **SQLAlchemy**: ORM para manejo de base de datos
- **WebSocket**: Comunicación en tiempo real
- **OpenAI Integration**: GPT-4 para respuestas inteligentes
- **LangChain**: Framework para aplicaciones con LLM

### Base de Datos
- **SQLite**: Base de datos ligera y eficiente
- **Tablas Principales**:
  - `products`: Catálogo de productos
  - `chat_history`: Historial de conversaciones
  - `global_user_preferences`: Preferencias sin sesiones
  - `user_interactions`: Registro de interacciones
  - `sales`: Registro de ventas

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8+
- Node.js 18+
- npm o yarn

### Configuración del Backend

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd Makers-Case
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env
OPENAI_API_KEY=tu_clave_de_openai
```

5. **Inicializar base de datos**
```bash
python main.py
```

### Configuración del Frontend

1. **Navegar al directorio frontend**
```bash
cd frontend
```

2. **Instalar dependencias**
```bash
npm install
```

3. **Configurar variables de entorno**
```bash
# Crear archivo .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

4. **Ejecutar en desarrollo**
```bash
npm run dev
```

## 🔧 Uso del Sistema

### Ejecutar la Aplicación

1. **Iniciar Backend**
```bash
# En el directorio raíz
python main.py
```
El backend estará disponible en `http://localhost:8000`

2. **Iniciar Frontend**
```bash
# En el directorio frontend
npm run dev
```
El frontend estará disponible en `http://localhost:3000`

### Funcionalidades

1. **Chat**: Interactúa con el bot para consultas sobre productos
2. **Productos**: Explora el catálogo completo con filtros y búsqueda
3. **Métricas**: Visualiza estadísticas de uso y comportamiento
4. **Tecnologías**: Información sobre el stack tecnológico

## 📚 Estructura del Proyecto

```
Makers-Case/
├── backend/
│   ├── api/                 # Endpoints de la API
│   ├── models/              # Modelos de base de datos
│   ├── services/            # Lógica de negocio
│   └── main.py             # Punto de entrada
├── frontend/
│   ├── app/                # Páginas de Next.js
│   ├── components/         # Componentes React
│   └── public/             # Archivos estáticos
├── products.db            # Base de datos SQLite
└── README.md              # Este archivo
```

## 🔄 Características del Sistema

### Sin Sistema de Sesiones
- **Historial Global**: Una sola conversación persistente
- **Preferencias Únicas**: Un registro de preferencias para todo el sistema
- **Simplicidad**: Sin complicaciones de manejo de múltiples sesiones

### Actualizaciones Dinámicas
- **Detección Automática**: Reconoce categorías mencionadas en el chat
- **Normalización**: Maneja formas plurales y variaciones de categorías
- **Límites Inteligentes**: Máximo 2 categorías preferidas, 3 marcas favoritas

### Sistema de Métricas
- **Comportamiento del Usuario**: Conteo de interacciones y patrones
- **Preferencias Visuales**: Top categorías y marcas con colores
- **Rango de Precios**: Análisis de preferencias económicas
- **Inventario**: Control de stock con alertas de bajo inventario

## 🌟 Tecnologías Utilizadas

| Categoría | Tecnología | Descripción |
|-----------|------------|-------------|
| **Frontend** | Next.js 15 | Framework React con SSR |
| | React | Biblioteca para interfaces de usuario |
| | TypeScript | JavaScript con tipado estático |
| | Tailwind CSS | Framework de utilidades CSS |
| **Backend** | FastAPI | Framework web Python moderno |
| | SQLAlchemy | ORM Python |
| | SQLite | Base de datos ligera |
| **IA** | OpenAI GPT-4 | Modelo de lenguaje |
| | LangChain | Framework para aplicaciones LLM |
| **Comunicación** | WebSocket | Protocolo de comunicación bidireccional |

## 📈 Métricas y Analytics

El sistema incluye un dashboard completo de métricas que proporciona:

- **Interacciones Totales**: Número de mensajes procesados
- **Categorías Preferidas**: Top 2 categorías más consultadas
- **Marcas Favoritas**: Marcas más mencionadas
- **Rango de Precios**: Análisis de preferencias de precio
- **Ventas Recientes**: Últimas transacciones registradas
- **Estado del Inventario**: Stock disponible por categoría

## 🛠️ Desarrollo y Contribución

### Comandos Útiles

```bash
# Backend - Ejecutar servidor de desarrollo
python main.py

# Frontend - Desarrollo
npm run dev

# Frontend - Build de producción
npm run build

# Frontend - Ejecutar producción
npm start
```

### Estructura de la Base de Datos

La aplicación utiliza SQLite con las siguientes tablas principales:

- **products**: Catálogo de productos con especificaciones
- **chat_history**: Historial completo de conversaciones
- **global_user_preferences**: Preferencias del usuario sin sesiones
- **user_interactions**: Registro de todas las interacciones
- **sales**: Registro de ventas y transacciones

## 📝 Notas de Desarrollo

### Cambios Principales Implementados

1. **Eliminación de Sesiones**: Migración de sistema basado en sesiones a preferencias globales
2. **Expansión del Catálogo**: Incremento de 14 a 29 productos
3. **Mejoras en Recomendaciones**: Algoritmo basado en última categoría mencionada
4. **Dashboard de Métricas**: Sistema completo de análisis de comportamiento
5. **Confirmación de Compras**: Proceso mejorado con validación
6. **Comunicación WebSocket**: Implementación de chat en tiempo real

### Problemas Resueltos

- ✅ Duplicación de categorías normalizadas
- ✅ Sobrescritura de preferencias corregida
- ✅ Commits explícitos en endpoints de chat
- ✅ Manejo de errores en llamadas API
- ✅ Configuración de variables de entorno

## 📄 Licencia

Este proyecto es parte de un caso de estudio para Makers y está destinado únicamente para fines educativos y de demostración.

---

**Desarrollado con ❤️ para demostrar capacidades de desarrollo full-stack con IA** 
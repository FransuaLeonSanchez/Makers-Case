# Sistema de Recomendaciones Inteligente - Makers Tech

## Descripción

El sistema de recomendaciones de Makers Tech es una solución basada en **Inteligencia Artificial** que aprende automáticamente de las interacciones del usuario para ofrecer recomendaciones personalizadas de productos.

## Características Principales

### 1. **Aprendizaje Automático**
- El sistema aprende de CADA interacción del usuario con el chatbot
- Detecta patrones de comportamiento y preferencias automáticamente
- No requiere configuración manual de filtros

### 2. **Integración con Chat**
Cuando un usuario interactúa con el chatbot:
- Si menciona una categoría (ej: "laptops"), se registra el interés
- Si pregunta por un producto específico, se guarda la preferencia
- Si busca por marca o características, se actualiza su perfil

### 3. **Recomendaciones en Tiempo Real**
Las recomendaciones se actualizan automáticamente basándose en:
- **Categorías visitadas**: Productos similares a los que ha consultado
- **Marcas preferidas**: Detectadas por las búsquedas y menciones
- **Rango de precio**: Calculado según los productos que ha visto
- **Historial de interacciones**: Evita mostrar productos ya vistos recientemente

### 4. **Categorización Inteligente**
Los productos se clasifican en tres niveles:
- **⭐⭐⭐ Altamente Recomendados**: Coinciden perfectamente con las preferencias
- **⭐⭐ Recomendados**: Buenos matches con el perfil del usuario
- **⭐ Otras opciones**: Productos alternativos disponibles

## Arquitectura Técnica

### Base de Datos
```sql
-- Tabla de interacciones
user_interactions:
  - session_id: Identificador único del usuario
  - product_id: Producto visto/mencionado
  - category_viewed: Categoría consultada
  - search_query: Búsqueda realizada
  - interaction_type: Tipo de interacción
  - timestamp: Momento de la interacción

-- Tabla de preferencias
user_preferences:
  - session_id: Usuario único
  - preferred_categories: Top 3 categorías
  - preferred_brands: Top 3 marcas
  - price_range_min/max: Rango de precio preferido
  - interaction_count: Número de interacciones
```

### Algoritmo de Puntuación

Cada producto recibe una puntuación de 0-100 basada en:
1. **Categoría preferida** (30 puntos máx)
2. **Marca preferida** (25 puntos máx)
3. **Rango de precio** (20 puntos máx)
4. **Disponibilidad** (15 puntos máx)
5. **Similitud con productos vistos** (10 puntos máx)

### Flujo de Datos

1. **Usuario pregunta al chatbot**: "¿Qué laptops tienen?"
2. **Sistema registra interacción**: Categoría=LAPTOPS, tipo=chat_mention
3. **Actualiza preferencias**: LAPTOPS sube en ranking de categorías
4. **Recalcula recomendaciones**: Prioriza laptops en futuras sugerencias

## API Endpoints

### Obtener Recomendaciones
```
POST /api/recommendations?session_id={session_id}
```
Retorna productos categorizados según el perfil del usuario.

### Ver Preferencias del Usuario
```
GET /api/recommendations/user-preferences/{session_id}
```
Muestra las preferencias aprendidas del usuario.

### Registrar Interacción Manual
```
POST /api/recommendations/track-interaction
{
  "session_id": "xxx",
  "product_id": 123,
  "interaction_type": "view"
}
```

## Ventajas del Sistema

1. **Zero-config**: No requiere que el usuario configure filtros manualmente
2. **Adaptativo**: Mejora con cada interacción
3. **Contextual**: Entiende el contexto de las búsquedas
4. **Persistente**: Mantiene las preferencias entre sesiones
5. **Privado**: Usa session_id anónimo, no requiere login

## Ejemplo de Uso

1. Usuario nuevo entra al sitio
2. Pregunta al chat: "¿Tienen tablets?"
3. Sistema registra interés en TABLETS
4. Usuario pregunta: "¿Qué tal el iPad Pro?"
5. Sistema detecta preferencia por Apple
6. En Recomendaciones aparecen:
   - Altamente recomendado: iPad Pro (coincide categoría + marca)
   - Recomendado: MacBook Air (misma marca)
   - Otras opciones: Samsung Galaxy Tab (misma categoría)

## Métricas de Éxito

- **Precisión**: Productos recomendados que coinciden con búsquedas
- **Engagement**: Clicks en productos recomendados
- **Conversión**: Compras desde recomendaciones
- **Aprendizaje**: Tiempo para detectar preferencias (usualmente 3-5 interacciones) 
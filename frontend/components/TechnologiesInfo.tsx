'use client';

import { motion } from 'framer-motion';
import { 
  FaPython, 
  FaReact, 
  FaDatabase, 
  FaServer, 
  FaCode, 
  FaBrain,
  FaRocket,
  FaPalette
} from 'react-icons/fa';
import { 
  SiTypescript, 
  SiNextdotjs, 
  SiFastapi, 
  SiTailwindcss,
  SiOpenai,
  SiSqlite
} from 'react-icons/si';
import { BiNetworkChart } from 'react-icons/bi';

export default function TechnologiesInfo() {
  const technologies = [
    {
      category: "Frontend (Interfaz de Usuario)",
      icon: <FaReact className="text-4xl text-blue-500" />,
      description: "La parte visual que interactúas en tu navegador",
      techs: [
        {
          name: "Next.js 15",
          icon: <SiNextdotjs className="text-2xl" />,
          description: "Framework de React para crear aplicaciones web modernas. Es como un kit completo que incluye todo lo necesario para hacer páginas web rápidas.",
          whyUse: "Porque maneja automáticamente la navegación, optimización de imágenes y muchas cosas que serían complicadas de hacer desde cero."
        },
        {
          name: "React",
          icon: <FaReact className="text-2xl text-blue-400" />,
          description: "Biblioteca de JavaScript para construir interfaces de usuario. Permite crear componentes reutilizables como piezas de LEGO.",
          whyUse: "Hace que actualizar la página sea súper rápido sin recargar todo el navegador."
        },
        {
          name: "TypeScript",
          icon: <SiTypescript className="text-2xl text-blue-600" />,
          description: "JavaScript con superpoderes. Te ayuda a detectar errores antes de ejecutar el código.",
          whyUse: "Evita errores comunes y hace el código más fácil de mantener. Es como tener un corrector ortográfico para código."
        },
        {
          name: "Tailwind CSS",
          icon: <SiTailwindcss className="text-2xl text-cyan-500" />,
          description: "Framework de CSS que permite diseñar directamente en el HTML usando clases predefinidas.",
          whyUse: "En lugar de escribir CSS separado, puedes diseñar todo directamente donde lo necesitas. Súper rápido y eficiente."
        }
      ]
    },
    {
      category: "Backend (Servidor)",
      icon: <FaServer className="text-4xl text-green-500" />,
      description: "El cerebro detrás de la aplicación que procesa toda la lógica",
      techs: [
        {
          name: "Python 3",
          icon: <FaPython className="text-2xl text-yellow-500" />,
          description: "Lenguaje de programación fácil de leer y escribir. Es como escribir en inglés pero para computadoras.",
          whyUse: "Perfecto para principiantes, tiene muchísimas librerías y es el lenguaje #1 para IA."
        },
        {
          name: "FastAPI",
          icon: <SiFastapi className="text-2xl text-teal-500" />,
          description: "Framework moderno para crear APIs REST. Es súper rápido y genera documentación automáticamente.",
          whyUse: "Combina la simplicidad de Python con alto rendimiento. Perfecto para crear APIs modernas."
        },
        {
          name: "SQLAlchemy",
          icon: <FaDatabase className="text-2xl text-orange-500" />,
          description: "ORM (Object Relational Mapper) que permite trabajar con bases de datos usando código Python en lugar de SQL puro.",
          whyUse: "Convierte las tablas de la base de datos en objetos Python, haciendo el código más intuitivo."
        }
      ]
    },
    {
      category: "Base de Datos",
      icon: <FaDatabase className="text-4xl text-purple-500" />,
      description: "Donde se guarda toda la información de productos, ventas y chats",
      techs: [
        {
          name: "SQLite",
          icon: <SiSqlite className="text-2xl text-blue-700" />,
          description: "Base de datos ligera que guarda todo en un solo archivo. No necesita instalación separada.",
          whyUse: "Perfecta para proyectos pequeños y medianos. Súper fácil de usar y no requiere configuración."
        }
      ]
    },
    {
      category: "Comunicación en Tiempo Real",
      icon: <BiNetworkChart className="text-4xl text-pink-500" />,
      description: "Para que el chat funcione instantáneamente",
      techs: [
        {
          name: "WebSocket",
          icon: <BiNetworkChart className="text-2xl text-pink-500" />,
          description: "Protocolo que permite comunicación bidireccional en tiempo real entre el navegador y el servidor.",
          whyUse: "Permite que los mensajes del chat aparezcan instantáneamente sin recargar la página."
        }
      ]
    },
    {
      category: "Inteligencia Artificial",
      icon: <FaBrain className="text-4xl text-red-500" />,
      description: "El asistente inteligente que responde las preguntas",
      techs: [
        {
          name: "OpenAI GPT-4",
          icon: <SiOpenai className="text-2xl" />,
          description: "Modelo de lenguaje avanzado que entiende y genera texto en español de forma natural.",
          whyUse: "Permite crear un chatbot que realmente entiende lo que le preguntas y responde de forma coherente."
        },
        {
          name: "LangChain",
          icon: <FaCode className="text-2xl text-gray-600" />,
          description: "Framework para construir aplicaciones con modelos de lenguaje. Facilita la integración con OpenAI.",
          whyUse: "Simplifica el manejo de conversaciones, contexto y memoria del chat."
        }
      ]
    }
  ];

  const learningPath = [
    {
      step: 1,
      title: "HTML & CSS Básico",
      description: "Aprende la estructura y diseño de páginas web",
      time: "2-3 semanas"
    },
    {
      step: 2,
      title: "JavaScript Fundamentals",
      description: "Entiende la programación básica y lógica",
      time: "1-2 meses"
    },
    {
      step: 3,
      title: "React Basics",
      description: "Aprende componentes y estado",
      time: "1 mes"
    },
    {
      step: 4,
      title: "Python para Backend",
      description: "Sintaxis básica y conceptos de programación",
      time: "1-2 meses"
    },
    {
      step: 5,
      title: "Bases de Datos SQL",
      description: "Cómo guardar y consultar información",
      time: "2-3 semanas"
    },
    {
      step: 6,
      title: "APIs REST",
      description: "Cómo frontend y backend se comunican",
      time: "2 semanas"
    }
  ];

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <h1 className="text-3xl font-bold text-gray-900 mb-4">
          🚀 Stack Tecnológico del Proyecto
        </h1>
        <p className="text-lg text-gray-600">
          Descubre las herramientas y tecnologías que hacen posible esta aplicación
        </p>
      </motion.div>

      {/* Arquitectura Overview */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-6"
      >
        <h2 className="text-xl font-semibold mb-4 text-gray-900">
          🏗️ Arquitectura de la Aplicación
        </h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="text-center mb-2">
              <FaPalette className="text-3xl text-blue-500 mx-auto" />
            </div>
            <h3 className="font-semibold text-center">Frontend</h3>
            <p className="text-sm text-gray-600 text-center">
              Lo que ves e interactúas
            </p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="text-center mb-2">
              <FaRocket className="text-3xl text-green-500 mx-auto" />
            </div>
            <h3 className="font-semibold text-center">Backend</h3>
            <p className="text-sm text-gray-600 text-center">
              Procesa la lógica y datos
            </p>
          </div>
          <div className="bg-white rounded-lg p-4 shadow-sm">
            <div className="text-center mb-2">
              <FaDatabase className="text-3xl text-purple-500 mx-auto" />
            </div>
            <h3 className="font-semibold text-center">Base de Datos</h3>
            <p className="text-sm text-gray-600 text-center">
              Guarda toda la información
            </p>
          </div>
        </div>
      </motion.div>

      {/* Tecnologías Detalladas */}
      {technologies.map((category, categoryIndex) => (
        <motion.div
          key={category.category}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 + categoryIndex * 0.1 }}
          className="bg-white rounded-lg shadow-md p-6"
        >
          <div className="flex items-center gap-4 mb-6">
            {category.icon}
            <div>
              <h2 className="text-2xl font-bold text-gray-900">
                {category.category}
              </h2>
              <p className="text-gray-600">{category.description}</p>
            </div>
          </div>

          <div className="space-y-4">
            {category.techs.map((tech, techIndex) => (
              <motion.div
                key={tech.name}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + categoryIndex * 0.1 + techIndex * 0.05 }}
                className="border-l-4 border-blue-400 pl-4 py-2"
              >
                <div className="flex items-center gap-3 mb-2">
                  {tech.icon}
                  <h3 className="text-lg font-semibold text-gray-900">
                    {tech.name}
                  </h3>
                </div>
                <p className="text-gray-700 mb-2">{tech.description}</p>
                <div className="bg-gray-50 rounded p-3">
                  <p className="text-sm text-gray-600">
                    <span className="font-semibold">¿Por qué lo usamos?</span> {tech.whyUse}
                  </p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      ))}

      {/* Ruta de Aprendizaje */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.8 }}
        className="bg-gradient-to-br from-green-50 to-blue-50 rounded-lg p-6"
      >
        <h2 className="text-2xl font-bold text-gray-900 mb-6 text-center">
          📚 Ruta de Aprendizaje Recomendada
        </h2>
        <p className="text-center text-gray-600 mb-6">
          Si quieres aprender a crear algo similar, este es el camino sugerido:
        </p>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {learningPath.map((item) => (
            <motion.div
              key={item.step}
              whileHover={{ scale: 1.05 }}
              className="bg-white rounded-lg p-4 shadow-md"
            >
              <div className="flex items-center gap-3 mb-2">
                <div className="w-8 h-8 bg-blue-500 text-white rounded-full flex items-center justify-center font-bold">
                  {item.step}
                </div>
                <h3 className="font-semibold text-gray-900">{item.title}</h3>
              </div>
              <p className="text-sm text-gray-600 mb-2">{item.description}</p>
              <p className="text-xs text-blue-600 font-semibold">
                ⏱️ Tiempo estimado: {item.time}
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Tips para Principiantes */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.9 }}
        className="bg-yellow-50 rounded-lg p-6"
      >
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          💡 Tips para Principiantes
        </h2>
        <ul className="space-y-2">
          <li className="flex items-start gap-2">
            <span className="text-yellow-600 mt-1">•</span>
            <span className="text-gray-700">
              <strong>Empieza con lo básico:</strong> No intentes aprender todo de una vez. Domina HTML/CSS antes de saltar a React.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-yellow-600 mt-1">•</span>
            <span className="text-gray-700">
              <strong>Practica mucho:</strong> La programación se aprende haciendo. Crea proyectos pequeños para practicar.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-yellow-600 mt-1">•</span>
            <span className="text-gray-700">
              <strong>No te frustres con los errores:</strong> Los errores son normales y son la mejor forma de aprender.
            </span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-yellow-600 mt-1">•</span>
            <span className="text-gray-700">
              <strong>Usa la documentación:</strong> Cada tecnología tiene documentación oficial. Aprende a leerla.
            </span>
          </li>
        </ul>
      </motion.div>
    </div>
  );
} 
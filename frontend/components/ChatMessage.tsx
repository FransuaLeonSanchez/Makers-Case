'use client';

import { motion } from 'framer-motion';
import { FaUser, FaRobot } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';

interface ChatMessageProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

export default function ChatMessage({ message, isUser, timestamp }: ChatMessageProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}
    >
      <div
        className={`flex max-w-[70%] ${
          isUser ? 'flex-row-reverse' : 'flex-row'
        } items-start gap-3`}
      >
        <div
          className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center ${
            isUser ? 'bg-blue-600' : 'bg-green-600'
          }`}
        >
          {isUser ? (
            <FaUser className="text-white" size={18} />
          ) : (
            <FaRobot className="text-white" size={18} />
          )}
        </div>
        
        <div
          className={`px-4 py-3 rounded-2xl ${
            isUser
              ? 'bg-blue-100 text-gray-900'
              : 'bg-gray-100 text-gray-900'
          } shadow-sm`}
        >
          {isUser ? (
            <p className="text-sm">{message}</p>
          ) : (
            <div className="text-sm prose prose-sm max-w-none">
              <ReactMarkdown>
                {message}
              </ReactMarkdown>
            </div>
          )}
          
          {timestamp && (
            <p className="text-xs text-gray-500 mt-1">
              {new Date(timestamp).toLocaleTimeString()}
            </p>
          )}
        </div>
      </div>
    </motion.div>
  );
} 
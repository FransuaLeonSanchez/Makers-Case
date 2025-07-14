import { useEffect, useRef, useState, useCallback } from 'react';

interface WebSocketMessage {
  type: 'message' | 'response' | 'error' | 'info';
  content: string;
  timestamp?: string;
}

export function useWebSocket(url: string) {
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      console.log('WebSocket connected');
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'typing') {
        setIsTyping(true);
      } else if (data.type === 'response') {
        setIsTyping(false);
        setMessages((prev) => [...prev, {
          type: 'response',
          content: data.response,
          timestamp: new Date().toISOString(),
        }]);
      } else if (data.type === 'error') {
        setIsTyping(false);
        setMessages((prev) => [...prev, {
          type: 'error',
          content: data.message,
          timestamp: new Date().toISOString(),
        }]);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      console.log('WebSocket disconnected');
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = useCallback((message: string) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      setMessages((prev) => [...prev, {
        type: 'message',
        content: message,
        timestamp: new Date().toISOString(),
      }]);
      
      wsRef.current.send(JSON.stringify({
        message,
        session_id: sessionStorage.getItem('chatSessionId') || undefined,
      }));
    }
  }, []);

  return {
    messages,
    sendMessage,
    isConnected,
    isTyping,
  };
} 
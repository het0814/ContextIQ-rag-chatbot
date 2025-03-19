import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';

const ChatComponent = ({ onSubmitQuery, response }) => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [currentTyping, setCurrentTyping] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (response) {
      setIsTyping(true);
      setCurrentTyping(response[0]);

      let index = 1; 
      const typingInterval = setInterval(() => {
        if (index < response.length) {
          setCurrentTyping((prev) => prev + response[index]);
          index++;
        } else {
          clearInterval(typingInterval);
          setIsTyping(false);
          setMessages((prev) => [
            ...prev,
            { type: 'bot', text: response }
          ]);
          setCurrentTyping('');
        }
      }, 20);

      return () => clearInterval(typingInterval);
    }
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (input.trim()) {
      setMessages((prev) => [...prev, { type: 'user', text: input }]);
      onSubmitQuery(input);
      setInput('');
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, currentTyping]);

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            className={`message ${msg.type}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {msg.text}
          </motion.div>
        ))}
        {isTyping && (
          <div className="message bot">
            {currentTyping || 'Typing...'}
          </div>
        )}
        <div ref={messagesEndRef}></div>
      </div>
      <form onSubmit={handleSubmit} className="input-area">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default ChatComponent;

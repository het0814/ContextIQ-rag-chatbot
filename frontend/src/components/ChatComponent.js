import React, { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";

const ChatComponent = ({ onSubmitQuery, response }) => {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [currentTyping, setCurrentTyping] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    if (response) {
      setIsTyping(true);
      setCurrentTyping("");

      let index = -1;
      const typingInterval = setInterval(() => {
        if (index < response.length) {
          setCurrentTyping((prev) => prev + response[index]);
          index++;
        } else {
          clearInterval(typingInterval);
          setIsTyping(false);
          setMessages((prev) => [...prev, { type: "bot", text: response }]);
          setCurrentTyping("");
        }
      }, 40);

      return () => clearInterval(typingInterval);
    }
  }, [response]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      setMessages((prev) => [...prev, { type: "user", text: input }]);
      onSubmitQuery(input);
      setInput("");
    }
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, currentTyping]);

  return (
    <div className="flex flex-col h-[70vh] overflow-hidden">
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            className={`p-3 rounded-lg shadow ${
              msg.type === "user"
                ? "bg-blue-500 text-white self-end"
                : "bg-gray-200 text-black self-start"
            }`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            {msg.text}
          </motion.div>
        ))}
        {isTyping && (
          <motion.div
            className="p-3 bg-gray-300 text-black rounded-lg self-start"
            initial={{ opacity: 0.5 }}
            animate={{ opacity: 1 }}
            transition={{ repeat: Infinity, duration: 0.5 }}
          >
            {currentTyping || <TypingAnimation />}
          </motion.div>
        )}
        <div ref={messagesEndRef}></div>
      </div>
      <form onSubmit={handleSubmit} className="flex gap-2 p-3 bg-white border-t">
        <input
          type="text"
          className="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button className="p-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600">
          Send
        </button>
      </form>
    </div>
  );
};


const TypingAnimation = () => {
  return (
    <div className="flex space-x-1">
      <motion.div
        className="w-2 h-2 bg-black rounded-full"
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ repeat: Infinity, duration: 1, ease: "easeInOut" }}
      ></motion.div>
      <motion.div
        className="w-2 h-2 bg-black rounded-full"
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ repeat: Infinity, duration: 1, ease: "easeInOut", delay: 0.2 }}
      ></motion.div>
      <motion.div
        className="w-2 h-2 bg-black rounded-full"
        animate={{ opacity: [0.3, 1, 0.3] }}
        transition={{ repeat: Infinity, duration: 1, ease: "easeInOut", delay: 0.4 }}
      ></motion.div>
    </div>
  );
};

export default ChatComponent;

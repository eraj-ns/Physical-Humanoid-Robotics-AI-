import React, { useState, useEffect } from 'react';
import './ChatWidget.css';

const ChatWidget = ({ title = "Book Assistant" }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your Book Assistant. How can I help you today?", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use the environment variable for API URL, fallback to localhost
      const apiUrl = (typeof window !== 'undefined' && window.ENV)
        ? (window.ENV.REACT_APP_API_URL || 'http://localhost:8000')
        : 'http://localhost:8000';

      const response = await fetch(`${apiUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          max_tokens: 1024
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const botMessage = {
          id: Date.now() + 1,
          text: data.content,
          sender: 'bot',
          sources: data.sources,
          confidence: data.confidence
        };
        setMessages(prev => [...prev, botMessage]);
      } else {
        const errorText = await response.text();
        const errorMessage = {
          id: Date.now() + 1,
          text: `Error: ${errorText}`,
          sender: 'bot'
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: `Connection error: ${error.message}`,
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="chat-widget">
      {isOpen ? (
        <div className="chat-popup">
          <div className="chat-header">
            <span className="chat-title">{title}</span>
            <button className="chat-close" onClick={toggleChat}>×</button>
          </div>
          <div className="chat-messages" id="chat-messages">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.sender}`}>
                <div className="message-text">{message.text}</div>
                {message.sources && message.sources.length > 0 && (
                  <div className="message-sources">
                    <details>
                      <summary>Sources</summary>
                      <ul>
                        {message.sources.map((source, idx) => (
                          <li key={idx}>{typeof source === 'string' ? source : source.url || source.text || source.id || JSON.stringify(source)}</li>
                        ))}
                      </ul>
                    </details>
                  </div>
                )}
              </div>
            ))}
            {isLoading && (
              <div className="message bot">
                <div className="message-text">Thinking...</div>
              </div>
            )}
          </div>
          <div className="chat-input-area">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book..."
              className="chat-input"
              rows="1"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className="chat-send"
            >
              Send
            </button>
          </div>
        </div>
      ) : null}

      <button className="chat-toggle" onClick={toggleChat}>
        💬
      </button>
    </div>
  );
};

export default ChatWidget;
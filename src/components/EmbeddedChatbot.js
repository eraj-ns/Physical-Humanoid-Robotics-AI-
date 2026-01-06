import React from 'react';
import ChatWidget from './ChatWidget';
import './EmbeddedChatbot.css';

const EmbeddedChatbot = ({ title = "Book Assistant" }) => {
  return (
    <div className="embedded-chatbot-container">
      <ChatWidget title={title} />
    </div>
  );
};

export default EmbeddedChatbot;
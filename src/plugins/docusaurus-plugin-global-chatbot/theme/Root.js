import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

// This component will be rendered at the root level of the application
const Root = ({ children }) => {
  return (
    <>
      {children}
      <ChatWidget title="Book Assistant" />
    </>
  );
};

export default Root;
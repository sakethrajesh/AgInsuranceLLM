import React, { useState } from 'react';
import { Chat } from './chat';
import { Header } from './header';

export function ChatContainer() {
  const defaultModel = 'llama2:chat';
  const [selectedModel, setSelectedModel] = useState(defaultModel);

  return (
    <>
      <Header selectedModel={selectedModel} /> {/* Pass selectedModel to Header */}
      <Chat selectedModel={selectedModel} onModelChange={setSelectedModel} />
    </>
  );
}
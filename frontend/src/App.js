import React, { useState } from 'react';
import axios from 'axios';
import ChatComponent from './components/ChatComponent';
import FileUpload from './components/FileUpload';

function App() {
  const [response, setResponse] = useState("");

  const handleQuerySubmit = async (query) => {
    try {
      const res = await axios.post('http://localhost:8000/generate-response', { query });
      setResponse(res.data.response);
    } catch (error) {
      console.error(error);
      setResponse("Error generating response.");
    }
  };

  return (
    <div className="App">
      <h1>ContextIQ - RAG Chatbot</h1>
      <div style={{ display: "flex", justifyContent: "space-between" }}>
        <div style={{ flex: 1 }}>
          <ChatComponent onSubmitQuery={handleQuerySubmit} response={response} />
        </div>
        <div style={{ flex: 1, marginLeft: "20px" }}>
          <FileUpload />
        </div>
      </div>
    </div>
  );
}

export default App;
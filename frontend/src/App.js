import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ChatComponent from './components/ChatComponent';
import FileUpload from './components/FileUpload';

function App() {
  const [response, setResponse] = useState("");
  const [contextSources, setContextSources] = useState([]);

  const fetchContextSources = async () => {
    try {
      const res = await axios.get('http://localhost:8000/get-context-sources');
      setContextSources(res.data.context_sources);
    } catch (error) {
      console.error("Error fetching context sources:", error);
    }
  };

  useEffect(() => {
    fetchContextSources();
  }, []);

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
    <div className="app">
      <h1 className="header">ContextIQ - RAG Chatbot</h1>
      <div className="container">
        {/* Chat Window */}
        <div className="chat-window">
          <ChatComponent onSubmitQuery={handleQuerySubmit} response={response} />
        </div>

        {/* Upload + Context Sources */}
        <div className="sidebar">
          <FileUpload onUploadSuccess={fetchContextSources} />
          <div className="context-list">
            <h3>Added Context Sources</h3>
            <ul>
              {contextSources.length > 0 ? (
                contextSources.map((source, index) => (
                  <li key={index}>{source.source || "Unnamed document"}</li>
                ))
              ) : (
                <li>No context sources added yet.</li>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

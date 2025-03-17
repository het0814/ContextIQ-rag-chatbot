import React, { useState } from 'react';

function ChatComponent({ onSubmitQuery, response }) {
  const [query, setQuery] = useState("");

  const handleInputChange = (e) => setQuery(e.target.value);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmitQuery(query);
    setQuery("");
  };

  return (
    <div>
      <h2>Chat</h2>
      <form onSubmit={handleSubmit}>
        <input 
          type="text" 
          value={query}
          onChange={handleInputChange}
          placeholder="Ask a question..." 
          style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
        />
        <button type="submit">Ask</button>
      </form>
      {response && (
        <div>
          <h3>Response:</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}

export default ChatComponent;

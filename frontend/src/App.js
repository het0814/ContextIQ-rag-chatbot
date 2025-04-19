import React, { useState, useEffect } from "react";
import axios from "axios";
import ChatComponent from "./components/ChatComponent";
import FileUpload from "./components/FileUpload";
import { Toaster, toast } from "react-hot-toast";

function App() {
  const [response, setResponse] = useState("");
  const [contextSources, setContextSources] = useState([]);

  const fetchContextSources = async () => {
    try {
      const res = await axios.get("http://localhost:8000/get-context-sources");
      setContextSources(res.data.context_sources);
    } catch (error) {
      console.error("Error fetching context sources:", error);
      toast.error("Failed to fetch context sources!");
    }
  };

  useEffect(() => {
    fetchContextSources();
  }, []);

  const handleQuerySubmit = async (query) => {
    toast.loading("Generating response...");
    try {
      const res = await axios.post("http://localhost:8000/generate-response", { query });
      setResponse(res.data.response);
      toast.dismiss();
      toast.success("Response generated!");
    } catch (error) {
      console.error(error);
      setResponse("Error generating response.");
      toast.dismiss();
      toast.error("Failed to generate response!");
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-6">
      <Toaster />
      <h1 className="text-3xl font-bold text-blue-600 mb-6 flex items-center"><img src="/favicon.ico" alt="App Icon" className="w-12 h-12 mr-3" />ContextIQ - RAG Chatbot</h1>
      
      {/* Layout Wrapper */}
      <div className="w-full max-w-6xl flex flex-col lg:flex-row gap-6 px-4">
        
        {/* Upload Section */}
        <div className="w-full lg:w-1/3 bg-white shadow-lg rounded-lg p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-700">📂 Manage Context Sources</h2>
          <FileUpload onUploadSuccess={fetchContextSources} />
          <div className="mt-4">
            <h3 className="text-lg font-semibold">Added Context Sources</h3>
            <ul className="mt-2">
              {contextSources.length > 0 ? (
                contextSources.map((source, index) => (
                  <li key={index} className="text-sm text-gray-700">{source.source || "Unnamed document"}</li>
                ))
              ) : (
                <li className="text-sm text-gray-500">No context sources added yet.</li>
              )}
            </ul>
          </div>
        </div>

        {/* Chat Section */}
        <div className="flex-1 bg-white shadow-lg rounded-lg p-6">
          <ChatComponent onSubmitQuery={handleQuerySubmit} response={response} />
        </div>

      </div>
    </div>
  );
}

export default App;

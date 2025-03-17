import React, { useState } from 'react';
import axios from 'axios';

function FileUpload() {
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:8000/add-url', { url });
      alert("URL content added successfully.");
      setUrl("");
    } catch (error) {
      console.error(error);
      alert("Error adding URL.");
    }
  };

  const handleFileChange = (e) => setFile(e.target.files[0]);

  const handleFileUpload = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post('http://localhost:8000/upload-document', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      alert("File uploaded successfully.");
      setFile(null);
    } catch (error) {
      console.error(error);
      alert("Error uploading file.");
    }
  };

  return (
    <div>
      <h2>Upload File / URL</h2>
      <div>
        <form onSubmit={handleUrlSubmit}>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL"
            style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
          />
          <button type="submit">Add URL</button>
        </form>
      </div>
      <div>
        <form onSubmit={handleFileUpload}>
          <input 
            type="file" 
            onChange={handleFileChange} 
            accept=".pdf, .docx, .txt"
            style={{ marginBottom: "10px" }}
          />
          <button type="submit">Upload File</button>
        </form>
      </div>
    </div>
  );
}

export default FileUpload;

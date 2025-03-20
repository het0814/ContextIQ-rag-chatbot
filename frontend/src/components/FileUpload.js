import React, { useState } from "react";
import axios from "axios";
import { toast } from "react-hot-toast";

function FileUpload({ onUploadSuccess }) {
  const [url, setUrl] = useState("");
  const [file, setFile] = useState(null);

  const handleUrlSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:8000/add-url", { url });
      toast.success("URL added successfully!");
      setUrl("");
      onUploadSuccess();
    } catch (error) {
      console.error(error);
      toast.error("Error adding URL!");
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileUpload = async (e) => {
    e.preventDefault();
    if (!file) return toast.error("Please select a file!");

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/upload-document", formData);
      toast.success("File uploaded successfully!");
      setFile(null);
      onUploadSuccess();
    } catch (error) {
      console.error(error);
      toast.error("Error uploading file!");
    }
  };

  return (
    <div className="space-y-4">
      <input
        type="text"
        className="w-full p-2 border rounded"
        placeholder="Enter URL"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
      />
      <button onClick={handleUrlSubmit} className="w-full bg-blue-500 text-white p-2 rounded">
        Add URL
      </button>

      <input type="file" onChange={handleFileChange} className="w-full" />

      <button onClick={handleFileUpload} className="w-full bg-green-500 text-white p-2 rounded">
        Upload File
      </button>
    </div>
  );
}

export default FileUpload;

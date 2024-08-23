import React, { useState } from "react";
import "./ReceiptUpload.css";

function ReceiptUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      setUploadStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://127.0.0.1:8000/upload_receipt", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setUploadStatus("Upload successful!");
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        setUploadStatus("Error uploading file.");
      });
  };

  return (
    <div className="receipt-upload-container">
      <h2>Upload Receipt</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p className="upload-status">{uploadStatus}</p> {/* Added class here */}
    </div>
  );
}

export default ReceiptUpload;

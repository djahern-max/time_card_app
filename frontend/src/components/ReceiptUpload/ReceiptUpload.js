import React, { useState } from "react";
import "./ReceiptUpload.css";

function ReceiptUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [receiptData, setReceiptData] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    console.log("Upload function triggered");

    const token = localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      setUploadStatus("Unauthorized: Please log in.");
      return;
    }

    console.log("Proceeding with upload...");

    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://127.0.0.1:8000/upload_receipt", {
      method: "POST",
      body: formData,
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (response.status === 401) {
          throw new Error("Unauthorized: Please log in again.");
        } else if (!response.ok) {
          throw new Error("Upload failed");
        }
        return response.json();
      })
      .then((data) => {
        setUploadStatus("Upload successful!");
        setReceiptData(data); // Store the receipt data for display
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        setUploadStatus(error.message);
      });
  };

  return (
    <div className="receipt-upload-container">
      <h2>Upload Receipt</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{uploadStatus}</p>

      {receiptData && (
        <div className="receipt-info">
          <h3>Receipt Information</h3>
          <p>
            <strong>OCR Text:</strong>
          </p>
          <pre>{receiptData.text}</pre>
          <p>
            <strong>Image Path:</strong>
          </p>
          <a
            href={receiptData.image_path}
            target="_blank"
            rel="noopener noreferrer"
          >
            View Image
          </a>
        </div>
      )}
    </div>
  );
}

export default ReceiptUpload;

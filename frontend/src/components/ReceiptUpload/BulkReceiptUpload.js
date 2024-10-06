// BulkReceiptUpload.js
import React, { useState } from "react";
import axios from "axios";

function BulkReceiptUpload() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [results, setResults] = useState([]);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/admin/bulk_upload_receipts",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      console.log("Server Response:", response.data); // Add this line
      if (response.data.results) {
        setUploadStatus("Upload successful!");
        setResults(response.data.results);
      } else {
        setUploadStatus("Unexpected response structure.");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      setUploadStatus("Upload failed. Please try again.");
    }
  };

  return (
    <div className="bulk-receipt-upload">
      <h2>Bulk Receipt Upload</h2>
      <input type="file" accept=".pdf" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      {uploadStatus && <p>{uploadStatus}</p>}
      {results.length > 0 && (
        <div>
          <h3>Upload Results:</h3>
          <ul>
            {results.map((result, index) => (
              <li key={index}>
                {result.status === "success"
                  ? `Successfully matched to transaction ${result.transaction_id}`
                  : `No match found for receipt ${index + 1}`}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default BulkReceiptUpload;

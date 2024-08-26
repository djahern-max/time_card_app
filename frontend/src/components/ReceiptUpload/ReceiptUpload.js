import React, { useState, useEffect } from "react";
import "./ReceiptUpload.css";

function ReceiptUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [receiptData, setReceiptData] = useState(null);
  const [coding, setCoding] = useState(""); // New state for coding
  const [empCode, setEmpCode] = useState(""); // State for emp_code
  const [transactionId, setTransactionId] = useState(""); // State for transaction_id

  useEffect(() => {
    // Fetch emp_code based on the logged-in user
    const fetchEmpCode = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        setUploadStatus("Unauthorized: Please log in.");
        return;
      }

      try {
        const response = await fetch("http://127.0.0.1:8000/get_emp_code", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        const data = await response.json();
        setEmpCode(data.emp_code);
      } catch (error) {
        console.error("Error fetching emp_code:", error);
      }
    };

    fetchEmpCode();
  }, []);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleCodingChange = (event) => {
    setCoding(event.target.value);
  };

  const handleTransactionIdChange = (event) => {
    setTransactionId(event.target.value);
  };

  const handleUpload = () => {
    console.log("Upload function triggered");

    const token = localStorage.getItem("token");
    console.log("Token:", token);

    if (!token) {
      setUploadStatus("Unauthorized: Please log in.");
      return;
    }

    if (!selectedFile) {
      setUploadStatus("Please select a file first.");
      return;
    }

    console.log("Proceeding with upload...");

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("coding", coding); // Include coding information
    formData.append("transaction_id", transactionId); // Add transaction_id
    formData.append("employee_coding", coding); // Add employee_coding
    formData.append("emp_code", empCode); // Add emp_code

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
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Enter coding information"
        value={coding}
        onChange={handleCodingChange}
      />
      <input
        type="text"
        placeholder="Enter transaction ID"
        value={transactionId}
        onChange={handleTransactionIdChange}
      />
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

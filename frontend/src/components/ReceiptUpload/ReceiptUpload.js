import React, { useState, useEffect } from "react";
import "./ReceiptUpload.css";
import { useNavigate } from "react-router-dom";
import logoutIcon from "../../assets/logout.svg";
import uploadIcon from "../../assets/upload.svg";

function ReceiptUpload() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [receiptData, setReceiptData] = useState(null);
  const [coding, setCoding] = useState("");
  const [empCode, setEmpCode] = useState("");
  const [transactionId, setTransactionId] = useState("");
  const [userTransactions, setUserTransactions] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      setUploadStatus("Unauthorized: Please log in.");
      return;
    }

    const fetchEmpCode = async () => {
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

    const fetchUserTransactions = async () => {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/get_user_transactions",
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        );
        const data = await response.json();
        setUserTransactions(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error fetching user transactions:", error);
        setUserTransactions([]);
      }
    };

    fetchEmpCode();
    fetchUserTransactions();
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
    const token = localStorage.getItem("token");

    if (!token) {
      setUploadStatus("Unauthorized: Please log in.");
      return;
    }

    if (!selectedFile) {
      setUploadStatus("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    formData.append("coding", coding);
    formData.append("transaction_id", transactionId);
    formData.append("employee_coding", coding);
    formData.append("emp_code", empCode);

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
        setReceiptData(data);
      })
      .catch((error) => {
        console.error("Error uploading file:", error);
        setUploadStatus(error.message);
      });
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div className="receipt-upload-container">
      <div className="icon-container">
        <img
          src={logoutIcon}
          className="logout-icon"
          alt="Logout"
          onClick={handleLogout}
        />
        <img
          src={uploadIcon}
          className="upload-icon"
          alt="Upload"
          onClick={handleUpload}
        />
      </div>
      <h2>Upload Receipt</h2>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      <input
        type="text"
        placeholder="Enter coding information"
        value={coding}
        onChange={handleCodingChange}
      />
      <select value={transactionId} onChange={handleTransactionIdChange}>
        <option value="">Select Transaction</option>
        {userTransactions.map((transaction) => (
          <option key={transaction.id} value={transaction.id}>
            {transaction.description} - {transaction.amount} on{" "}
            {transaction.transaction_date}
          </option>
        ))}
      </select>
      <button onClick={handleUpload}>Upload</button>

      {uploadStatus && <p className="upload-success-message">{uploadStatus}</p>}

      {receiptData && (
        <div className="receipt-info">
          <h3>Receipt Information</h3>
          <p>
            <strong>OCR Text:</strong>
          </p>
          <pre>{receiptData.text}</pre>
        </div>
      )}
    </div>
  );
}

export default ReceiptUpload;

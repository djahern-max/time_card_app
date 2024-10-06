import React, { useState } from "react";
import "./upload.css";

function Upload() {
  const [file, setFile] = useState(null);
  const [dataset, setDataset] = useState("employees"); // Default to employees

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleDatasetChange = (e) => {
    setDataset(e.target.value);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    let url;

    // Determine the URL based on the selected dataset
    if (dataset === "employees") {
      url = `http://127.0.0.1:8000/upload/?dataset=${dataset}`;
    } else if (dataset === "equipment") {
      url = `http://127.0.0.1:8000/upload/equipment/?dataset=${dataset}`;
    } else if (dataset === "timecards") {
      url = `http://127.0.0.1:8000/upload/timecards/?dataset=${dataset}`;
    } else if (dataset === "jobs") {
      url = `http://127.0.0.1:8000/upload/jobs/?dataset=${dataset}`;
    } else if (dataset === "receipts") {
      url = `http://127.0.0.1:8000/admin/bulk_upload_receipts`;
    } else {
      alert("Unsupported dataset");
      return;
    }

    try {
      const response = await fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`, // Add token for protected routes
        },
      });

      if (response.ok) {
        alert("File uploaded successfully");
      } else {
        alert("File upload failed");
      }
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Error uploading file");
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-box">
        <h2>Upload Data</h2>
        <select value={dataset} onChange={handleDatasetChange}>
          <option value="employees">Employees</option>
          <option value="jobs">Jobs</option>
          <option value="equipment">Equipment</option>
          <option value="timecards">Timecards</option>
          <option value="receipts">Receipts</option>{" "}
          {/* Added Receipts option */}
        </select>
        <input
          type="file"
          onChange={handleFileChange}
          accept={dataset === "receipts" ? ".pdf" : "*"} // Restrict to PDFs for receipts
        />
        <button onClick={handleUpload}>Upload</button>
      </div>
    </div>
  );
}

export default Upload;

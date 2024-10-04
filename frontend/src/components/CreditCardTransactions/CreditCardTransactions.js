// CreditCardTransactions.js is a component that displays credit card transactions for employees. It fetches the transactions from the backend API and allows the user to filter the transactions by employee code. The component also allows the user to update the coding for each transaction and view the receipt image associated with each transaction. The component includes a button to export the transactions to a CSV file.
import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "./CreditCardTransactions.css";
// import logout from "../../assets/logout.svg";
// import download from "../../assets/download.svg";
import NavigationBar from "../Navigation/NavigationBar";

function CreditCardTransactions() {
  const [transactions, setTransactions] = useState([]);
  const [employeeCodes, setEmployeeCodes] = useState([]);
  const [selectedEmpCode, setSelectedEmpCode] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = () => {
    fetch("http://127.0.0.1:8000/credit_card_transactions")
      .then((response) => response.json())
      .then((data) => {
        if (!Array.isArray(data)) {
          throw new Error("Unexpected response format");
        }

        // Filter out transactions with negative amounts (payments)
        const filteredData = data.filter(
          (transaction) => transaction.amount >= 0
        );

        // Sort data by emp_code alphabetically
        const sortedData = filteredData.sort((a, b) =>
          a.emp_code.localeCompare(b.emp_code)
        );
        setTransactions(sortedData);

        // Extract unique emp_codes for dropdown
        const codes = Array.from(
          new Set(sortedData.map((entry) => entry.emp_code))
        );
        setEmployeeCodes(codes);
      })
      .catch((error) => console.error("Error fetching transactions:", error));
  };

  const handleCodeChange = (event, transactionId) => {
    const newCode = event.target.value;
    const cursorPosition = event.target.selectionStart;
    const token = localStorage.getItem("token"); // Assuming the token is stored in localStorage

    fetch(
      `http://127.0.0.1:8000/update_code/${transactionId}?coding=${newCode}`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("Code updated:", data);

        // Update the transactions state
        setTransactions((prevTransactions) =>
          prevTransactions.map((transaction) =>
            transaction.id === transactionId
              ? { ...transaction, coding: newCode }
              : transaction
          )
        );

        // Use a timeout to allow the state to update before setting the cursor position
        setTimeout(() => {
          const input = document.querySelector(`input[value="${newCode}"]`);
          if (input) {
            input.setSelectionRange(cursorPosition, cursorPosition);
          }
        }, 0);
      })
      .catch((error) => {
        console.error("Error updating code:", error);
      });
  };

  const fetchReceipt = (transactionId) => {
    const token = localStorage.getItem("token"); // Assuming the token is stored in localStorage

    if (!token) {
      console.error("No token found in localStorage");
      return;
    }

    console.log("Token:", token);

    fetch(`http://127.0.0.1:8000/receipt_image/${transactionId}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (response.status === 404) {
          throw new Error("Receipt not found");
        }
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const newWindow = window.open();
        newWindow.document.write(
          `<img src="${url}" alt="Receipt Image" style="width: 500px; height: auto;"/>`
        );
      })
      .catch((error) => {
        console.error("Error fetching receipt:", error);
        // Display a placeholder or message if needed
        alert("No receipt available or error occurred");
      });
  };

  const handleViewScheduleClick = (empCode) => {
    navigate(`/schedule/${empCode}`);
  };

  const handleExport = () => {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("Please log in.");
      return;
    }

    fetch("http://127.0.0.1:8000/export_transactions", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => response.blob())
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "credit_card_transactions.csv";
        a.click();
        window.URL.revokeObjectURL(url);
      })
      .catch((error) => {
        console.error("Error exporting data:", error);
      });
  };

  const filteredTransactions = selectedEmpCode
    ? transactions.filter(
        (transaction) => transaction.emp_code === selectedEmpCode
      )
    : transactions;

  if (transactions.length === 0) {
    return <div>No transactions found.</div>;
  }

  return (
    <div className="credit-card-transactions-container">
      {/* <div className="header-container">
        <div className="left-container">
          <button className="logout-button" onClick={handleLogout}>
            <img src={logout} alt="Logout" className="button-icon" />
            Logout
          </button>
        </div>
        <div className="right-container">
          <button className="download-button" onClick={handleExport}>
            <img src={download} alt="Download" className="button-icon" />
            Download CSV
          </button>
        </div>
      </div> */}
      <NavigationBar />
      <h1>Credit Card Transactions</h1>

      <div className="filter-container">
        <label htmlFor="employee-select">Filter by Employee Code:</label>
        <select
          id="employee-select"
          value={selectedEmpCode}
          onChange={(e) => setSelectedEmpCode(e.target.value)}
        >
          <option value="">All Employees</option>
          {employeeCodes.map((code, index) => (
            <option key={index} value={code}>
              {code}
            </option>
          ))}
        </select>
      </div>

      <table className="transactions-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Employee Code</th>
            <th>Card Last Four</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Coding (Admin)</th>
            <th>Coding (Employee)</th>
            <th>Links</th>
          </tr>
        </thead>
        <tbody>
          {filteredTransactions.map((transaction) => (
            <tr key={transaction.id}>
              <td>{transaction.date}</td>
              <td>{transaction.emp_code}</td>
              <td>{transaction.card_last_four}</td>
              <td>
                {parseFloat(transaction.amount).toLocaleString(undefined, {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2,
                })}
              </td>
              <td>{transaction.description}</td>
              <td>
                <input
                  type="text"
                  value={transaction.coding || ""}
                  onChange={(e) => handleCodeChange(e, transaction.id)}
                  onClick={(e) => e.stopPropagation()} // Prevent row click when input is clicked
                />
              </td>
              <td>
                <input
                  type="text"
                  value={transaction.employee_coding || ""}
                  readOnly
                />
              </td>
              <td>
                {transaction.image_path ? (
                  <a
                    href="#"
                    onClick={(e) => {
                      e.preventDefault();
                      fetchReceipt(transaction.id);
                    }}
                  >
                    View Receipt
                  </a>
                ) : (
                  "No Receipt Uploaded"
                )}
                {" | "}
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    handleViewScheduleClick(transaction.emp_code);
                  }}
                >
                  View Schedule
                </a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CreditCardTransactions;

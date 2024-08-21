import React, { useState, useEffect } from "react";
import "./CreditCardTransactions.css";

function CreditCardTransactions() {
  const [transactions, setTransactions] = useState([]);
  const [employeeCodes, setEmployeeCodes] = useState([]);
  const [selectedEmpCode, setSelectedEmpCode] = useState("");
  const [inputValues, setInputValues] = useState({});

  useEffect(() => {
    fetch("http://127.0.0.1:8000/credit_card_transactions")
      .then((response) => response.json())
      .then((data) => {
        // Sort data by emp_code alphabetically
        const sortedData = data.sort((a, b) =>
          a.emp_code.localeCompare(b.emp_code)
        );
        setTransactions(sortedData);

        // Extract unique emp_codes for dropdown
        const codes = Array.from(
          new Set(sortedData.map((entry) => entry.emp_code))
        );
        setEmployeeCodes(codes);

        // Populate input values with existing coding data
        const initialValues = {};
        sortedData.forEach((transaction) => {
          initialValues[transaction.id] = transaction.coding || "";
        });
        setInputValues(initialValues);
      })
      .catch((error) => console.error("Error fetching transactions:", error));
  }, []);

  const handleCodeChange = (event, transactionId) => {
    const newCode = event.target.value;
    setInputValues({
      ...inputValues,
      [transactionId]: newCode,
    });

    // Save the new code to the backend
    fetch(
      `http://127.0.0.1:8000/update_code/${transactionId}?coding=${newCode}`,
      {
        method: "POST",
      }
    )
      .then((response) => response.json())
      .then((data) => {
        console.log("Code updated:", data);
      })
      .catch((error) => {
        console.error("Error updating code:", error);
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

      <p className="clickable-row-note">
        Click on a row to view the employee's schedule.
      </p>

      <table className="transactions-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Employee Code</th>
            <th>Card Last Four</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Coding</th>
          </tr>
        </thead>
        <tbody>
          {filteredTransactions.map((transaction) => (
            <tr key={transaction.id} style={{ cursor: "pointer" }}>
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
                  value={inputValues[transaction.id] || ""}
                  onChange={(e) => handleCodeChange(e, transaction.id)}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CreditCardTransactions;

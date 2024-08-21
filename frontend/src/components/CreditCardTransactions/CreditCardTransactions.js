import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "./CreditCardTransactions.css";

function CreditCardTransactions() {
  const [transactions, setTransactions] = useState([]);
  const [employeeCodes, setEmployeeCodes] = useState([]);
  const [selectedEmpCode, setSelectedEmpCode] = useState("");

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
      })
      .catch((error) => console.error("Error fetching transactions:", error));
  }, []);

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

      <table className="transactions-table">
        <thead>
          <tr>
            <th>Date</th>
            <th>Employee Code</th>
            <th>Card Last Four</th>
            <th>Amount</th>
            <th>Description</th>
            <th>Schedule</th>
          </tr>
        </thead>
        <tbody>
          {filteredTransactions.map((transaction, index) => (
            <tr key={index}>
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
                <Link to={`/schedule/${transaction.emp_code}`}>
                  View Schedule
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default CreditCardTransactions;

import React, { useEffect, useState } from "react";

const HistoricalSchedule = () => {
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/combined")
      .then((response) => response.json())
      .then((data) => setSchedule(data))
      .catch((error) => console.error("Error fetching schedule:", error));
  }, []);

  return (
    <div>
      <h1>Historical Schedule</h1>
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Name</th>
            <th>Job</th>
            <th>Phase</th>
            <th>Card Last Four</th>
            <th>Amount</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          {schedule.map((entry, index) => (
            <tr key={index}>
              <td>{entry.date}</td>
              <td>{entry.name}</td>
              <td>{entry.job}</td>
              <td>{entry.phase}</td>
              <td>{entry.card_last_four}</td>
              <td>{entry.amount}</td>
              <td>{entry.description}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoricalSchedule;

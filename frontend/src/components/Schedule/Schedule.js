import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Schedule() {
  const { emp_code, date } = useParams();
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/schedule/${emp_code}/${date}`)
      .then((response) => response.json())
      .then((data) => setSchedule(data))
      .catch((error) => console.error("Error fetching schedule:", error));
  }, [emp_code, date]);

  if (schedule.length === 0) {
    return <div>No schedule found for this date.</div>;
  }

  return (
    <div>
      <h1>
        Schedule for {emp_code} on {date}
      </h1>
      <ul>
        {schedule.map((entry, index) => (
          <li key={index}>
            Job: {entry.job}, Phase: {entry.phase}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Schedule;

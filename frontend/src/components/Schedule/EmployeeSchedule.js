import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Schedule.css";

function EmployeeSchedule() {
  const { empCode } = useParams(); // Only get empCode now
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/schedule/${empCode}`) // Fetch data without date
      .then((response) => response.json())
      .then((data) => setSchedule(data))
      .catch((error) => console.error("Error fetching schedule:", error));
  }, [empCode]);

  if (!schedule) {
    return <div>Loading schedule...</div>;
  }

  if (!Array.isArray(schedule.jobs)) {
    return <div>Invalid schedule data.</div>;
  }

  return (
    <div className="schedule-container">
      <h1>Schedule for {schedule.name}</h1>
      <ul>
        {schedule.jobs.map((job, index) => (
          <li key={index}>
            <b>Date:</b> {job.date} - <b>Job:</b> {job.job}, <b>Phase:</b>{" "}
            {job.phase}, <b>Hours Worked:</b> {job.hours_worked}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default EmployeeSchedule;

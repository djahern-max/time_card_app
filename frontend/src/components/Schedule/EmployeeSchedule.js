import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./EmployeeSchedule.css";

function EmployeeSchedule() {
  const { empCode } = useParams();
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/schedule/${empCode}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched schedule data:", data);
        setSchedule(data);
      })
      .catch((error) => console.error("Error fetching schedule:", error));
  }, [empCode]);

  if (!schedule) {
    return <div>Loading schedule...</div>;
  }

  return (
    <div className="schedule-container">
      <h1>Schedule for {schedule.name}</h1>
      {schedule.jobs.length > 0 ? (
        schedule.jobs.map((jobEntry, index) => (
          <div key={index}>
            <h2>Date: {jobEntry.date}</h2>
            <ul>
              {jobEntry.jobs.map((job, jIndex) => (
                <li key={jIndex}>
                  <b>Job:</b> {job.job || "No job assigned"}, <b>Phase:</b>{" "}
                  {job.phase || "No phase assigned"}
                </li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No jobs found for this employee.</p>
      )}
    </div>
  );
}

export default EmployeeSchedule;

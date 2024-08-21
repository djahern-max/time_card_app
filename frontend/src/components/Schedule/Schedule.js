import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Schedule.css";

function Schedule() {
  const { empCode } = useParams();
  const [schedule, setSchedule] = useState(null);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/schedule/${empCode}`)
      .then((response) => response.json())
      .then((data) => {
        setSchedule(data);
      })
      .catch((error) => console.error("Error fetching schedule:", error));
  }, [empCode]);

  if (!schedule) {
    return <div>Loading...</div>;
  }

  return (
    <div className="schedule-container">
      <h1>Schedule for {schedule.name}</h1>
      {schedule.jobs.length === 0 ? (
        <p>No jobs found for this employee.</p>
      ) : (
        schedule.jobs.map((day, index) => (
          <div key={index}>
            <h2>Date: {day.date}</h2>
            <ul>
              {day.jobs.map((job, jobIndex) => (
                <li key={jobIndex}>
                  <b>Job:</b> {job.job || "N/A"} | <b>Phase:</b>{" "}
                  {job.phase || "N/A"}
                </li>
              ))}
            </ul>
          </div>
        ))
      )}
    </div>
  );
}

export default Schedule;

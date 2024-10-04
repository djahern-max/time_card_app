//EmployeeSchedule.js is a component that displays the schedule for a specific employee. It fetches the schedule data from the backend API based on the employee code provided in the URL parameters. The component allows the user to select a date from a dropdown menu and displays the jobs assigned to the employee for that date.
import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./EmployeeSchedule.css"; // Ensure this file is correctly imported

function EmployeeSchedule() {
  const { empCode } = useParams();
  const [schedule, setSchedule] = useState(null);
  const [selectedDate, setSelectedDate] = useState("");

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/schedule/${empCode}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Fetched schedule data:", data);
        setSchedule(data);
        if (data.jobs.length > 0) {
          setSelectedDate(data.jobs[0].date); // Default to the first available date
        }
      })
      .catch((error) => console.error("Error fetching schedule:", error));
  }, [empCode]);

  if (!schedule) {
    return <div>Loading schedule...</div>;
  }

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
  };

  const filteredJobs =
    schedule.jobs.find((job) => job.date === selectedDate) || [];

  return (
    <div className="schedule-container">
      <h1>Schedule for {schedule.name}</h1>

      {/* Date Dropdown */}
      <label htmlFor="date-select">Select Date:</label>
      <select id="date-select" value={selectedDate} onChange={handleDateChange}>
        {schedule.jobs.map((jobEntry, index) => (
          <option key={index} value={jobEntry.date}>
            {jobEntry.date}
          </option>
        ))}
      </select>

      {/* Jobs Display */}
      {filteredJobs.jobs && filteredJobs.jobs.length > 0 ? (
        <div>
          <h2>Date: {filteredJobs.date}</h2>
          <ul>
            {filteredJobs.jobs.map((job, jIndex) => (
              <li key={jIndex}>
                <b>Job:</b> {job.job.split(".")[0] || "No job assigned"},
                <b>Phase:</b> {job.phase || "No phase assigned"}
                <br />
                <b>Hours Worked:</b> {job.hours_worked || "N/A"}
                <br />
                {/* <b>Rate:</b> {job.rate || "N/A"} */}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>No jobs found for this date.</p>
      )}
    </div>
  );
}

export default EmployeeSchedule;

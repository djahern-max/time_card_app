//App.js
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import LandingPage from "./components/LandingPage/LandingPage";
import Login from "./components/Authentication/Login";
import Register from "./components/Authentication/Register";
import AdminDashboard from "./components/Dashboard/AdminDashboard";
import GeneralTimeReport from "./components/TimeReports/GeneralTimeReport";
import MechanicsTimeReport from "./components/TimeReports/MechanicsTimeReport";
import Upload from "./components/Upload/Upload";
import CreditCardTransactions from "./components/CreditCardTransactions/CreditCardTransactions";
import EmployeeSchedule from "./components/Schedule/EmployeeSchedule";
import ReceiptUpload from "./components/ReceiptUpload/ReceiptUpload";
import MechanicDashboard from "./components/Dashboard/MechanicDashboard";
import GeneralDashboard from "./components/Dashboard/GeneralDashboard";
import BulkReceiptUpload from "./components/ReceiptUpload/BulkReceiptUpload";

function App() {
  const role = localStorage.getItem("role");

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/admin-dashboard" element={<AdminDashboard />} />
        <Route path="/mechanic-dashboard" element={<MechanicDashboard />} />
        <Route path="/general-dashboard" element={<GeneralDashboard />} />
        <Route path="/general-time-report" element={<GeneralTimeReport />} />
        <Route
          path="/mechanics-time-report"
          element={<MechanicsTimeReport />}
        />
        <Route path="/upload" element={<Upload />} />
        <Route
          path="/credit-card-transactions"
          element={<CreditCardTransactions />}
        />
        <Route path="/schedule/:empCode" element={<EmployeeSchedule />} />
        <Route path="/upload-receipt" element={<ReceiptUpload />} />
        <Route path="/bulk-receipt-upload" element={<BulkReceiptUpload />} />
      </Routes>
    </Router>
  );
}

export default App;

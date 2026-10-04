import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Intake from './pages/Intake';
import Coding from './pages/Coding';
import Claims from './pages/Claims';
import Appeals from './pages/Appeals';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-background text-foreground overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-hidden flex flex-col">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/intake" element={<Intake />} />
            <Route path="/coding" element={<Coding />} />
            <Route path="/claims" element={<Claims />} />
            <Route path="/appeals" element={<Appeals />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

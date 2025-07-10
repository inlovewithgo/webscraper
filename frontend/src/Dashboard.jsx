import { useState, useEffect } from "react";
import ScrapeForm from "./ScrapeForm";
import ResultsTable from "./ResultsTable";
import TaskStatus from "./TaskStatus";
import api from "./api";

export default function Dashboard() {
  const [taskId, setTaskId] = useState(null);
  const [results, setResults] = useState([]);
  const [fetching, setFetching] = useState(false);
  const [taskStatus, setTaskStatus] = useState('');

  useEffect(() => {
    if (!taskId) return;
    setResults([]);
    setFetching(true);
    
    let interval = setInterval(async () => {
      try {
        const tasksRes = await api.get('/tasks');
        const currentTask = tasksRes.data.find(t => t.id === taskId);
        
        if (currentTask) {
          setTaskStatus(currentTask.status);
          
          if (currentTask.status === 'completed') {
            const resultsRes = await api.get(`/result/${taskId}`);
            if (resultsRes.data && resultsRes.data.data) {
              setResults(resultsRes.data.data);
              setFetching(false);
              clearInterval(interval);
            }
          } else if (currentTask.status === 'failed') {
            setFetching(false);
            clearInterval(interval);
            alert('Scraping task failed. Please try again.');
          }
        }
      } catch (error) {
        console.error('Error checking task status:', error);
      }
    }, 2000);
    
    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div className="dashboard-bg">
      <div className="dashboard-glass">
        <h1 className="dashboard-title">
          <span className="accent">⚡</span> Scraper Dashboard
        </h1>
        <p className="dashboard-sub">
          Extract company data from any site, generate professional reports.
        </p>
        
        <ScrapeForm onStart={setTaskId} />
        
        {taskId && (
          <TaskStatus 
            taskId={taskId} 
            onComplete={() => setFetching(false)} 
          />
        )}
        
        {fetching && (
          <div className="dashboard-spinner">
            <div className="spinner"></div>
            <span>Processing data...</span>
          </div>
        )}
        
        <ResultsTable data={results} taskId={taskId} />
      </div>
    </div>
  );
}

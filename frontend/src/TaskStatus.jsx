import { useEffect, useState } from "react";
import api from "./api";

export default function TaskStatus({ taskId, onComplete }) {
  const [status, setStatus] = useState("queued");

  useEffect(() => {
    if (!taskId) return;
    let interval = setInterval(async () => {
      try {
        const res = await api.get(`/tasks`);
        const task = res.data.find(t => t.id === taskId);
        if (task) {
          setStatus(task.status);
          if (task.status === "completed") {
            clearInterval(interval);
            onComplete();
          }
        }
      } catch {}
    }, 1200);
    return () => clearInterval(interval);
  }, [taskId, onComplete]);

  return (
    <div className="task-status">
      <span className={`status-badge status-${status}`}>
        {status === "queued" && "Queued"}
        {status === "running" && "Scraping..."}
        {status === "completed" && "Done!"}
      </span>
    </div>
  );
}
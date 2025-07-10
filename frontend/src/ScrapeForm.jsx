import { useState } from "react";
import api from "./api";

export default function ScrapeForm({ onStart }) {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/scrape", { url });
      onStart(res.data.task_id);
      setUrl("");
    } catch (err) {
      alert("Failed to start scraping");
    }
    setLoading(false);
  };

  return (
    <form className="scrape-form" onSubmit={submit}>
      <input
        className="scrape-input"
        value={url}
        onChange={e => setUrl(e.target.value)}
        placeholder="Paste any website URL…"
        required
      />
      <button className="scrape-btn" type="submit" disabled={loading || !url}>
        {loading ? "Starting..." : "Scrape"}
      </button>
    </form>
  );
}

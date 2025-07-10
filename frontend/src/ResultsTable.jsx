
import { useState } from "react";
import api from "./api";

export default function ResultsTable({ data, taskId }) {
  const [downloading, setDownloading] = useState(false);

  const downloadPDF = async () => {
    if (!taskId) return;

    setDownloading(true);
    try {
      const response = await api.get(`/download-pdf/${taskId}`, {
        responseType: 'blob'
      });

      const pdfBlob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(pdfBlob);

      const link = document.createElement('a');
      link.href = url;
      link.download = `scraping_report_${taskId}.pdf`;
      document.body.appendChild(link);
      link.click();

      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Failed to download PDF report. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  if (!data || !data.length) {
    return (
      <div className="results-empty">
        <p>No results yet. Start a scrape to see data here.</p>
      </div>
    );
  }

  return (
    <div className="results-section">
      <div className="results-header">
        <h2>Scraping Results ({data.length} sites)</h2>
        <button 
          className="download-btn" 
          onClick={downloadPDF}
          disabled={downloading || !taskId}
        >
          {downloading ? 'Generating PDF...' : '📥 Download PDF Report'}
        </button>
      </div>

      <div className="results-table-outer">
        <table className="results-table">
          <thead>
            <tr>
              <th>URL</th>
              <th>Company</th>
              <th>Contacts</th>
              <th>Tagline</th>
              <th>Services</th>
              <th>Social Media</th>
              <th>Industry</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i}>
                <td>
                  <a href={row.url} target="_blank" rel="noopener noreferrer" className="url-link">
                    {row.url.length > 40 ? row.url.substring(0, 40) + '...' : row.url}
                  </a>
                </td>
                <td className="company-cell">
                  {row.company || <span className="no-data">-</span>}
                </td>
                <td className="contacts-cell">
                  <div className="contact-info">
                    {row.contacts?.emails?.length > 0 && (
                      <div className="emails">
                        📧 {row.contacts.emails.slice(0, 2).join(', ')}
                        {row.contacts.emails.length > 2 && <span className="more">+{row.contacts.emails.length - 2} more</span>}
                      </div>
                    )}
                    {row.contacts?.phones?.length > 0 && (
                      <div className="phones">
                        📞 {row.contacts.phones.slice(0, 2).join(', ')}
                        {row.contacts.phones.length > 2 && <span className="more">+{row.contacts.phones.length - 2} more</span>}
                      </div>
                    )}
                    {(!row.contacts?.emails?.length && !row.contacts?.phones?.length) && (
                      <span className="no-data">-</span>
                    )}
                  </div>
                </td>
                <td className="tagline-cell">
                  {row.tagline ? (
                    <span title={row.tagline}>
                      {row.tagline.length > 60 ? row.tagline.substring(0, 60) + '...' : row.tagline}
                    </span>
                  ) : (
                    <span className="no-data">-</span>
                  )}
                </td>
                <td className="services-cell">
                  {row.services?.length > 0 ? (
                    <div className="services-list">
                      {row.services.slice(0, 3).map((service, idx) => (
                        <span key={idx} className="service-tag">{service}</span>
                      ))}
                      {row.services.length > 3 && <span className="more">+{row.services.length - 3} more</span>}
                    </div>
                  ) : (
                    <span className="no-data">-</span>
                  )}
                </td>
                <td className="social-cell">
                  {row.social_media && Object.keys(row.social_media).length > 0 ? (
                    <div className="social-links">
                      {Object.entries(row.social_media).slice(0, 3).map(([platform, url], idx) => (
                        <a key={idx} href={url} target="_blank" rel="noopener noreferrer" className="social-link">
                          {platform}
                        </a>
                      ))}
                    </div>
                  ) : (
                    <span className="no-data">-</span>
                  )}
                </td>
                <td className="industry-cell">
                  {row.industry ? (
                    <span className="industry-tag">{row.industry}</span>
                  ) : (
                    <span className="no-data">-</span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
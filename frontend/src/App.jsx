import { useMemo, useState } from "react";
import { uploadQuestions } from "./api";

function downloadCsv(rows) {
  const headers = ["question", "category", "answer", "RBI", "ISO27001", "OWASP", "confidence"];
  const lines = [headers.join(",")];

  rows.forEach((row) => {
    const values = [
      row.question,
      row.category,
      row.answer,
      row.compliance?.RBI,
      row.compliance?.ISO27001,
      row.compliance?.OWASP,
      row.confidence,
    ].map((value) => `"${String(value ?? "").replaceAll('"', '""')}"`);

    lines.push(values.join(","));
  });

  const blob = new Blob([lines.join("\n")], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.setAttribute("download", "rfp_responses.csv");
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export default function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState([]);

  const hasResults = useMemo(() => results.length > 0, [results]);

  const onSubmit = async (event) => {
    event.preventDefault();
    setError("");

    if (!file) {
      setError("Please choose a CSV file first.");
      return;
    }

    setLoading(true);
    try {
      const payload = await uploadQuestions(file);
      setResults(payload.results || []);
    } catch (err) {
      setError(err?.response?.data?.detail || "Upload failed. Check backend and CSV format.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <h1>AppSec RFP Automation MVP</h1>
      <p>
        Upload a CSV with a <code>question</code> column to classify and generate compliance-aligned
        answers.
      </p>

      <form onSubmit={onSubmit} className="upload-form">
        <input type="file" accept=".csv" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : "Upload & Generate"}
        </button>
        <button type="button" disabled={!hasResults} onClick={() => downloadCsv(results)}>
          Export CSV
        </button>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {hasResults ? (
        <table>
          <thead>
            <tr>
              <th>Question</th>
              <th>Category</th>
              <th>Answer</th>
              <th>Compliance</th>
              <th>Confidence</th>
            </tr>
          </thead>
          <tbody>
            {results.map((row, index) => (
              <tr key={`${row.question}-${index}`}>
                <td>{row.question}</td>
                <td>{row.category}</td>
                <td>{row.answer}</td>
                <td>
                  <div>RBI: {row.compliance?.RBI}</div>
                  <div>ISO27001: {row.compliance?.ISO27001}</div>
                  <div>OWASP: {row.compliance?.OWASP}</div>
                </td>
                <td>{row.confidence}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : null}
    </main>
  );
}

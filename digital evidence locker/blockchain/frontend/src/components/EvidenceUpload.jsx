import { useState } from "react";

export default function UploadEvidence() {
  const [file, setFile] = useState(null);
  const [caseId, setCaseId] = useState("");

  const handleUpload = async (e) => {
    e.preventDefault(); // 🔥 VERY IMPORTANT

    const formData = new FormData();
    formData.append("file", file);     // MUST be "file"
    formData.append("caseId", caseId);

    try {
      const response = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if (data.success) {
        alert("✅ Upload successful");
      } else {
        alert("❌ Upload failed: " + data.error);
      }
    } catch (err) {
      console.error(err);
      alert("❌ Network error");
    }
  };

  return (
    <form onSubmit={handleUpload}>
      <input
        type="text"
        placeholder="Case ID (e.g. CASE_001)"
        value={caseId}
        onChange={(e) => setCaseId(e.target.value)}
      />

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button type="submit">Upload Evidence</button>
    </form>
  );
}

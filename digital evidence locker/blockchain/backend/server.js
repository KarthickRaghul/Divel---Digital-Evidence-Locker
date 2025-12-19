const express = require("express");
const cors = require("cors");
const multer = require("multer");
require("dotenv").config();

const generateSHA256 = require("./utils/hashUtil");
const { storeHash } = require("./utils/blockchainUtil");

const app = express();
app.use(cors());
app.use(express.json());

// ✅ Multer config for LARGE FILES (videos)
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 500 * 1024 * 1024, // 500 MB
  },
});

// ✅ Upload route
app.post("/upload", upload.single("file"), async (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: "No file received" });
    }

    const { caseId } = req.body;
    if (!caseId) {
      return res.status(400).json({ error: "Case ID missing" });
    }

    console.log("📂 File received:", req.file.originalname);
    console.log("📦 File size:", req.file.size / (1024 * 1024), "MB");
    console.log("🆔 Case ID:", caseId);

    // ✅ Generate hash (works for ANY file type)
    const hash = generateSHA256(req.file.buffer);
    console.log("🔐 Generated SHA-256 Hash:", hash);

    console.log("⛓️ Storing hash on blockchain...");
    await storeHash(caseId, hash);

    console.log("✅ Hash stored on blockchain");

    res.json({
      success: true,
      message: "File uploaded and hash stored on blockchain",
      hash,
    });
  } catch (err) {
    console.error("❌ Upload error:", err.message);
    res.status(500).json({
      success: false,
      error: err.message,
    });
  }
});

app.listen(5000, () => {
  console.log("🚀 Backend running on port 5000");
});

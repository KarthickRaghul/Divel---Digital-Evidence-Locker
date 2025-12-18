const generateSHA256 = require("../utils/hashUtil");
const { storeHash } = require("../utils/blockchainUtil");

exports.uploadEvidence = async (req, res) => {
  try {
    const { caseId } = req.body;
    const fileBuffer = req.file.buffer;

    // 1️⃣ Generate hash
    const hash = generateSHA256(fileBuffer);

    // 2️⃣ Store hash on blockchain
    await storeHash(caseId, hash);

    res.json({
      message: "Evidence uploaded & hash stored on blockchain",
      hash
    });
  } catch (err) {
    res.status(500).json({ error: "Upload failed" });
  }
};

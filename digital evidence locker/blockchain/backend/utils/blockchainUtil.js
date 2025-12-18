const { ethers } = require("ethers");
require("dotenv").config();

const contractABI = [
  {
    inputs: [
      { internalType: "string", name: "caseId", type: "string" },
      { internalType: "string", name: "fileHash", type: "string" }
    ],
    name: "storeEvidence",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function"
  },
  {
    inputs: [{ internalType: "string", name: "caseId", type: "string" }],
    name: "getEvidence",
    outputs: [
      { internalType: "string", type: "string" },
      { internalType: "uint256", type: "uint256" }
    ],
    stateMutability: "view",
    type: "function"
  }
];

const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

const contract = new ethers.Contract(
  process.env.CONTRACT_ADDRESS,
  contractABI,
  wallet
);

async function storeHash(caseId, hash) {
  const tx = await contract.storeEvidence(caseId, hash);
  await tx.wait();
}

module.exports = { storeHash };

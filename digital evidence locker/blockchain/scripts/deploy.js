async function main() {
  // Get the contract factory
  const EvidenceHash = await ethers.getContractFactory("EvidenceHash");

  // Deploy the contract
  const evidenceHash = await EvidenceHash.deploy();

  // Wait for deployment to complete
  await evidenceHash.waitForDeployment();

  // Print deployed address
  console.log(
    "EvidenceHash contract deployed to:",
    await evidenceHash.getAddress()
  );
}

// Hardhat recommended pattern
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

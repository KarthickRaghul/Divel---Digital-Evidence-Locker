// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvidenceHash {
    struct Evidence {
        string fileHash;
        uint256 timestamp;
    }

    mapping(string => Evidence) public evidences;

    event EvidenceStored(string caseId, string fileHash);

    function storeEvidence(string memory caseId, string memory fileHash) public {
        evidences[caseId] = Evidence(fileHash, block.timestamp);
        emit EvidenceStored(caseId, fileHash);
    }

    function getEvidence(string memory caseId)
        public
        view
        returns (string memory, uint256)
    {
        Evidence memory e = evidences[caseId];
        return (e.fileHash, e.timestamp);
    }
}

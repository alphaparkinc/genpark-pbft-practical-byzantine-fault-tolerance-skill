"""
Autonomous Agent PBFT (Practical Byzantine Fault Tolerance) Skill
Pure Python Standard Library implementation.
"""
from typing import List, Dict, Any, Set

class PBFTCluster:
    """
    PBFT 3-Phase Consensus Cluster (Pre-Prepare, Prepare, Commit).
    """
    def __init__(self, num_nodes: int):
        self.n = num_nodes
        self.f = (num_nodes - 1) // 3
        self.view = 0
        self.primary = 0
        self.logs = {i: [] for i in range(num_nodes)}

    def consensus_round(self, request: str, faulty_nodes: List[int] = None) -> Dict[str, Any]:
        faulty = set(faulty_nodes or [])
        quorum_needed = 2 * self.f + 1

        prepares = sum(1 for i in range(self.n) if i not in faulty)
        prepared = prepares >= quorum_needed

        commits = sum(1 for i in range(self.n) if i not in faulty)
        committed = prepared and (commits >= quorum_needed)

        if committed:
            for i in range(self.n):
                if i not in faulty:
                    self.logs[i].append(request)

        return {
            "committed": committed,
            "quorum_needed": quorum_needed,
            "honest_nodes": self.n - len(faulty),
            "max_byzantine_faults": self.f,
            "request": request,
            "view": self.view
        }

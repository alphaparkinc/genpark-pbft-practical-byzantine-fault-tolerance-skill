"""Example usage for PBFT Consensus Skill."""
from client import PBFTCluster

def main():
    print("Executing PBFT Consensus Protocol...")
    # 4 nodes cluster tolerates 1 faulty Byzantine node
    pbft = PBFTCluster(4)
    res = pbft.consensus_round("PROPOSE_TRANSACTION_TX001", faulty_nodes=[3])
    print("PBFT Result:", res)
    assert res["committed"] == True, "Failed to commit consensus"
    assert res["max_byzantine_faults"] == 1
    print("PBFT Consensus verified successfully!")

if __name__ == "__main__":
    main()

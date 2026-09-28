from client import PBFTNode

replica = PBFTNode("replica_0", total_nodes=4, f=1)
replica.receive_pre_prepare(view=0, seq=1, req="transfer(alice, bob, 100)")

prep_ready = replica.receive_prepare(view=0, seq=1, sender_id="replica_1")
prep_ready2 = replica.receive_prepare(view=0, seq=1, sender_id="replica_2")
print("Prepared status (>=2f):", prep_ready2)

for nid in ["replica_0", "replica_1", "replica_2"]:
    com_ready = replica.receive_commit(view=0, seq=1, sender_id=nid)
print("Committed status (>=2f+1):", com_ready)

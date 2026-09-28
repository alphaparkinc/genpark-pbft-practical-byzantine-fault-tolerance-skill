"""Practical Byzantine Fault Tolerance (PBFT) Engine.
100% Python Standard Library.
"""

import collections

class PBFTNode:
    """PBFT state machine replication node with 3-phase consensus."""
    def __init__(self, node_id, total_nodes=4, f=1):
        self.node_id = node_id
        self.f = f
        self.view = 0
        self.pre_prepare_log = {}
        self.prepare_votes = collections.defaultdict(set)
        self.commit_votes = collections.defaultdict(set)

    def receive_pre_prepare(self, view, seq, req):
        if view == self.view:
            self.pre_prepare_log[seq] = req
            return True
        return False

    def receive_prepare(self, view, seq, sender_id):
        self.prepare_votes[(seq, view)].add(sender_id)
        return len(self.prepare_votes[(seq, view)]) >= 2 * self.f

    def receive_commit(self, view, seq, sender_id):
        self.commit_votes[(seq, view)].add(sender_id)
        return len(self.commit_votes[(seq, view)]) >= 2 * self.f + 1

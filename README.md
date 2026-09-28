# Practical Byzantine Fault Tolerance (PBFT) Skill

High-efficiency, zero-dependency Python implementation of **Practical Byzantine Fault Tolerance (PBFT)** state machine replication.

## Features
- **3-Phase Consensus Protocol**: Pre-Prepare, Prepare (\(\ge 2f\)), and Commit (\(\ge 2f + 1\)).
- **Byzantine Resilience**: Tolerates up to \(f = \lfloor(N - 1)/3floor\) malicious, compromised, or arbitrarily behaving replicas.
- **Zero External Dependencies**: Pure Python standard library.
- **Native MCP Protocol**: JSON-RPC 2.0 stdio server compatible with Claude Desktop, Cursor, and Windsurf.

## Architecture
```mermaid
graph TD
    Client["Client Request"] --> Primary["Primary Replica"]
    Primary --> PrePrep["Pre-Prepare Phase"]
    PrePrep --> Prep["Prepare Phase (2f quorum)"]
    Prep --> Commit["Commit Phase (2f+1 quorum)"]
    Commit --> Exec["Execute & Reply to Client"]
```

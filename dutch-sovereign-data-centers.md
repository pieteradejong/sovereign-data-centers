# Dutch Sovereign Data Centers / RijksCloud

> Working design document for a sovereign Dutch government and critical-infrastructure compute platform.

## 1. Core idea

Create a Dutch-controlled national cloud and data-center capability — provisionally **RijksCloud** or a **Dutch National Cloud Authority** — for workloads where sovereignty, continuity, security, and jurisdiction matter more than hyperscaler convenience.

The objective is **not** to reproduce AWS/Azure/GCP for every workload. It is to establish a sovereign core for the Dutch state and critical national functions, while retaining a pragmatic hybrid relationship with commercial cloud.

## 2. Why this exists

The Netherlands increasingly depends on digital infrastructure that is economically and operationally critical but often rests on foreign-controlled technology stacks. The strategic problem is broader than where a server is physically located.

Sovereignty requires control over:

- physical facilities and access;
- cryptographic keys and identity systems;
- networks and inter-site connectivity;
- operations and privileged administration;
- data jurisdiction and legal exposure;
- software/platform dependencies;
- hardware and replacement supply chains;
- disaster recovery and continuity of government.

A Dutch sovereign platform would reduce the risk that essential state functions depend entirely on foreign hyperscalers, foreign jurisdictions, or a small number of external operators.

## 3. Proposed institutional model

Establish a dedicated national operator: **RijksCloud / Dutch National Cloud Authority**.

Its responsibilities could include:

- operating sovereign data centers;
- providing government compute, storage, databases, networking, IAM, secrets, and backup services;
- defining security and sovereignty standards;
- operating national disaster-recovery capacity;
- coordinating procurement and hardware lifecycle management;
- providing controlled environments for sensitive AI and data workloads;
- maintaining interoperability with commercial cloud;
- supporting defense and other highly sensitive tenants through separately secured environments.

The organization should behave more like a serious infrastructure operator than a conventional government IT department.

## 4. Physical architecture

### Initial concept

Build approximately **3–5 geographically separated data centers inside the Netherlands**.

The important property is not merely redundancy but **failure-domain separation**. Sites should avoid sharing the same critical dependencies wherever practical:

- electricity substations;
- flood exposure;
- fiber routes;
- metropolitan concentration;
- physical security risks;
- regional infrastructure bottlenecks.

A conceptual topology:

```text
                    Dutch Government / Agencies
                              |
                       Sovereign Network
                              |
              +---------------+---------------+
              |               |               |
          Region A        Region B        Region C
          DC A1           DC B1           DC C1
              \              |              /
               \-------------+-------------/
                    replicated services

              + optional Regions / DR sites D–E
```

No single site should be the indispensable "main" data center.

## 5. Preliminary scale

Earlier working estimates put the initial national platform on the order of:

- **10,000–30,000 servers** across the estate;
- **hundreds of petabytes of replicated storage**;
- multiple independent sites with enough spare capacity to survive significant outages;
- dedicated accelerator capacity for AI/HPC where justified.

These are **order-of-magnitude planning numbers**, not a finished capacity model. They need to be derived bottom-up from actual government workloads, growth, replication policy, resilience targets, and reserve capacity.

## 6. Logical platform architecture

The sovereign layer should expose standard cloud primitives rather than forcing agencies to operate bare hardware.

### Core services

- virtual machines;
- Kubernetes/container orchestration;
- object storage;
- block and file storage;
- managed relational databases;
- message/event infrastructure;
- identity and access management;
- secrets/key management;
- observability and audit logging;
- backup and archival storage;
- infrastructure-as-code APIs;
- internal artifact/container registries.

### Design principle

Prefer open protocols and portable workloads. Avoid rebuilding proprietary hyperscaler products unless there is a strong national requirement.

A plausible engineering philosophy is:

```text
applications
    ↓
portable platform services
    ↓
containers / VMs / storage / databases
    ↓
Dutch-controlled orchestration and security plane
    ↓
Dutch data-center hardware + sovereign network
```

## 7. Hybrid cloud model

The proposal is **not "everything must run on RijksCloud."**

A workload classification model makes more sense:

| Class | Example | Preferred environment |
|---|---|---|
| Sovereign / critical | DigiD, core state identity, sensitive registries | RijksCloud |
| Classified / defense | military intelligence, classified models/data | isolated sovereign defense environment |
| Sensitive government | protected administrative data and internal systems | RijksCloud by default |
| Commodity government IT | collaboration, ordinary SaaS, public web workloads | sovereign or commercial cloud based on risk/cost |
| Elastic public workloads | public websites, burst compute, commodity analytics | commercial cloud acceptable |

Commercial hyperscalers therefore remain useful. The strategic change is that the Netherlands retains a **credible independent execution environment** for workloads it cannot prudently outsource.

## 8. Digital identity as a foundational workload

**DigiD and related identity infrastructure** are obvious candidates for sovereign hosting because identity sits near the root of the state's digital trust graph.

The larger architecture should treat identity, authorization, certificates, signing, and key management as foundational infrastructure rather than ordinary applications.

Compromise or external loss of control at this layer can cascade across many government services.

## 9. Defense extension

The same infrastructure concept extends naturally to Dutch defense, but defense should not simply be another tenant on an ordinary government cloud.

Potential capabilities include:

- classified compute and storage;
- isolated military networks;
- sovereign cryptographic/key infrastructure;
- intelligence data processing;
- training and inference for military AI/LLMs;
- simulation and HPC;
- geospatial and sensor-data processing;
- logistics and operational software;
- replicated command infrastructure.

### Edge computing

Defense introduces a second tier beyond central data centers:

```text
Sovereign Core Data Centers
          ↓
Military / Classified Regional Compute
          ↓
Deployable Edge Nodes
          ↓
Ships / bases / vehicles / field units / sensors
```

Edge systems must tolerate intermittent or hostile connectivity and therefore cannot assume permanent access to a central cloud.

## 10. Sovereignty is a stack, not a building

Owning Dutch data centers alone does not create technological sovereignty.

A useful decomposition is:

```text
Physical sovereignty
    facilities, power, cooling, physical security

Network sovereignty
    fiber, routing, DDoS protection, interconnects

Hardware sovereignty
    servers, accelerators, storage, firmware, spares

Platform sovereignty
    hypervisors, orchestration, databases, IAM

Operational sovereignty
    administrators, incident response, deployment

Cryptographic sovereignty
    keys, HSMs, certificates, signing infrastructure

Application sovereignty
    critical applications and source/code supply chain

Data sovereignty
    custody, jurisdiction, access and replication
```

The Netherlands can realistically control some layers much more completely than others. For example, complete domestic semiconductor independence is unrealistic; operational and cryptographic control are much more attainable.

## 11. Hardware and supply-chain reality

"Dutch sovereign" should not be interpreted as "every component manufactured in the Netherlands."

Modern servers depend on global supply chains: CPUs, GPUs, memory, disks, networking silicon, firmware, and manufacturing equipment. Even with the Netherlands' strategic position through ASML, full vertical hardware sovereignty would be economically unrealistic.

The more practical objective is **supply-chain resilience**:

- multiple approved vendors;
- strategic inventories of critical spares;
- long-term procurement agreements;
- firmware and component provenance controls;
- ability to operate through temporary external supply disruption;
- avoidance of single-vendor architectural lock-in.

## 12. Power and cooling

Power is likely to become one of the most important constraints, especially if sovereign AI capacity becomes substantial.

A serious design needs explicit models for:

- IT load (MW);
- peak versus average utilization;
- PUE;
- grid connection capacity;
- redundant feeds/substations;
- backup generation;
- UPS/battery duration;
- cooling technology;
- water consumption;
- future high-density GPU racks;
- ability to expand each site.

This should eventually become a **power-first capacity model**: workloads → servers/accelerators → rack density → MW → site requirements.

## 13. Network topology

The sovereign estate should use multiple physically diverse fiber paths between regions and connect to relevant Dutch and European networks without creating a single carrier dependency.

Desired properties:

- redundant inter-data-center links;
- route diversity;
- encryption in transit;
- sovereign key control;
- strong segmentation between tenants/security domains;
- high-bandwidth replication links;
- independent external connectivity paths;
- graceful operation during partial network partition.

The network should be designed as critical national infrastructure in its own right.

## 14. Resilience model

The system should be designed around explicit failure assumptions rather than generic claims of "high availability."

Scenarios to model include:

1. rack/server failure;
2. complete data-center outage;
3. regional power failure;
4. fiber partition;
5. ransomware or destructive administrator compromise;
6. hyperscaler outage affecting hybrid dependencies;
7. loss of a critical hardware supplier;
8. flooding or other physical disaster;
9. hostile cyberattack during a geopolitical crisis;
10. simultaneous cyber and physical disruption.

Critical services should have documented RPO/RTO targets and periodically demonstrate that they can actually recover.

## 15. Security model

Security should assume compromise is possible.

Important principles:

- zero-trust access architecture;
- hardware-backed keys/HSMs;
- strong separation of duties;
- immutable/offline backups;
- reproducible infrastructure deployment;
- comprehensive audit logs;
- privileged-access workstations;
- aggressive network segmentation;
- continuous supply-chain verification;
- red-team exercises;
- disaster-recovery exercises;
- independent security oversight.

The control plane is especially important: whoever controls IAM, orchestration, firmware, signing keys, and deployment systems effectively controls the cloud.

## 16. European dimension

Dutch sovereignty does not necessarily imply isolation from Europe.

There are at least three possible layers:

```text
Netherlands sovereign core
        ↓
trusted bilateral / EU sovereign federation
        ↓
commercial global cloud
```

The Netherlands could maintain independent national capability while interoperating with trusted European infrastructure for resilience, joint programs, scientific computing, or defense.

The key distinction is between **interdependence by choice** and **dependency without an alternative**.

## 17. What should not be done

Several tempting approaches would weaken the project:

- attempting to replace every commercial cloud workload;
- creating a bespoke government technology stack for its own sake;
- treating Dutch physical location as sufficient sovereignty;
- concentrating all capacity around Amsterdam;
- depending on one hardware supplier;
- designing only for ordinary IT failures rather than geopolitical disruption;
- building infrastructure without a first-class developer platform;
- allowing individual ministries to recreate incompatible mini-clouds.

## 18. Questions still to answer

### Capacity

- What workloads currently exist across Dutch ministries and agencies?
- How many CPU cores, GPUs, PB of storage, and network bandwidth do they actually consume?
- What reserve margin is appropriate?
- What would five- and ten-year demand look like?

### Geography

- Where should the 3–5 regions be located?
- How should flood risk, grid constraints, latency, security, and fiber connectivity be weighted?
- Should any hardened/bunker-style facility exist?

### Power

- How many MW per region?
- Can the Dutch grid support this without major new transmission investment?
- How much on-site generation/storage is warranted?

### Technology

- OpenStack, Kubernetes-centric infrastructure, commercial sovereign-cloud software, or a combination?
- Which databases/storage systems become supported national primitives?
- How much platform engineering should be built internally?

### Economics

- Initial CAPEX?
- Annual OPEX?
- Cost versus current government cloud/data-center spending?
- How much capacity should deliberately remain unused as strategic reserve?

### Governance

- Which ministry or independent authority owns RijksCloud?
- How independent should it be from ordinary procurement cycles?
- How are agencies compelled or incentivized to migrate critical workloads?
- How should defense and intelligence governance differ?

### European integration

- Which services should be national only?
- Which could federate with EU partners?
- What mutual disaster-recovery arrangements make sense?

## 19. Recommended next analytical work

The next iteration should turn this concept into an engineering model rather than adding more prose.

### A. Geographic design

Select candidate regions and score them on:

- grid capacity;
- flood risk;
- fiber connectivity;
- distance/failure independence;
- physical security;
- land availability;
- cooling/environmental constraints.

### B. Capacity model

Create a spreadsheet/model connecting:

```text
government workloads
      ↓
CPU / GPU / RAM / storage demand
      ↓
replication + reserve factor
      ↓
server count
      ↓
rack count
      ↓
power + cooling
      ↓
data-center size and cost
```

### C. Network graph

Model data centers, fiber paths, IXPs, power dependencies, and critical services as a graph. Then calculate failure domains, min-cuts, centrality, and the consequences of losing particular nodes or edges.

### D. Threat model

Create explicit adversaries and failure scenarios ranging from ordinary hardware failure through nation-state attack and geopolitical supply disruption.

### E. Cost model

Estimate CAPEX/OPEX for 3-, 4-, and 5-region architectures and compare them with continued dependence on hyperscalers.

## 20. Working thesis

> The Netherlands does not need to become technologically autarkic. It needs enough independently controlled compute, storage, networking, identity, cryptography, and operational capability that the Dutch state can continue functioning when foreign commercial infrastructure is unavailable, politically constrained, compromised, or no longer trustworthy.

That is the standard against which **RijksCloud** should be designed.

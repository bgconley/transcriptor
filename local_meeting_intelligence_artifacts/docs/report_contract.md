# Report Contract

Purpose: define the final architectural report shape so the builder and
validator can work section-by-section against a stable contract.

Each section must be generated as `report_section.schema.json`. The final
Markdown report is rendered from validated section JSON. Every substantive
claim must have a `CLM-0001` style claim ID and must cite evidence IDs and
segment IDs unless the claim is explicitly `not_stated`.

## Global Rules

- Preserve transcript-stated facts separately from inference, implication,
  risk, open question, and not-stated fields.
- Never fill absent customer facts with general Nutanix, Azure, NC2, or cloud
  knowledge.
- Use "Not stated in transcript" where the report contract expects a topic and
  the evidence is absent.
- Do not assign action, requirement, or risk ownership to a low-confidence
  speaker without human review.
- Include validation caveats rather than smoothing them out.

## Required Sections

1. Executive Summary
   - Business driver
   - Proposed direction
   - High-confidence facts
   - Material caveats

2. Meeting Context and Participants
   - Meeting purpose
   - Participant map
   - Speaker confidence notes
   - Customer/Nutanix/partner attribution caveats

3. Current Environment
   - Existing platforms
   - Data center or cloud footprint
   - Operational ownership
   - Unknowns

4. Workloads and Applications
   - Named workloads
   - Criticality
   - Dependencies
   - Not-stated workload details

5. Networking Architecture
   - IPs, subnets, VLANs, VNets, delegated subnets
   - Routing, BGP, ExpressRoute, VPN, NAT, firewalls
   - Access paths and traffic flow
   - Network risks and open questions

6. Storage and Data
   - Data services
   - Capacity, growth, performance, and protection requirements
   - Migration data paths
   - Data-retention unknowns

7. Identity, Security, Compliance, and Governance
   - Identity systems
   - Security controls
   - Compliance requirements
   - Audit and governance gaps

8. Operations and Support Model
   - Monitoring
   - Backup/restore operations
   - Support boundaries
   - Runbook or handoff gaps

9. Migration and Cutover
   - Migration phases
   - Cutover constraints
   - Rollback expectations
   - Downtime and dependency risks

10. DR and Business Continuity
    - RTO/RPO
    - Replication or failover expectations
    - Testing evidence
    - Not-stated assumptions

11. Cost and Commercial Considerations
    - Pricing or commercial constraints stated in transcript
    - Licensing considerations
    - Procurement blockers
    - Not-stated commercial facts

12. NC2, Azure, and Nutanix Platform Guidance
    - Transcript-stated guidance
    - Architectural implications
    - Product capabilities explicitly mentioned
    - Product facts not stated in transcript

13. Requirements Register
    - Requirements grouped by domain
    - Owner, confidence, evidence, and status
    - Human-review flags

14. Constraints and Design Drivers
    - Hard constraints
    - Soft preferences
    - Implied design drivers
    - Conflicts between drivers

15. Risks and Gaps
    - Risk statement
    - Impact
    - Evidence
    - Mitigation or required clarification

16. Open Questions
    - Question
    - Why it matters
    - Owner if stated
    - Evidence or not-stated label

17. Decisions and Action Items
    - Decision/action text
    - Owner
    - Due date if stated
    - Evidence and confidence

18. Proposed Architecture Narrative
    - Evidence-grounded narrative only
    - Explicit separation of transcript facts and implications
    - Alternatives if transcript supports them
    - Not-stated dependencies

19. Validation and Processing Integrity
    - ASR/diarization caveats
    - Extraction coverage
    - Validator findings summary
    - Remaining human-review items
    - Model/runtime/prompt versions used

## Completion Gate

A report is publishable only when:
- all 19 sections exist
- every section validates against `report_section.schema.json`
- every section has a validation result
- no critical validation findings remain
- all low-confidence ownership claims are removed, labeled, or human-reviewed
- the evidence appendix contains every cited evidence ID

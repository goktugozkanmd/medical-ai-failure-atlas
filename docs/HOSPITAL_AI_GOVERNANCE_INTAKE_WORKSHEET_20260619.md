# Hospital AI Governance Intake Worksheet

Date: 2026 06 19

Status: public intake worksheet for health AI governance readiness.

Purpose: convert the CHAI governance companion lanes into a practical intake worksheet that a hospital, medical faculty, open source maintainer, or project team can use before making public health AI claims.

This worksheet is not CHAI affiliation, not CHAI membership, not CHAI partner status, not CHAI endorsement, not Joint Commission endorsement, not certification, not legal advice, not regulatory evidence, not clinical validation, not clinical deployment, not patient data clearance, not procurement evidence, not institutional adoption, not payment, and not terms acceptance.

## Source anchors

1. CHAI homepage

Source: https://www.chai.org/

Use in this worksheet: keep health AI work framed as responsible development, deployment, and oversight preparation, not as deployment authority or institutional approval.

2. CHAI governance playbooks announcement

Source: https://www.chai.org/news/coalition-for-health-ai-chai-releases-comprehensive-governance-playbooks-to

Use in this worksheet: use the eight governance elements as intake lanes while avoiding certification, partner, endorsement, and adoption language.

3. CHAI AI Governance page

Source: https://www.chai.org/workgroup/cross-cutting/ai-governance

Use in this worksheet: separate policy, structure, resources, lifecycle, risk, data, third party review, education, and feedback instead of using one generic checklist.

4. CHAI Responsible AI Guide page

Source: https://www.chai.org/workgroup/responsible-ai/responsible-ai-guide-raig-and-raig-executive-summary

Use in this worksheet: make ethics, quality assurance, clinician review, patient perspective, and role clarity visible before public claims.

5. CHAI draft responsible health AI framework release

Source: https://www.chai.org/blog/chai-releases-draft-responsible-health-ai-framework-for-public-comment

Use in this worksheet: keep public reporting focused on risk, evidence, and uncertainty rather than model ranking or score certification.

## Intake worksheet

### 1. AI policy

Question: What exact use is this AI work allowed to support.

Record before public release:

1. Allowed use.
2. Not allowed use.
3. Public claim boundary.
4. Owner who can change the scope.

Block public claim if: the artifact implies policy approval.

### 2. Organizational structures

Question: Who is responsible for review before any safety conclusion.

Record before public release:

1. Clinical reviewer role.
2. Data reviewer role.
3. Source support reviewer role.
4. Escalation route.

Block public claim if: the artifact implies institutional governance adoption.

### 3. Organizational resources

Question: What review time, staff, access, and maintenance are needed before use.

Record before public release:

1. Minimum staff.
2. Review time.
3. Source review capacity.
4. Maintenance owner.

Block public claim if: the artifact implies operational readiness.

### 4. Responsible AI lifecycle management and use

Question: Is there a route from intake to review, release, correction, and retirement.

Record before public release:

1. Intake route.
2. Review route.
3. Release gate.
4. Correction route.
5. Retirement route.

Block public claim if: the artifact implies deployment lifecycle completion.

### 5. Risk and impact assessment

Question: Which users can be affected and what harm can happen if the system fails.

Record before public release:

1. Failure mode.
2. Affected user.
3. Likely harm.
4. Uncertainty.
5. Required reviewer question.

Block public claim if: the artifact implies safety proof.

### 6. Responsible data management and use

Question: What data source, label source, leakage risk, access limit, and missingness are visible.

Record before public release:

1. Data source.
2. Label provenance.
3. Leakage check.
4. Access boundary.
5. Missingness note.

Block public claim if: the artifact implies patient data clearance.

### 7. Third party management

Question: Are model, vendor, benchmark, and tool claims below endorsement or procurement language.

Record before public release:

1. Model or tool named.
2. Vendor or benchmark named.
3. Source support status.
4. Blocked wording.
5. Review owner.

Block public claim if: the artifact implies vendor approval or procurement evidence.

### 8. Education, training, and feedback

Question: Can clinicians and builders read the artifact without treating it as medical advice.

Record before public release:

1. Intended learner.
2. Learning goal.
3. Feedback route.
4. Reviewer question.
5. Medical advice boundary.

Block public claim if: the artifact implies clinical training certification.

### 9. Public transparency and no ranking reporting

Question: Does the public output explain risk evidence without ranking models or implying a validated leaderboard.

Record before public release:

1. Public risk statement.
2. Evidence source.
3. Uncertainty statement.
4. No ranking boundary.
5. Release note.

Block public claim if: the artifact implies score certification.

## Minimum pass condition

Do not publish a health AI safety claim unless all nine lanes have a named answer, every blocked claim is explicitly avoided, and uncertainty is visible.

## Stop conditions

Stop the public claim if any of these are true:

1. Patient data is mentioned without a verified governance route.
2. Clinical deployment is implied.
3. Clinical validation is implied.
4. A hospital, university, regulator, CHAI, Joint Commission, benchmark owner, vendor, or public body appears to endorse the work without written verification.
5. A model score is presented as safety proof.
6. A benchmark result is used as procurement evidence.
7. A route owner, reviewer, or maintainer cannot be named.

## Public next use

1. Pair with the CHAI Governance Companion Note.
2. Pair with the EU AI Act Health AI Sandbox Readiness Crosswalk.
3. Pair with the MedHELM HealthBench BRIDGE Compatibility Note.
4. Pair with SourceCheckup Medical before any source support claim.
5. Pair with the no ranking medical AI assurance card before any public benchmark or score language.

## Runnable check

```bash
make hospital_ai_governance_intake_worksheet
```

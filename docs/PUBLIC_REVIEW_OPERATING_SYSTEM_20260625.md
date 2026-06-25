# Public Review Operating System

Date: 2026 06 25

Status: local operating system for public review flow.

## Purpose

Turn public attention into one concrete review action without claiming acceptance, endorsement, validation, deployment, or institutional support.

## Live inputs

1. BAGLAM2 live state
2. approval queue
3. Gmail route owner replies
4. LinkedIn comments and direct messages
5. GitHub issue and pull request state
6. local validators

## Review lanes

### 1. Public objection intake

Route: Issue 154.

Action: Ask for one weak sentence or one missing gate.

Stop rule: Do not call a comment external validation.

### 2. LinkedIn visibility

Route: Drafted posts and public comments.

Action: Ask for critique that names one risk or one unclear phrase.

Stop rule: Do not imply review, adoption, or partner interest from views or reactions.

### 3. Route owner response

Route: Gmail or GitHub reply.

Action: Answer only the question asked and keep claims at acknowledgement level.

Stop rule: Do not invent affiliation, role, support, or commitment.

### 4. Maintainer route

Route: Open pull requests and issues.

Action: Wait for review, comment, requested change, or branch refresh request.

Stop rule: Do not ask for review again without a new reason.

### 5. Repo readiness

Route: Local validators and README surfaces.

Action: Keep each public surface linked, runnable, and guarded by a validator.

Stop rule: Do not publish route state without a fresh preflight check.

## Queue states

1. Draft ready
2. Public signal received
3. Waiting for user fact
4. Build and wait
5. Respond only after maintainer request
6. Ready for external action after live preflight

## Daily loop

1. Read BAGLAM2 and the current approval queue.
2. Check Gmail for route owner replies.
3. Check LinkedIn for direct messages, invitations, comments, and post state.
4. Run public GitHub route preflight.
5. Choose the highest value lane with no hard boundary.
6. Produce one concrete artifact.
7. Run the narrow validator and the full validation target.
8. Record the result in BAGLAM2 and the relevant tracker.

## Blocked claims

1. endorsement
2. partnership
3. institutional support
4. clinical validation
5. clinical deployment
6. model superiority
7. score certification
8. patient data use
9. regulatory approval
10. terms or payment action
11. acceptance
12. merge

## Validator commands

1. `make public_review_operating_system`
2. `make public_github_route_preflight`
3. `make validate`

## Current use

Use this operating system to decide whether the next public move should be a reply, post, route owner clarification, local repo build, or wait state.

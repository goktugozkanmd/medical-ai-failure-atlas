Summary

Adds the P10 Health AI Assurance feedback triage board.

Scope

1. Adds the public triage guide.
2. Adds the machine readable triage manifest.
3. Adds a validator and pytest coverage.
4. Links the triage board from the README.

Boundary

This PR adds no patient data, no private clinical text, no provider API run, no new cases, no agent selected physicians, no medical advice, no clinical validation claim, no model ranking, no source truth certification claim, no regulatory compliance claim, no official compatibility claim, and no institution support claim.

Checks

1. python3 scripts/validate_health_ai_assurance_feedback_triage_board_20260708.py
2. make health_ai_assurance_feedback_triage_board_20260708
3. pytest for the P10 triage board, P9 intake, and README links
4. make validate public
5. academic submission audit passed
6. reference verification found zero references in the new P10 public files

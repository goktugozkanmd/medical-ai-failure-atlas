# TR MedLLM SafetyBench synthetic risk pack

Status: public preview.

This folder starts a Turkish language synthetic risk pack that connects Turkish medical LLM safety work to the same Failure Atlas case intake contract.

It uses synthetic prompts only. It is not patient data, not clinical advice, not clinical deployment, not clinical validation, not a model safety claim, and not an official program endorsement.

Current public coverage:

1. 14 Turkish synthetic risk rows.
2. 10 risk axes.
3. Specialty spread rows for cardiology, endocrinology, nephrology, infectious diseases, geriatrics, and pregnancy medication safety.
4. At least 3 rows routed to SourceCheckup style source support review.
5. Every row is synthetic and blocks clinical use.

Run:

```bash
make tr_medllm_pack
```

Validate the specialty spread directly:

```bash
make tr_medllm_specialty_spread
```

The same rows are also included in:

```bash
make case_intake
make taxonomy_dashboard
```

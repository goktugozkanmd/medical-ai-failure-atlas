from pathlib import Path
import re
import tomllib


CI_WORKFLOW = Path(__file__).parents[1] / ".github" / "workflows" / "ci.yml"
GITLEAKS_CONFIG = Path(__file__).parents[1] / ".gitleaks.toml"


def _job_block(workflow: str, job_name: str) -> str:
    marker = f"  {job_name}:\n"
    start = workflow.index(marker)
    match = re.search(r"^  [A-Za-z0-9_-]+:\s*$", workflow[start + len(marker) :], re.MULTILINE)
    return workflow[start:] if match is None else workflow[start : start + len(marker) + match.start()]


def test_secret_scan_is_fail_closed_and_uses_current_action() -> None:
    secret_scan = _job_block(CI_WORKFLOW.read_text(encoding="utf-8"), "secret-scan")

    assert "gitleaks/gitleaks-action@v3" in secret_scan
    assert "continue-on-error: true" not in secret_scan
    assert "GITLEAKS_CONFIG: .gitleaks.toml" in secret_scan
    assert 'GITLEAKS_ENABLE_UPLOAD_ARTIFACT: "false"' in secret_scan


def test_gitleaks_config_extends_default_rules() -> None:
    config = tomllib.loads(GITLEAKS_CONFIG.read_text(encoding="utf-8"))

    assert config["extend"]["useDefault"] is True


def test_gitleaks_allows_only_the_known_jwt_negative_fixture() -> None:
    config = tomllib.loads(GITLEAKS_CONFIG.read_text(encoding="utf-8"))

    assert config["rules"] == [
        {
            "id": "jwt",
            "allowlists": [
                {
                    "description": "Known fake JWT used by leaderboard rejection tests",
                    "condition": "AND",
                    "regexTarget": "line",
                    "paths": [r"^tests/test_leaderboard_(?:submissions_validator|app)\.py$"],
                    "regexes": [
                        r"token eyJhbGciOiJIUzI1NiJ9\.eyJzdWIiOiJzdWJtaXNzaW9uIn0\.signaturepayload123"
                    ],
                }
            ],
        }
    ]

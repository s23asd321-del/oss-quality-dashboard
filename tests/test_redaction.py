from oss_quality_dashboard.redaction import redact_text


def test_local_absolute_path_redaction():
    text = redact_text("Path: /Users/demo-user/private/project")
    assert "/Users/<redacted>/private/project" in text


def test_sensitive_assignment_redaction():
    text = redact_text("token=DEMO_ONLY_NOT_A_REAL_SECRET password:FAKE_VALUE_FOR_TESTING_ONLY")
    assert "DEMO_ONLY_NOT_A_REAL_SECRET" not in text
    assert "FAKE_VALUE_FOR_TESTING_ONLY" not in text
    assert "token=<redacted>" in text
    assert "password:<redacted>" in text


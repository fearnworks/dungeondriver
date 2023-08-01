import pytest
from datetime import datetime, timedelta
from unittest.mock import patch

from ai_driver.server.core.auth import _create_token


@patch("jose.jwt.encode")
def test_should_create_valid_token_with_given_input(mock_encode):
    mock_encode.return_value = "mock_token"
    token_type = "access"
    lifetime = timedelta(minutes=15)
    sub = "user_id"
    result = _create_token(token_type, lifetime, sub)
    called_payload = mock_encode.call_args[0][0]
    assert called_payload["type"] == token_type
    assert called_payload["sub"] == sub
    assert result == "mock_token"


@patch("jose.jwt.encode")
def test_should_set_correct_expiration_given_lifetime(mock_encode):
    mock_encode.return_value = "mock_token"
    token_type = "access"
    lifetime = timedelta(minutes=15)
    sub = "user_id"
    _create_token(token_type, lifetime, sub)
    called_payload = mock_encode.call_args[0][0]
    time_diff = (called_payload["exp"] - called_payload["iat"]).total_seconds()
    assert abs(time_diff - lifetime.total_seconds()) < 0.001  # 1 millisecond tolerance


@patch("jose.jwt.encode")
def test_should_handle_different_token_types_correctly(mock_encode):
    mock_encode.return_value = "mock_token"
    token_type = "refresh"
    lifetime = timedelta(minutes=15)
    sub = "user_id"
    _create_token(token_type, lifetime, sub)
    called_payload = mock_encode.call_args[0][0]
    assert called_payload["type"] == token_type


@patch("jose.jwt.encode")
def test_should_set_sub_claim_correctly(mock_encode):
    mock_encode.return_value = "mock_token"
    token_type = "access"
    lifetime = timedelta(minutes=15)
    sub = "user_id"
    _create_token(token_type, lifetime, sub)
    called_payload = mock_encode.call_args[0][0]
    assert called_payload["sub"] == sub


@patch("jose.jwt.encode")
def test_should_raise_error_on_invalid_input(mock_encode):
    mock_encode.side_effect = Exception("Invalid input")
    token_type = "access"
    lifetime = timedelta(minutes=15)
    sub = "user_id"
    with pytest.raises(Exception) as exc_info:
        _create_token(token_type, lifetime, sub)
    assert str(exc_info.value) == "Invalid input"

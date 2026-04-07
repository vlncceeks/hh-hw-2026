import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1

def test_register_call_with_incomplete_data() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="Invalid call data format"):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,2,John Smith"
        )

def test_register_call_with_not_integer_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="invalid literal for int()"):
        switchboard.register_call(
            "1a,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
        )

    with pytest.raises(ValueError, match="invalid literal for int()"):
        switchboard.register_call(
            ",Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
        )

def test_register_call_with_negative_id() -> None:
    switchboard = Switchboard()

    with pytest.raises(ValueError, match="user_id cannot be negative"):
        switchboard.register_call(
            "-1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
        )

def test_register_call_with_empty_fullname() -> None:
    switchboard = Switchboard()
    
    with pytest.raises(ValueError, match="User fullname cannot be empty"):
        switchboard.register_call(
            "1,,+79990000000,2,John Smith,+15551234567"
        )

    with pytest.raises(ValueError, match="User fullname cannot be empty"):
        switchboard.register_call(
            "1,         ,+79990000000,2,John Smith,+15551234567"
        )
        
def test_register_call_with_empty_number() -> None:
    switchboard = Switchboard()
    
    with pytest.raises(ValueError, match="User phone cannot be empty"):
        switchboard.register_call(
            "1,Ivan Ivanov,+79990000000,2,John Smith,"
        )


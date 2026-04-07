from __future__ import annotations

from dataclasses import dataclass
from re import U

from app.users import ForeignUser, LocalUser, User


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_count: int = 0

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,receiver_id,receiver_name,receiver_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        args = raw_call.split(",")
        if len(args) != 6: raise ValueError("Invalid call data format")

        caller = self.create_user(args[0], args[1], args[2])
        receiver = self.create_user(args[3], args[4], args[5])

        active_call = ActiveCall(caller, receiver)
        self._active_calls.append(active_call)

        if active_call.is_cross_border:
            self._cross_border_count += 1

        return active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return self._cross_border_count
    
    def create_user(self, user_id, name, phone) -> User:        
        user_id_int = int(user_id)
        if user_id_int < 0: 
            raise ValueError(f"Invalid call data format: user_id cannot be negative, got {user_id_int}")
        
        if phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(user_id_int, name, phone)
        return ForeignUser(user_id_int, name, phone)

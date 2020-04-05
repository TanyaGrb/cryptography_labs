from secrets import token_hex

from des import DesKey


class KDC:
    def __init__(self):
        self.local_database = dict()

    def get_session_key(self, timestamp, user_1_id, user_2_id):
        print(f"Алиса передала метку: {timestamp}, свой id: {user_1_id}, id Боба: {user_2_id}")
        user_1_key = self.local_database[user_1_id]
        user_2_key = self.local_database[user_2_id]
        session_key = token_hex(8)
        user_2_ticket = DesKey(user_2_key).encrypt(user_1_id.encode() + session_key.encode())
        return DesKey(user_1_key).encrypt(
            str(timestamp).encode() + user_2_id.encode() + session_key.encode() + user_2_ticket, padding=True)

    def register_user(self, user_id):
        password = token_hex(8).encode()
        self.local_database.update({user_id: password})
        return password

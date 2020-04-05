from time import time

from des import DesKey

from IW5.md5_main import md5


class User:
    def __init__(self, name):
        self.name = name
        self.key = None
        self.id = md5(name.encode()).hex()
        print(f"Пользователь {self.name} получил id: {self.id}")
        self.sessions = dict()

    def save_user_key(self, key):
        print(f"Пользователь {self.name} сохранил свой постоянный ключ: {key}")
        self.key = key

    def save_session_key(self, user_id, session_key):
        print(f"Пользователь {self.name} сохранил свой сессионный ключ ({session_key}) с {user_id}")
        self.sessions.update({user_id: session_key})

    def step_3_4(self, ticket):
        decrypted_ticket = DesKey(self.key).decrypt(ticket[:-6])
        user_id, session_key = decrypted_ticket[:32].decode(), decrypted_ticket[32:].decode()
        nonce_r_b = int(time())
        print(f"Пользователь {self.name} получил билет {ticket} от {user_id}")
        self.save_session_key(user_id, session_key.encode())
        print(f"Пользователь {self.name} отправил метку {nonce_r_b} пользователю {user_id}")
        return DesKey(session_key.encode()).encrypt(str(nonce_r_b).encode(), padding=True)

    def step_5(self, nonce, user_id):
        session_key = self.sessions[user_id]
        decrypted_nonce = DesKey(session_key).decrypt(nonce)
        print(f"Пользователь {self.name} получил метку: {decrypted_nonce[:10].decode()}")


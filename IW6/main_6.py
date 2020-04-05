from time import time

from des import DesKey
from kdc import KDC
from user import User

task = """1. Реализовать программный продукт, эмулирующий обмен
зашифрованными сообщениями между двумя пользователями. Шифрование
происходит любым симметричным алгоритмом. Возможно применение
встроенных библиотек. Распределение ключей происходит с помощью
протокола Ниидома–Шредера."""

alice = User("Alice")
bob = User("Bob")
kdc = KDC()

alice.save_user_key(kdc.register_user(alice.id))
bob.save_user_key(kdc.register_user(bob.id))

nonce_r_a = int(time())
alice_id = alice.id
bob_id = bob.id

message = kdc.get_session_key(nonce_r_a, alice_id, bob_id)
print(f"Пользователь {alice.name} получил сообщение от KDC: {message}")
decrypted_message = DesKey(alice.key).decrypt(message)
timestamp, bobs_id = decrypted_message[:10].decode(), decrypted_message[10:42].decode()
session_key, bobs_ticket = decrypted_message[42:58], decrypted_message[58:]
print(f"Пользователь {alice.name} получил сессионный ключ: {session_key.decode()}")

alice.save_session_key(bobs_id, session_key)
assert bob_id == bobs_id
assert int(timestamp) == nonce_r_a

bobs_timestamp = bob.step_3_4(bobs_ticket)
decrypted_bobs_timestamp = DesKey(session_key).decrypt(bobs_timestamp)[:10].decode()
print(f"Пользователь {alice.name} получил метку {decrypted_bobs_timestamp}")

print(f"Пользователь {alice.name} отправил метку {int(decrypted_bobs_timestamp) + 1}")
bob.step_5(DesKey(session_key).encrypt(str(int(decrypted_bobs_timestamp) + 1).encode(), padding=True), alice_id)

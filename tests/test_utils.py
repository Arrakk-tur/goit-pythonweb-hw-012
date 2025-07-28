from random import randint
from typing import Dict

rand_num = randint(100, 1000)


def test_user() -> Dict:
    return {"email": f"tester_user_{rand_num}@example.com",
            "password": "testpass123"}

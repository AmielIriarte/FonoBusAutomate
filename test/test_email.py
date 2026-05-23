if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.emailer import send_email
from src.config import config

def test_email():

    send_email(
        subject="TEST EMAIL",
        body="Si recibiste esto, SMTP funciona.",
        config=config
    )

    assert True


if __name__ == "__main__":
    test_email()

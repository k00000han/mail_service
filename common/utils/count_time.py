import random
from datetime import datetime, timedelta


async def time_randomizer():
    """
    This is function wich count time for Celery Tasks

    :return: random time
    """
    now = datetime.utcnow()
    random_time = random.randint(0, 300)
    eta_time = now + timedelta(seconds=random_time)

    return eta_time

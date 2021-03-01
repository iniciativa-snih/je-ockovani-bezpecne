import pytest
from jeockovanibezpecne.db import get_db


def test_index(client):
    response = client.get('/')
    assert b'2021-01-01' in response.data

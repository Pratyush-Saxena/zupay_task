import requests as req
from app.tests import test


def test_auth_login_before_signup():
    """Test login before signup"""
    resp = req.get(
        test.host + "/auth/login",
        params={"email": test.email, "password": test.password},
    )
    assert resp.status_code == 401


def test_auth_signup():
    """Test signup"""
    resp = req.post(
        test.host + "/auth/signup",
        json={"email": test.email, "password": test.password},
    )
    assert resp.status_code == 201
    resp = req.post(
        test.host + "/auth/signup",
        json={"email": test.email, "password": test.password},
    )
    assert resp.status_code == 409


def test_auth_login_after_signup():
    """Test login after signup"""
    resp = req.get(
        test.host + "/auth/login",
        params={"email": test.email, "password": test.password},
    )
    assert resp.status_code == 200
    assert "token" in resp.json()
    assert type(resp.json()["token"]) == str
    test.token = resp.json()["token"]


def test_verify_token():
    """Test verify token"""
    resp = req.get(test.host + "/auth/verify_token", params={"token": test.token})
    assert resp.status_code == 200


def test_refresh_token():
    """Test refresh token"""
    resp = req.get(test.host + "/auth/refresh_token", params={"token": test.token})
    assert resp.status_code == 200
    assert "token" in resp.json()
    test.token = resp.json()["token"]

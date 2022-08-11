import requests as req
from app.tests import test



def test_create_post():
    """Test create post"""
    resp=req.post(test.host+'/todo/',json=test.todo)
    assert resp.status_code==401
    test.set_token()
    resp=req.post(test.host+'/todo/',headers=test.headers,json=test.todo)
    assert resp.status_code==201
    assert resp.json() == {'message': 'Post created'}


def test_get_all_posts():
    """Test get all posts"""
    resp=req.get(test.host+'/todo/')
    assert resp.status_code==401
    test.set_token()
    resp=req.get(test.host+'/todo/',headers=test.headers)
    assert resp.status_code==200
    post = resp.json()['posts'][0]
    test.todo=post

def test_update_post():
    """Test update post"""
    resp=req.put(test.host+'/todo/',json=test.todo)
    assert resp.status_code==401
    test.set_token()
    resp=req.put(test.host+'/todo/',headers=test.headers,json=test.todo)
    assert resp.status_code==200
    assert resp.json() == {'message': 'Post updated'}

def test_delete_post():
    """Test delete post"""
    resp=req.delete(test.host+'/todo/',json=test.todo)
    assert resp.status_code==401
    test.set_token()
    resp=req.delete(test.host+'/todo/',headers=test.headers,params={'post_id':test.todo['id']})
    assert resp.status_code==200
    assert resp.json() == {'message': 'Post deleted'}



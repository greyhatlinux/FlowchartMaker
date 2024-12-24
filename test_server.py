from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_fastapi_server():
    response = client.get('/')

    assert response.status_code == 200

def test_get_all_flowcharts():
    response = client.get('/flowcharts')   

    assert response.status_code == 200
    assert response.json()['message'] == 'All flowcharts'

def test_create_new_flowchart_success():
    response = client.post('/flowchart/new/TestFlowchart/ABCDAD')

    assert response.status_code == 200
    assert response.json()['message'] == 'Created the following flowchart'
    assert 'data' in response.json()

def test_create_new_flowchart_incomplete_relations():
    response = client.post('/flowchart/new/TestFlowchart/ABCDC')

    assert response.status_code == 400
    assert response.json()['detail'] == "Relationship is not complete"

def test_create_new_flowchart_empty_relation():
    response = client.post('/flowchart/new/TestFlowchart/')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'

def test_update_add_edge_flowchart_success():
    response =  client.patch('/flowchart/addedge/1/ABCDRD')

    assert response.status_code == 200
    assert response.json()['message'] == 'Added the edges in the flowchart'

def test_update_add_edge_flowchart_failure():
    response =  client.patch('/flowchart/addedge/1/ABC')

    assert response.status_code == 400
    assert response.json()['detail'] == 'Relationship is not complete'

def test_update_remove_edge_flowchart_success():
    response =  client.patch('/flowchart/removeedge/1/ABCDEF')

    assert response.json()['message'] == 'Removed the edges in the flowchart'
    assert response.status_code == 200

def test_update_remove_edge_flowchart_failure():
    response =  client.patch('/flowchart/removeedge/2/ABC')

    assert response.status_code == 400
    assert response.json()['detail'] == 'Relationship is not complete'


def test_update_remove_edge_flowchart_incomplete_request():
    response =  client.patch('/flowchart/removeedge/2/')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'


def test_get_all_outgoing_edges_success():
    response = client.get('/flowchart/1/outgoingedge/A')

    assert response.status_code == 200
    assert response.json()['message'] == 'Fetched all outgoing edges for Flowchart : 1 for Edge A'

def test_get_all_outgoing_edges_failure():
    response = client.get('/flowchart/1/outgoingedge/AX')

    assert response.status_code == 400
    assert response.json()['detail'] == 'Provide one node to fetch the outgoing edges'

def test_delete_flowchart_success():
    response = client.delete('/flowchart/delete/1')

    assert response.status_code == 200
    assert response.json()['message'] == 'Deleted the flowchart with id : 1'

def test_delete_flowchart_failure():
    response = client.delete('/flowchart/delete/1/de')

    assert response.status_code == 404
    assert response.json()['detail'] == 'Not Found'

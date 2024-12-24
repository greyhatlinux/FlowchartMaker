from fastapi import FastAPI, HTTPException, responses
from fastapi.responses import JSONResponse, HTMLResponse
from models import graph
from typing import Optional, List, Dict
from pydantic import BaseModel
from models.flowchart import Flowchart, updated_flowchart
import os

app = FastAPI()

# In-memory data store for the project 
all_flowcharts = []

# Global id variable to keep assign unique keys to all flowcharts
global_id = 0

@app.get("/", response_class=HTMLResponse)
def fastapi_server():
    with open(os.path.join('index.html')) as html:
        html_content = html.read()
    return HTMLResponse(content=html_content)
    # return "Hello from FLowchart Server. Please visit 127.0.0.1:8000/docs for API endpoints"

# GET - get all flowcharts
@app.get("/flowcharts", response_model=list[Flowchart])
def get_all_flowcharts():
    response = {
        'message' : 'All flowcharts',
        'data' : [flowchart.__dict__ for flowchart in all_flowcharts]
    }
    return JSONResponse(content=response)

# Get a particular flowchart
@app.get("/flowchart/{id}", response_model=Flowchart)
def get_one_flowchart(id: int):
    for flowchart in all_flowcharts:
        if flowchart.id == id :
            nodes = [node for node in flowchart.graph.keys()]
            response = {
                'message' : f'Flowchart with id : {id}',
                'name' : flowchart.name,
                'nodes' : nodes,
                'data' : flowchart.__dict__
            }
            return JSONResponse(content=response)
    raise HTTPException(status_code=404, detail=f"Flowchart with id : {id} not found")


# POST - create new flowchart
@app.post("/flowchart/new/{name}/{relations}", response_model=Flowchart)
def create_new_flowchart(name: str, relations: str):
    if len(relations)%2 != 0:
         raise HTTPException(status_code=400, detail="Relationship is not complete")
    global global_id 
    global_id += 1
    new_flowchart = graph.create_flowchart(id=global_id, name=name, relations=relations)
    all_flowcharts.append(new_flowchart)
    response = {
        'message' : 'Created the following flowchart',
        'data': new_flowchart.__dict__
    }
    return JSONResponse(content=response)


# PATCH - update existing flowchart
@app.patch("/flowchart/addedge/{id}/{relations}", response_model=Flowchart)
def update_add_edge_flowchart(id: int, relations: str):
    if len(relations)%2 != 0:
        raise HTTPException(status_code=400, detail="Relationship is not complete")

    for flowchart in all_flowcharts:
        if flowchart.id == id:
            new_flowchart = flowchart
            new_flowchart.graph = graph.update_add_edge(new_flowchart, relations)
            flowchart = new_flowchart
            response = {
                'message' : 'Added the edges in the flowchart',
                'data' : new_flowchart.__dict__
            }
            return JSONResponse(content=response)
    raise HTTPException(status_code=404, detail=f"Flowchart with id : {id} not found")


#  Remove edges from the flowchart
@app.patch("/flowchart/removeedge/{id}/{relations}")
def update_remove_edge_flowchart(id: int, relations: str):
    if len(relations)%2 != 0:
        raise HTTPException(status_code=400, detail="Relationship is not complete")

    for flowchart in all_flowcharts:
        if flowchart.id == id:
            new_flowchart = flowchart
            new_flowchart.graph = graph.update_remove_edge(new_flowchart, relations)
            flowchart = new_flowchart
            response = {
                'message' : 'Removed the edges in the flowchart',
                'data' : new_flowchart.__dict__
            }
            return JSONResponse(content=response)
    raise HTTPException(status_code=404, detail=f"Flowchart with id : {id} not found")


# Fetch all outgoing edges
@app.get("/flowchart/{id}/outgoingedge/{edge}")
def get_all_outgoing_edges(id: int, edge: str):
    if len(edge) > 1:
        raise HTTPException(status_code=400, detail="Provide one node to fetch the outgoing edges")
    for flowchart in all_flowcharts:
        if flowchart.id == id:
            outgoing_edges = graph.fetch_outgoing_edges(flowchart, edge)
            if outgoing_edges < 0 :
                raise HTTPException(status_code=400, detail=f"Flowchart with id : {id} doesn't have {edge} as a node")
            response = {
                'message' : f'Fetched all outgoing edges for Flowchart : {id} for Edge {edge}',
                'data': outgoing_edges
            }
            return JSONResponse(content=response)
    raise HTTPException(status_code=404, detail=f"Flowchart with id : {id} not found")


# DELETE - delete a flowchart
@app.delete("/flowchart/delete/{id}", response_model=Flowchart)
def delete_flowchart(id: int):
    if id > global_id:
        raise HTTPException(status_code=404, detail=f"Flowchart with id {id} doesn't exist")
    for flowchart in all_flowcharts:
        if flowchart.id == id:
            deleted_flowchart = flowchart
            all_flowcharts.remove(flowchart)
            response = {
                'message' : f'Deleted the flowchart with id : {id}',
                'data' : flowchart.__dict__
            }
            return JSONResponse(content=response)
    raise HTTPException(status_code=404, detail=f"Flowchart with id : {id} was already deleted")

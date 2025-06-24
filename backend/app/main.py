from fastapi import FastAPI

from backend.app.api.v1.endpoints import project_events, all_events, own_events, calendar_events, event_instance_detail

app = FastAPI()

app.include_router(project_events.router)
app.include_router(all_events.router)
app.include_router(own_events.router)
app.include_router(calendar_events.router)
app.include_router(event_instance_detail.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

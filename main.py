import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Post

app = FastAPI(title="Manhwa Forum API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PostIn(Post):
    pass

class PostOut(Post):
    id: str


def serialize_post(doc: dict) -> PostOut:
    return PostOut(
        id=str(doc.get("_id")),
        title=doc.get("title"),
        summary=doc.get("summary"),
        rating=doc.get("rating"),
        genres=doc.get("genres", []),
        links=doc.get("links", []),
        image_urls=doc.get("image_urls", []),
        image_data=doc.get("image_data", []),
        author=doc.get("author"),
    )


@app.get("/")
def read_root():
    return {"message": "Manhwa Forum API running"}


@app.get("/api/posts", response_model=List[PostOut])
def list_posts(limit: int = 50):
    try:
        docs = get_documents("post", {}, limit)
        return [serialize_post(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/posts", response_model=dict)
def create_post(payload: PostIn):
    try:
        post_id = create_document("post", payload)
        return {"id": post_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

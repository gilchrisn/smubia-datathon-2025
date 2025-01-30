import os
import httpx  # Use async HTTP client
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debugging: Print environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
print("SUPABASE_URL:", SUPABASE_URL)
print("SUPABASE_KEY:", SUPABASE_KEY)

# Check if values are None
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ Environment variables not loaded properly!")

# Create Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
}

# FastAPI app
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "FastAPI is running!"}

@app.get("/graph")
async def fetch_graph():
    async with httpx.AsyncClient() as client:
        # Fetch nodes
        nodes_response = await client.get(f"{SUPABASE_URL}/rest/v1/nodes", headers=HEADERS)
        edges_response = await client.get(f"{SUPABASE_URL}/rest/v1/edges", headers=HEADERS)

        if nodes_response.status_code != 200 or edges_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error fetching data from Supabase")

        nodes = nodes_response.json()
        edges = edges_response.json()

    return {"nodes": nodes, "edges": edges}

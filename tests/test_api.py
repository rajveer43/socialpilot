from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
import json
import os

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_generate_reply_with_dataset():
    # Load the dataset
    df = pd.read_csv("datasets/posts - Sheet1.csv")
    
    # Create results directory if it doesn't exist
    os.makedirs("results", exist_ok=True)
    
    # Test with LinkedIn post
    linkedin_post = df[df['platform'] == 'linkedin'].iloc[0]
    test_data = {
        "platform": linkedin_post['platform'],
        "post_text": linkedin_post['post_text']
    }
    response = client.post("/reply", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["platform"] == test_data["platform"]
    assert data["post_text"] == test_data["post_text"]
    
    # Save LinkedIn results
    with open("results/linkedin_reply.json", "w") as f:
        json.dump(data, f, indent=2)
    
    # Test with Twitter post
    twitter_post = df[df['platform'] == 'twitter'].iloc[0]
    test_data = {
        "platform": twitter_post['platform'],
        "post_text": twitter_post['post_text']
    }
    response = client.post("/reply", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["platform"] == test_data["platform"]
    assert data["post_text"] == test_data["post_text"]
    
    # Save Twitter results
    with open("results/twitter_reply.json", "w") as f:
        json.dump(data, f, indent=2)
    
    # Test with Instagram post
    instagram_post = df[df['platform'] == 'instagram'].iloc[0]
    test_data = {
        "platform": instagram_post['platform'],
        "post_text": instagram_post['post_text']
    }
    response = client.post("/reply", json=test_data)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["platform"] == test_data["platform"]
    assert data["post_text"] == test_data["post_text"]
    
    # Save Instagram results
    with open("results/instagram_reply.json", "w") as f:
        json.dump(data, f, indent=2)

def test_invalid_platform():
    test_data = {
        "platform": "invalid_platform",
        "post_text": "Test post"
    }
    response = client.post("/reply", json=test_data)
    assert response.status_code == 422  # Validation error
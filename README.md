# Social Media Reply Generator

A FastAPI-based service that generates human-like replies to social media posts using Groq LLM.

## Features

- Generates platform-specific, human-like replies for Twitter, LinkedIn, and Instagram
- RESTful API with FastAPI
- MongoDB integration for storing post-reply pairs
- Sophisticated prompting workflow for natural responses
- Platform-specific tone and style matching

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following variables:
```
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_uri
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Usage

### Generate Reply

```http
POST /reply
Content-Type: application/json

{
    "platform": "twitter",
    "post_text": "Your post text here"
}
```

Response:
```json
{
    "reply": "Generated reply text",
    "platform": "twitter",
    "post_text": "Original post text",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── database.py          # MongoDB connection
│   ├── services/
│   │   ├── llm_service.py   # Groq LLM integration
│   │   └── reply_service.py # Reply generation logic
│   └── utils/
│       └── prompt_templates.py # Platform-specific prompts
├── tests/                   # Test files
├── .env                     # Environment variables
├── requirements.txt         # Project dependencies
└── README.md               # Project documentation
```

## Architecture

The system uses a multi-step approach to generate human-like replies:

1. Platform Detection: Identifies the social media platform
2. Context Analysis: Analyzes the post content and context
3. Tone Matching: Determines appropriate tone and style
4. Reply Generation: Uses Groq LLM with platform-specific prompting
5. Response Storage: Saves the generated reply in MongoDB

## License

MIT 
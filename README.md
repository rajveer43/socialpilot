# Socialpilot 

A FastAPI-based service that generates human-like replies to social media posts using Groq LLM. This project uses advanced language models to create contextually appropriate, platform-specific responses that mimic human interaction.

## Features

- 🤖 AI-Powered Reply Generation
  - Uses Groq's llama 4 model for high-quality responses
  - Platform-specific tone and style matching
  - Context-aware reply generation

- 🌐 Multi-Platform Support
  - Twitter: Concise, engaging tweets with hashtags
  - LinkedIn: Professional, insightful responses
  - Instagram: Friendly, emoji-rich interactions

- 💾 Data Management
  - MongoDB integration for storing post-reply pairs
  - Efficient data retrieval and storage
  - Timestamp tracking for all interactions

- 🛠️ Technical Features
  - RESTful API with FastAPI
  - Async/await for better performance
  - Comprehensive error handling
  - CORS middleware support
  - Health check endpoint

## Prerequisites

- Python 3.8+
- MongoDB (local or Atlas)
- Groq API key

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/socialpilot.git
cd socialpilot
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
MONGODB_URI=your_mongodb_uri_here
```

5. Run the application:
```bash
uvicorn app.main:app --reload
```

you can also run the app by pulling docker container
```bash
docker pull rajveer43/socialpilot:latest
```

## Results

### Testing Results

The API has been tested using Postman with three different approaches:

1. **Agent-based Testing**
   - Successfully tested autonomous agent interactions
   - Verified agent decision-making capabilities
   - Confirmed proper handling of complex conversation flows

2. **Prompt Chain Testing**
   - Validated multi-step prompt processing
   - Confirmed proper context maintenance between steps
   - Verified chain execution order and dependencies

3. **Standard Prompt Testing**
   - Tested basic prompt-response functionality
   - Verified response formatting and structure
   - Confirmed proper error handling

All test results and screenshots are available in the `results/` directory:


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

### Health Check

```http
GET /health
```

Response:
```json
{
    "status": "healthy"
}
```

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI application and routes
│   ├── models.py            # Pydantic models for request/response
│   ├── database.py          # MongoDB connection and operations
│   └── services/
│       ├── llm_service.py   # Groq LLM integration
│       └── reply_service.py # Reply generation logic
├── tests/
│   └── test_api.py         # API endpoint tests
├── datasets/               # Sample data and training sets
├── .env                    # Environment variables
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Testing

Run the test suite:
```bash
pytest tests/test_api.py -v
```

## Architecture

The system follows a multi-step approach to generate human-like replies:

1. **Request Processing**
   - Validates input using Pydantic models
   - Extracts platform and post text

2. **Context Analysis**
   - Determines platform-specific requirements
   - Analyzes post content and context

3. **Reply Generation**
   - Uses Groq LLM with platform-specific prompts
   - Applies tone and style matching
   - Generates contextually appropriate response

4. **Response Handling**
   - Stores reply in MongoDB
   - Returns formatted response
   - Includes metadata and timestamp

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 

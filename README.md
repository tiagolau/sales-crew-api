# Sales Follow-up Crew API

This is a Python microservice that uses CrewAI to generate personalized follow-up messages for sales leads.

## Setup

1.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in your API Key (OpenAI is default).
    ```bash
    cp .env.example .env
    ```

2.  **Local Run (Python)**:
    ```bash
    pip install -r requirements.txt
    python main.py
    ```
    API will be running at `http://localhost:8000`.

3.  **Docker Run**:
    ```bash
    docker build -t sales-crew-api .
    docker run -p 8000:8000 --env-file .env sales-crew-api
    ```

## Usage

Send a POST request to `/generate-followup`:

```json
{
  "client_name": "Carlos Silva",
  "pain_points": "High employee turnover",
  "meeting_date": "Thursday at 2pm"
}
```

The response will contain the generated WhatsApp message.

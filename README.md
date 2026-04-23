# Prompt Quality Evaluator

A Flask-based API service that uses LangChain and OpenAI to evaluate the quality of prompts.

## Features

- Evaluates prompts on clarity, specificity, and context
- Assigns an overall quality score (1-10)
- Provides detailed feedback and improvement suggestions
- RESTful API endpoint for easy integration

## API Endpoints

### POST /evaluate
Evaluate a prompt quality.

**Request:**
```json
{
  "prompt": "Your prompt text here"
}
```

**Response:**
```json
{
  "input_prompt": "Your prompt text here",
  "evaluation": {
    "overall_score": 7,
    "breakdown": {
      "clarity": 8,
      "specificity": 6,
      "context": 7
    },
    "feedback": "The prompt is reasonably clear...",
    "improvements": [
      "Add more specific examples",
      "Include expected output format"
    ]
  }
}
```

### GET /health
Health check endpoint.

### GET /
Service information.

## Deployment

Deployed on Heroku.

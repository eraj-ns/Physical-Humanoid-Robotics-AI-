# Data Model: FastAPI RAG Integration

## Entities

### QueryRequest
**Description**: Represents a query sent from the frontend to the backend API

**Fields**:
- `query` (string, required): The user's question or query text
- `session_id` (string, optional): Session identifier for conversation context (future enhancement)
- `metadata` (object, optional): Additional query metadata (future enhancement)

**Validation Rules**:
- `query` must be non-empty string
- `query` length should be reasonable (e.g., < 10000 characters)

### AgentResponse
**Description**: Represents the response from the RAG agent, returned to the frontend

**Fields**:
- `content` (string, required): The agent's response content
- `sources` (array of objects, required): List of sources used to generate the response
  - `id` (string): Unique identifier for the source
  - `url` (string): URL of the source document
  - `text` (string): Preview text of the source content
- `confidence` (string, required): Confidence level ("high", "medium", "low")
- `follow_up_questions` (array of strings, optional): Suggested follow-up questions

**Validation Rules**:
- `content` must be non-empty string
- `sources` must be an array of source objects
- `confidence` must be one of the allowed values
- `follow_up_questions` is optional and may be null or empty array

### APIError
**Description**: Represents an error response from the API

**Fields**:
- `error` (string, required): Error message
- `status_code` (integer, required): HTTP status code
- `details` (object, optional): Additional error details

**Validation Rules**:
- `error` must be non-empty string
- `status_code` must be valid HTTP error code

## State Transitions

### Query Processing Flow
1. **QueryReceived**: API receives a QueryRequest from frontend
2. **Processing**: RAG agent processes the query with retrieval
3. **ResponseReady**: AgentResponse is prepared for return
4. **ResponseSent**: API returns AgentResponse to frontend

### Error Handling Flow
1. **QueryReceived**: API receives a QueryRequest from frontend
2. **ValidationError**: If request doesn't meet validation rules
3. **ErrorResponse**: API returns APIError to frontend

## Relationships

- QueryRequest is sent to the API endpoint which processes it using the RAG agent
- RAG agent generates an AgentResponse based on the query and retrieved information
- AgentResponse is returned to the frontend that sent the original QueryRequest
- APIError is returned to frontend when processing fails
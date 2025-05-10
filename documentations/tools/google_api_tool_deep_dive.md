# GoogleApiTool Deep Dive Documentation

## Architectural Overview

The `GoogleApiTool` system provides a streamlined way to integrate Google API services into ADK-powered agents. It serves as a specialized bridge between ADK's tool infrastructure and Google's extensive API ecosystem, enabling agents to perform actions like managing calendars, sending emails, accessing Google Drive documents, and more.

### Core Architecture

```
┌────────────────────┐     ┌────────────────────┐
│                    │     │                    │
│   ADK Framework    │─────►  GoogleApiTool     │
│                    │     │                    │
└────────────────────┘     └─────────┬──────────┘
                                     │
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │                     │
                           │  RestApiTool        │
                           │  (OpenAPI Wrapper)  │
                           │                     │
                           └─────────┬───────────┘
                                     │
                                     │
                                     ▼
                           ┌─────────────────────┐
                           │                     │
                           │  Google API         │
                           │  Services           │
                           │                     │
                           └─────────────────────┘
```

The architecture consists of several key components that work together:

1. **GoogleApiTool**: The main wrapper for individual Google API calls
2. **GoogleApiToolSet**: A collection manager for related Google API tools
3. **GoogleApiToOpenApiConverter**: Converts Google's Discovery Service documents to OpenAPI format
4. **RestApiTool**: The underlying infrastructure for making authenticated REST API calls
5. **Authentication Components**: Handles OAuth2 credentials and token management

## Layer Breakdown

### Layer 1: GoogleApiTool (Wrapper Layer)

This is the entry point and main interface for agents. It wraps around RestApiTool to provide:

- Google-specific authentication handling
- Simplified tool initialization
- Consistent naming and description conventions

### Layer 2: RestApiTool (API Interface Layer)

The operational layer that:

- Builds HTTP requests with proper parameters
- Handles authentication token management
- Processes API responses
- Manages errors and retries

### Layer 3: OpenAPI Spec (Definition Layer)

The specification layer that defines:

- Available API endpoints
- Input/output schemas
- Authentication requirements
- Parameter definitions

### Layer 4: Google API Services (Service Layer)

The actual Google services being accessed:

- Gmail, Calendar, Drive, YouTube, etc.
- Each with their own authentication scopes
- Each with unique functionality and constraints

## Internal Workflows

### Tool Initialization Flow

```
┌───────────────┐     ┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│               │     │                    │     │                    │     │                    │
│ Get Tool Set  ├────►│ Convert Google API ├────►│ Create RestApiTool ├────►│ Wrap with          │
│ for Service   │     │ Spec to OpenAPI    │     │ Instances          │     │ GoogleApiTool      │
│               │     │                    │     │                    │     │                    │
└───────────────┘     └────────────────────┘     └────────────────────┘     └────────────────────┘
```

### Authentication Flow

```
┌───────────────┐     ┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│               │     │                    │     │                    │     │                    │
│ Configure     ├────►│ Create OAuth       ├────►│ Request User       ├────►│ Store and Use      │
│ Auth Creds    │     │ Credentials        │     │ Authorization      │     │ Access Token       │
│               │     │                    │     │                    │     │                    │
└───────────────┘     └────────────────────┘     └────────────────────┘     └────────────────────┘
```

### API Call Flow

```
┌───────────────┐     ┌────────────────────┐     ┌────────────────────┐     ┌────────────────────┐
│               │     │                    │     │                    │     │                    │
│ Agent Calls   ├────►│ Process Input      ├────►│ Add Authentication ├────►│ Make API Request   │
│ Tool Method   │     │ Parameters         │     │ Credentials        │     │                    │
│               │     │                    │     │                    │     │                    │
└───────────────┘     └────────────────────┘     └────────────────────┘     └────────┬───────────┘
                                                                                     │
┌───────────────┐     ┌────────────────────┐     ┌────────────────────┐              │
│               │     │                    │     │                    │              │
│ Return Result ◄─────┤ Process Response   ◄─────┤ Parse API          ◄──────────────┘
│ to Agent      │     │ Data               │     │ Response           │
│               │     │                    │     │                    │
└───────────────┘     └────────────────────┘     └────────────────────┘
```

## Integration Patterns

### 1. Direct Tool Integration

The simplest approach, integrating specific Google API tools into an agent:

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import gmail_tool_set

# Create an agent with Gmail capabilities
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # Add specific Gmail API tools
        gmail_tool_set.get_tool("messages_list"),
        gmail_tool_set.get_tool("messages_send")
    ],
    instructions="""
    You can help users manage their Gmail. You can:
    - List messages in their inbox
    - Send new emails
    """
)
```

### 2. Complete Service Integration

Adding an entire Google service toolset to an agent:

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import calendar_tool_set

# Configure authentication for all tools in the set
calendar_tool_set.configure_auth(
    client_id="YOUR_CLIENT_ID",
    client_secret="YOUR_CLIENT_SECRET"
)

# Create an agent with all Calendar capabilities
calendar_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=calendar_tool_set.get_tools(),  # Add all calendar tools
    instructions="""
    You're a calendar management assistant. You can:
    - Create and update events
    - List upcoming events
    - Manage calendar settings
    - Add and remove attendees
    """
)
```

### 3. Multi-Service Integration

Combining multiple Google API services in a single agent:

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import (
    gmail_tool_set,
    calendar_tool_set,
    drive_tool_set
)

# Create a comprehensive productivity agent
productivity_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # Gmail tools
        gmail_tool_set.get_tool("messages_list"),
        gmail_tool_set.get_tool("messages_send"),

        # Calendar tools
        calendar_tool_set.get_tool("events_list"),
        calendar_tool_set.get_tool("events_insert"),

        # Drive tools
        drive_tool_set.get_tool("files_list"),
        drive_tool_set.get_tool("files_create")
    ],
    instructions="""
    You're a productivity assistant that can help with:
    - Email management via Gmail
    - Calendar scheduling and meeting coordination
    - File management in Google Drive
    """
)
```

### 4. Authentication-Focused Integration

Centralized authentication management for Google services:

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import (
    gmail_tool_set,
    calendar_tool_set
)

# Centralized auth configuration
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

# Configure all tool sets with the same credentials
gmail_tool_set.configure_auth(client_id, client_secret)
calendar_tool_set.configure_auth(client_id, client_secret)

# Create agent with authenticated tools
agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        *gmail_tool_set.get_tools(),
        *calendar_tool_set.get_tools()
    ]
)
```

## Available Google API Tool Sets

The Google API Tool system provides pre-built tool sets for several Google services:

| Tool Set            | API             | Description                    |
| ------------------- | --------------- | ------------------------------ |
| `bigquery_tool_set` | BigQuery API v2 | Data analytics and SQL queries |
| `calendar_tool_set` | Calendar API v3 | Calendar and event management  |
| `gmail_tool_set`    | Gmail API v1    | Email management               |
| `youtube_tool_set`  | YouTube API v3  | Video management and search    |
| `slides_tool_set`   | Slides API v1   | Presentation management        |
| `sheets_tool_set`   | Sheets API v4   | Spreadsheet manipulation       |
| `docs_tool_set`     | Docs API v1     | Document creation and editing  |

Each tool set is lazily loaded when first accessed, improving performance by only loading APIs that are actually used.

## Authentication Mechanism

### OAuth2 Configuration

Google API tools use OAuth2 for authentication. The standard setup involves:

```python
# Configure client credentials
client_id = "YOUR_CLIENT_ID_FROM_GOOGLE_CLOUD_CONSOLE"
client_secret = "YOUR_CLIENT_SECRET_FROM_GOOGLE_CLOUD_CONSOLE"

# Configure all tools in a tool set
tool_set.configure_auth(client_id, client_secret)
```

### Authentication Flow

When a GoogleApiTool is used:

1. The tool checks if it has valid credentials
2. If not, it initiates the OAuth2 authorization flow:
   - Redirects the user to Google's authorization page
   - User grants permissions for the requested scopes
   - Google returns an authorization code
   - The code is exchanged for access and refresh tokens
3. The access token is attached to API calls
4. When the token expires, the refresh token is used to obtain a new access token

### Scope Configuration

Each tool set automatically requests the minimum required scopes for its operations. For example:

- Gmail: `https://www.googleapis.com/auth/gmail.modify`
- Calendar: `https://www.googleapis.com/auth/calendar`
- Drive: `https://www.googleapis.com/auth/drive`

## Implementation Details

### GoogleApiTool Class

The `GoogleApiTool` class serves as a thin wrapper around `RestApiTool` with Google-specific customizations:

```python
class GoogleApiTool(BaseTool):
    def __init__(self, rest_api_tool: RestApiTool):
        super().__init__(
            name=rest_api_tool.name,
            description=rest_api_tool.description,
            is_long_running=rest_api_tool.is_long_running,
        )
        self.rest_api_tool = rest_api_tool

    def _get_declaration(self) -> FunctionDeclaration:
        return self.rest_api_tool._get_declaration()

    async def run_async(
        self, *, args: dict[str, Any], tool_context: Optional[ToolContext]
    ) -> Dict[str, Any]:
        return await self.rest_api_tool.run_async(
            args=args, tool_context=tool_context
        )

    def configure_auth(self, client_id: str, client_secret: str):
        self.rest_api_tool.auth_credential = AuthCredential(
            auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
            oauth2=OAuth2Auth(
                client_id=client_id,
                client_secret=client_secret,
            ),
        )
```

### GoogleApiToolSet Class

The `GoogleApiToolSet` manages collections of related GoogleApiTool instances:

```python
class GoogleApiToolSet:
    def __init__(self, tools: List[RestApiTool]):
        self.tools: Final[List[GoogleApiTool]] = [
            GoogleApiTool(tool) for tool in tools
        ]

    def get_tools(self) -> List[GoogleApiTool]:
        """Get all tools in the toolset."""
        return self.tools

    def get_tool(self, tool_name: str) -> Optional[GoogleApiTool]:
        """Get a tool by name."""
        matching_tool = filter(lambda t: t.name == tool_name, self.tools)
        return next(matching_tool, None)

    def configure_auth(self, client_id: str, client_secret: str):
        for tool in self.tools:
            tool.configure_auth(client_id, client_secret)

    @classmethod
    def load_tool_set(
        cls: Type[GoogleApiToolSet],
        api_name: str,
        api_version: str,
    ) -> GoogleApiToolSet:
        spec_dict = GoogleApiToOpenApiConverter(api_name, api_version).convert()
        scope = list(
            spec_dict['components']['securitySchemes']['oauth2']['flows'][
                'authorizationCode'
            ]['scopes'].keys()
        )[0]
        return cls(
            cls._load_tool_set_with_oidc_auth(
                spec_dict=spec_dict, scopes=[scope]
            ).get_tools()
        )
```

### GoogleApiToOpenApiConverter

This converter transforms Google's API Discovery documents into OpenAPI specifications:

```python
class GoogleApiToOpenApiConverter:
    def __init__(self, api_name: str, api_version: str):
        self.api_name = api_name
        self.api_version = api_version
        self.google_api_resource = None
        self.google_api_spec = None
        self.openapi_spec = {
            "openapi": "3.0.0",
            "info": {},
            "servers": [],
            "paths": {},
            "components": {"schemas": {}, "securitySchemes": {}},
        }

    def convert(self) -> Dict[str, Any]:
        """Convert the Google API spec to OpenAPI v3 format."""
        if not self.google_api_spec:
            self.fetch_google_api_spec()

        # Convert basic API information
        self._convert_info()
        self._convert_servers()
        self._convert_security_schemes()
        self._convert_schemas()
        self._convert_resources(self.google_api_spec.get("resources", {}))
        self._convert_methods(self.google_api_spec.get("methods", {}), "/")

        return self.openapi_spec
```

## Advanced Usage Scenarios

### 1. Gmail Workflow Automation

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import gmail_tool_set
from google.adk.tools import FunctionTool

# Configure authentication
gmail_tool_set.configure_auth(client_id="...", client_secret="...")

# Custom function to analyze email sentiment
def analyze_email_sentiment(email_content: str) -> dict:
    """Analyze the sentiment of an email."""
    # Sentiment analysis logic here
    return {"sentiment": "positive", "confidence": 0.85}

# Create email automation agent
email_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # Gmail tools
        gmail_tool_set.get_tool("messages_list"),
        gmail_tool_set.get_tool("messages_get"),
        gmail_tool_set.get_tool("messages_send"),
        gmail_tool_set.get_tool("messages_trash"),

        # Custom analysis tool
        FunctionTool(analyze_email_sentiment)
    ],
    instructions="""
    You are an email management assistant that can:
    1. Check for new emails in the inbox
    2. Analyze email sentiment
    3. Draft responses for positive emails
    4. Move spam or irrelevant emails to trash
    """
)
```

### 2. Calendar and Meeting Coordinator

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import calendar_tool_set, gmail_tool_set
from datetime import datetime, timedelta

# Configure authentication for both services
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
calendar_tool_set.configure_auth(client_id, client_secret)
gmail_tool_set.configure_auth(client_id, client_secret)

# Create meeting coordinator agent
meeting_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # Calendar tools
        calendar_tool_set.get_tool("events_list"),
        calendar_tool_set.get_tool("events_insert"),
        calendar_tool_set.get_tool("freeBusy_query"),

        # Gmail tools for notifications
        gmail_tool_set.get_tool("messages_send")
    ],
    instructions="""
    You are a meeting coordinator that can:
    1. Check calendar availability
    2. Schedule new meetings at optimal times
    3. Send meeting invitations via email
    4. Find common free time slots between multiple calendars
    """
)
```

### 3. Document Collaboration System

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import (
    docs_tool_set,
    drive_tool_set,
    gmail_tool_set
)

# Configure all tool sets
for tool_set in [docs_tool_set, drive_tool_set, gmail_tool_set]:
    tool_set.configure_auth(client_id="...", client_secret="...")

# Create document collaboration agent
docs_agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # Docs tools
        docs_tool_set.get_tool("documents_get"),
        docs_tool_set.get_tool("documents_create"),
        docs_tool_set.get_tool("documents_batchUpdate"),

        # Drive tools for sharing
        drive_tool_set.get_tool("permissions_create"),

        # Gmail for notifications
        gmail_tool_set.get_tool("messages_send")
    ],
    instructions="""
    You are a document collaboration assistant that can:
    1. Create new Google Docs
    2. Edit document content
    3. Share documents with collaborators
    4. Send email notifications about document updates
    """
)
```

## Performance Considerations

### Optimizing API Usage

To improve performance and avoid API rate limits:

1. **Request Batching**: Combine multiple operations when possible

   ```python
   # Instead of multiple single operations
   for email_id in email_ids:
       gmail_tool_set.get_tool("messages_get").run({"id": email_id})

   # Use batch operation
   gmail_tool_set.get_tool("messages_batchGet").run({"ids": email_ids})
   ```

2. **Partial Responses**: Request only needed fields

   ```python
   # Request only specific fields
   calendar_tool_set.get_tool("events_list").run({
       "calendarId": "primary",
       "fields": "items(id,summary,start,end)",
       "timeMin": "2023-01-01T00:00:00Z"
   })
   ```

3. **Pagination Control**: Manage result size for large data sets
   ```python
   # Control page size and fetch specific pages
   drive_tool_set.get_tool("files_list").run({
       "pageSize": 50,
       "pageToken": next_page_token,
       "q": "mimeType='application/pdf'"
   })
   ```

### Rate Limit Management

Google APIs have various rate limits. To handle them properly:

```python
from time import sleep
from google.api_core.exceptions import ResourceExhausted

def rate_limit_aware_call(tool, args, max_retries=3):
    """Execute a tool call with rate limit awareness."""
    retries = 0
    while retries < max_retries:
        try:
            return tool.run(args)
        except ResourceExhausted as e:
            if "Rate Limit Exceeded" in str(e):
                # Exponential backoff
                sleep_time = 2 ** retries
                sleep(sleep_time)
                retries += 1
            else:
                raise
    raise Exception("Maximum retries exceeded for rate limit")
```

## Security Considerations

### OAuth Scope Management

Follow the principle of least privilege by requesting only necessary scopes:

```python
# Create a tool set with minimal scopes
from google.adk.tools.openapi_tool import OpenAPIToolset
from google.adk.auth import OpenIdConnectWithConfig

# Custom scope configuration
gmail_spec = GoogleApiToOpenApiConverter("gmail", "v1").convert()
gmail_toolset = OpenAPIToolset(
    spec_dict=gmail_spec,
    auth_scheme=OpenIdConnectWithConfig(
        scopes=["https://www.googleapis.com/auth/gmail.readonly"]  # Read-only
    )
)
```

### Credential Security

Best practices for handling OAuth credentials:

1. **Environment Variables**: Store secrets in environment variables, not code

   ```python
   import os

   client_id = os.environ.get("GOOGLE_CLIENT_ID")
   client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
   ```

2. **Secret Management**: Use a secure secret management service

   ```python
   from google.cloud import secretmanager

   def get_secret(secret_id):
       client = secretmanager.SecretManagerServiceClient()
       name = f"projects/your-project/secrets/{secret_id}/versions/latest"
       response = client.access_secret_version(request={"name": name})
       return response.payload.data.decode("UTF-8")

   client_id = get_secret("google-client-id")
   client_secret = get_secret("google-client-secret")
   ```

3. **Token Storage**: Secure token persistence

   ```python
   # Using encryption for token storage
   from cryptography.fernet import Fernet

   def encrypt_token(token, key):
       f = Fernet(key)
       return f.encrypt(token.encode())

   def decrypt_token(encrypted_token, key):
       f = Fernet(key)
       return f.decrypt(encrypted_token).decode()
   ```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue                      | Possible Causes                     | Solutions                                                    |
| -------------------------- | ----------------------------------- | ------------------------------------------------------------ |
| Authentication failures    | Invalid credentials, expired tokens | Verify client ID/secret, refresh tokens                      |
| API permission denied      | Insufficient OAuth scopes           | Request appropriate scopes for the operation                 |
| Rate limiting              | Too many requests                   | Implement exponential backoff, reduce request frequency      |
| Invalid parameters         | Incorrect parameter format          | Check API documentation for exact parameter requirements     |
| Missing fields in response | Partial response settings           | Ensure requested fields are included in the fields parameter |

### Debugging Techniques

```python
import logging

# Enable detailed logging for the GoogleApiTool
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("google.adk.tools.google_api_tool")
logger.setLevel(logging.DEBUG)

# Add request/response logging to troubleshoot API calls
def log_api_call(tool_name, args, response=None, error=None):
    """Log API request and response details."""
    logger.debug(f"API Call: {tool_name}")
    logger.debug(f"Arguments: {args}")
    if response:
        logger.debug(f"Response: {response}")
    if error:
        logger.error(f"Error: {error}")

# Wrapper for debugging
def debug_tool_call(tool, args):
    """Execute a tool call with detailed logging."""
    try:
        response = tool.run(args)
        log_api_call(tool.name, args, response=response)
        return response
    except Exception as e:
        log_api_call(tool.name, args, error=str(e))
        raise
```

## Case Studies

### Case Study 1: Email Categorization System

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import gmail_tool_set
from pydantic import BaseModel

# Define structured output
class EmailCategory(BaseModel):
    category: str  # "work", "personal", "promotional", "urgent"
    confidence: float
    action: str  # "reply", "archive", "flag", "ignore"

# Create email categorization agent
categorizer = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        gmail_tool_set.get_tool("messages_list"),
        gmail_tool_set.get_tool("messages_get"),
        gmail_tool_set.get_tool("messages_modify"),
        gmail_tool_set.get_tool("labels_create"),
        gmail_tool_set.get_tool("labels_list")
    ],
    output_schema=EmailCategory,
    instructions="""
    You analyze emails and categorize them as:
    - work: Work-related communications
    - personal: Friends and family emails
    - promotional: Marketing and promotional content
    - urgent: Time-sensitive items requiring immediate action

    For each email, recommend an action: reply, archive, flag, or ignore.
    """
)

# Usage flow
async def categorize_emails():
    # Get recent emails
    emails = await gmail_tool_set.get_tool("messages_list").run_async(
        args={"maxResults": 10, "labelIds": ["INBOX", "UNREAD"]}
    )

    for email in emails.get("messages", []):
        # Get email content
        email_data = await gmail_tool_set.get_tool("messages_get").run_async(
            args={"id": email["id"]}
        )

        # Categorize the email
        category = await categorizer.run(email_data["snippet"])

        # Apply appropriate label
        await gmail_tool_set.get_tool("messages_modify").run_async(
            args={
                "id": email["id"],
                "addLabelIds": [f"Label_{category.category.upper()}"]
            }
        )
```

### Case Study 2: Meeting Scheduler with Calendar Integration

```python
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import calendar_tool_set
from datetime import datetime, timedelta

# Create meeting scheduler agent
scheduler = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        calendar_tool_set.get_tool("events_list"),
        calendar_tool_set.get_tool("events_insert"),
        calendar_tool_set.get_tool("freeBusy_query"),
        calendar_tool_set.get_tool("calendarList_list")
    ],
    instructions="""
    You help schedule meetings by:
    1. Finding available time slots across multiple calendars
    2. Creating calendar events at optimal times
    3. Managing meeting details including location and attendees
    4. Suggesting alternative times when conflicts exist
    """
)

# Implementation for finding meeting times
async def find_meeting_time(participants, duration_minutes=30, days_ahead=7):
    # Get participant calendars
    calendars = await calendar_tool_set.get_tool("calendarList_list").run_async(args={})

    # Calculate time range
    start_time = datetime.now().isoformat() + "Z"
    end_time = (datetime.now() + timedelta(days=days_ahead)).isoformat() + "Z"

    # Check availability
    availability = await calendar_tool_set.get_tool("freeBusy_query").run_async(
        args={
            "timeMin": start_time,
            "timeMax": end_time,
            "items": [{"id": participant} for participant in participants]
        }
    )

    # Find common free times
    # (This would involve analyzing the busy periods and finding gaps)

    # Schedule the meeting
    event = await calendar_tool_set.get_tool("events_insert").run_async(
        args={
            "calendarId": "primary",
            "body": {
                "summary": "Team Meeting",
                "description": "Discuss project status",
                "start": {"dateTime": optimal_start_time},
                "end": {"dateTime": optimal_end_time},
                "attendees": [{"email": participant} for participant in participants]
            }
        }
    )

    return event
```

## Future Considerations

### Upcoming Enhancements

1. **Expanded API Coverage**:

   - Google Cloud Platform API integration
   - Additional Google Workspace services
   - YouTube API enhancements for content creation

2. **Advanced Authentication**:

   - Service account support for headless operation
   - Domain-wide delegation for workspace administrators
   - Improved token management and refresh handling

3. **Specialized Tool Variants**:
   - Read-only variants with minimal permissions
   - Administrative tools with expanded capabilities
   - Composite tools combining multiple API operations into logical actions

### Integration with Other ADK Components

```python
# Future integration with memory systems
from google.adk.agents import LlmAgent
from google.adk.tools.google_api_tool import gmail_tool_set
from google.adk.tools import load_memory_tool, preload_memory_tool

# Create memory-aware email assistant
email_assistant = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        # Gmail tools
        *gmail_tool_set.get_tools(),

        # Memory tools
        load_memory_tool,
        preload_memory_tool
    ],
    instructions="""
    You're an email assistant that remembers past conversations.
    When helping with emails, use your memory to provide context and
    maintain continuity in discussions.
    """
)
```

## Conclusion

The GoogleApiTool system represents a powerful interface between ADK agents and Google's ecosystem of services. It enables sophisticated automation scenarios across email, calendar, documents, and more through a consistent and secure interface. By leveraging the conversion of Google's API Discovery documents to OpenAPI specifications, it provides a seamless experience for developers while maintaining the flexibility to access Google's diverse array of services.

The layered architecture, robust authentication handling, and comprehensive tool set abstractions allow for both simple integration of individual services and complex multi-service workflows. As the system continues to evolve, the potential applications span productivity enhancement, content management, data analysis, and beyond - turning LLM-powered agents into capable assistants that can interact with the full range of Google services.

# 🛡️ MCP Sentinel Guard

**AI-Powered Security Gateway for Model Context Protocol (MCP)**

> *Prevents Prompt Injection, unauthorized file access, and malicious tool use by analyzing MCP traffic with Google Gemini AI.*

---

## 📖 Overview

Standard MCP servers execute LLM commands blindly. **MCP Sentinel Guard** introduces a "Man-in-the-Middle" security gateway that intercepts JSON-RPC traffic between the Host (Claude/Cursor) and the Server.

It uses **LLM-as-a-Judge** (Google Gemini 2.0 Flash) to semantically analyze every request. If a threat is detected, it blocks the request, logs the incident, and sends a real-time email alert to the admin.



✨ Key Features

    🧠 Context-Aware Analysis: Uses LLM to detect semantic attacks (e.g., "Ignore previous instructions").

    🛡️ Active Interception: Blocks malicious tools (delete_system_files) before they reach the backend.

    📧 Real-Time Alerts: Sends HTML-formatted email alerts via SMTP upon attack detection.

    📝 Audit Logging: Records every allowed/blocked transaction in security_log.txt.

    🔌 Plug & Play: Works as a standard MCP server wrapper.


    🚀 Installation
    1. Clone the Repository

    git clone [https://github.com/KVRIND3S3N/mcp-sentinel-guard.git](https://github.com/KVRIND3S3N/mcp-sentinel-guard.git)
    cd mcp-sentinel-guard   

    2. Install Dependencies

    pip install mcp google-generativeai python-dotenv

    3. Configuration (.env)

    GOOGLE_API_KEY=your_gemini_api_key
    GMAIL_USER=your_email@gmail.com
    GMAIL_APP_PASSWORD=your_16_digit_app_password

    Usage

    Start the Gateway & Host Simulation
    python attack_test.py


    Project Structure

    sentinel_gateway.py: Core Logic. Intercepts traffic and calls AI.

    vulnerable_server.py: Backend. Simulates an unprotected MCP server.

    notification_service.py: Alerts. Handles SMTP email dispatch.

    attack_test.py: Client. Simulates Host behavior (Safe & Attack scenarios).
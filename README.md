# ScholarPilot

ScholarPilot is a self-hosted, AI-powered research paper organizer. It helps researchers analyze, organize, and extract insights from academic papers using local or remote LLMs.

## Features

-   **Paper Organization**: Upload and organize research papers into projects.
-   **AI Analysis**: Automatically extract metadata, summaries, contributions, methodologies, and more using LLMs.
-   **Customizable Columns**: Define analysis columns based on templates (e.g., Survey, Experiment, SE) or custom prompts.
-   **Flexible LLM Support**: Supports OpenAI, Anthropic, Gemini, DeepSeek, and Local LLMs (via Ollama/vLLM).
-   **Export**: Export results to Excel, CSV, Markdown, or sync directly to Notion.
-   **Self-Hosted**: Full control over your data with a Docker-based deployment.

## Prerequisites

-   **Docker** and **Docker Compose** installed.
-   **API Keys** for your preferred LLM providers (e.g., OpenAI API Key).

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hyeokkiyaa/ScholarPilot-V1.0.git
cd ScholarPilot-V1.0
```

### 2. Start the Application

Run the application using Docker Compose:

```bash
docker-compose up -d --build
```

This will start:
-   **Frontend**: http://localhost:3000
-   **Backend**: http://localhost:8000

### 3. Configure Settings

1.  Open your browser and navigate to `http://localhost:3000`.
2.  You will be redirected to the **Onboarding Page**.
3.  Select your **Model Provider** (e.g., OpenAI, Ollama) and enter your **API Key** (or Base URL for local models).
4.  Click **Save & Continue**.

### 4. Create a Project

1.  Click **New Project**.
2.  Enter a project name and select a **Template**:
    -   **Basic**: Standard Summary, Key Contributions, Method.
    -   **Experiment**: Adds Baselines, Datasets, Metrics.
    -   **Survey**: Adds Research Questions, Related Work, Limitations.
    -   **SE/Systems**: Adds Architecture, Validity Threats.
3.  Upload papers (PDFs) or add links.
4.  Click **Run Analysis** to start processing.

## Export & Integration

### Export to File
-   Open a project and click the **Export** buttons (XLSX, CSV, MD) to download results.

### Notion Integration
1.  Go to **Settings**.
2.  Enter your **Notion Integration Token** and **Database ID**.
    -   *Note: Ensure your integration has access to the target database in Notion.*
3.  Go to your project and click **Export -> Notion**.

## Development

### Backend
The backend is built with **FastAPI**.
-   Docs: http://localhost:8000/docs
-   Code: `backend/app`

### Frontend
The frontend is built with **React**, **Vite**, and **Tailwind CSS**.
-   Code: `frontend/src`

## License
MIT License

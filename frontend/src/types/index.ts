export interface Project {
    id: string;
    name: string;
    template: string | null;
    created_at: string;
    updated_at: string;
    paper_count?: number;
    status_summary?: {
        done: number;
        processing: number;
        error: number;
        queued: number;
    };
}

export interface ColumnDef {
    id: string;
    project_id: string;
    name: string;
    tool_name: string;
    custom_prompt: string | null;
    order_index: number;
}

export interface Paper {
    id: string;
    project_id: string;
    title: string | null;
    status: 'queued' | 'processing' | 'done' | 'error' | 'need_pdf';
    pdf_path: string | null;
    source_url: string | null;
    source_type: string | null;
    error_message: string | null;
    created_at: string;
    updated_at: string;
    results: Record<string, Result>;
}

export interface Result {
    id: string;
    paper_id: string;
    column_id: string;
    value: any;
    status: 'pending' | 'processing' | 'done' | 'error' | 'skipped';
    error_message: string | null;
}

export interface Settings {
    model_provider: 'claude' | 'openai' | 'gemini' | 'grok' | 'solar';
    api_key: string;
    notion_api_key: string | null;
    notion_database_id: string | null;
    notion_enabled: boolean;
    google_sheets_enabled: boolean;
    onboarding_completed: boolean;
}

export interface ToolInfo {
    name: string;
    category: 'basic' | 'structure' | 'experiment' | 'research' | 'custom';
    description: string;
}

export interface ProjectTemplate {
    name: string;
    description: string;
    columns: string[];
}

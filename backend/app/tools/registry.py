# We will import tool classes here as we create them
# from app.tools.metadata_extractor import MetadataExtractor
# ...

TOOL_REGISTRY = {
    # To be populated as tools are implemented
}

TOOL_INFO = {
    "metadata_extractor": {
        "name": "Metadata",
        "category": "basic",
        "description": "Title, authors, year, affiliation"
    },
    "summarizer": {
        "name": "Summary",
        "category": "basic",
        "description": "3-5 sentence summary"
    },
    "one_sentence_summary": {
        "name": "One Sentence",
        "category": "basic",
        "description": "Single sentence summary"
    },
    "contribution_extractor": {
        "name": "Contributions",
        "category": "basic",
        "description": "Key contributions list"
    },
    "methodology_analyzer": {
        "name": "Methodology",
        "category": "basic",
        "description": "Method and approach analysis"
    },
    "keyword_tagger": {
        "name": "Keywords",
        "category": "basic",
        "description": "Field, technology, keywords"
    },
    "architecture_extractor": {
        "name": "Architecture",
        "category": "structure",
        "description": "System/model architecture"
    },
    "limitation_finder": {
        "name": "Limitations",
        "category": "structure",
        "description": "Limitations and future work"
    },
    "threat_to_validity": {
        "name": "Validity Threats",
        "category": "structure",
        "description": "Threats to validity (SE papers)"
    },
    "baseline_extractor": {
        "name": "Baselines",
        "category": "experiment",
        "description": "Baseline methods/systems"
    },
    "dataset_extractor": {
        "name": "Datasets",
        "category": "experiment",
        "description": "Dataset information"
    },
    "metric_extractor": {
        "name": "Metrics",
        "category": "experiment",
        "description": "Evaluation metrics and results"
    },
    "research_question_extractor": {
        "name": "Research Questions",
        "category": "research",
        "description": "RQs addressed"
    },
    "related_work_summarizer": {
        "name": "Related Work",
        "category": "research",
        "description": "Related work summary"
    },
    "citation_context": {
        "name": "Key Citations",
        "category": "research",
        "description": "Important citations and context"
    },
    "reproducibility_checker": {
        "name": "Reproducibility",
        "category": "research",
        "description": "Code/data availability"
    },
    "custom_prompt": {
        "name": "Custom",
        "category": "custom",
        "description": "User-defined prompt"
    }
}

PROJECT_TEMPLATES = {
    "basic": {
        "name": "Basic",
        "description": "Title, Summary, Contribution, Method, Keywords",
        "columns": ["metadata_extractor", "summarizer", "contribution_extractor", "methodology_analyzer", "keyword_tagger"]
    },
    "experiment": {
        "name": "Experiment Comparison",
        "description": "Basic + Baseline, Dataset, Metrics",
        "columns": ["metadata_extractor", "summarizer", "contribution_extractor", "methodology_analyzer", "keyword_tagger", "baseline_extractor", "dataset_extractor", "metric_extractor"]
    },
    "survey": {
        "name": "Survey Writing",
        "description": "Basic + RQ, Related Work, Limitations",
        "columns": ["metadata_extractor", "summarizer", "contribution_extractor", "methodology_analyzer", "keyword_tagger", "research_question_extractor", "related_work_summarizer", "limitation_finder"]
    },
    "se": {
        "name": "SE/Systems Paper",
        "description": "Basic + Architecture, Validity, Reproducibility",
        "columns": ["metadata_extractor", "summarizer", "contribution_extractor", "methodology_analyzer", "keyword_tagger", "architecture_extractor", "threat_to_validity", "reproducibility_checker"]
    }
}

PROMPT_PRESETS = [
    {
        "name": "Baseline Comparison",
        "prompt": "List all baseline models or systems this paper compares against."
    },
    {
        "name": "Dataset Details",
        "prompt": "Extract dataset names, sizes, sources, and availability."
    },
    {
        "name": "Evaluation Metrics",
        "prompt": "List evaluation metrics used and their reported values."
    },
    {
        "name": "Code Representation",
        "prompt": "Identify code representation techniques (AST, CFG, DFG, etc.) and how they are used."
    },
    {
        "name": "Research Gap",
        "prompt": "Identify the research gap this paper addresses."
    },
    {
        "name": "Novelty Claims",
        "prompt": "Extract the main novelty claims made by the authors."
    },
    {
        "name": "Experimental Setup",
        "prompt": "Describe the experimental setup including hardware and configurations."
    },
    {
        "name": "Ablation Study",
        "prompt": "Summarize any ablation studies and their findings."
    },
    {
        "name": "Use Cases",
        "prompt": "Identify practical use cases or applications discussed."
    },
    {
        "name": "Comparison Table",
        "prompt": "Create a comparison with related work in terms of features, methods, or results."
    }
]

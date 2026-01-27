import { useState } from 'react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { useProjectStore } from '../../stores/projectStore';
import { X, Plus, Trash2 } from 'lucide-react';

import axios from 'axios';
import toast from 'react-hot-toast';

interface ColumnManagerModalProps {
    isOpen: boolean;
    onClose: () => void;
    projectId: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Hardcoded for now, should come from backend registry ideally
const AVAILABLE_TOOLS: { value: string; label: string; description: string }[] = [
    { value: 'metadata_extractor', label: 'Metadata', description: 'Title, Authors, Year' },
    { value: 'summarizer', label: 'Summary', description: '3-5 sentence summary' },
    { value: 'one_sentence_summary', label: 'One Sentence Summary', description: 'Single sentence' },
    { value: 'contribution_extractor', label: 'Contributions', description: 'List of contributions' },
    { value: 'methodology_analyzer', label: 'Methodology', description: 'Approach analysis' },
    { value: 'keyword_tagger', label: 'Keywords', description: 'Fields and keywords' },
    { value: 'architecture_extractor', label: 'Architecture', description: 'System architecture' },
    { value: 'limitation_finder', label: 'Limitations', description: 'Limitations & Future Work' },
    { value: 'threat_to_validity', label: 'Validity Threats', description: 'Internal/External validity' },
    { value: 'baseline_extractor', label: 'Baselines', description: 'Comparison baselines' },
    { value: 'dataset_extractor', label: 'Datasets', description: 'Used datasets' },
    { value: 'metric_extractor', label: 'Metrics', description: 'Evaluation metrics' },
    { value: 'research_question_extractor', label: 'Research Questions', description: 'RQs' },
    { value: 'related_work_summarizer', label: 'Related Work', description: 'Summary of related work' },
    { value: 'citation_context', label: 'Key Citations', description: 'Important references' },
    { value: 'reproducibility_checker', label: 'Reproducibility', description: 'Code/Data availability' },
    { value: 'custom_prompt', label: 'Custom Prompt', description: 'Your own instruction' },
];

export function ColumnManagerModal({ isOpen, onClose, projectId }: ColumnManagerModalProps) {
    const { columns, createColumn, fetchColumns } = useProjectStore();
    const [isAdding, setIsAdding] = useState(false);

    // New Column State
    const [newName, setNewName] = useState('');
    const [selectedTool, setSelectedTool] = useState(AVAILABLE_TOOLS[0].value);
    const [customPrompt, setCustomPrompt] = useState('');

    if (!isOpen) return null;

    const handleDelete = async (columnId: string) => {
        if (!confirm('Delete this column? Existing results will be lost.')) return;
        try {
            await axios.delete(`${API_URL}/api/columns/${columnId}`);
            fetchColumns(projectId);
            toast.success('Column deleted');
        } catch (error) {
            toast.error('Failed to delete column');
        }
    };

    const handleAdd = async () => {
        if (!newName) {
            toast.error('Name is required');
            return;
        }

        try {
            await createColumn(projectId, {
                name: newName,
                tool_name: selectedTool,
                custom_prompt: selectedTool === 'custom_prompt' ? customPrompt : null
            });
            toast.success('Column added');
            // Reset form
            setNewName('');
            setCustomPrompt('');
            setIsAdding(false);
        } catch (error) {
            toast.error('Failed to add column');
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="w-full max-w-lg rounded-lg bg-background p-6 shadow-xl animate-in fade-in zoom-in duration-200 flex flex-col max-h-[85vh]">
                <div className="flex items-center justify-between mb-4 flex-shrink-0">
                    <h2 className="text-xl font-semibold">Manage Columns</h2>
                    <Button variant="ghost" size="icon" onClick={onClose}>
                        <X className="h-4 w-4" />
                    </Button>
                </div>

                <div className="flex-1 overflow-auto space-y-4">
                    {/* Existing Columns List */}
                    <div className="space-y-2">
                        {columns.map((col, index) => (
                            <div key={col.id} className="flex items-center justify-between p-3 border rounded-md bg-card">
                                <div className="flex items-center gap-3">
                                    <span className="text-muted-foreground text-sm font-mono w-6">{index + 1}</span>
                                    <div>
                                        <div className="font-medium">{col.name}</div>
                                        <div className="text-xs text-muted-foreground">{col.tool_name}</div>
                                    </div>
                                </div>
                                <Button
                                    variant="ghost"
                                    size="icon"
                                    className="text-destructive hover:text-destructive h-8 w-8"
                                    onClick={() => handleDelete(col.id)}
                                >
                                    <Trash2 className="h-4 w-4" />
                                </Button>
                            </div>
                        ))}
                    </div>

                    {/* Add New Section */}
                    {isAdding ? (
                        <div className="border rounded-md p-4 bg-muted/30 space-y-4 mt-4">
                            <h3 className="font-medium text-sm">New Column</h3>
                            <Input
                                label="Column Name"
                                value={newName}
                                onChange={(e) => setNewName(e.target.value)}
                                placeholder="e.g. Key Findings"
                            />

                            <div className="space-y-2">
                                <label className="text-sm font-medium">Tool</label>
                                <select
                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                    value={selectedTool}
                                    onChange={(e) => setSelectedTool(e.target.value)}
                                >
                                    {AVAILABLE_TOOLS.map(t => (
                                        <option key={t.value} value={t.value}>{t.label} - {t.description}</option>
                                    ))}
                                </select>
                            </div>

                            {selectedTool === 'custom_prompt' && (
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">Custom Prompt</label>
                                    <textarea
                                        className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        value={customPrompt}
                                        onChange={(e) => setCustomPrompt(e.target.value)}
                                        placeholder="Enter your instructions for the AI..."
                                    />
                                </div>
                            )}

                            <div className="flex justify-end gap-2 pt-2">
                                <Button variant="ghost" onClick={() => setIsAdding(false)}>Cancel</Button>
                                <Button onClick={handleAdd}>Save Column</Button>
                            </div>
                        </div>
                    ) : (
                        <Button
                            variant="outline"
                            className="w-full border-dashed"
                            onClick={() => setIsAdding(true)}
                        >
                            <Plus className="mr-2 h-4 w-4" />
                            Add Column
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
}

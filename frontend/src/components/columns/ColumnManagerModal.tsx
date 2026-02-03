import { useState } from 'react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { useProjectStore } from '../../stores/projectStore';
import { X, Plus, Trash2 } from 'lucide-react';

import axios from 'axios';
import toast from 'react-hot-toast';
import { useTranslation } from 'react-i18next';

interface ColumnManagerModalProps {
    isOpen: boolean;
    onClose: () => void;
    projectId: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const TOOL_KEYS = [
    'metadata_extractor',
    'summarizer',
    'one_sentence_summary',
    'contribution_extractor',
    'methodology_analyzer',
    'keyword_tagger',
    'architecture_extractor',
    'limitation_finder',
    'threat_to_validity',
    'baseline_extractor',
    'dataset_extractor',
    'metric_extractor',
    'research_question_extractor',
    'related_work_summarizer',
    'citation_context',
    'reproducibility_checker',
    'custom_prompt',
];

export function ColumnManagerModal({ isOpen, onClose, projectId }: ColumnManagerModalProps) {
    const { t } = useTranslation();
    const { columns, createColumn, fetchColumns } = useProjectStore();
    const [isAdding, setIsAdding] = useState(false);

    // New Column State
    const [newName, setNewName] = useState('');
    const [selectedTool, setSelectedTool] = useState(TOOL_KEYS[0]);
    const [customPrompt, setCustomPrompt] = useState('');

    if (!isOpen) return null;

    const handleDelete = async (columnId: string) => {
        if (!confirm(t('columns.deleteConfirm'))) return;
        try {
            await axios.delete(`${API_URL}/api/columns/${columnId}`);
            fetchColumns(projectId);
            toast.success(t('columns.deleteSuccess'));
        } catch (error) {
            toast.error(t('columns.deleteFail'));
        }
    };

    const handleAdd = async () => {
        if (!newName) {
            toast.error(t('columns.nameRequired'));
            return;
        }

        try {
            await createColumn(projectId, {
                name: newName,
                tool_name: selectedTool,
                custom_prompt: selectedTool === 'custom_prompt' ? customPrompt : null
            });
            toast.success(t('columns.addSuccess'));
            // Reset form
            setNewName('');
            setCustomPrompt('');
            setIsAdding(false);
        } catch (error) {
            toast.error(t('columns.addFail'));
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="w-full max-w-lg rounded-lg bg-background p-6 shadow-xl animate-in fade-in zoom-in duration-200 flex flex-col max-h-[85vh]">
                <div className="flex items-center justify-between mb-4 flex-shrink-0">
                    <h2 className="text-xl font-semibold">{t('columns.title')}</h2>
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
                                        <div className="text-xs text-muted-foreground">
                                            {t(`columns.tools.${col.tool_name}`, { defaultValue: col.tool_name })}
                                        </div>
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
                            <h3 className="font-medium text-sm">{t('columns.newColumn')}</h3>
                            <Input
                                label={t('columns.columnNameLabel')}
                                value={newName}
                                onChange={(e) => setNewName(e.target.value)}
                                placeholder={t('columns.columnNamePlaceholder')}
                            />

                            <div className="space-y-2">
                                <label className="text-sm font-medium">{t('columns.toolLabel')}</label>
                                <select
                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                    value={selectedTool}
                                    onChange={(e) => setSelectedTool(e.target.value)}
                                >
                                    {TOOL_KEYS.map(key => (
                                        <option key={key} value={key}>
                                            {t(`columns.tools.${key}`)} - {t(`columns.tools.${key}_desc`)}
                                        </option>
                                    ))}
                                </select>
                            </div>

                            {selectedTool === 'custom_prompt' && (
                                <div className="space-y-2">
                                    <label className="text-sm font-medium">{t('columns.customPromptLabel')}</label>
                                    <textarea
                                        className="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                        value={customPrompt}
                                        onChange={(e) => setCustomPrompt(e.target.value)}
                                        placeholder={t('columns.customPromptPlaceholder')}
                                    />
                                </div>
                            )}

                            <div className="flex justify-end gap-2 pt-2">
                                <Button variant="ghost" onClick={() => setIsAdding(false)}>{t('columns.cancel')}</Button>
                                <Button onClick={handleAdd}>{t('columns.save')}</Button>
                            </div>
                        </div>
                    ) : (
                        <Button
                            variant="outline"
                            className="w-full border-dashed"
                            onClick={() => setIsAdding(true)}
                        >
                            <Plus className="mr-2 h-4 w-4" />
                            {t('columns.addColumn')}
                        </Button>
                    )}
                </div>
            </div>
        </div>
    );
}

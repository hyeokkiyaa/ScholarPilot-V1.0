import { useState, useRef } from 'react';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { useProjectStore } from '../../stores/projectStore';
import { Upload, X, FileText, Link as LinkIcon } from 'lucide-react';
import { cn } from '../../lib/utils';
import toast from 'react-hot-toast';

interface AddPaperModalProps {
    projectId: string;
    isOpen: boolean;
    onClose: () => void;
}

export function AddPaperModal({ projectId, isOpen, onClose }: AddPaperModalProps) {
    const [activeTab, setActiveTab] = useState<'upload' | 'link'>('upload');
    const [file, setFile] = useState<File | null>(null);
    const [url, setUrl] = useState('');
    const [isSubmitting, setIsSubmitting] = useState(false);
    const { addPaper } = useProjectStore();
    const fileInputRef = useRef<HTMLInputElement>(null);

    if (!isOpen) return null;

    const handleSubmit = async () => {
        if (activeTab === 'upload' && !file) {
            toast.error('Please select a file');
            return;
        }
        if (activeTab === 'link' && !url) {
            toast.error('Please enter a URL');
            return;
        }

        setIsSubmitting(true);
        try {
            await addPaper(projectId, file, url);
            toast.success('Paper added successfully');
            onClose();
            // Reset form
            setFile(null);
            setUrl('');
        } catch (error) {
            toast.error('Failed to add paper');
            console.error(error);
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="w-full max-w-md rounded-lg bg-background p-6 shadow-xl animate-in fade-in zoom-in duration-200">
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold">Add New Paper</h2>
                    <Button variant="ghost" size="icon" onClick={onClose}>
                        <X className="h-4 w-4" />
                    </Button>
                </div>

                <div className="flex space-x-2 mb-6 border-b">
                    <button
                        className={cn(
                            "pb-2 px-4 text-sm font-medium transition-colors relative",
                            activeTab === 'upload' ? "text-primary border-b-2 border-primary" : "text-muted-foreground hover:text-foreground"
                        )}
                        onClick={() => setActiveTab('upload')}
                    >
                        <div className="flex items-center gap-2">
                            <Upload className="h-4 w-4" />
                            Upload PDF
                        </div>
                    </button>
                    <button
                        className={cn(
                            "pb-2 px-4 text-sm font-medium transition-colors relative",
                            activeTab === 'link' ? "text-primary border-b-2 border-primary" : "text-muted-foreground hover:text-foreground"
                        )}
                        onClick={() => setActiveTab('link')}
                    >
                        <div className="flex items-center gap-2">
                            <LinkIcon className="h-4 w-4" />
                            Import from Link
                        </div>
                    </button>
                </div>

                <div className="space-y-4">
                    {activeTab === 'upload' ? (
                        <div
                            className="border-2 border-dashed rounded-lg p-8 text-center hover:bg-muted/50 transition-colors cursor-pointer"
                            onClick={() => fileInputRef.current?.click()}
                        >
                            <input
                                type="file"
                                className="hidden"
                                ref={fileInputRef}
                                accept=".pdf"
                                onChange={handleFileChange}
                            />

                            {file ? (
                                <div className="flex flex-col items-center text-primary">
                                    <FileText className="h-10 w-10 mb-2" />
                                    <p className="font-medium">{file.name}</p>
                                    <p className="text-xs text-muted-foreground mt-1">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                                </div>
                            ) : (
                                <div className="flex flex-col items-center text-muted-foreground">
                                    <Upload className="h-10 w-10 mb-2" />
                                    <p className="font-medium">Click to upload PDF</p>
                                    <p className="text-xs mt-1">Maximum size: 20MB</p>
                                </div>
                            )}
                        </div>
                    ) : (
                        <div className="space-y-4">
                            <Input
                                label="Paper URL / ArXiv ID / DOI"
                                placeholder="https://arxiv.org/abs/..."
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                            />
                            <p className="text-xs text-muted-foreground">
                                Supported sources: ArXiv, PDF URLs, DOI (Auto-downloading not fully implemented yet)
                            </p>
                        </div>
                    )}
                </div>

                <div className="flex justify-end gap-2 mt-6">
                    <Button variant="ghost" onClick={onClose} disabled={isSubmitting}>
                        Cancel
                    </Button>
                    <Button onClick={handleSubmit} isLoading={isSubmitting}>
                        Add Paper
                    </Button>
                </div>
            </div>
        </div>
    );
}

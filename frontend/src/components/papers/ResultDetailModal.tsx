import { Button } from '../common/Button';
import { X, Copy } from 'lucide-react';
import toast from 'react-hot-toast';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ResultDetailModalProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    content: any;
}

export function ResultDetailModal({ isOpen, onClose, title, content }: ResultDetailModalProps) {
    if (!isOpen) return null;

    const handleCopy = () => {
        const text = typeof content === 'object' ? JSON.stringify(content, null, 2) : String(content);
        navigator.clipboard.writeText(text);
        toast.success('Copied to clipboard');
    };

    const renderContent = () => {
        let parsedContent = content;

        // Try parsing JSON if string
        if (typeof content === 'string' && (content.trim().startsWith('{') || content.trim().startsWith('['))) {
            try {
                parsedContent = JSON.parse(content);
            } catch (e) {
                // Ignore
            }
        }

        if (typeof parsedContent === 'object' && parsedContent !== null) {
            // Arrays: List for readability
            if (Array.isArray(parsedContent)) {
                return (
                    <div className="bg-muted/30 rounded-md border p-4">
                        <ul className="list-disc list-inside space-y-1 text-sm text-foreground">
                            {parsedContent.map((item: any, i: number) => (
                                <li key={i}>{String(item)}</li>
                            ))}
                        </ul>
                    </div>
                );
            }

            // Object (Metadata) - Clean Description List
            return (
                <div className="border rounded-md divide-y overflow-hidden">
                    {Object.entries(parsedContent).map(([k, v]) => {
                        if (v === null || v === "" || (Array.isArray(v) && v.length === 0)) return null;

                        return (
                            <div key={k} className="grid grid-cols-[140px_1fr] md:grid-cols-[180px_1fr] bg-card">
                                <div className="px-4 py-3 bg-muted/40 border-r flex items-center">
                                    <span className="text-xs font-semibold uppercase text-muted-foreground tracking-wide">
                                        {k.replace(/_/g, ' ')}
                                    </span>
                                </div>
                                <div className="px-4 py-3 text-sm flex items-center">
                                    {Array.isArray(v) ? (
                                        <div className="flex flex-col gap-1 w-full">
                                            {v.map((item: any, i: number) => (
                                                <div key={i} className="flex items-start gap-2">
                                                    <span className="text-muted-foreground/60 select-none">•</span>
                                                    <span>{String(item)}</span>
                                                </div>
                                            ))}
                                        </div>
                                    ) : (
                                        <span className="leading-relaxed whitespace-pre-wrap">{String(v)}</span>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            );
        }

        return (
            <div className="prose prose-sm dark:prose-invert max-w-none 
                prose-headings:font-bold prose-headings:tracking-tight 
                prose-h1:text-xl prose-h1:mb-4 prose-h1:pb-2 prose-h1:border-b
                prose-h2:text-lg prose-h2:mt-6
                prose-p:leading-7 prose-p:my-3">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {String(parsedContent)}
                </ReactMarkdown>
            </div>
        );
    };

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
            <div className="w-full max-w-2xl rounded-lg bg-background p-6 shadow-xl animate-in fade-in zoom-in duration-200 flex flex-col max-h-[85vh]">
                <div className="flex items-center justify-between mb-4 flex-shrink-0">
                    <h2 className="text-xl font-semibold truncate pr-4">{title}</h2>
                    <div className="flex gap-2">
                        <Button variant="ghost" size="icon" onClick={handleCopy} title="Copy Content">
                            <Copy className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" onClick={onClose}>
                            <X className="h-4 w-4" />
                        </Button>
                    </div>
                </div>

                <div className="flex-1 overflow-auto rounded-md bg-muted p-4 text-sm">
                    {renderContent()}
                </div>

                <div className="mt-4 flex justify-end flex-shrink-0">
                    <Button onClick={onClose}>Close</Button>
                </div>
            </div>
        </div>
    );
}

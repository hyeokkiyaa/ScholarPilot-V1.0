import { Button } from '../common/Button';
import { X, Copy } from 'lucide-react';
import toast from 'react-hot-toast';

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

                <div className="flex-1 overflow-auto rounded-md bg-muted p-4 font-mono text-sm">
                    <pre className="whitespace-pre-wrap break-words">
                        {typeof content === 'object' ? JSON.stringify(content, null, 2) : String(content)}
                    </pre>
                </div>

                <div className="mt-4 flex justify-end flex-shrink-0">
                    <Button onClick={onClose}>Close</Button>
                </div>
            </div>
        </div>
    );
}

import { useState } from 'react';
import {
    flexRender,
    getCoreRowModel,
    useReactTable,
    getSortedRowModel,
    SortingState,
    createColumnHelper,
} from '@tanstack/react-table';
import { Paper, ColumnDef } from '../../types';
import { Button } from '../common/Button';
import { FileText, ExternalLink, RefreshCw, Trash2, Eye } from 'lucide-react';
import { cn } from '../../lib/utils';
import axios from 'axios';
import { useProjectStore } from '../../stores/projectStore';
import { ResultDetailModal } from './ResultDetailModal';

interface PaperTableProps {
    papers: Paper[];
    columns: ColumnDef[];
    projectId: string;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function PaperTable({ papers, columns, projectId }: PaperTableProps) {
    const [sorting, setSorting] = useState<SortingState>([]);
    const { fetchPapers, deletePaper } = useProjectStore();
    const [processingId, setProcessingId] = useState<string | null>(null);
    const [detailModal, setDetailModal] = useState<{ isOpen: boolean; title: string; content: any }>({
        isOpen: false,
        title: '',
        content: null
    });

    const handleDelete = async (paperId: string) => {
        if (!confirm('Are you sure you want to delete this paper?')) return;
        try {
            await deletePaper(paperId);
            // No need to fetchPapers manually as store updates local state
        } catch (error) {
            console.error('Failed to delete paper', error);
        }
    };

    const handleRetry = async (paperId: string) => {
        setProcessingId(paperId);
        try {
            await axios.post(`${API_URL}/api/projects/${projectId}/papers/${paperId}/retry`);
            setTimeout(() => fetchPapers(projectId), 2000);
        } catch (error) {
            console.error('Failed to retry analysis', error);
        } finally {
            setProcessingId(null);
        }
    };

    const openDetail = (title: string, content: any) => {
        setDetailModal({ isOpen: true, title, content });
    };

    const columnHelper = createColumnHelper<Paper>();

    const defaultColumns = [
        columnHelper.accessor('title', {
            header: 'Paper',
            cell: (info) => {
                const paper = info.row.original;
                return (
                    <div className="min-w-[200px] max-w-[300px]">
                        <div className="font-medium truncate" title={paper.title || 'Untitled'}>
                            {paper.title || 'Untitled'}
                        </div>
                        <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                            {paper.source_url && (
                                <a href={paper.source_url} target="_blank" rel="noreferrer" className="flex items-center hover:underline">
                                    <ExternalLink className="mr-1 h-3 w-3" />
                                    Source
                                </a>
                            )}
                            {paper.pdf_path && (
                                <span className="flex items-center">
                                    <FileText className="mr-1 h-3 w-3" />
                                    PDF
                                </span>
                            )}
                            <span className={cn(
                                "px-1.5 py-0.5 rounded-full text-[10px] uppercase font-bold",
                                paper.status === 'done' ? "bg-green-100 text-green-700" :
                                    paper.status === 'error' ? "bg-red-100 text-red-700" :
                                        paper.status === 'processing' ? "bg-blue-100 text-blue-700" :
                                            "bg-gray-100 text-gray-700"
                            )}>
                                {paper.status}
                            </span>
                        </div>
                        {paper.error_message && (
                            <div className="text-xs text-red-500 mt-1 truncate" title={paper.error_message}>
                                {paper.error_message}
                            </div>
                        )}
                    </div>
                );
            },
        }),
    ];

    const dynamicCols = columns.map((col) =>
        columnHelper.accessor(row => {
            const result = row.results?.[col.id];
            return result ? result.value : null;
        }, {
            id: col.id,
            header: col.name,
            cell: (info) => {
                const value = info.getValue();
                const paper = info.row.original;
                const result = paper.results?.[col.id];

                if (!result) return <span className="text-muted-foreground">-</span>;

                if (result.status === 'processing') {
                    return <RefreshCw className="h-4 w-4 animate-spin text-muted-foreground" />;
                }
                if (result.status === 'error') {
                    return <span className="text-red-500 text-xs" title={result.error_message || 'Error'}>Error</span>;
                }

                // Click to view details
                return (
                    <div
                        className="max-h-[100px] overflow-hidden text-sm min-w-[150px] cursor-pointer hover:bg-muted/50 p-1 rounded transition-colors group relative"
                        onClick={() => openDetail(col.name, value)}
                    >
                        <div className="line-clamp-4 whitespace-pre-wrap">
                            {typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}
                        </div>
                        {/* Hover hint */}
                        <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 bg-white/50 backdrop-blur-[1px] transition-opacity">
                            <Eye className="h-4 w-4 text-primary" />
                        </div>
                    </div>
                );
            }
        })
    );

    const actionCol = columnHelper.display({
        id: 'actions',
        header: 'Actions',
        cell: (info) => (
            <div className="flex items-center gap-1">
                <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => handleRetry(info.row.original.id)}
                    disabled={processingId === info.row.original.id}
                    title="Retry Analysis"
                >
                    <RefreshCw className={cn("h-4 w-4", processingId === info.row.original.id && "animate-spin")} />
                </Button>
                <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8 text-destructive hover:text-destructive"
                    onClick={() => handleDelete(info.row.original.id)}
                    title="Delete Paper"
                >
                    <Trash2 className="h-4 w-4" />
                </Button>
            </div>
        )
    });

    const tableColumns = [...defaultColumns, ...dynamicCols, actionCol];

    const table = useReactTable({
        data: papers,
        columns: tableColumns,
        getCoreRowModel: getCoreRowModel(),
        onSortingChange: setSorting,
        getSortedRowModel: getSortedRowModel(),
        state: {
            sorting,
        },
    });

    return (
        <>
            <div className="rounded-md border">
                <div className="relative w-full overflow-auto">
                    <table className="w-full caption-bottom text-sm text-left">
                        <thead className="[&_tr]:border-b">
                            {table.getHeaderGroups().map((headerGroup) => (
                                <tr key={headerGroup.id} className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                                    {headerGroup.headers.map((header) => (
                                        <th key={header.id} className="h-12 px-4 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0">
                                            {header.isPlaceholder
                                                ? null
                                                : flexRender(
                                                    header.column.columnDef.header,
                                                    header.getContext()
                                                )}
                                        </th>
                                    ))}
                                </tr>
                            ))}
                        </thead>
                        <tbody className="[&_tr:last-child]:border-0">
                            {table.getRowModel().rows.length > 0 ? (
                                table.getRowModel().rows.map((row) => (
                                    <tr
                                        key={row.id}
                                        className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted"
                                    >
                                        {row.getVisibleCells().map((cell) => (
                                            <td key={cell.id} className="p-4 align-top [&:has([role=checkbox])]:pr-0">
                                                {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                            </td>
                                        ))}
                                    </tr>
                                ))
                            ) : (
                                <tr>
                                    <td colSpan={tableColumns.length} className="h-24 text-center">
                                        No results.
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <ResultDetailModal
                isOpen={detailModal.isOpen}
                title={detailModal.title}
                content={detailModal.content}
                onClose={() => setDetailModal(prev => ({ ...prev, isOpen: false }))}
            />
        </>
    );
}

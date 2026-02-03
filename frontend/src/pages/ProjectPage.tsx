import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Sidebar, Header } from '../components/layout/Layout';
import { useProjectStore } from '../stores/projectStore';
import { Button } from '../components/common/Button';
import { Upload, Play, Settings2 } from 'lucide-react';
import { PaperTable } from '../components/papers/PaperTable';
import { AddPaperModal } from '../components/papers/AddPaperModal';
import { ColumnManagerModal } from '../components/columns/ColumnManagerModal';
import axios from 'axios';
import toast from 'react-hot-toast';
import { useTranslation } from 'react-i18next';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ProjectPage() {
    const { t } = useTranslation();
    const { id } = useParams<{ id: string }>();
    const { currentProject, papers, columns, fetchProjectDetails, fetchPapers, isLoading } = useProjectStore();
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isColumnModalOpen, setIsColumnModalOpen] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [isExporting, setIsExporting] = useState(false);

    useEffect(() => {
        if (id) {
            fetchProjectDetails(id);
            const interval = setInterval(() => {
                const hasProcessing = useProjectStore.getState().papers.some(p => p.status === 'processing');
                if (hasProcessing) {
                    fetchPapers(id);
                }
            }, 5000);
            return () => clearInterval(interval);
        }
    }, [id, fetchProjectDetails, fetchPapers]);

    const handleAnalyzeAll = async () => {
        if (!id) return;
        setIsAnalyzing(true);
        try {
            await axios.post(`${API_URL}/api/analyze`, { project_id: id });
            toast.success(t('project.analysisStarted'));
            fetchPapers(id);
        } catch (error) {
            toast.error(t('project.analysisFailed'));
        } finally {
            setIsAnalyzing(false);
        }
    };

    const handleExport = async (type: 'excel' | 'csv' | 'markdown' | 'notion') => {
        if (!id) return;

        if (type === 'notion') {
            setIsExporting(true);
            try {
                const res = await axios.post(`${API_URL}/api/projects/${id}/export/notion`);
                toast.success(t('project.notionExportSuccess', { count: res.data.exported }));
            } catch (error) {
                toast.error(t('project.notionExportFail'));
            } finally {
                setIsExporting(false);
            }
            return;
        }

        // For file downloads, we can just open in new window or use fetch blob
        // Using window.open is simplest for GET downloads
        window.open(`${API_URL}/api/projects/${id}/export/${type}`);
    };

    if (isLoading && !currentProject) {
        return <div className="flex h-screen items-center justify-center">{t('project.loading')}</div>;
    }

    if (!currentProject) {
        return <div className="flex h-screen items-center justify-center">{t('project.notFound')}</div>;
    }

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col w-0">
                <Header
                    title={currentProject.name}
                    actions={
                        <div className="flex gap-2">
                            <div className="flex items-center gap-1 mr-2 border-r pr-2">
                                <Button variant="ghost" size="sm" onClick={() => handleExport('excel')} title={t('project.exportExcel')}>
                                    XLSX
                                </Button>
                                <Button variant="ghost" size="sm" onClick={() => handleExport('csv')} title={t('project.exportCSV')}>
                                    CSV
                                </Button>
                                <Button variant="ghost" size="sm" onClick={() => handleExport('markdown')} title={t('project.exportMarkdown')}>
                                    MD
                                </Button>
                                <Button variant="ghost" size="sm" onClick={() => handleExport('notion')} disabled={isExporting} title={t('project.exportNotion')}>
                                    Notion
                                </Button>
                            </div>

                            <Button variant="outline" onClick={() => setIsColumnModalOpen(true)}>
                                <Settings2 className="mr-2 h-4 w-4" />
                                {t('project.columnsButton')}
                            </Button>
                            <Button variant="secondary" onClick={handleAnalyzeAll} disabled={isAnalyzing}>
                                <Play className="mr-2 h-4 w-4" />
                                {t('project.runAnalysisButton')}
                            </Button>
                            <Button onClick={() => setIsAddModalOpen(true)}>
                                <Upload className="mr-2 h-4 w-4" />
                                {t('project.addPaperButton')}
                            </Button>
                        </div>
                    }
                />
                <main className="flex-1 p-6 overflow-auto">
                    <PaperTable
                        papers={papers}
                        columns={columns}
                        projectId={id!}
                    />
                </main>
            </div>

            <AddPaperModal
                projectId={id!}
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
            />

            <ColumnManagerModal
                projectId={id!}
                isOpen={isColumnModalOpen}
                onClose={() => setIsColumnModalOpen(false)}
            />
        </div>
    );
}

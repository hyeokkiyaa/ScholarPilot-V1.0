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

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function ProjectPage() {
    const { id } = useParams<{ id: string }>();
    const { currentProject, papers, columns, fetchProjectDetails, fetchPapers, isLoading } = useProjectStore();
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isColumnModalOpen, setIsColumnModalOpen] = useState(false);
    const [isAnalyzing, setIsAnalyzing] = useState(false);

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
            toast.success('Analysis started');
            fetchPapers(id);
        } catch (error) {
            toast.error('Failed to start analysis');
        } finally {
            setIsAnalyzing(false);
        }
    };

    if (isLoading && !currentProject) {
        return <div className="flex h-screen items-center justify-center">Loading...</div>;
    }

    if (!currentProject) {
        return <div className="flex h-screen items-center justify-center">Project not found</div>;
    }

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col w-0">
                <Header
                    title={currentProject.name}
                    actions={
                        <div className="flex gap-2">
                            <Button variant="outline" onClick={() => setIsColumnModalOpen(true)}>
                                <Settings2 className="mr-2 h-4 w-4" />
                                Columns
                            </Button>
                            <Button variant="secondary" onClick={handleAnalyzeAll} disabled={isAnalyzing}>
                                <Play className="mr-2 h-4 w-4" />
                                Run Analysis
                            </Button>
                            <Button onClick={() => setIsAddModalOpen(true)}>
                                <Upload className="mr-2 h-4 w-4" />
                                Add Paper
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

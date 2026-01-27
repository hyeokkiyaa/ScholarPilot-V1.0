import { useEffect, useState } from 'react';
import { Sidebar, Header } from '../components/layout/Layout'; // Fix import path based on previous step
import { useProjectStore } from '../stores/projectStore';
import { Button } from '../components/common/Button';
import { Plus } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Input } from '../components/common/Input';
import { Select } from '../components/common/Select';
// Basic modal implementation inline for now or separate component later
import { Project } from '../types';

export default function HomePage() {
    const { projects, fetchProjects, createProject, isLoading, templates, fetchTemplates } = useProjectStore();
    const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
    const [newProjectName, setNewProjectName] = useState('');
    const [template, setTemplate] = useState('basic');

    useEffect(() => {
        fetchProjects();
        fetchTemplates();
    }, [fetchProjects, fetchTemplates]);

    const handleCreate = async () => {
        if (!newProjectName) return;
        await createProject(newProjectName, template);
        setIsCreateModalOpen(false);
        setNewProjectName('');
    };

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <Header title="Projects" />
                <main className="flex-1 p-6">
                    <div className="mb-6 flex items-center justify-between">
                        <h2 className="text-2xl font-bold tracking-tight">Your Projects</h2>
                        <Button onClick={() => setIsCreateModalOpen(true)}>
                            <Plus className="mr-2 h-4 w-4" />
                            New Project
                        </Button>
                    </div>

                    {isLoading && projects.length === 0 ? (
                        <div>Loading...</div>
                    ) : (
                        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                            {projects.map((project: Project) => (
                                <Link
                                    key={project.id}
                                    to={`/project/${project.id}`}
                                    className="group relative rounded-lg border p-6 hover:border-foreground/50 transition-colors"
                                >
                                    <h3 className="font-semibold">{project.name}</h3>
                                    <p className="text-sm text-muted-foreground mt-2">
                                        Template: {project.template || 'Custom'}
                                    </p>
                                    <div className="mt-4 text-xs text-muted-foreground">
                                        Last updated: {new Date(project.updated_at).toLocaleDateString()}
                                    </div>
                                </Link>
                            ))}

                            {projects.length === 0 && (
                                <div className="col-span-full text-center py-12 text-muted-foreground">
                                    No projects yet. Create one to get started.
                                </div>
                            )}
                        </div>
                    )}
                </main>
            </div>

            {/* Simple Modal */}
            {isCreateModalOpen && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
                    <div className="w-full max-w-md rounded-lg bg-background p-6 shadow-lg">
                        <h2 className="mb-4 text-lg font-semibold">Create New Project</h2>
                        <div className="space-y-4">
                            <Input
                                label="Project Name"
                                value={newProjectName}
                                onChange={(e) => setNewProjectName(e.target.value)}
                            />
                            <div className="space-y-2">
                                <label className="text-sm font-medium">Template</label>
                                <select
                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                                    value={template}
                                    onChange={(e) => setTemplate(e.target.value)}
                                >
                                    {templates.map(t => (
                                        <option key={t.id} value={t.id}>{t.name} ({t.description})</option>
                                    ))}
                                </select>
                            </div>
                            <div className="flex justify-end gap-2 pt-4">
                                <Button variant="ghost" onClick={() => setIsCreateModalOpen(false)}>
                                    Cancel
                                </Button>
                                <Button onClick={handleCreate} disabled={!newProjectName}>
                                    Create
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}

import { create } from 'zustand';
import axios from 'axios';
import { Project, ColumnDef, Paper } from '../types';

interface ProjectState {
    projects: Project[];
    currentProject: Project | null;
    columns: ColumnDef[];
    papers: Paper[];
    templates: { id: string; name: string; description: string }[];
    isLoading: boolean;
    error: string | null;

    fetchProjects: () => Promise<void>;
    createProject: (name: string, template: string) => Promise<Project>;
    fetchProjectDetails: (id: string) => Promise<void>;
    fetchTemplates: () => Promise<void>;

    // Column actions
    fetchColumns: (projectId: string) => Promise<void>;
    createColumn: (projectId: string, column: Partial<ColumnDef>) => Promise<void>;

    // Paper actions
    fetchPapers: (projectId: string) => Promise<void>;
    addPaper: (projectId: string, file: File | null, input: string) => Promise<void>;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useProjectStore = create<ProjectState>((set, get) => ({
    projects: [],
    currentProject: null,
    columns: [],
    papers: [],
    templates: [],
    isLoading: false,
    error: null,

    fetchProjects: async () => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.get(`${API_URL}/api/projects`);
            set({ projects: response.data, isLoading: false });
        } catch (error) {
            set({ error: 'Failed to fetch projects', isLoading: false });
        }
    },

    fetchTemplates: async () => {
        try {
            const response = await axios.get(`${API_URL}/api/projects/templates`);
            set({ templates: response.data });
        } catch (error) {
            console.error('Failed to fetch templates:', error);
        }
    },

    createProject: async (name, template) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.post(`${API_URL}/api/projects`, { name, template });
            const newProject = response.data;
            set((state) => ({
                projects: [...state.projects, newProject],
                isLoading: false
            }));
            return newProject;
        } catch (error) {
            set({ error: 'Failed to create project', isLoading: false });
            throw error;
        }
    },

    fetchProjectDetails: async (id) => {
        set({ isLoading: true, error: null });
        try {
            const response = await axios.get(`${API_URL}/api/projects/${id}`);
            set({ currentProject: response.data });

            // Parallel fetch for columns and papers
            await Promise.all([
                get().fetchColumns(id),
                get().fetchPapers(id)
            ]);

            set({ isLoading: false });
        } catch (error) {
            set({ error: 'Failed to load project details', isLoading: false });
        }
    },

    fetchColumns: async (projectId) => {
        try {
            const response = await axios.get(`${API_URL}/api/projects/${projectId}/columns`);
            set({ columns: response.data });
        } catch (error) {
            console.error('Failed to fetch columns');
        }
    },

    createColumn: async (projectId, column) => {
        try {
            const response = await axios.post(`${API_URL}/api/projects/${projectId}/columns`, column);
            set((state) => ({ columns: [...state.columns, response.data] }));
        } catch (error) {
            console.error('Failed to create column');
        }
    },

    fetchPapers: async (projectId) => {
        try {
            const response = await axios.get(`${API_URL}/api/projects/${projectId}/papers`);
            set({ papers: response.data });
        } catch (error) {
            console.error('Failed to fetch papers');
        }
    },

    addPaper: async (projectId, file, input) => {
        try {
            const formData = new FormData();
            if (file) {
                formData.append('file', file);
            }
            if (input) {
                // Assuming backend schema handles this input structure
                formData.append('input_value', input);
            }

            await axios.post(`${API_URL}/api/projects/${projectId}/papers`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            await get().fetchPapers(projectId); // Refresh list
        } catch (error) {
            console.error('Failed to add paper');
            throw error;
        }
    }

}));

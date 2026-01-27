import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import axios from 'axios';
import { Settings } from '../types';

interface SettingsState extends Settings {
    isLoading: boolean;
    updateSettings: (settings: Partial<Settings>) => void;
    fetchSettings: () => Promise<void>;
    saveSettings: () => Promise<void>;
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const useSettingsStore = create<SettingsState>()(
    persist(
        (set, get) => ({
            model_provider: 'claude',
            api_key: '',
            notion_api_key: null,
            notion_database_id: null,
            notion_enabled: false,
            google_sheets_enabled: false,
            onboarding_completed: false, // Default to false to show onboarding first
            isLoading: false,

            updateSettings: (newSettings) => set((state) => ({ ...state, ...newSettings })),

            fetchSettings: async () => {
                set({ isLoading: true });
                try {
                    // Sync with backend if needed, but for now specific local settings trigger onboarding
                    // const response = await axios.get(`${API_URL}/api/settings`);
                    // set({ ...response.data });
                } catch (error) {
                    console.error('Failed to fetch settings:', error);
                } finally {
                    set({ isLoading: false });
                }
            },

            saveSettings: async () => {
                const state = get();
                set({ isLoading: true });
                try {
                    // Save to backend
                    await axios.put(`${API_URL}/api/settings`, {
                        settings: [
                            { key: 'model_provider', value: state.model_provider },
                            { key: 'api_key', value: state.api_key },
                            { key: 'onboarding_completed', value: String(state.onboarding_completed) },
                            { key: 'notion_api_key', value: state.notion_api_key },
                            { key: 'notion_database_id', value: state.notion_database_id }
                        ]
                    });
                } catch (error) {
                    console.error('Failed to save settings:', error);
                } finally {
                    set({ isLoading: false });
                }
            },
        }),
        {
            name: 'scholarpilot-settings',
        }
    )
);

import { useEffect, useState } from 'react';
import { Sidebar, Header } from '../components/layout/Layout';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { useSettingsStore } from '../stores/settingsStore';
import toast from 'react-hot-toast';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function SettingsPage() {
    const { settings, fetchSettings, updateSettings, saveSettings, isLoading } = useSettingsStore();

    // Local state for Notion inputs to control controlled inputs
    const [notionKey, setNotionKey] = useState('');
    const [notionDbId, setNotionDbId] = useState('');
    const [isTesting, setIsTesting] = useState(false);

    useEffect(() => {
        fetchSettings().then(() => {
            // Sync store to local state
            const currentSettings = useSettingsStore.getState().settings;
            setNotionKey(currentSettings.notion_api_key || '');
            setNotionDbId(currentSettings.notion_database_id || '');
        });
    }, [fetchSettings]);

    const handleSave = async () => {
        updateSettings({
            notion_api_key: notionKey,
            notion_database_id: notionDbId
        });
        await saveSettings();
        toast.success("Settings saved");
    };

    const handleTestNotion = async () => {
        setIsTesting(true);
        try {
            await axios.post(`${API_URL}/api/export/test-connection/notion`, {
                api_key: notionKey,
                database_id: notionDbId
            });
            toast.success("Notion connection successful!");
        } catch (error) {
            toast.error("Notion connection failed. Check credentials.");
        } finally {
            setIsTesting(false);
        }
    };

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <Header title="Settings" />
                <main className="flex-1 p-6 max-w-2xl">
                    <div className="space-y-8">

                        <div className="space-y-4 border p-4 rounded-md">
                            <h2 className="text-lg font-semibold">Notion Integration</h2>
                            <p className="text-sm text-muted-foreground">
                                Configure Notion to export your analysis results directly to a Notion Database.
                            </p>

                            <Input
                                label="Notion API Key (Internal Integration Token)"
                                type="password"
                                placeholder="secret_..."
                                value={notionKey}
                                onChange={(e) => setNotionKey(e.target.value)}
                            />

                            <Input
                                label="Notion Database ID"
                                placeholder="32 character ID"
                                value={notionDbId}
                                onChange={(e) => setNotionDbId(e.target.value)}
                            />

                            <div className="flex gap-2">
                                <Button variant="outline" onClick={handleTestNotion} isLoading={isTesting} disabled={!notionKey || !notionDbId}>
                                    Test Connection
                                </Button>
                            </div>
                        </div>

                        <div className="flex justify-end">
                            <Button onClick={handleSave}>
                                Save Settings
                            </Button>
                        </div>

                    </div>
                </main>
            </div>
        </div>
    );
}

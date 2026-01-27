import { useEffect, useState } from 'react';
import { Sidebar, Header } from '../components/layout/Layout';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { useSettingsStore } from '../stores/settingsStore';
import toast from 'react-hot-toast';
import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function SettingsPage() {
    const { fetchSettings, updateSettings, saveSettings } = useSettingsStore();

    // Local state
    const [notionKey, setNotionKey] = useState('');
    const [notionDbId, setNotionDbId] = useState('');
    const [modelProvider, setModelProvider] = useState('claude');
    const [apiKey, setApiKey] = useState('');
    const [isTesting, setIsTesting] = useState(false);

    // Masking state
    const [isEditingKey, setIsEditingKey] = useState(false);

    useEffect(() => {
        fetchSettings().then(() => {
            // Sync store to local state
            const currentSettings = useSettingsStore.getState();
            setNotionKey(currentSettings.notion_api_key || '');
            setNotionDbId(currentSettings.notion_database_id || '');
            setModelProvider(currentSettings.model_provider || 'claude');
            setApiKey(currentSettings.api_key || '');
        });
    }, [fetchSettings]);

    const handleSave = async () => {
        updateSettings({
            notion_api_key: notionKey,
            notion_database_id: notionDbId,
            model_provider: modelProvider as any,
            api_key: apiKey
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

    const getMaskedKey = (key: string) => {
        if (!key) return '';
        if (key.length <= 8) return '********';
        return `${key.substring(0, 6)}...******`;
    };

    return (
        <div className="flex min-h-screen">
            <Sidebar />
            <div className="flex-1 flex flex-col">
                <Header title="Settings" />
                <main className="flex-1 p-6 max-w-2xl">
                    <div className="space-y-8">

                        {/* Model Configuration */}
                        <div className="space-y-4 border p-4 rounded-md">
                            <h2 className="text-lg font-semibold">Model Configuration</h2>
                            <p className="text-sm text-muted-foreground">
                                Select your LLM provider and enter your API key.
                            </p>

                            <div className="space-y-2">
                                <label className="text-sm font-medium">Model Provider</label>
                                <select
                                    className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                                    value={modelProvider}
                                    onChange={(e) => setModelProvider(e.target.value)}
                                >
                                    <option value="claude">Claude (Anthropic)</option>
                                    <option value="openai">OpenAI (GPT-4)</option>
                                    <option value="gemini">Gemini (Google)</option>
                                    <option value="grok">Grok (xAI)</option>
                                    <option value="solar">Solar (Upstage)</option>
                                </select>
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium">API Key</label>
                                <div className="relative">
                                    <Input
                                        type={isEditingKey ? "text" : "text"}
                                        value={isEditingKey ? apiKey : getMaskedKey(apiKey)}
                                        onChange={(e) => setApiKey(e.target.value)}
                                        onFocus={() => setIsEditingKey(true)}
                                        onBlur={() => setIsEditingKey(false)}
                                        placeholder="sk-..."
                                        className={!isEditingKey && apiKey ? "text-muted-foreground" : ""}
                                    />
                                    {/* Helper text or clear button could go here */}
                                </div>
                            </div>
                        </div>

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

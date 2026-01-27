import { useState } from 'react';
import { useSettingsStore } from '../stores/settingsStore';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { Select } from '../components/common/Select';
import { useNavigate } from 'react-router-dom';

export default function OnboardingPage() {
    const { updateSettings, saveSettings } = useSettingsStore();
    const navigate = useNavigate();
    const [step, setStep] = useState(0);
    const [apiKey, setApiKey] = useState('');
    const [provider, setProvider] = useState('claude');

    const handleComplete = async () => {
        if (!apiKey) {
            alert("Please enter an API Key");
            return;
        }

        try {
            updateSettings({
                api_key: apiKey,
                // @ts-ignore
                model_provider: provider,
                onboarding_completed: true
            });
            await saveSettings();
            navigate('/');
        } catch (error) {
            console.error("Onboarding error:", error);
            alert("Failed to save settings. Check console for details.");
        }
    };

    return (
        <div className="flex min-h-screen items-center justify-center bg-gray-50 dark:bg-gray-900">
            <div className="w-full max-w-md space-y-8 rounded-lg border bg-card p-8 shadow-lg">
                <div className="text-center">
                    <h2 className="text-3xl font-bold tracking-tight">Welcome to ScholarPilot</h2>
                    <p className="mt-2 text-sm text-muted-foreground">
                        Your AI-powered research assistant. Let's get set up.
                    </p>
                </div>

                <div className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Select Model Provider</label>
                        <select
                            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
                            value={provider}
                            onChange={(e) => setProvider(e.target.value)}
                        >
                            <option value="claude">Anthropic Claude</option>
                            <option value="openai">OpenAI GPT-4</option>
                            <option value="gemini">Google Gemini</option>
                            <option value="grok">Grok</option>
                            <option value="solar">Upstage Solar</option>
                        </select>
                    </div>

                    <Input
                        label="API Key"
                        type="password"
                        placeholder="sk-..."
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                    />

                    <Button onClick={handleComplete} className="w-full">
                        Get Started
                    </Button>
                </div>
            </div>
        </div>
    );
}

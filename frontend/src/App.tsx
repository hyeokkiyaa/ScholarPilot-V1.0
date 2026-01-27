import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useSettingsStore } from './stores/settingsStore';
import HomePage from './pages/HomePage';
import ProjectPage from './pages/ProjectPage';
import OnboardingPage from './pages/OnboardingPage';

// Placeholder Pages (will implement next)
const PlaceholderPage = ({ title }: { title: string }) => (
    <div className="flex items-center justify-center min-h-screen">
        <h1 className="text-2xl font-bold">{title} Under Construction</h1>
    </div>
);

function App() {
    const { onboardingCompleted } = useSettingsStore();

    return (
        <BrowserRouter>
            <Toaster position="top-right" />
            <Routes>
                {!onboardingCompleted ? (
                    <>
                        <Route path="/onboarding" element={<OnboardingPage />} />
                        <Route path="*" element={<Navigate to="/onboarding" replace />} />
                    </>
                ) : (
                    <>
                        <Route path="/" element={<HomePage />} />
                        <Route path="/project/:id" element={<ProjectPage />} />
                        <Route path="*" element={<Navigate to="/" replace />} />
                    </>
                )}
            </Routes>
        </BrowserRouter>
    );
}

export default App;

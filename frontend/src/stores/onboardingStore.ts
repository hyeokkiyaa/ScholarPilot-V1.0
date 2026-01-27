import { create } from 'zustand';

interface OnboardingState {
    currentStep: number;
    nextStep: () => void;
    prevStep: () => void;
    setStep: (step: number) => void;
}

export const useOnboardingStore = create<OnboardingState>((set) => ({
    currentStep: 0,
    nextStep: () => set((state) => ({ currentStep: state.currentStep + 1 })),
    prevStep: () => set((state) => ({ currentStep: Math.max(0, state.currentStep - 1) })),
    setStep: (step) => set({ currentStep: step }),
}));

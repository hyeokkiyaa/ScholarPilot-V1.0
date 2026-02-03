import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';

export function LanguageSwitcher() {
    const { i18n } = useTranslation();

    const changeLanguage = (lng: string) => {
        i18n.changeLanguage(lng);
    };

    return (
        <div className="flex items-center gap-1">
            <Button
                variant="ghost"
                size="sm"
                onClick={() => changeLanguage(i18n.language === 'en' ? 'ko' : 'en')}
                className="w-12 font-semibold"
            >
                {i18n.language === 'en' ? 'KO' : 'EN'}
            </Button>
        </div>
    );
}

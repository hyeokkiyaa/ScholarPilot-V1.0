import { ReactNode, useState } from 'react';
import { cn } from '../../lib/utils';
import { LayoutDashboard, Settings as SettingsIcon, Menu } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { MobileSidebar } from './MobileSidebar';
import { Button } from '../common/Button';
import { LanguageSwitcher } from '../common/LanguageSwitcher';
import { useTranslation } from 'react-i18next';

interface SidebarProps {
    className?: string;
}

export function Sidebar({ className }: SidebarProps) {
    const { t } = useTranslation();

    const links = [
        { href: '/', icon: LayoutDashboard, label: t('sidebar.projects') },
        { href: '/settings', icon: SettingsIcon, label: t('sidebar.settings') },
    ];

    return (
        <div className={cn("hidden lg:block pb-12 w-64 border-r min-h-screen bg-card", className)}>
            <div className="space-y-4 py-4">
                <div className="px-3 py-2">
                    <h2 className="mb-2 px-4 text-lg font-semibold tracking-tight">
                        ScholarPilot
                    </h2>
                    <div className="space-y-1">
                        {links.map((link) => (
                            <NavLink
                                key={link.href}
                                to={link.href}
                                className={({ isActive }) =>
                                    cn(
                                        "flex items-center rounded-md px-3 py-2 text-sm font-medium hover:bg-accent hover:text-accent-foreground",
                                        isActive ? "bg-accent text-accent-foreground" : "transparent"
                                    )
                                }
                            >
                                <link.icon className="mr-2 h-4 w-4" />
                                {link.label}
                            </NavLink>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

interface HeaderProps {
    title?: string;
    actions?: ReactNode;
}

export function Header({ title, actions }: HeaderProps) {
    const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

    return (
        <>
            <MobileSidebar open={mobileMenuOpen} setOpen={setMobileMenuOpen} />
            <header className="flex h-14 items-center gap-4 border-b bg-background px-6">
                <Button
                    variant="ghost"
                    className="-ml-2 px-2 hover:bg-transparent lg:hidden"
                    onClick={() => setMobileMenuOpen(true)}
                >
                    <Menu className="h-6 w-6" />
                </Button>
                <h1 className="text-lg font-semibold">{title}</h1>
                <div className="ml-auto flex items-center gap-2">
                    <LanguageSwitcher />
                    <div className="h-4 w-px bg-border mx-2" />
                    {actions}
                </div>
            </header>
        </>
    );
}

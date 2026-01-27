import React, { ReactNode } from 'react';
import { cn } from '../../lib/utils';
import { LayoutDashboard, Settings as SettingsIcon, Database, BookOpen, LogOut } from 'lucide-react';
import { NavLink } from 'react-router-dom';

interface SidebarProps {
    className?: string;
}

export function Sidebar({ className }: SidebarProps) {
    const links = [
        { href: '/', icon: LayoutDashboard, label: 'Projects' },
        // { href: '/templates', icon: Database, label: 'Templates' },
        // { href: '/settings', icon: SettingsIcon, label: 'Settings' },
    ];

    return (
        <div className={cn("pb-12 w-64 border-r min-h-screen bg-card", className)}>
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
    return (
        <header className="flex h-14 items-center gap-4 border-b bg-background px-6">
            <h1 className="text-lg font-semibold">{title}</h1>
            <div className="ml-auto flex items-center gap-2">
                {actions}
            </div>
        </header>
    );
}

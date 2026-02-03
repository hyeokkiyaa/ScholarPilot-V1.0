import { Fragment } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { NavLink } from 'react-router-dom';
import { X, LayoutDashboard, Settings as SettingsIcon } from 'lucide-react'; // Import icons directly for now
import { cn } from '../../lib/utils';

interface MobileSidebarProps {
    open: boolean;
    setOpen: (open: boolean) => void;
}

// Duplicating links temporarily, will refactor to shared constant in next step
const links = [
    { href: '/', icon: LayoutDashboard, label: 'Projects' },
    { href: '/settings', icon: SettingsIcon, label: 'Settings' },
];

export function MobileSidebar({ open, setOpen }: MobileSidebarProps) {
    return (
        <Transition.Root show={open} as={Fragment}>
            <Dialog as="div" className="relative z-50 lg:hidden" onClose={setOpen}>
                <Transition.Child
                    as={Fragment}
                    enter="transition-opacity ease-linear duration-300"
                    enterFrom="opacity-0"
                    enterTo="opacity-100"
                    leave="transition-opacity ease-linear duration-300"
                    leaveFrom="opacity-100"
                    leaveTo="opacity-0"
                >
                    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm" />
                </Transition.Child>

                <div className="fixed inset-0 flex">
                    <Transition.Child
                        as={Fragment}
                        enter="transition ease-in-out duration-300 transform"
                        enterFrom="-translate-x-full"
                        enterTo="translate-x-0"
                        leave="transition ease-in-out duration-300 transform"
                        leaveFrom="translate-x-0"
                        leaveTo="-translate-x-full"
                    >
                        <Dialog.Panel className="relative mr-16 flex w-full max-w-xs flex-1">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-in-out duration-300"
                                enterFrom="opacity-0"
                                enterTo="opacity-100"
                                leave="ease-in-out duration-300"
                                leaveFrom="opacity-100"
                                leaveTo="opacity-0"
                            >
                                <div className="absolute left-full top-0 flex w-16 justify-center pt-5">
                                    <button
                                        type="button"
                                        className="-m-2.5 p-2.5"
                                        onClick={() => setOpen(false)}
                                    >
                                        <span className="sr-only">Close sidebar</span>
                                        <X className="h-6 w-6 text-foreground" aria-hidden="true" />
                                    </button>
                                </div>
                            </Transition.Child>

                            {/* Sidebar Content Matches Desktop Sidebar */}
                            <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-card px-6 pb-4 border-r">
                                <div className="flex h-16 shrink-0 items-center">
                                    <h2 className="text-lg font-semibold tracking-tight">
                                        ScholarPilot
                                    </h2>
                                </div>
                                <nav className="flex flex-1 flex-col">
                                    <ul role="list" className="flex flex-1 flex-col gap-y-7">
                                        <li>
                                            <ul role="list" className="-mx-2 space-y-1">
                                                {links.map((link) => (
                                                    <li key={link.href}>
                                                        <NavLink
                                                            to={link.href}
                                                            onClick={() => setOpen(false)}
                                                            className={({ isActive }) =>
                                                                cn(
                                                                    "group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-medium hover:bg-accent hover:text-accent-foreground",
                                                                    isActive ? "bg-accent text-accent-foreground" : "text-muted-foreground"
                                                                )
                                                            }
                                                        >
                                                            <link.icon className="h-6 w-6 shrink-0" aria-hidden="true" />
                                                            {link.label}
                                                        </NavLink>
                                                    </li>
                                                ))}
                                            </ul>
                                        </li>
                                    </ul>
                                </nav>
                            </div>
                        </Dialog.Panel>
                    </Transition.Child>
                </div>
            </Dialog>
        </Transition.Root>
    );
}

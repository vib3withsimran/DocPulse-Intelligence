'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function PageLayout({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  const getLinkClass = (path: string) => {
    const isActive = pathname === path;
    if (isActive) {
      return 'flex items-center gap-3.5 px-4 py-3 rounded-xl text-primary font-bold bg-primary/10 border-l-2 border-primary shadow-sm transition-all duration-200';
    }
    return 'flex items-center gap-3.5 px-4 py-3 rounded-xl text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface transition-all duration-200';
  };

  return (
    <div className="min-h-screen bg-background text-on-background">
      {/* SideNavBar */}
      <aside className="h-screen w-64 flex flex-col fixed left-0 top-0 bg-surface-container dark:bg-surface-container z-[60] border-r border-outline-variant/20 shadow-xl">
        <div className="flex flex-col h-full py-6 px-4">
          <div className="mb-8 px-2">
            <Link href="/" className="flex items-center gap-3 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-primary to-primary-container flex items-center justify-center flex-shrink-0 shadow-md group-hover:scale-105 transition-transform duration-300">
                <span className="material-symbols-outlined text-on-primary-container text-2xl font-bold" style={{ fontVariationSettings: "'FILL' 1" }}>
                  dataset
                </span>
              </div>
              <div className="min-w-0">
                <div className="flex items-center gap-1.5">
                  <span className="text-base font-extrabold text-on-surface tracking-tight group-hover:text-primary transition-colors">DocPulse</span>
                </div>
                <div className="flex items-center gap-1.5 -mt-0.5">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-primary">Intelligence</span>
                  <span className="text-[9px] bg-primary/10 border border-primary/25 text-primary px-1.5 py-0.5 rounded font-mono font-medium scale-90 origin-left">ENT</span>
                </div>
              </div>
            </Link>
          </div>
          <nav className="flex-1 space-y-1.5">
            <Link href="/" className={getLinkClass('/')}>
              <span className="material-symbols-outlined text-[22px]">dashboard</span>
              <span className="text-sm font-medium">Dashboard</span>
            </Link>
            <Link href="/upload" className={getLinkClass('/upload')}>
              <span className="material-symbols-outlined text-[22px]">cloud_upload</span>
              <span className="text-sm font-medium">Upload</span>
            </Link>
            <Link href="/chat" className={getLinkClass('/chat')}>
              <span className="material-symbols-outlined text-[22px]">chat</span>
              <span className="text-sm font-medium">Chat</span>
            </Link>
            <a href="#" className="flex items-center gap-3.5 px-4 py-3 rounded-xl text-on-surface-variant hover:bg-surface-container-highest hover:text-on-surface transition-all duration-200">
              <span className="material-symbols-outlined text-[22px]">settings</span>
              <span className="text-sm font-medium">Settings</span>
            </a>
          </nav>
          <div className="mt-auto">
            <Link href="/upload" className="w-full bg-primary-container text-on-primary-container py-3 rounded-xl font-bold flex items-center justify-center gap-2 shadow-lg shadow-primary-container/10 hover:shadow-primary-container/20 hover:brightness-110 active:scale-98 transition-all duration-200">
              <span className="material-symbols-outlined text-lg">add</span>
              <span className="text-sm">New Extraction</span>
            </Link>
          </div>
        </div>
      </aside>

      {/* TopAppBar */}
      <header className="h-16 fixed top-0 right-0 left-64 z-50 bg-surface/70 backdrop-blur-xl border-b border-outline-variant/20 shadow-sm flex justify-between items-center px-8">
        <div className="flex items-center gap-4 flex-1 max-w-xl">
          <div className="relative w-full group">
            <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant group-focus-within:text-primary transition-colors">search</span>
            <input
              type="text"
              placeholder="Search documents..."
              className="w-full bg-surface-container-low border border-outline-variant/60 rounded-full py-2 pl-11 pr-4 focus:ring-2 focus:ring-primary/45 focus:border-primary transition-all outline-none text-sm text-on-surface placeholder:text-on-surface-variant/50"
            />
          </div>
        </div>
        <div className="flex items-center gap-6">
          <button className="w-10 h-10 rounded-xl hover:bg-surface-container-highest text-on-surface-variant hover:text-primary transition-all flex items-center justify-center relative" title="Notifications">
            <span className="material-symbols-outlined">notifications</span>
            <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-error rounded-full"></span>
          </button>
          <button className="w-10 h-10 rounded-xl hover:bg-surface-container-highest text-on-surface-variant hover:text-primary transition-all flex items-center justify-center" title="Help">
            <span className="material-symbols-outlined">help</span>
          </button>
          <div className="h-8 w-[1px] bg-outline-variant/30"></div>
          <div className="flex items-center gap-3 cursor-pointer group active:opacity-80">
            <div className="text-right hidden sm:block">
              <p className="text-sm font-bold text-on-surface group-hover:text-primary transition-colors">Alex Rivera</p>
              <p className="text-[10px] text-on-surface-variant/85 font-semibold uppercase tracking-wider">Admin</p>
            </div>
            <img
              alt="User profile"
              className="w-10 h-10 rounded-xl border border-primary/20 object-cover shadow-md group-hover:border-primary/40 transition-colors"
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuBIJ9-Gkdq2AFGcF19zjLT6nVWWKeNU2Mv051p6FqtFc22fPMYvqU8yZgNsjbpoxViJpo1vtLHQ1ViITtH3SDi_0XY1nBpUCxOc9o9VaiWcOkIeSi19v9qd_Cr9qmn49fxHnGWcBxZ0VOQXT43ly1gXVXRvlFR8-5BMs1OwNIilO7iACFC9upQ5inkucefiaxkpNjxUwwpQuXPRRzfO5J6XGjlWQJ6fTQsl_SAUtTXSEPs2Cl4xEXy1Ur1U4ARYIw1Z66ULd88qu_k"
            />
          </div>
        </div>
      </header>

      {/* Main Content */}
      {children}
    </div>
  );
}



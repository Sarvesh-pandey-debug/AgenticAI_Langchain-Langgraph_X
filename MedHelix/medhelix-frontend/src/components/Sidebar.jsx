import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  FileCode, 
  FileText, 
  CreditCard, 
  AlertCircle, 
  Settings,
  ShieldCheck,
  ChevronRight
} from 'lucide-react';
import { cn } from '../lib/utils';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
  { icon: Users, label: 'Intake & Eligibility', path: '/intake' },
  { icon: FileCode, label: 'AI Coding', path: '/coding' },
  { icon: FileText, label: 'Claims', path: '/claims' },
  { icon: AlertCircle, label: 'Denials & Appeals', path: '/appeals' },
  { icon: CreditCard, label: 'Payments', path: '/payments' },
  { icon: ShieldCheck, label: 'Audit Log', path: '/audit' },
];

export default function Sidebar() {
  const location = useLocation();

  return (
    <div className="w-72 h-screen sidebar-gradient text-slate-300 flex flex-col shadow-xl z-20">
      <div className="p-8">
        <Link to="/" className="text-2xl font-bold text-white flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg shadow-lg shadow-blue-500/20">
            <ShieldCheck className="text-white w-6 h-6" />
          </div>
          MedHelix
        </Link>
      </div>
      
      <nav className="flex-1 px-4 space-y-1 py-4">
        {navItems.map((item, index) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={index}
              to={item.path}
              className={cn(
                "w-full flex items-center gap-3 px-4 py-3.5 rounded-xl text-sm font-medium transition-all duration-200",
                isActive 
                  ? "bg-white/10 text-white shadow-sm" 
                  : "hover:bg-white/5 hover:text-white"
              )}
            >
              <item.icon className={cn("w-5 h-5", isActive ? "text-blue-400" : "text-slate-400")} />
              {item.label}
              {isActive && <div className="ml-auto w-1.5 h-1.5 bg-blue-400 rounded-full shadow-[0_0_8px_rgba(96,165,250,0.8)]" />}
            </Link>
          );
        })}
      </nav>
      
      <div className="p-6 border-t border-white/10">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium hover:bg-white/5 hover:text-white transition-all text-slate-400">
          <Settings className="w-5 h-5" />
          Settings
        </button>
      </div>
    </div>
  );
}

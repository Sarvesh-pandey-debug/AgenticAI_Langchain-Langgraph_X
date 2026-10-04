import React from 'react';
import { 
  BarChart3, 
  Activity, 
  CheckCircle2, 
  XCircle, 
  Search,
  Bell,
  Calendar,
  ChevronRight
} from 'lucide-react';
import MetricCard from '../components/MetricCard';

export default function Dashboard() {
  return (
    <div className="flex-1 p-10 space-y-10 overflow-y-auto bg-[#f8fafc]">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-3xl font-extrabold tracking-tight text-slate-900">RCM Command Center</h2>
          <p className="text-slate-500 mt-1">Streamlining medical billing with AI precision.</p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input 
              type="text" 
              placeholder="Search patients..." 
              className="bg-white border border-slate-200 rounded-xl pl-10 pr-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all w-72 shadow-sm"
            />
          </div>
          <button className="p-2.5 bg-white border border-slate-200 rounded-xl hover:bg-slate-50 transition-all relative shadow-sm">
            <Bell className="w-5 h-5 text-slate-600" />
            <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-rose-500 rounded-full border-2 border-white"></span>
          </button>
          <div className="flex items-center gap-3 px-4 py-2.5 bg-white border border-slate-200 rounded-xl shadow-sm">
            <Calendar className="w-4 h-4 text-blue-600" />
            <span className="text-sm font-semibold text-slate-700">May 3, 2026</span>
          </div>
        </div>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <MetricCard 
          label="AI Coding Accuracy" 
          value="98.4%" 
          trend="up" 
          trendValue="2.1" 
          icon={CheckCircle2} 
          color="bg-blue-600" 
        />
        <MetricCard 
          label="Clean Claim Rate" 
          value="94.2%" 
          trend="up" 
          trendValue="1.5" 
          icon={Activity} 
          color="bg-indigo-600" 
        />
        <MetricCard 
          label="Total Denials" 
          value="12" 
          trend="down" 
          trendValue="4.2" 
          icon={XCircle} 
          color="bg-rose-500" 
        />
        <MetricCard 
          label="Revenue Collected" 
          value="$1.2M" 
          trend="up" 
          trendValue="8.4" 
          icon={BarChart3} 
          color="bg-emerald-600" 
        />
      </div>

      {/* Main Content Area */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
        {/* Recent Coding Sessions */}
        <div className="lg:col-span-2 bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-bold text-slate-900">Recent Coding Sessions</h3>
            <button className="text-sm text-blue-600 font-bold hover:text-blue-700">View History</button>
          </div>
          
          <div className="space-y-4">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="flex items-center justify-between p-5 rounded-2xl hover:bg-slate-50 transition-all border border-transparent hover:border-slate-200 group">
                <div className="flex items-center gap-5">
                  <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600 font-bold text-lg">
                    {['JD', 'AS', 'RK', 'ML'][i-1]}
                  </div>
                  <div>
                    <p className="font-bold text-slate-900">{['John Doe', 'Alice Smith', 'Robert King', 'Maria Lopez'][i-1]}</p>
                    <p className="text-xs text-slate-500 font-medium">Encounter #E-1002{i} • Cardiology</p>
                  </div>
                </div>
                <div className="flex items-center gap-8">
                  <div className="text-right">
                    <p className="text-sm font-bold text-slate-800">ICD-10: J18.9</p>
                    <p className="text-xs text-slate-500">CPT: 99213</p>
                  </div>
                  <div className="px-3 py-1 rounded-full bg-emerald-50 text-emerald-600 text-xs font-bold border border-emerald-100">
                    Auto-Approved
                  </div>
                  <button className="p-2 text-slate-400 group-hover:text-blue-600 transition-all">
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Priority Actions */}
        <div className="space-y-8">
          <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
            <h3 className="text-xl font-bold text-slate-900 mb-6">Priority Actions</h3>
            <div className="space-y-5">
              <div className="p-5 rounded-2xl bg-rose-50 border border-rose-100">
                <div className="flex items-center gap-2 mb-2">
                  <XCircle className="w-4 h-4 text-rose-500" />
                  <p className="text-sm font-bold text-rose-700">Claim Denial Alert</p>
                </div>
                <p className="text-xs text-rose-600 leading-relaxed font-medium">Encounter #E-9901 requires an immediate appeal (CARC 16: Missing Info).</p>
                <button className="mt-4 w-full py-2.5 bg-rose-600 text-white text-xs font-bold rounded-xl hover:bg-rose-700 transition-all shadow-md shadow-rose-200">
                  Write Appeal with AI
                </button>
              </div>
              
              <div className="p-5 rounded-2xl bg-amber-50 border border-amber-100">
                <div className="flex items-center gap-2 mb-2">
                  <Activity className="w-4 h-4 text-amber-500" />
                  <p className="text-sm font-bold text-amber-700">HITL Review Needed</p>
                </div>
                <p className="text-xs text-amber-600 leading-relaxed font-medium">2 coding sessions have low confidence scores (0.65). Please verify.</p>
                <button className="mt-4 w-full py-2.5 bg-amber-500 text-white text-xs font-bold rounded-xl hover:bg-amber-600 transition-all shadow-md shadow-amber-200">
                  Start Manual Review
                </button>
              </div>
            </div>
          </div>
          
          <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-2xl p-8 text-white shadow-lg shadow-blue-200 relative overflow-hidden group">
            <div className="relative z-10">
              <h3 className="text-xl font-bold mb-3">AI Smart Insights</h3>
              <p className="text-sm text-blue-50 leading-relaxed opacity-90">
                Based on current trends, adding **Modifier 25** to your E/M visits could increase clean claim rates by **12%**.
              </p>
              <button className="mt-6 flex items-center gap-2 text-white text-xs font-bold uppercase tracking-wider group-hover:translate-x-1 transition-transform">
                <span>View Insight Report</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
            <div className="absolute -right-4 -bottom-4 w-32 h-32 bg-white/10 rounded-full blur-3xl" />
          </div>
        </div>
      </div>
    </div>
  );
}

import React, { useState } from 'react';
import axios from 'axios';
import { 
  Users, 
  Search, 
  Database, 
  ShieldCheck, 
  Loader2, 
  CheckCircle2, 
  XCircle,
  Stethoscope
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function Intake() {
  const [patientId, setPatientId] = useState('P-12345');
  const [encounterId, setEncounterId] = useState('E-98765');
  const [provider, setProvider] = useState('mock');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleIntake = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/intake/process', {
        patient_id: patientId,
        encounter_id: encounterId,
        provider: provider
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process intake. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-10 space-y-10 overflow-y-auto bg-[#f8fafc]">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-extrabold tracking-tight text-slate-900">Intake & Eligibility</h2>
        <p className="text-slate-500 mt-1">Onboard patients and verify insurance coverage in real-time.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        {/* Form Section */}
        <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-blue-100 p-2 rounded-lg">
              <Users className="text-blue-600 w-5 h-5" />
            </div>
            <h3 className="text-lg font-bold">New Intake Request</h3>
          </div>

          <div className="space-y-4">
            <div>
              <label className="text-sm font-semibold text-slate-700 block mb-2">Patient ID</label>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input 
                  type="text" 
                  value={patientId}
                  onChange={(e) => setPatientId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-3 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                  placeholder="Enter Patient ID..."
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-semibold text-slate-700 block mb-2">Encounter ID</label>
              <div className="relative">
                <Stethoscope className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
                <input 
                  type="text" 
                  value={encounterId}
                  onChange={(e) => setEncounterId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl pl-10 pr-4 py-3 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all"
                  placeholder="Enter Encounter ID..."
                />
              </div>
            </div>

            <div>
              <label className="text-sm font-semibold text-slate-700 block mb-2">EHR Provider</label>
              <div className="grid grid-cols-3 gap-3">
                {['mock', 'epic', 'ecw'].map((p) => (
                  <button
                    key={p}
                    onClick={() => setProvider(p)}
                    className={cn(
                      "py-2.5 rounded-xl text-xs font-bold uppercase tracking-wider border transition-all",
                      provider === p 
                        ? "bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-100" 
                        : "bg-white text-slate-600 border-slate-200 hover:border-blue-300"
                    )}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button 
            onClick={handleIntake}
            disabled={loading}
            className="w-full py-4 bg-slate-900 text-white rounded-xl font-bold flex items-center justify-center gap-3 hover:bg-slate-800 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <ShieldCheck className="w-5 h-5" />}
            {loading ? 'Verifying...' : 'Verify Eligibility & Process Intake'}
          </button>
        </div>

        {/* Status / Result Section */}
        <div className="space-y-6">
          {!result && !loading && !error && (
            <div className="h-full bg-slate-100 border-2 border-dashed border-slate-300 rounded-2xl flex flex-col items-center justify-center p-10 text-center space-y-4">
              <Database className="w-12 h-12 text-slate-400" />
              <div>
                <p className="font-bold text-slate-600">No Active Process</p>
                <p className="text-sm text-slate-400">Fill the form to start a new patient intake workflow.</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="h-full bg-white border border-slate-200 rounded-2xl flex flex-col items-center justify-center p-10 text-center space-y-6 animate-pulse">
              <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center">
                <Loader2 className="w-8 h-8 text-blue-600 animate-spin" />
              </div>
              <div>
                <p className="font-bold text-slate-900">Connecting to EHR & Clearinghouse</p>
                <p className="text-sm text-slate-500 mt-2">Fetching patient records and verifying insurance status...</p>
              </div>
            </div>
          )}

          {error && (
            <div className="bg-rose-50 border border-rose-200 rounded-2xl p-8 space-y-4">
              <div className="flex items-center gap-3 text-rose-600">
                <XCircle className="w-6 h-6" />
                <h3 className="font-bold">Process Error</h3>
              </div>
              <p className="text-sm text-rose-600 font-medium">{error}</p>
              <button onClick={handleIntake} className="text-xs font-bold text-rose-700 underline">Try Again</button>
            </div>
          )}

          {result && (
            <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className={cn(
                "p-6 flex items-center justify-between",
                result.eligibility === 'ACTIVE' ? "bg-emerald-500" : "bg-blue-600"
              )}>
                <div className="flex items-center gap-3 text-white">
                  <CheckCircle2 className="w-6 h-6" />
                  <h3 className="font-bold">Intake Successful</h3>
                </div>
                <span className="text-xs font-bold bg-white/20 px-3 py-1 rounded-full text-white">
                  {result.intake_id}
                </span>
              </div>
              
              <div className="p-8 space-y-6">
                <div className="grid grid-cols-2 gap-8">
                  <div>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Patient Name</p>
                    <p className="font-bold text-slate-900 text-lg">{result.patient_name}</p>
                  </div>
                  <div>
                    <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Service Date</p>
                    <p className="font-bold text-slate-900 text-lg">{result.date_of_service}</p>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <ShieldCheck className={cn(
                      "w-5 h-5",
                      result.eligibility === 'ACTIVE' ? "text-emerald-500" : "text-blue-500"
                    )} />
                    <div>
                      <p className="text-sm font-bold text-slate-900">Insurance Eligibility</p>
                      <p className="text-xs text-slate-500">Verified via Stedi Clearinghouse</p>
                    </div>
                  </div>
                  <span className={cn(
                    "px-3 py-1 rounded-lg text-xs font-bold border",
                    result.eligibility === 'ACTIVE' 
                      ? "bg-emerald-50 text-emerald-600 border-emerald-100" 
                      : "bg-blue-50 text-blue-600 border-blue-100"
                  )}>
                    {result.eligibility}
                  </span>
                </div>

                <div className="pt-4 border-t border-slate-100">
                  <button className="w-full py-3 border-2 border-slate-900 text-slate-900 rounded-xl font-bold hover:bg-slate-900 hover:text-white transition-all">
                    Continue to AI Coding
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

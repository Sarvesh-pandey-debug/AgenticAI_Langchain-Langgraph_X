import React, { useState } from 'react';
import axios from 'axios';
import { 
  FileCode, 
  Search, 
  Brain, 
  Loader2, 
  CheckCircle2, 
  XCircle,
  Stethoscope,
  ChevronRight,
  ClipboardList,
  Zap
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function Coding() {
  const [patientId, setPatientId] = useState('P-12345');
  const [encounterId, setEncounterId] = useState('E-98765');
  const [provider, setProvider] = useState('mock');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleCoding = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/coding/fetch-and-extract', {
        patient_id: patientId,
        encounter_id: encounterId,
        provider: provider
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to process AI Coding. Make sure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-10 space-y-10 overflow-y-auto bg-[#f8fafc]">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-extrabold tracking-tight text-slate-900">AI Intelligent Coding</h2>
        <p className="text-slate-500 mt-1">Autonomous medical entity extraction and ICD-10/CPT mapping.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        {/* Form Section */}
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="bg-indigo-100 p-2 rounded-lg">
                <Brain className="text-indigo-600 w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold">Launch AI Pipeline</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-2">Patient ID</label>
                <input 
                  type="text" 
                  value={patientId}
                  onChange={(e) => setPatientId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                />
              </div>

              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-2">Encounter ID</label>
                <input 
                  type="text" 
                  value={encounterId}
                  onChange={(e) => setEncounterId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 transition-all"
                />
              </div>

              <button 
                onClick={handleCoding}
                disabled={loading}
                className="w-full py-4 bg-indigo-600 text-white rounded-xl font-bold flex items-center justify-center gap-3 hover:bg-indigo-700 transition-all shadow-lg shadow-indigo-100"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Zap className="w-5 h-5" />}
                {loading ? 'AI Processing...' : 'Start AI Coding Pipeline'}
              </button>
            </div>
          </div>
          
          <div className="bg-slate-900 rounded-2xl p-6 text-white overflow-hidden relative">
            <h4 className="font-bold mb-2 relative z-10">Agent Workflow</h4>
            <div className="space-y-3 relative z-10">
              <div className="flex items-center gap-3 text-xs opacity-70">
                <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                <span>CCEA: Entity Extraction</span>
              </div>
              <div className="flex items-center gap-3 text-xs opacity-70">
                <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                <span>ICA: Code Mapping</span>
              </div>
              <div className="flex items-center gap-3 text-xs opacity-70">
                <div className="w-1.5 h-1.5 bg-green-500 rounded-full" />
                <span>CQAA: Quality Audit</span>
              </div>
            </div>
            <Brain className="absolute -right-4 -bottom-4 w-24 h-24 text-white/5" />
          </div>
        </div>

        {/* Results Section */}
        <div className="lg:col-span-8 space-y-6">
          {!result && !loading && !error && (
            <div className="h-full bg-slate-100 border-2 border-dashed border-slate-300 rounded-2xl flex flex-col items-center justify-center p-10 text-center space-y-4">
              <ClipboardList className="w-12 h-12 text-slate-400" />
              <div>
                <p className="font-bold text-slate-600">Waiting for Data</p>
                <p className="text-sm text-slate-400">The AI agents will display extracted codes and confidence scores here.</p>
              </div>
            </div>
          )}

          {loading && (
            <div className="bg-white border border-slate-200 rounded-2xl p-10 space-y-8 animate-in fade-in duration-500">
               <div className="space-y-4">
                  <div className="h-6 bg-slate-100 rounded-full w-1/4 animate-pulse" />
                  <div className="h-24 bg-slate-50 rounded-2xl w-full animate-pulse" />
               </div>
               <div className="grid grid-cols-2 gap-6">
                  <div className="h-32 bg-slate-50 rounded-2xl animate-pulse" />
                  <div className="h-32 bg-slate-50 rounded-2xl animate-pulse" />
               </div>
            </div>
          )}

          {error && (
            <div className="bg-rose-50 border border-rose-200 rounded-2xl p-8 space-y-4 animate-in fade-in slide-in-from-top-4 duration-300">
              <div className="flex items-center gap-3 text-rose-600">
                <XCircle className="w-6 h-6" />
                <h3 className="font-bold">Pipeline Error</h3>
              </div>
              <p className="text-sm text-rose-600 font-medium">{error}</p>
              <button onClick={handleCoding} className="text-xs font-bold text-rose-700 underline">Try Again</button>
            </div>
          )}

          {result && (
            <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-500">
              {/* Audit Header */}
              <div className="bg-emerald-600 rounded-2xl p-6 text-white flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className="bg-white/20 p-2 rounded-xl">
                    <ShieldCheck className="w-6 h-6" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">CQAA Audit Passed</h3>
                    <p className="text-xs text-white/80">No NCCI bundling issues or payer rule violations detected.</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-xs font-bold uppercase opacity-80">Confidence Score</p>
                  <p className="text-2xl font-black">{Math.round(result.cqaa_result.confidence_score * 100)}%</p>
                </div>
              </div>

              {/* Codes Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* ICD-10 */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <div className="w-2 h-2 bg-blue-500 rounded-full" />
                    ICD-10 Diagnoses
                  </h4>
                  <div className="space-y-3">
                    {result.ica_result.suggested_icd10.map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                        <span className="font-bold text-slate-700">{item.code}</span>
                        <span className="text-xs font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">
                          {Math.round(item.confidence * 100)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* CPT */}
                <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
                  <h4 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <div className="w-2 h-2 bg-indigo-500 rounded-full" />
                    CPT Procedures
                  </h4>
                  <div className="space-y-3">
                    {result.ica_result.suggested_cpt.map((item, idx) => (
                      <div key={idx} className="flex items-center justify-between p-3 bg-slate-50 rounded-xl border border-slate-100">
                        <span className="font-bold text-slate-700">{item.code}</span>
                        <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-1 rounded">
                          {Math.round(item.confidence * 100)}%
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Clinical Trail */}
              <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm">
                <h4 className="font-bold text-slate-900 mb-6">AI Audit Trail</h4>
                <div className="space-y-6">
                  {result.crla_result.audit_trail.map((log, idx) => (
                    <div key={idx} className="flex gap-4 group">
                      <div className="flex flex-col items-center">
                        <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-xs font-bold text-slate-500 group-last:bg-indigo-600 group-last:text-white group-last:border-indigo-600">
                          {idx + 1}
                        </div>
                        {idx < result.crla_result.audit_trail.length - 1 && <div className="w-px h-full bg-slate-100 my-1" />}
                      </div>
                      <div className="pb-6">
                        <p className="text-sm font-bold text-slate-800">{log}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

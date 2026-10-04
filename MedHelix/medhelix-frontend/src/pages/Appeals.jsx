import React, { useState } from 'react';
import axios from 'axios';
import { 
  AlertCircle, 
  Send, 
  Loader2, 
  CheckCircle2, 
  FileText,
  Brain,
  History,
  Copy
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function Appeals() {
  const [claimId, setClaimId] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleAppeal = async () => {
    if (!claimId) return setError('Please enter a Claim ID.');
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/appeals/generate', {
        claim_id: claimId
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to generate appeal. Ensure the claim exists.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-10 space-y-10 overflow-y-auto bg-[#f8fafc]">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-extrabold tracking-tight text-slate-900">Denials & Appeals</h2>
        <p className="text-slate-500 mt-1">Autonomous AI agent for insurance appeal letter generation.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div className="lg:col-span-4 bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-6 self-start">
           <div className="flex items-center gap-3 mb-4">
              <div className="bg-rose-100 p-2 rounded-lg">
                <AlertCircle className="text-rose-600 w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold">Initiate AI Appeal</h3>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-sm font-semibold text-slate-700 block mb-2">Denied Claim ID</label>
                <input 
                  type="text" 
                  value={claimId}
                  onChange={(e) => setClaimId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-rose-500/20 focus:border-rose-500 transition-all"
                  placeholder="e.g. 7777..."
                />
                <p className="text-[10px] text-slate-400 mt-2 italic">Tip: Use a claim ID from the 'Claims' page that received a denial code.</p>
              </div>

              <button 
                onClick={handleAppeal}
                disabled={loading}
                className="w-full py-4 bg-rose-600 text-white rounded-xl font-bold flex items-center justify-center gap-3 hover:bg-rose-700 transition-all shadow-lg shadow-rose-100 disabled:opacity-50"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Brain className="w-5 h-5" />}
                {loading ? 'AI is Writing...' : 'Generate AI Appeal Letter'}
              </button>
            </div>
        </div>

        <div className="lg:col-span-8 space-y-6">
           {loading && (
             <div className="bg-white border border-slate-200 rounded-2xl p-12 flex flex-col items-center text-center space-y-6 animate-pulse">
                <div className="w-16 h-16 bg-rose-50 rounded-full flex items-center justify-center">
                  <Brain className="w-8 h-8 text-rose-600 animate-bounce" />
                </div>
                <div>
                  <h4 className="text-xl font-bold text-slate-900">AI Specialist is Working</h4>
                  <p className="text-sm text-slate-500 mt-2 max-w-sm">
                    Analyzing denial reason codes (CARC/RARC), cross-referencing medical necessity, and drafting a professional appeal.
                  </p>
                </div>
             </div>
           )}

           {error && (
             <div className="bg-rose-50 border border-rose-200 rounded-2xl p-8 text-rose-600 font-medium">
               {error}
             </div>
           )}

           {result && (
             <div className="bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden animate-in zoom-in-95 duration-500">
                <div className="bg-slate-900 p-6 flex justify-between items-center">
                  <div className="flex items-center gap-3 text-white">
                    <FileText className="w-5 h-5 text-blue-400" />
                    <span className="font-bold">Appeal Letter Draft</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold text-slate-400 uppercase bg-white/10 px-2 py-1 rounded">Status: {result.status}</span>
                    <button className="p-2 bg-white/10 hover:bg-white/20 rounded-lg transition-all text-white">
                      <Copy className="w-4 h-4" />
                    </button>
                  </div>
                </div>
                <div className="p-10">
                   <div className="bg-slate-50 rounded-xl p-8 border border-slate-100 shadow-inner max-h-[500px] overflow-y-auto whitespace-pre-wrap font-serif text-slate-700 leading-relaxed">
                      {result.letter_preview}
                   </div>
                   <div className="mt-8 flex gap-4">
                      <button className="flex-1 py-4 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 transition-all shadow-lg shadow-blue-100">
                        Approve & Send to Payer
                      </button>
                      <button className="px-6 py-4 border-2 border-slate-200 text-slate-600 rounded-xl font-bold hover:bg-slate-50 transition-all">
                        Edit Draft
                      </button>
                   </div>
                </div>
             </div>
           )}

           {!result && !loading && (
             <div className="bg-white border border-slate-200 rounded-2xl p-12 text-center flex flex-col items-center space-y-4">
                <div className="w-16 h-16 bg-slate-50 rounded-full flex items-center justify-center">
                  <History className="w-8 h-8 text-slate-300" />
                </div>
                <div>
                  <h4 className="font-bold text-slate-900 text-lg">No Active Appeal</h4>
                  <p className="text-sm text-slate-400">Enter a Claim ID to begin the automated appeal process.</p>
                </div>
             </div>
           )}
        </div>
      </div>
    </div>
  );
}

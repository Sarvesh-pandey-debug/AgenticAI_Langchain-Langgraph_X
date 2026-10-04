import React, { useState } from 'react';
import axios from 'axios';
import { 
  FileText, 
  Search, 
  Send, 
  Loader2, 
  CheckCircle2, 
  XCircle,
  Clock,
  ArrowRight
} from 'lucide-react';
import { cn } from '../lib/utils';

export default function Claims() {
  const [patientId, setPatientId] = useState('P-12345');
  const [encounterId, setEncounterId] = useState('E-98765');
  const [icd10, setIcd10] = useState('J18.9');
  const [cpt, setCpt] = useState('99213');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await axios.post('http://localhost:8000/api/v1/claims/submit', {
        patient_id: patientId,
        encounter_id: encounterId,
        icd10_codes: [icd10],
        cpt_codes: [cpt]
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to submit claim.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex-1 p-10 space-y-10 overflow-y-auto bg-[#f8fafc]">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-extrabold tracking-tight text-slate-900">Claim Management</h2>
        <p className="text-slate-500 mt-1">Submit EDI 837P transactions to insurance payers via Stedi.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
        <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm space-y-6">
           <div className="flex items-center gap-3 mb-4">
              <div className="bg-blue-100 p-2 rounded-lg">
                <FileText className="text-blue-600 w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold">Prepare Submission</h3>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="col-span-2 md:col-span-1">
                <label className="text-sm font-semibold text-slate-700 block mb-2">Patient ID</label>
                <input 
                  type="text" 
                  value={patientId}
                  onChange={(e) => setPatientId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm"
                />
              </div>
              <div className="col-span-2 md:col-span-1">
                <label className="text-sm font-semibold text-slate-700 block mb-2">Encounter ID</label>
                <input 
                  type="text" 
                  value={encounterId}
                  onChange={(e) => setEncounterId(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm"
                />
              </div>
              <div className="col-span-2 md:col-span-1">
                <label className="text-sm font-semibold text-slate-700 block mb-2">ICD-10 Code</label>
                <input 
                  type="text" 
                  value={icd10}
                  onChange={(e) => setIcd10(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm"
                />
              </div>
              <div className="col-span-2 md:col-span-1">
                <label className="text-sm font-semibold text-slate-700 block mb-2">CPT Code</label>
                <input 
                  type="text" 
                  value={cpt}
                  onChange={(e) => setCpt(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-sm"
                />
              </div>
            </div>

            <button 
              onClick={handleSubmit}
              disabled={loading}
              className="w-full py-4 bg-blue-600 text-white rounded-xl font-bold flex items-center justify-center gap-3 hover:bg-blue-700 transition-all"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
              {loading ? 'Submitting EDI...' : 'Submit Claim to Payer'}
            </button>
        </div>

        <div className="space-y-6">
          {result && (
            <div className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-lg animate-in zoom-in-95 duration-300">
               <div className="p-8 space-y-6">
                  <div className="flex items-center gap-4">
                    <div className="w-14 h-14 rounded-full bg-emerald-100 flex items-center justify-center">
                      <CheckCircle2 className="w-8 h-8 text-emerald-600" />
                    </div>
                    <div>
                      <h4 className="text-xl font-bold text-slate-900">Claim Transmitted</h4>
                      <p className="text-sm text-slate-500">Transaction ID: {result.stedi_claim_id}</p>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-6 pt-6 border-t border-slate-100">
                    <div>
                      <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Charge Amount</p>
                      <p className="font-bold text-slate-900 text-2xl">${result.total_charge.toFixed(2)}</p>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Status</p>
                      <div className="flex items-center gap-2 text-emerald-600 font-bold">
                        <Clock className="w-4 h-4" />
                        {result.submission_status}
                      </div>
                    </div>
                  </div>

                  <div className="p-5 rounded-2xl bg-slate-900 text-white flex items-center justify-between">
                    <div>
                      <p className="text-xs opacity-60 font-bold uppercase tracking-widest mb-1">Payer Acknowledgment</p>
                      <p className="font-bold">EDI 277: Accepted for Processing</p>
                    </div>
                    <ArrowRight className="w-5 h-5 text-blue-400" />
                  </div>
               </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

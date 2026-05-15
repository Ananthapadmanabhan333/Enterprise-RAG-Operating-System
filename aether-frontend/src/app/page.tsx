"use client";

import { useState } from "react";
import { Search, Loader2, ShieldAlert, CheckCircle2, ShieldCheck } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function Home() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      // Pointing to the FastAPI backend proxy defined in docker-compose / env
      const res = await fetch("http://localhost:8000/api/v1/retrieval/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query,
          tenant_id: "tenant-001",
          metadata_filters: {}
        }),
      });

      if (!res.ok) throw new Error("Retrieval failed.");
      
      const data = await res.json();
      setResponse(data);
    } catch (err: any) {
      setError(err.message || "An error occurred connecting to AetherOS.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 lg:p-24 relative overflow-hidden">
      {/* Background ambient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />

      <div className="z-10 w-full max-w-4xl flex flex-col items-center gap-12">
        
        {/* Header */}
        <div className="text-center space-y-4">
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-primary/30 bg-primary/10 text-primary text-sm font-medium mb-4"
          >
            <ShieldCheck className="w-4 h-4" />
            Zero-Hallucination Guardrails Active
          </motion.div>
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-5xl lg:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white to-white/40"
          >
            AetherOS
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-lg text-white/50 max-w-2xl mx-auto"
          >
            Autonomous Enterprise RAG Intelligence. Query your entire organizational knowledge graph with absolute confidence.
          </motion.p>
        </div>

        {/* Search Bar */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3 }}
          className="w-full relative"
        >
          <form onSubmit={handleSearch} className="relative group">
            <div className="absolute inset-0 bg-primary/20 rounded-2xl blur-xl group-hover:bg-primary/30 transition-all duration-500" />
            <div className="relative glass-panel rounded-2xl flex items-center p-2 focus-within:ring-2 focus-within:ring-primary/50 transition-all">
              <div className="pl-4 pr-2 text-white/50">
                <Search className="w-6 h-6" />
              </div>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask a mission-critical question..."
                className="w-full bg-transparent border-none outline-none text-lg text-white placeholder:text-white/30 py-4 px-2"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !query.trim()}
                className="bg-primary hover:bg-primary/90 text-white px-8 py-3 rounded-xl font-medium transition-all disabled:opacity-50 flex items-center gap-2"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Synthesize"}
              </button>
            </div>
          </form>
        </motion.div>

        {/* Results Area */}
        <AnimatePresence>
          {error && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95 }}
              className="w-full glass-panel border-red-500/30 bg-red-500/10 p-6 rounded-2xl flex items-start gap-4 text-red-200"
            >
              <ShieldAlert className="w-6 h-6 shrink-0 text-red-500" />
              <p>{error}</p>
            </motion.div>
          )}

          {response && !loading && (
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="w-full space-y-6"
            >
              {/* Answer Card */}
              <div className="glass-panel rounded-3xl p-8 relative overflow-hidden">
                <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary to-accent" />
                
                <div className="flex items-center justify-between mb-6 border-b border-white/10 pb-4">
                  <h3 className="text-xl font-semibold text-white/90">Synthesized Intelligence</h3>
                  <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-500/10 text-green-400 text-sm border border-green-500/20">
                    <CheckCircle2 className="w-4 h-4" />
                    Confidence: {(response.confidence_score * 100).toFixed(1)}%
                  </div>
                </div>
                
                <p className="text-lg text-white/80 leading-relaxed">
                  {response.answer}
                </p>
              </div>

              {/* Retrieval Trace / Context */}
              <div className="space-y-4">
                <h4 className="text-sm font-medium text-white/40 uppercase tracking-widest pl-2">Retrieval Trace</h4>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {response.retrieved_chunks.map((chunk: any, i: number) => (
                    <motion.div 
                      key={chunk.id || i}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.1 * i }}
                      className="glass-panel p-5 rounded-2xl text-sm"
                    >
                      <div className="flex justify-between items-center mb-3">
                        <span className="text-xs font-mono text-primary/80 bg-primary/10 px-2 py-1 rounded">CHUNK_{chunk.id || i}</span>
                        <span className="text-xs text-white/40">Score: {chunk.score?.toFixed(2) || 'N/A'}</span>
                      </div>
                      <p className="text-white/60 line-clamp-3">{chunk.content}</p>
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </main>
  );
}

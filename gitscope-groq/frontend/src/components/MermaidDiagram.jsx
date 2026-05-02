import { useEffect, useRef, useState } from "react";
import mermaid from "mermaid";
import { ZoomIn, ZoomOut, Download, RefreshCw } from "lucide-react";

let initialized = false;
function initMermaid() {
  if (!initialized) {
    mermaid.initialize({
      startOnLoad: false, theme: "dark", darkMode: true,
      themeVariables: {
        background: "#0d1526", primaryColor: "#1a2844",
        primaryTextColor: "#e2e8f0", primaryBorderColor: "#06b6d4",
        lineColor: "#06b6d4", secondaryColor: "#121e34",
        fontFamily: "JetBrains Mono, monospace", fontSize: "12px",
      },
      flowchart: { curve: "basis", htmlLabels: true },
    });
    initialized = true;
  }
}

export default function MermaidDiagram({ chart }) {
  const containerRef = useRef(null);
  const [zoom, setZoom] = useState(1);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const idRef = useRef(`mm-${Math.random().toString(36).slice(2)}`);

  useEffect(() => { if (chart) { initMermaid(); render(); } }, [chart]);

  async function render() {
    setLoading(true); setError(null);
    try {
      const { svg } = await mermaid.render(idRef.current, chart);
      if (containerRef.current) {
        containerRef.current.innerHTML = svg;
        const svgEl = containerRef.current.querySelector("svg");
        if (svgEl) { svgEl.style.width = "100%"; svgEl.style.height = "auto"; svgEl.removeAttribute("width"); svgEl.removeAttribute("height"); }
      }
    } catch (e) { setError("Failed to render diagram."); }
    finally { setLoading(false); }
  }

  function download() {
    const svg = containerRef.current?.querySelector("svg");
    if (!svg) return;
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([svg.outerHTML], { type: "image/svg+xml" }));
    a.download = "gitscope-flowchart.svg"; a.click();
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center gap-2">
          {[ZoomOut, ZoomIn].map((Icon, i) => (
            <button key={i} onClick={() => setZoom(z => Math.max(0.5, Math.min(2, z + (i ? 0.15 : -0.15))))}
              className="p-1.5 rounded-lg bg-surface-700/50 hover:bg-surface-600 transition-colors text-gray-400 hover:text-white">
              <Icon size={13} />
            </button>
          ))}
          <span className="text-xs font-mono text-gray-600 w-10 text-center">{Math.round(zoom*100)}%</span>
          <button onClick={render} className="p-1.5 rounded-lg bg-surface-700/50 hover:bg-surface-600 transition-colors text-gray-400 hover:text-white"><RefreshCw size={13} /></button>
        </div>
        <button onClick={download} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-brand-600/20 hover:bg-brand-600/30 text-brand-400 text-xs font-medium transition-colors">
          <Download size={12} /> Export SVG
        </button>
      </div>

      <div className="overflow-auto rounded-xl bg-surface-900/80 border border-white/5 p-4 min-h-40">
        {loading && <div className="flex justify-center items-center h-40 gap-2">{[0,1,2].map(i=><div key={i} className="w-2 h-2 rounded-full bg-brand-500 animate-bounce" style={{animationDelay:`${i*0.15}s`}}/>)}</div>}
        {error && <div className="flex justify-center items-center h-40 text-red-400 text-sm">{error}</div>}
        <div ref={containerRef} className={loading ? "hidden" : ""} style={{ transform: `scale(${zoom})`, transformOrigin: "top left" }} />
      </div>

      <details className="mt-2">
        <summary className="text-xs text-gray-600 cursor-pointer hover:text-gray-400">View Mermaid source</summary>
        <pre className="mt-2 p-3 rounded-lg bg-surface-900 border border-white/5 text-xs font-mono text-gray-500 overflow-auto max-h-36">{chart}</pre>
      </details>
    </div>
  );
}

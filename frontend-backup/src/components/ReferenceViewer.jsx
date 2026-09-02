export default function ReferenceViewer({
  originalUrl,
  edgeUrl,
  viewMode,
  onViewModeChange
}) {
  return (
    <section className="workspace-card reference-card">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Reference</p>
          <h3>Use the source image as your anchor.</h3>
          <p className="section-subcopy">
            Switch views to compare silhouette, placement, and the edge structure underneath.
          </p>
        </div>
        <div className="segmented-control" role="tablist" aria-label="Reference view">
          {["original", "edges", "compare"].map((mode) => (
            <button
              key={mode}
              type="button"
              role="tab"
              aria-selected={viewMode === mode}
              className={viewMode === mode ? "is-active" : ""}
              onClick={() => onViewModeChange(mode)}
            >
              {mode === "original" ? "Original" : mode === "edges" ? "Edges" : "Compare"}
            </button>
          ))}
        </div>
      </div>

      {viewMode === "compare" ? (
        <div className="reference-grid compare-grid">
          <figure>
            <img src={originalUrl} alt="Original reference" />
            <figcaption>Original reference</figcaption>
          </figure>
          <figure>
            <img src={edgeUrl} alt="Detected edge map" />
            <figcaption>Edge map</figcaption>
          </figure>
        </div>
      ) : (
        <figure className="reference-grid single-view">
          <img
            src={viewMode === "edges" ? edgeUrl : originalUrl}
            alt={viewMode === "edges" ? "Detected edge map" : "Original reference"}
          />
          <figcaption>{viewMode === "edges" ? "Edge map" : "Original reference"}</figcaption>
        </figure>
      )}
    </section>
  );
}

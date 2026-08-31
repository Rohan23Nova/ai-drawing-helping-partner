function formatPercent(value) {
  return value == null ? "Not available" : `${Math.round(value * 100)}%`;
}

export default function AnalysisPanel({ analysis }) {
  const composition = analysis.composition || {};
  const shapes = analysis.shapes || {};
  const lines = analysis.lines || {};
  const proportions = analysis.proportions || {};
  const largestShape = proportions.largest_shape;

  return (
    <section className="workspace-card analysis-card">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Reference Analysis</p>
          <h3>Use the technical readout as support, not as gospel.</h3>
          <p className="section-subcopy">
            Read these signals as checkpoints for placement and structure while you draw.
          </p>
        </div>
      </div>

      <div className="analysis-metrics">
        <article>
          <span>Composition</span>
          <strong>{composition.position || "No subject detected"}</strong>
          <p>
            {composition.subject_detected
              ? `Subject width ${formatPercent(composition.size_ratio?.width)} and height ${formatPercent(
                  composition.size_ratio?.height
                )}.`
              : "The image did not produce a reliable main subject outline."}
          </p>
        </article>
        <article>
          <span>Shapes</span>
          <strong>{shapes.shape_count || 0} major forms</strong>
          <p>
            {largestShape
              ? `Largest form: ${largestShape.type} with aspect ratio ${largestShape.aspect_ratio}.`
              : "No dominant shape was detected."}
          </p>
        </article>
        <article>
          <span>Lines</span>
          <strong>{lines.line_count || 0} structural lines</strong>
          <p>
            {`H ${lines.orientation_counts?.horizontal || 0} · V ${
              lines.orientation_counts?.vertical || 0
            } · D ${lines.orientation_counts?.diagonal || 0}`}
          </p>
        </article>
      </div>

      <details className="technical-details">
        <summary>Technical details</summary>
        <pre>{JSON.stringify(analysis, null, 2)}</pre>
      </details>
    </section>
  );
}

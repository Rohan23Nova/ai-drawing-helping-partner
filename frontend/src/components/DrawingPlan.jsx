function meterWidth(value) {
  return `${Math.round(value * 100)}%`;
}

export default function DrawingPlan({
  plan,
  guidance,
  currentStep,
  onStepChange,
  onNextStep,
  onPreviousStep
}) {
  const activeStep =
    plan.steps.find((step) => step.step === currentStep) || plan.steps[0];
  const guidanceStep =
    guidance?.steps?.find((step) => step.step === activeStep.step) || activeStep;
  const completedSteps = Math.max(activeStep.step - 1, 0);
  const progressRatio = plan.step_count > 1 ? completedSteps / (plan.step_count - 1) : 1;

  return (
    <section className="workspace-card plan-card">
      <div className="section-heading">
        <div>
          <p className="section-kicker">Drawing Plan</p>
          <h3>Move from big decisions to smaller refinements.</h3>
          <p className="section-subcopy">
            Stay with one decision at a time. The active step is your only immediate priority.
          </p>
        </div>
        <p className="section-meta">{plan.step_count} steps</p>
      </div>

      <div className="current-step-panel">
        <div className="plan-progressbar" aria-hidden="true">
          <div style={{ width: meterWidth(progressRatio) }} />
        </div>
        <p className="step-progress">
          Step {activeStep.step} of {plan.step_count}
        </p>
        <h4>{activeStep.title}</h4>
        <p className="step-instruction">{guidanceStep.guidance || activeStep.instruction}</p>
        <div className="current-step-details">
          <span>{activeStep.category.replaceAll("_", " ")}</span>
          <span>{activeStep.difficulty}</span>
          <span>{activeStep.confidence_level} confidence</span>
        </div>
        <div className="confidence-meter" aria-label={`Confidence ${Math.round(activeStep.confidence * 100)} percent`}>
          <div style={{ width: meterWidth(activeStep.confidence) }} />
        </div>
        <p className="step-purpose">
          <strong>Why:</strong> {activeStep.purpose}
        </p>
        <div className="step-nav">
          <button
            type="button"
            className="secondary-button"
            onClick={onPreviousStep}
            disabled={activeStep.step === 1}
          >
            Previous
          </button>
          <button
            type="button"
            className="primary-button"
            onClick={onNextStep}
            disabled={activeStep.step === plan.step_count}
          >
            Mark complete
          </button>
        </div>
      </div>

      <div className="timeline" aria-label="Drawing plan steps">
        {plan.steps.map((step) => {
          const isActive = step.step === activeStep.step;
          const isComplete = step.step < activeStep.step;

          return (
            <button
              key={step.step}
              type="button"
              className={`timeline-step${isActive ? " is-active" : ""}${isComplete ? " is-complete" : ""}`}
              onClick={() => onStepChange(step.step)}
            >
              <span className="timeline-index">{String(step.step).padStart(2, "0")}</span>
              <span className="timeline-copy">
                <span className="timeline-title">{step.title}</span>
                <span className="timeline-instruction">{step.instruction}</span>
                <span className="timeline-tags">
                  <span>{step.category.replaceAll("_", " ")}</span>
                  <span>{step.difficulty}</span>
                  <span>{Math.round(step.confidence * 100)}% confidence</span>
                </span>
              </span>
            </button>
          );
        })}
      </div>
    </section>
  );
}

import AnalysisPanel from "./AnalysisPanel";
import ChatPanel from "./ChatPanel";
import DrawingPlan from "./DrawingPlan";
import ReferenceViewer from "./ReferenceViewer";

export default function AnalysisWorkspace(props) {
  return (
    <main className="workspace-shell">
      <section className="workspace-overview">
        <div>
          <p className="section-kicker">Workspace</p>
          <h2>{props.filename || "Reference study"} ready for breakdown</h2>
          <p className="section-subcopy">
            Keep the reference visible, work from the current step, and use chat only when you
            need a nudge.
          </p>
        </div>
        <div className="workspace-overview-metrics" aria-label="Workspace summary">
          <div>
            <strong>{props.plan.step_count}</strong>
            <span>plan steps</span>
          </div>
          <div>
            <strong>{props.analysis.shapes?.shape_count || 0}</strong>
            <span>major forms</span>
          </div>
          <div>
            <strong>{props.analysis.lines?.line_count || 0}</strong>
            <span>structural lines</span>
          </div>
        </div>
      </section>
      <div className="workspace-grid">
        <div className="workspace-left">
          <ReferenceViewer
            originalUrl={props.originalUrl}
            edgeUrl={props.edgeUrl}
            viewMode={props.viewMode}
            onViewModeChange={props.onViewModeChange}
          />
          <AnalysisPanel analysis={props.analysis} />
        </div>
        <div className="workspace-right">
          <DrawingPlan
            plan={props.plan}
            guidance={props.guidance}
            currentStep={props.currentStep}
            onStepChange={props.onStepChange}
            onNextStep={props.onNextStep}
            onPreviousStep={props.onPreviousStep}
          />
          <ChatPanel
            messages={props.messages}
            onSendMessage={props.onSendMessage}
            isLoading={props.isChatLoading}
            error={props.chatError}
            currentStepTitle={props.currentStepTitle}
          />
        </div>
      </div>
    </main>
  );
}

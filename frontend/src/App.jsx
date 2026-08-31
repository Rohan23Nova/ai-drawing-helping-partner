import { useEffect, useMemo, useState } from "react";
import AnalysisWorkspace from "./components/AnalysisWorkspace";
import Header from "./components/Header";
import UploadView from "./components/UploadView";
import {
  getEdgeMapUrl,
  getOriginalImageUrl,
  sendChatMessage,
  updateProgress,
  uploadReference
} from "./services/api";

const loadingStages = [
  "Preparing image",
  "Finding major forms",
  "Studying proportions",
  "Building drawing plan"
];

export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [uploadError, setUploadError] = useState("");
  const [uploadState, setUploadState] = useState("idle");
  const [analysisData, setAnalysisData] = useState(null);
  const [currentStep, setCurrentStep] = useState(1);
  const [viewMode, setViewMode] = useState("original");
  const [chatMessages, setChatMessages] = useState([]);
  const [chatError, setChatError] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  const [loadingStageIndex, setLoadingStageIndex] = useState(0);

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl("");
      return undefined;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);

    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    if (uploadState !== "uploading") {
      setLoadingStageIndex(0);
      return undefined;
    }

    const intervalId = window.setInterval(() => {
      setLoadingStageIndex((current) =>
        current < loadingStages.length - 1 ? current + 1 : current
      );
    }, 900);

    return () => window.clearInterval(intervalId);
  }, [uploadState]);

  const currentPlanStep = useMemo(() => {
    return analysisData?.drawing_plan?.steps?.find((step) => step.step === currentStep) || null;
  }, [analysisData, currentStep]);

  async function handleAnalyze() {
    if (!selectedFile) {
      return;
    }

    setUploadError("");
    setUploadState("uploading");

    try {
      const response = await uploadReference(selectedFile);
      setAnalysisData(response);
      setCurrentStep(1);
      setViewMode("compare");
      setChatMessages([]);
      setChatError("");
      setUploadState("complete");
    } catch (error) {
      setUploadError(error.message);
      setUploadState("idle");
    }
  }

  async function syncStep(step) {
    setCurrentStep(step);

    if (!analysisData?.image_id) {
      return;
    }

    try {
      await updateProgress(analysisData.image_id, step);
    } catch {
      // The UI still manages local step focus even if persistence fails.
    }
  }

  async function handleSendMessage(message) {
    if (!analysisData?.image_id) {
      return false;
    }

    setChatError("");
    setIsChatLoading(true);
    setChatMessages((current) => [...current, { role: "user", content: message }]);

    try {
      const response = await sendChatMessage(analysisData.image_id, message);
      setChatMessages((current) => [...current, { role: "assistant", content: response.response }]);
      return true;
    } catch (error) {
      setChatError(error.message);
      return false;
    } finally {
      setIsChatLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <div className="background-veil" aria-hidden="true" />
      <Header />

      {!analysisData ? (
        <>
          <UploadView
            file={selectedFile}
            previewUrl={previewUrl}
            isUploading={uploadState === "uploading"}
            error={uploadError}
            loadingStageIndex={loadingStageIndex}
            onFileSelect={(file) => {
              setSelectedFile(file);
              setUploadError("");
            }}
            onRemove={() => {
              setSelectedFile(null);
              setUploadError("");
            }}
            onAnalyze={handleAnalyze}
          />

          <section className="loading-card" aria-live="polite">
            <div className="section-heading">
              <div>
                <p className="section-kicker">Workflow</p>
                <h3>Reference → Understand → Plan → Draw → Ask your partner</h3>
                <p className="section-subcopy">
                  A calm workspace for turning a single reference into a clearer first pass.
                </p>
              </div>
            </div>
            <div className="loading-list">
              {loadingStages.map((stage, index) => {
                let status = "pending";
                if (uploadState === "uploading") {
                  status =
                    index < loadingStageIndex
                      ? "complete"
                      : index === loadingStageIndex
                        ? "active"
                        : "pending";
                }

                return (
                  <div key={stage} className={`loading-row ${status}`}>
                    <span className="loading-dot" aria-hidden="true" />
                    <span>{stage}</span>
                  </div>
                );
              })}
            </div>
          </section>
        </>
      ) : (
        <AnalysisWorkspace
          originalUrl={getOriginalImageUrl(analysisData.image_id)}
          edgeUrl={getEdgeMapUrl(analysisData.image_id)}
          viewMode={viewMode}
          onViewModeChange={setViewMode}
          analysis={analysisData.analysis}
          plan={analysisData.drawing_plan}
          guidance={analysisData.guidance}
          filename={analysisData.filename}
          currentStep={currentStep}
          onStepChange={syncStep}
          onNextStep={() =>
            syncStep(Math.min(currentStep + 1, analysisData.drawing_plan.step_count))
          }
          onPreviousStep={() => syncStep(Math.max(currentStep - 1, 1))}
          messages={chatMessages}
          onSendMessage={handleSendMessage}
          isChatLoading={isChatLoading}
          chatError={chatError}
          currentStepTitle={currentPlanStep?.title}
        />
      )}
    </div>
  );
}

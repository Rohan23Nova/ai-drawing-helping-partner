import { useMemo, useRef, useState } from "react";

function formatFileSize(size) {
  if (size < 1024 * 1024) {
    return `${(size / 1024).toFixed(1)} KB`;
  }

  return `${(size / (1024 * 1024)).toFixed(1)} MB`;
}

export default function UploadView({
  file,
  previewUrl,
  isUploading,
  error,
  loadingStageIndex,
  onFileSelect,
  onRemove,
  onAnalyze
}) {
  const inputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const accepts = "image/png,image/jpeg,image/webp";

  const fileMeta = useMemo(() => {
    if (!file) {
      return null;
    }

    return {
      name: file.name,
      type: file.type.replace("image/", "").toUpperCase() || "Image",
      size: formatFileSize(file.size)
    };
  }, [file]);

  function handleFiles(files) {
    const nextFile = files?.[0];
    if (nextFile) {
      onFileSelect(nextFile);
    }
  }

  return (
    <section className="hero-shell">
      <div className="hero-copy">
        <p className="eyebrow">Your drawing companion</p>
        <h2>Study form, proportion, and placement before you chase detail.</h2>
        <p className="hero-text">
          Upload a reference and get a structured breakdown of major forms,
          relative shapes, and the next best step to draw.
        </p>
        <div className="hero-flow">
          <div>
            <span>01</span>
            <p>Upload a reference you want to understand.</p>
          </div>
          <div>
            <span>02</span>
            <p>Read the plan before committing to darker lines.</p>
          </div>
          <div>
            <span>03</span>
            <p>Ask focused questions when you hit uncertainty.</p>
          </div>
        </div>
        <div className="hero-notes" aria-label="Supported file types">
          <span>JPG</span>
          <span>PNG</span>
          <span>WEBP</span>
        </div>
      </div>

      <div className="upload-panel">
        <div
          className={[
            "upload-dropzone",
            isDragging ? "is-dragging" : "",
            file ? "has-file" : "",
            isUploading ? "is-disabled" : ""
          ]
            .filter(Boolean)
            .join(" ")}
          role="button"
          tabIndex={isUploading ? -1 : 0}
          aria-disabled={isUploading}
          onClick={() => !isUploading && inputRef.current?.click()}
          onKeyDown={(event) => {
            if ((event.key === "Enter" || event.key === " ") && !isUploading) {
              event.preventDefault();
              inputRef.current?.click();
            }
          }}
          onDragOver={(event) => {
            event.preventDefault();
            if (!isUploading) {
              setIsDragging(true);
            }
          }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={(event) => {
            event.preventDefault();
            setIsDragging(false);
            if (!isUploading) {
              handleFiles(event.dataTransfer.files);
            }
          }}
        >
          <input
            ref={inputRef}
            className="sr-only"
            type="file"
            accept={accepts}
            onChange={(event) => handleFiles(event.target.files)}
            disabled={isUploading}
          />

          {!file ? (
            <div className="upload-empty">
              <div className="sketch-mark" aria-hidden="true">
                <span />
                <span />
                <span />
              </div>
              <h3>Upload reference</h3>
              <p>Drag and drop an image here, or click to browse your files.</p>
              <div className="upload-hint-row">
                <span>Best for single subjects, objects, or simple scenes.</span>
              </div>
            </div>
          ) : (
            <div className="upload-selected">
              <div className="preview-frame">
                <img src={previewUrl} alt={`Preview of ${file.name}`} />
              </div>
              <div className="file-row">
                <div>
                  <p className="file-name">{fileMeta.name}</p>
                  <p className="file-meta">
                    {fileMeta.type} · {fileMeta.size}
                  </p>
                </div>
                <div className="file-actions">
                  <button
                    type="button"
                    className="text-button"
                    onClick={(event) => {
                      event.stopPropagation();
                      onRemove();
                    }}
                    disabled={isUploading}
                  >
                    Remove
                  </button>
                  <span className="file-state">
                    {isUploading ? `Stage ${loadingStageIndex + 1} of 4` : "Ready to analyze"}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        <div className="upload-actions">
          <button
            type="button"
            className="secondary-button"
            onClick={() => inputRef.current?.click()}
            disabled={isUploading}
          >
            {file ? "Replace" : "Choose image"}
          </button>
          <button
            type="button"
            className="primary-button"
            onClick={onAnalyze}
            disabled={!file || isUploading}
          >
            {isUploading ? "Analyzing..." : "Analyze reference"}
          </button>
        </div>

        {error ? (
          <div className="error-banner" role="alert">
            <p>We couldn&apos;t analyze this image.</p>
            <span>{error}</span>
          </div>
        ) : null}
      </div>
    </section>
  );
}

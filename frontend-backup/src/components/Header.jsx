export default function Header() {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">AI Drawing Helping Partner</p>
        <h1>Turn a reference into a calm, usable drawing plan.</h1>
      </div>
      <div className="topbar-meta" aria-label="Product support links">
        <span className="meta-pill">FastAPI backend</span>
        <span className="meta-pill">Reference workspace</span>
      </div>
    </header>
  );
}

import { useState } from "react";

import {
  Upload,
  MapPin,
  Camera,
  ShieldCheck,
  ArrowRight,
  Loader2,
  X,
  AlertTriangle,
  CheckCircle2,
  Building2,
  FileText,
  RotateCcw,
  ChevronDown,
  ChevronUp,
} from "lucide-react";

import "./App.css";


function App() {

  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);

  const [description, setDescription] = useState("");
  const [location, setLocation] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [result, setResult] = useState(null);

  const [showInstructions, setShowInstructions] = useState(false);
  const [showLetter, setShowLetter] = useState(false);


  // ==========================================================
  // IMAGE
  // ==========================================================

  const handleImageChange = (event) => {

    const file = event.target.files?.[0];

    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));

    setError("");
  };


  const removeImage = () => {

    setImage(null);
    setPreview(null);
  };


  // ==========================================================
  // ANALYZE WITH GEMMA
  // ==========================================================

  const analyzeIssue = async () => {

    if (!image) {

      setError(
        "Please upload a photograph of the issue."
      );

      return;
    }


    setLoading(true);
    setError("");
    setResult(null);


    try {

      const formData = new FormData();

      formData.append("image", image);
      formData.append("description", description);
      formData.append("location", location);


      const response = await fetch(
        "http://127.0.0.1:8000/api/analyze",
        {
          method: "POST",
          body: formData,
        }
      );


      if (!response.ok) {

        const errorData =
          await response.json().catch(() => null);

        throw new Error(
          errorData?.detail ||
          `Server returned ${response.status}`
        );
      }


      const data = await response.json();

      console.log("CiviSense analysis:", data);

      setResult(data);


    } catch (error) {

      console.error(
        "CiviSense analysis failed:",
        error
      );

      setError(
        error.message ||
        "Unable to analyze the issue."
      );

    } finally {

      setLoading(false);
    }
  };


  // ==========================================================
  // RESET
  // ==========================================================

  const resetReport = () => {

    setImage(null);
    setPreview(null);

    setDescription("");
    setLocation("");

    setResult(null);
    setError("");

    setShowInstructions(false);
    setShowLetter(false);

    window.scrollTo({
      top: 0,
      behavior: "smooth",
    });
  };


  // ==========================================================
  // RESULT HELPERS
  // ==========================================================

  const analysis =
    result?.analysis || result || {};

  const severity =
    analysis?.severity || {};

  const score =
    Number(severity?.score ?? 0);

  const level =
    severity?.level ||
    (score >= 8
      ? "HIGH PRIORITY"
      : score >= 5
        ? "MEDIUM PRIORITY"
        : "LOW PRIORITY");


  const issue =
    analysis?.issue ||
    analysis?.issue_type ||
    analysis?.category ||
    "Civic issue";


  const evidence =
    analysis?.visible_evidence ||
    analysis?.evidence ||
    [];


  const risks =
    analysis?.potential_risks ||
    analysis?.risks ||
    [];


  const authority =
    analysis?.recommended_authority ||
    analysis?.authority ||
    {};


  const instructions =
    analysis?.citizen_instructions ||
    analysis?.instructions ||
    [];


  const complaintLetter =
    analysis?.complaint_letter ||
    analysis?.letter ||
    "";


  // ==========================================================
  // APPLICATION
  // ==========================================================

  return (

    <div className="app">


      {/* ====================================================
          NAVBAR
          ==================================================== */}

      <nav className="navbar">

        <div className="brand">

          <div className="brand-mark">
            C
          </div>

          <span>
            Civi<span>Sense</span>
          </span>

        </div>


        <div className="nav-badge">

          <span className="online-dot" />

          AI Civic Intelligence

        </div>

      </nav>



      {/* ====================================================
          REPORT FORM
          ==================================================== */}

      {!result && (

        <main>

          <section className="hero">

            <div className="hero-pill">

              <ShieldCheck size={15} />

              Powered by Gemma 4

            </div>


            <h1>

              See an issue.
              <br />

              <span>Make it matter.</span>

            </h1>


            <p>

              Turn a photograph of a civic problem
              into an actionable report — intelligently.

            </p>

          </section>



          <section className="report-wrapper">

            <div className="report-card">


              {/* HEADER */}

              <div className="report-header">

                <div>

                  <h2>
                    Report a civic issue
                  </h2>

                  <p>
                    Tell us what you found and we'll
                    determine what to do next.
                  </p>

                </div>

                <Camera size={24} />

              </div>



              {/* IMAGE */}

              <div className="form-section">

                <label className="field-label">
                  Photograph
                </label>


                {!preview ? (

                  <label className="upload-box">

                    <input
                      type="file"
                      accept="image/png,image/jpeg,image/webp"
                      onChange={handleImageChange}
                    />


                    <div className="upload-icon">

                      <Upload size={25} />

                    </div>


                    <h3>
                      Upload a photograph
                    </h3>


                    <p>
                      Click to browse your device
                    </p>


                    <span className="file-types">
                      PNG · JPG · WebP
                    </span>

                  </label>

                ) : (

                  <div className="preview-box">

                    <img
                      src={preview}
                      alt="Civic issue"
                    />


                    <button
                      className="remove-image"
                      onClick={removeImage}
                      type="button"
                    >

                      <X size={17} />

                    </button>


                    <div className="image-name">

                      {image?.name}

                    </div>

                  </div>

                )}

              </div>



              {/* DESCRIPTION */}

              <div className="form-section">

                <label className="field-label">

                  What did you notice?

                </label>


                <textarea
                  value={description}
                  onChange={(event) =>
                    setDescription(event.target.value)
                  }
                  placeholder="Example: There is a large pothole near the main road..."
                  rows={4}
                />

              </div>



              {/* LOCATION */}

              <div className="form-section">

                <label className="field-label">
                  Location
                </label>


                <div className="location-input">

                  <MapPin size={18} />

                  <input
                    type="text"
                    value={location}
                    onChange={(event) =>
                      setLocation(event.target.value)
                    }
                    placeholder="City, area or nearby landmark"
                  />

                </div>

              </div>



              {/* ERROR */}

              {error && (

                <div className="error-message">

                  <AlertTriangle size={16} />

                  {error}

                </div>

              )}



              {/* BUTTON */}

              <button
                className="analyze-button"
                onClick={analyzeIssue}
                disabled={loading}
                type="button"
              >

                {loading ? (

                  <>
                    <Loader2
                      size={19}
                      className="spinner"
                    />

                    Gemma is analyzing...

                  </>

                ) : (

                  <>
                    Analyze with Gemma 4

                    <ArrowRight size={19} />

                  </>

                )}

              </button>


              <p className="privacy-note">

                CiviSense uses AI to assess the reported
                civic issue and recommend the appropriate
                next steps.

              </p>

            </div>

          </section>

        </main>

      )}



      {/* ====================================================
          RESULTS
          ==================================================== */}

      {result && (

        <main className="results-main">


          {/* RESULT HERO */}

          <section className="results-hero">

            <div className="hero-pill">

              <CheckCircle2 size={15} />

              Analysis complete

            </div>


            <h1>

              Here's what
              <br />

              <span>CiviSense found.</span>

            </h1>


            <p>

              Gemma analyzed the submitted photograph
              and generated an actionable assessment.

            </p>

          </section>



          {/* RESULTS GRID */}

          <section className="results-grid">


            {/* =================================================
                LEFT COLUMN
                ================================================= */}

            <div className="results-left">


              {/* ISSUE CARD */}

              <div className="result-card issue-card">

                <div className="card-top">

                  <div>

                    <span className="small-label">
                      DETECTED ISSUE
                    </span>

                    <h2>
                      {issue}
                    </h2>

                  </div>


                  <div className="issue-icon">
                    <AlertTriangle size={22} />
                  </div>

                </div>


                {preview && (

                  <img
                    className="result-image"
                    src={preview}
                    alt="Analyzed civic issue"
                  />

                )}

              </div>



              {/* SEVERITY */}

              <div className="result-card severity-card">

                <div className="small-label">
                  SEVERITY ASSESSMENT
                </div>


                <div className="severity-row">

                  <div>

                    <div className="score">

                      {score}

                      <span>
                        /10
                      </span>

                    </div>

                    <div className="priority">
                      {level}
                    </div>

                  </div>


                  <div className="severity-meter">

                    <div
                      className="severity-fill"
                      style={{
                        width: `${Math.min(
                          Math.max(score * 10, 0),
                          100
                        )}%`,
                      }}
                    />

                  </div>

                </div>


                {severity?.urgency && (

                  <p className="severity-description">

                    {severity.urgency}

                  </p>

                )}

              </div>



              {/* EVIDENCE */}

              {evidence.length > 0 && (

                <div className="result-card">

                  <div className="small-label">
                    VISIBLE EVIDENCE
                  </div>


                  <div className="evidence-list">

                    {evidence.map(
                      (item, index) => (

                        <div
                          className="evidence-item"
                          key={index}
                        >

                          <CheckCircle2 size={17} />

                          <span>
                            {typeof item === "string"
                              ? item
                              : JSON.stringify(item)}
                          </span>

                        </div>

                      )
                    )}

                  </div>

                </div>

              )}



              {/* RISKS */}

              {risks.length > 0 && (

                <div className="result-card">

                  <div className="small-label">
                    POTENTIAL RISKS
                  </div>


                  <div className="risk-list">

                    {risks.map(
                      (risk, index) => (

                        <div
                          className="risk-item"
                          key={index}
                        >

                          <AlertTriangle size={17} />

                          <span>
                            {typeof risk === "string"
                              ? risk
                              : JSON.stringify(risk)}
                          </span>

                        </div>

                      )
                    )}

                  </div>

                </div>

              )}

            </div>



            {/* =================================================
                RIGHT COLUMN
                ================================================= */}

            <div className="results-right">


              {/* AUTHORITY */}

              <div className="result-card authority-card">

                <div className="small-label">
                  RECOMMENDED AUTHORITY
                </div>


                <div className="authority-icon">
                  <Building2 size={23} />
                </div>


                <h2>

                  {authority?.department ||
                    authority?.authority_type ||
                    "Relevant Civic Authority"}

                </h2>


                {authority?.authority_type && (

                  <p>

                    {authority.authority_type}

                  </p>

                )}


                <div className="authority-note">

                  <ShieldCheck size={16} />

                  Contact information is sourced from
                  CiviSense's verified authority database.

                </div>

              </div>



              {/* INSTRUCTIONS */}

              {instructions.length > 0 && (

                <div className="result-card">

                  <button
                    className="expand-button"
                    onClick={() =>
                      setShowInstructions(
                        !showInstructions
                      )
                    }
                  >

                    <div>

                      <div className="small-label">
                        WHAT TO DO NEXT
                      </div>

                      <strong>
                        Citizen instructions
                      </strong>

                    </div>


                    {showInstructions
                      ? <ChevronUp size={19} />
                      : <ChevronDown size={19} />
                    }

                  </button>


                  {showInstructions && (

                    <div className="instruction-list">

                      {instructions.map(
                        (instruction, index) => (

                          <div
                            className="instruction-item"
                            key={index}
                          >

                            <span className="step-number">
                              {index + 1}
                            </span>

                            <span>
                              {typeof instruction === "string"
                                ? instruction
                                : JSON.stringify(instruction)}
                            </span>

                          </div>

                        )
                      )}

                    </div>

                  )}

                </div>

              )}



              {/* COMPLAINT LETTER */}

              {complaintLetter && (

                <div className="result-card letter-card">

                  <button
                    className="expand-button"
                    onClick={() =>
                      setShowLetter(
                        !showLetter
                      )
                    }
                  >

                    <div>

                      <div className="small-label">
                        READY TO SEND
                      </div>

                      <strong>
                        Complaint letter
                      </strong>

                    </div>


                    <FileText size={19} />

                  </button>


                  {showLetter && (

                    <div className="letter-content">

                      <pre>
                        {complaintLetter}
                      </pre>


                      <button
                        className="copy-button"
                        onClick={() =>
                          navigator.clipboard.writeText(
                            complaintLetter
                          )
                        }
                      >

                        Copy letter

                      </button>

                    </div>

                  )}

                </div>

              )}



              {/* NEW REPORT */}

              <button
                className="new-report-button"
                onClick={resetReport}
              >

                <RotateCcw size={18} />

                Report another issue

              </button>

            </div>

          </section>

        </main>

      )}



      {/* ====================================================
          FOOTER
          ==================================================== */}

      <footer>

        <div>
          CiviSense AI
        </div>

        <div>
          Built for better communities.
        </div>

      </footer>

    </div>
  );
}


export default App;
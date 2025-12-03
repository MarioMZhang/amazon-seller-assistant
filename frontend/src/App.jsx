import { useState } from 'react'
import './App.css'

function App() {
  const [sellerElfFile, setSellerElfFile] = useState(null)
  const [sifFile, setSifFile] = useState(null)
  const [brandName, setBrandName] = useState('Amazing Cosy')
  const [productType, setProductType] = useState('')
  const [topN, setTopN] = useState(50)
  const [model, setModel] = useState('gemini-2.5-flash-lite')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!sellerElfFile || !sifFile) {
      setError('Please select both XLSX files')
      return
    }

    if (!brandName.trim()) {
      setError('Please enter a brand name')
      return
    }

    if (!productType.trim()) {
      setError('Please enter a product type')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    const formData = new FormData()
    formData.append('seller_elf', sellerElfFile)
    formData.append('sif', sifFile)
    formData.append('brand_name', brandName)
    formData.append('product_type', productType)
    formData.append('top_n', topN)
    formData.append('model', model)

    try {
      const response = await fetch('http://localhost:8000/generate', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Failed to generate content')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const downloadJSON = () => {
    if (!result) return

    const blob = new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `amazon-content-${Date.now()}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div className="app">
      <header>
        <h1>Amazon Content Generator</h1>
        <p>Upload your XLSX files to generate optimized Amazon product listings</p>
      </header>

      <div className="container">
        <form onSubmit={handleSubmit} className="upload-form">
          <div className="form-section">
            <h2>Upload Files</h2>

            <div className="file-input-group">
              <label htmlFor="seller-elf">
                Seller ELF File (.xlsx)
                {sellerElfFile && <span className="file-name">{sellerElfFile.name}</span>}
              </label>
              <input
                id="seller-elf"
                type="file"
                accept=".xlsx"
                onChange={(e) => setSellerElfFile(e.target.files[0])}
                required
              />
            </div>

            <div className="file-input-group">
              <label htmlFor="sif">
                SIF File (.xlsx)
                {sifFile && <span className="file-name">{sifFile.name}</span>}
              </label>
              <input
                id="sif"
                type="file"
                accept=".xlsx"
                onChange={(e) => setSifFile(e.target.files[0])}
                required
              />
            </div>
          </div>

          <div className="form-section">
            <h2>Parameters</h2>

            <div className="input-group">
              <label htmlFor="brand-name">Brand Name</label>
              <input
                id="brand-name"
                type="text"
                value={brandName}
                onChange={(e) => setBrandName(e.target.value)}
                placeholder="e.g., Amazing Cosy"
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="product-type">Product Type</label>
              <input
                id="product-type"
                type="text"
                value={productType}
                onChange={(e) => setProductType(e.target.value)}
                placeholder="e.g., Women's Slippers, Mini Winter Boots"
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="top-n">Top N Keywords</label>
              <input
                id="top-n"
                type="number"
                min="1"
                max="200"
                value={topN}
                onChange={(e) => setTopN(parseInt(e.target.value))}
                required
              />
            </div>

            <div className="input-group">
              <label htmlFor="model">AI Model</label>
              <select
                id="model"
                value={model}
                onChange={(e) => setModel(e.target.value)}
              >
                <option value="gemini-2.5-flash-lite">Gemini 2.5 Flash Lite</option>
                <option value="gemini-2.5-flash">Gemini 2.5 Flash</option>
                <option value="gemini-2.5-pro">Gemini 2.5 Pro</option>
              </select>
            </div>
          </div>

          <button type="submit" disabled={loading} className="submit-button">
            {loading ? 'Generating...' : 'Generate Content'}
          </button>
        </form>

        {error && (
          <div className="error-message">
            <h3>Error</h3>
            <p>{error}</p>
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Generating content... This may take a minute.</p>
          </div>
        )}

        {result && (
          <div className="result">
            <div className="result-header">
              <h2>Generated Content</h2>
              <button onClick={downloadJSON} className="download-button">
                Download JSON
              </button>
            </div>

            <div className="result-sections">
              {/* Market Research */}
              <section className="result-section">
                <h3>Market Research</h3>
                <div className="info-grid">
                  <div>
                    <strong>Brand:</strong> {result.market_research?.brand_name}
                  </div>
                  <div>
                    <strong>Product:</strong> {result.market_research?.product_type}
                  </div>
                  <div>
                    <strong>Core Keywords:</strong> {result.market_research?.core_keywords?.length}
                  </div>
                  <div>
                    <strong>Competitor Brands:</strong> {result.market_research?.competitor_brands?.join(', ')}
                  </div>
                </div>
              </section>

              {/* Titles */}
              <section className="result-section">
                <h3>Titles ({result.titles?.length || 0})</h3>
                {result.titles?.map((title, idx) => (
                  <div key={idx} className="item">
                    <strong>Title {idx + 1}:</strong>
                    <p>{title}</p>
                  </div>
                ))}
              </section>

              {/* Bullet Points */}
              <section className="result-section">
                <h3>Bullet Points - Version 1</h3>
                {result.bullet_points_version_1?.map((bullet, idx) => (
                  <div key={idx} className="item">
                    <strong>Bullet {idx + 1}:</strong>
                    <p>{bullet}</p>
                  </div>
                ))}
              </section>

              <section className="result-section">
                <h3>Bullet Points - Version 2</h3>
                {result.bullet_points_version_2?.map((bullet, idx) => (
                  <div key={idx} className="item">
                    <strong>Bullet {idx + 1}:</strong>
                    <p>{bullet}</p>
                  </div>
                ))}
              </section>

              {/* Product Description */}
              <section className="result-section">
                <h3>Product Description ({result.product_description?.length || 0} characters)</h3>
                <p className="description">{result.product_description}</p>
              </section>

              {/* Search Keywords */}
              <section className="result-section">
                <h3>Search Keywords ({result.search_keywords?.split(',').length || 0} terms)</h3>
                <p>{result.search_keywords}</p>
              </section>

              {/* Quality Check */}
              <section className="result-section">
                <h3>Quality Check</h3>
                <div className="quality-status">
                  <strong>Overall Status:</strong>
                  <span className={`status ${result.quality_check_results?.overall_status?.toLowerCase()}`}>
                    {result.quality_check_results?.overall_status}
                  </span>
                </div>
                <div className="scores-grid">
                  <div className="score">
                    <strong>Grammar:</strong>
                    <span>{result.quality_check_results?.grammar_score}/10</span>
                  </div>
                  <div className="score">
                    <strong>Brand Compliance:</strong>
                    <span>{result.quality_check_results?.brand_compliance_score}/10</span>
                  </div>
                  <div className="score">
                    <strong>Amazon Guidelines:</strong>
                    <span>{result.quality_check_results?.amazon_guidelines_score}/10</span>
                  </div>
                  <div className="score">
                    <strong>Keyword Optimization:</strong>
                    <span>{result.quality_check_results?.keyword_optimization_score}/10</span>
                  </div>
                  <div className="score">
                    <strong>Content Quality:</strong>
                    <span>{result.quality_check_results?.content_quality_score}/10</span>
                  </div>
                </div>
                {result.quality_check_results?.issues?.length > 0 && (
                  <div className="issues">
                    <strong>Issues:</strong>
                    <ul>
                      {result.quality_check_results.issues.map((issue, idx) => (
                        <li key={idx}>{issue}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {result.quality_check_results?.recommendations?.length > 0 && (
                  <div className="recommendations">
                    <strong>Recommendations:</strong>
                    <ul>
                      {result.quality_check_results.recommendations.map((rec, idx) => (
                        <li key={idx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </section>

              {/* Rationale */}
              <section className="result-section">
                <h3>Recommendations & Rationale</h3>
                <div className="recommendations-grid">
                  <div>
                    <strong>Recommended Title:</strong>
                    <p>{result.rationale?.recommended_title}</p>
                  </div>
                  <div>
                    <strong>Recommended Bullets:</strong>
                    <p>{result.rationale?.recommended_bullets}</p>
                  </div>
                </div>
                <div className="rationale-section">
                  <strong>SEO Strategy:</strong>
                  <p>{result.rationale?.seo_strategy}</p>
                </div>
                <div className="rationale-section">
                  <strong>Keyword Usage:</strong>
                  <p>{result.rationale?.keyword_usage}</p>
                </div>
                <div className="rationale-section">
                  <strong>Competitive Positioning:</strong>
                  <p>{result.rationale?.competitive_positioning}</p>
                </div>
                {result.rationale?.optimization_notes && (
                  <div className="rationale-section">
                    <strong>Optimization Notes:</strong>
                    <p>{result.rationale.optimization_notes}</p>
                  </div>
                )}
              </section>

              {/* Metadata */}
              <section className="result-section metadata">
                <h3>Metadata</h3>
                <div className="info-grid">
                  <div>
                    <strong>Generated:</strong> {new Date(result.metadata?.generated_at).toLocaleString()}
                  </div>
                  <div>
                    <strong>Duration:</strong> {result.metadata?.duration_seconds?.toFixed(2)}s
                  </div>
                  <div>
                    <strong>Model:</strong> {result.metadata?.model}
                  </div>
                </div>
              </section>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

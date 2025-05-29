import React from 'react';

function PreviewControls({ 
  previewText, 
  setPreviewText, 
  isGenerating, 
  onGenerate, 
  activeStyle, 
  previewImage 
}) {
  return (
    <div className="preview-controls">
      <label className="control-label">Preview Text</label>
      <input 
        type="text"
        className="text-input"
        value={previewText}
        onChange={(e) => setPreviewText(e.target.value)}
        placeholder="Enter text to preview..."
      />
      
      <button 
        className="generate-btn"
        onClick={onGenerate}
        disabled={isGenerating}
      >
        {isGenerating && <span className="loading-spinner"></span>}
        {isGenerating ? 'Generating...' : '🎯 Generate Accurate Preview'}
      </button>
      
      <div style={{color: '#999', fontSize: '12px', marginTop: '10px'}}>
        Current Style: <strong style={{color: '#007AFF'}}>{activeStyle.name}</strong> ({activeStyle.type})
        {previewImage && <><br/>✅ Showing accurate preview</>}
      </div>
    </div>
  );
}

export default PreviewControls;
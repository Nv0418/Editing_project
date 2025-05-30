import React, { useState, useEffect } from 'react';
import StyleGrid from './components/StyleGrid';
import CanvasPreview from './components/CanvasPreview';
import { styles } from './data/styles';

function App() {
  // Initialize with localStorage or fallback to first style
  const getInitialStyle = () => {
    const savedStyleId = localStorage.getItem('vinvideo-selected-style');
    if (savedStyleId) {
      const savedStyle = styles.find(style => style.id === savedStyleId);
      if (savedStyle) {
        return savedStyle;
      }
    }
    return styles[0];
  };

  const [activeStyle, setActiveStyle] = useState(getInitialStyle);
  const [previewText, setPreviewText] = useState(() => {
    return localStorage.getItem('vinvideo-preview-text') || 'THIS IS A SAMPLE SUBTITLE';
  });
  const [hoveredStyle, setHoveredStyle] = useState(null);

  // Save to localStorage whenever activeStyle changes
  useEffect(() => {
    localStorage.setItem('vinvideo-selected-style', activeStyle.id);
  }, [activeStyle]);

  // Save to localStorage whenever previewText changes
  useEffect(() => {
    localStorage.setItem('vinvideo-preview-text', previewText);
  }, [previewText]);

  return (
    <div className="app-container">
      <div className="header">
        <h1>🎬 VinVideo Subtitle Preview</h1>
        <p>Interactive preview with instant updates</p>
      </div>
      
      <div className="main-content">
        <div className="left-panel">
          <div className="text-input-container">
            <input
              type="text"
              className="text-input"
              placeholder="Enter your subtitle text..."
              value={previewText}
              onChange={(e) => setPreviewText(e.target.value)}
            />
          </div>
          
          <StyleGrid 
            styles={styles}
            activeStyle={activeStyle}
            hoveredStyle={hoveredStyle}
            onStyleSelect={setActiveStyle}
            onStyleHover={setHoveredStyle}
          />
        </div>
        
        <div className="right-panel">
          <div className="preview-section">
            <h3>Live Preview</h3>
            <div className="canvas-container">
              <CanvasPreview 
                text={previewText}
                styleId={activeStyle.id}
                hoveredStyleId={hoveredStyle?.id}
              />
            </div>
            <div className="preview-info">
              <p><strong>Current Style:</strong> {hoveredStyle?.name || activeStyle.name}</p>
              <p><strong>Effect Type:</strong> {hoveredStyle?.type || activeStyle.type}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

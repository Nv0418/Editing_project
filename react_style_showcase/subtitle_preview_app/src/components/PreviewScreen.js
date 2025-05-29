import React from 'react';

function PreviewScreen({ previewImage, lastGeneratedText, previewText, activeStyle }) {
  const renderSubtitle = () => {
    if (previewImage && lastGeneratedText === previewText) {
      return (
        <div className="subtitle-display">
          <img 
            src={previewImage} 
            alt={`${activeStyle.name} preview`}
            onError={(e) => {
              e.target.style.display = 'none';
            }}
          />
        </div>
      );
    } else {
      return (
        <div className="subtitle-display">
          <div className="fallback-text">
            Click "Generate Accurate Preview" below<br/>
            to see pixel-perfect preview
          </div>
        </div>
      );
    }
  };

  return (
    <div className="preview-container">
      <div className="preview-screen">
        {renderSubtitle()}
      </div>
    </div>
  );
}

export default PreviewScreen;
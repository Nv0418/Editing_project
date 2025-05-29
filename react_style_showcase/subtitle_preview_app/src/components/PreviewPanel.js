import React from 'react';
import PreviewScreen from './PreviewScreen';
import PreviewControls from './PreviewControls';

function PreviewPanel({ 
  activeStyle, 
  previewText, 
  setPreviewText, 
  previewImage, 
  lastGeneratedText,
  isGenerating, 
  onGenerate 
}) {
  return (
    <div className="right-panel">
      <div className="preview-header">
        Accurate Style Preview
      </div>
      
      <PreviewScreen 
        previewImage={previewImage}
        lastGeneratedText={lastGeneratedText}
        previewText={previewText}
        activeStyle={activeStyle}
      />

      <PreviewControls
        previewText={previewText}
        setPreviewText={setPreviewText}
        isGenerating={isGenerating}
        onGenerate={onGenerate}
        activeStyle={activeStyle}
        previewImage={previewImage}
      />
    </div>
  );
}

export default PreviewPanel;
import React from 'react';

// Font configurations matching the video pipeline exactly (from FONT_VERIFICATION_REPORT.md)
const styleConfigs = {
  simple_caption: { font: '"Oswald Heavy", "Oswald", Impact, sans-serif', fontWeight: 'heavy' },
  background_caption: { font: '"Bicyclette Black", Impact, sans-serif', fontWeight: '900' },
  glow_caption: { font: '"Impact", "Arial Black", sans-serif', fontWeight: 'bold' },
  karaoke_style: { font: '"Alverata Bold Italic", serif', fontWeight: '800', fontStyle: 'italic' },
  highlight_caption: { font: '"Mazzard M Bold", Impact, sans-serif', fontWeight: 'bold' },
  deep_diver: { font: '"Publica Sans Round Bold", "Nunito", sans-serif', fontWeight: 'bold' },
  popling_caption: { font: '"Bicyclette Black", Impact, sans-serif', fontWeight: 'bold' },
  greengoblin: { font: '"Manrope ExtraBold", Impact, sans-serif', fontWeight: '800' },
  sgone_caption: { font: '"The Sgone", Impact, sans-serif', fontWeight: 'normal' }
};

function StyleCard({ style, isActive, isHovered, onClick, onMouseEnter, onMouseLeave }) {
  const styleConfig = styleConfigs[style.id] || {};
  const fontFamily = styleConfig.font || 'Arial Black';
  const fontWeight = styleConfig.fontWeight || '700';
  const fontStyle = styleConfig.fontStyle || 'normal';
  
  // Use actual preview images instead of colored rectangles
  const previewImagePath = `/style_previews_cropped/${style.id}.png`;
  
  return (
    <div 
      className={`style-card ${isActive ? 'active' : ''} ${isHovered ? 'hovered' : ''}`}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <div className="style-preview-image-container">
        <img 
          src={previewImagePath}
          alt={`${style.name} preview`}
          className="style-preview-image"
          onError={(e) => {
            // Fallback to colored rectangle if image fails to load
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'flex';
          }}
        />
        <div 
          className={`style-preview-mini ${style.mini}`}
          style={{
            fontFamily: fontFamily,
            fontWeight: fontWeight,
            fontStyle: fontStyle,
            fontSize: '11px',
            display: 'none' // Hidden by default, shown only if image fails
          }}
        >
          {style.name.toUpperCase()}
        </div>
      </div>
      <div className="style-name">
        {style.name}
      </div>
    </div>
  );
}

export default StyleCard;
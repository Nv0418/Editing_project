import React from 'react';

// Import style configurations to get font info
const styleConfigs = {
  simple_caption: { font: '"Oswald", "Arial Black", Impact, sans-serif', fontWeight: '700' },
  glow_caption: { font: '"Impact", "Arial Black", sans-serif', fontWeight: '700' },
  karaoke_style: { font: '"Shrikhand", cursive, "Arial Black", sans-serif', fontWeight: '800' },
  background_caption: { font: '"Roboto Condensed", "Arial", sans-serif', fontWeight: '900' },
  highlight_caption: { font: '"Montserrat", "Arial Black", sans-serif', fontWeight: '600' },
  dashing_caption: { font: '"Quicksand", "Arial Black", sans-serif', fontWeight: '900' },
  newscore: { font: '"Oswald", "Arial Black", sans-serif', fontWeight: '700' },
  popling_caption: { font: '"Fredoka", "Arial Black", sans-serif', fontWeight: '400' },
  whistle_caption: { font: '"Nunito", "Arial", sans-serif', fontWeight: '400' },
  karaoke_caption: { font: '"Bebas Neue", "Arial Black", sans-serif', fontWeight: '500' },
  tilted_caption: { font: '"Lobster Two", cursive, "Arial Black", sans-serif', fontWeight: '400', fontStyle: 'italic' }
};

function StyleCard({ style, isActive, isHovered, onClick, onMouseEnter, onMouseLeave }) {
  const styleConfig = styleConfigs[style.id] || {};
  const fontFamily = styleConfig.font || 'Arial Black';
  const fontWeight = styleConfig.fontWeight || '700';
  const fontStyle = styleConfig.fontStyle || 'normal';
  
  return (
    <div 
      className={`style-card ${isActive ? 'active' : ''} ${isHovered ? 'hovered' : ''}`}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <div 
        className={`style-preview-mini ${style.mini}`}
        style={{
          fontFamily: fontFamily,
          fontWeight: fontWeight,
          fontStyle: fontStyle,
          fontSize: '11px'
        }}
      >
        {style.name.toUpperCase()}
      </div>
      <div className="style-name" style={{ fontFamily: fontFamily, fontWeight: fontWeight }}>
        {style.name}
      </div>
      <div className="style-type">{style.type}</div>
    </div>
  );
}

export default StyleCard;
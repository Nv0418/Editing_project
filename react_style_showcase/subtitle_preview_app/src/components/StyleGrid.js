import React from 'react';
import StyleCard from './StyleCard';

function StyleGrid({ styles, activeStyle, hoveredStyle, onStyleSelect, onStyleHover }) {
  return (
    <div className="styles-grid-container">
      <h2>Caption Styles</h2>
      <p className="grid-subtitle">Click to select, hover to preview</p>
      
      <div className="styles-grid">
        {styles.map((style) => (
          <StyleCard
            key={style.id}
            style={style}
            isActive={activeStyle.id === style.id}
            isHovered={hoveredStyle?.id === style.id}
            onClick={() => onStyleSelect(style)}
            onMouseEnter={() => onStyleHover(style)}
            onMouseLeave={() => onStyleHover(null)}
          />
        ))}
      </div>
    </div>
  );
}

export default StyleGrid;
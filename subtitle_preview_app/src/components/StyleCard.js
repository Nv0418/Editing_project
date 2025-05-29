import React from 'react';

function StyleCard({ style, isActive, isHovered, onClick, onMouseEnter, onMouseLeave }) {
  return (
    <div 
      className={`style-card ${isActive ? 'active' : ''} ${isHovered ? 'hovered' : ''}`}
      onClick={onClick}
      onMouseEnter={onMouseEnter}
      onMouseLeave={onMouseLeave}
    >
      <div className={`style-preview-mini ${style.mini}`}>
        {style.name.toUpperCase()}
      </div>
      <div className="style-name">{style.name}</div>
      <div className="style-type">{style.type}</div>
    </div>
  );
}

export default StyleCard;
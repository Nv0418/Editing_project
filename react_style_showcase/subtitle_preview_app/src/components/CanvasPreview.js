import React, { useEffect, useRef } from 'react';

// Style configurations matching the Python JSON implementation
const styleConfigs = {
  simple_caption: {
    name: 'SIMPLE CAPTION',
    effectType: 'Outline',
    font: '"Oswald", "Arial Black", Impact, sans-serif',
    fontWeight: '700',
    fontSize: 72,
    textColor: '#FFFFFF',
    outlineColor: '#000000',
    outlineWidth: 4,
    textTransform: 'uppercase'
  },
  glow_caption: {
    name: 'GLOW CAPTION',
    effectType: 'TextShadow',
    font: '"Impact", "Arial Black", sans-serif',
    fontWeight: '700',
    fontSize: 72,
    textColor: '#FFFFFF',
    highlightedTextColor: '#FF5050',
    shadowBlur1: 18,
    shadowOpacity1: 0.8,
    shadowOpacity1Highlighted: 0.96,
    shadowBlur2: 27,
    shadowOpacity2: 0.6,
    shadowOpacity2Highlighted: 0.72,
    textTransform: 'uppercase',
    currentColorGlow: true
  },
  karaoke_style: {
    name: 'KARAOKE STYLE',
    effectType: 'DualGlow',
    font: '"Shrikhand", cursive, "Arial Black", sans-serif',
    fontWeight: '800',
    fontSize: 72,
    textColor: '#FFFFFF',
    highlightedTextColor: '#FFFF00',
    glowColor: '#FFFFFF',
    highlightedGlowColor: '#FFFF00',
    glowRadius: 0,
    textTransform: 'uppercase',
    noGlowEffects: true
  },
  background_caption: {
    name: 'BACKGROUND CAPTION',
    effectType: 'Background',
    font: '"Roboto Condensed", "Arial", sans-serif',
    fontWeight: '900',
    fontSize: 140,
    textColor: '#FFFFFF',
    outlineColor: '#000000',
    outlineWidth: 6,
    backgroundColor: '#00FFFF',
    padding: { x: 120, y: 50 },
    borderRadius: 30,
    textTransform: 'uppercase',
    hasOutline: true
  },
  highlight_caption: {
    name: 'highlight caption',
    effectType: 'Gradient Background',
    font: '"Montserrat", "Arial Black", sans-serif',
    fontWeight: '600',
    fontSize: 60,
    textColor: '#FFFFFF',
    gradientColors: ['#9B59B6', '#8E44AD'],
    padding: { x: 30, y: 15 },
    borderRadius: 8,
    textTransform: 'lowercase'
  },
  dashing_caption: {
    name: 'dashing caption',
    effectType: 'Glow',
    font: '"Quicksand", "Arial Black", sans-serif',
    fontWeight: '900',
    fontSize: 70,
    textColor: '#FFA500',
    highlightedTextColor: '#FFD700',
    glowColor: '#FF8C00',
    glowRadius: 15,
    textTransform: 'lowercase'
  },
  newscore: {
    name: 'newscore',
    effectType: 'Outline',
    font: '"Oswald", "Arial Black", sans-serif',
    fontWeight: '700',
    fontSize: 68,
    textColor: '#FFFF00',
    highlightedTextColor: '#FFFF64',
    outlineColor: '#000000',
    outlineWidth: 4,
    textTransform: 'lowercase'
  },
  popling_caption: {
    name: 'popling caption',
    effectType: 'Glow',
    font: '"Fredoka", "Arial Black", sans-serif',
    fontWeight: '400',
    fontSize: 66,
    textColor: '#FF69B4',
    highlightedTextColor: '#FF1493',
    glowColor: '#FF00FF',
    glowRadius: 18,
    textTransform: 'lowercase'
  },
  whistle_caption: {
    name: 'WHISTLE CAPTION',
    effectType: 'Gradient Background',
    font: '"Nunito", "Arial", sans-serif',
    fontWeight: '400',
    fontSize: 58,
    textColor: '#FFFFFF',
    gradientColors: ['#20B2AA', '#008B8B'],
    padding: { x: 42, y: 22 },
    borderRadius: 6,
    textTransform: 'uppercase'
  },
  karaoke_caption: {
    name: 'KARAOKE CAPTION',
    effectType: 'Outline + Glow',
    font: '"Bebas Neue", "Arial Black", sans-serif',
    fontWeight: '500',
    fontSize: 70,
    textColor: '#FFFFFF',
    outlineColor: '#008000',
    highlightedOutlineColor: '#00FF00',
    outlineWidth: 5,
    glowColor: '#00FF00',
    glowRadius: 15,
    textTransform: 'uppercase'
  },
  tilted_caption: {
    name: 'TILTED CAPTION',
    effectType: 'Glow',
    font: '"Lobster Two", cursive, "Arial Black", sans-serif',
    fontWeight: '400',
    fontStyle: 'italic',
    fontSize: 72,
    textColor: '#FFA500',
    highlightedTextColor: '#FFD700',
    glowColor: '#FF8C00',
    glowRadius: 16,
    rotation: -5,
    textTransform: 'uppercase'
  }
};

function CanvasPreview({ text, styleId, hoveredStyleId }) {
  const canvasRef = useRef(null);

  const clearCanvas = (ctx, canvas) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  };

  const drawOutlineText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Draw outline
    ctx.strokeStyle = config.outlineColor;
    ctx.lineWidth = config.outlineWidth * 2;
    ctx.lineJoin = 'round';
    ctx.strokeText(text, x, y);
    
    // Draw fill
    ctx.fillStyle = config.textColor;
    ctx.fillText(text, x, y);
  };

  const drawGlowText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Save context
    ctx.save();
    
    // Draw glow layers
    const glowSteps = 10;
    for (let i = glowSteps; i > 0; i--) {
      const alpha = (i / glowSteps) * 0.5;
      ctx.shadowColor = config.glowColor;
      ctx.shadowBlur = config.glowRadius * (i / glowSteps);
      ctx.fillStyle = config.glowColor;
      ctx.globalAlpha = alpha;
      ctx.fillText(text, x, y);
    }
    
    // Reset and draw main text
    ctx.restore();
    ctx.shadowBlur = 0;
    ctx.fillStyle = config.textColor;
    ctx.fillText(text, x, y);
  };

  const drawBackgroundText = (ctx, text, x, y, config) => {
    // Store the original font size
    const originalFontSize = config.fontSize;
    let currentFontSize = originalFontSize;
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    
    // Set font to measure text
    ctx.font = `${fontStyle} ${fontWeight} ${currentFontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Get canvas width to determine maximum text width
    const canvas = ctx.canvas;
    const maxTextWidth = canvas.width - 200; // Leave 100px margin on each side
    
    // Check if text fits, and scale down if needed
    let metrics = ctx.measureText(text);
    while (metrics.width > maxTextWidth && currentFontSize > 20) {
      currentFontSize = Math.floor(currentFontSize * 0.95);
      ctx.font = `${fontStyle} ${fontWeight} ${currentFontSize}px ${config.font}`;
      metrics = ctx.measureText(text);
    }
    
    // Calculate scaling factor for padding
    const scaleFactor = currentFontSize / originalFontSize;
    
    // Scale padding proportionally
    const scaledPaddingX = Math.floor(config.padding.x * scaleFactor);
    const scaledPaddingY = Math.floor(config.padding.y * scaleFactor);
    
    // Scale border radius proportionally if it exists
    const scaledBorderRadius = config.borderRadius ? Math.floor(config.borderRadius * scaleFactor) : 0;
    
    // Measure text with final font size
    const textWidth = metrics.width;
    const textHeight = currentFontSize;
    
    // Draw background with scaled padding
    const bgX = x - textWidth/2 - scaledPaddingX;
    const bgY = y - textHeight/2 - scaledPaddingY;
    const bgWidth = textWidth + scaledPaddingX * 2;
    const bgHeight = textHeight + scaledPaddingY * 2;
    
    if (config.gradientColors) {
      // Gradient background
      const gradient = ctx.createLinearGradient(bgX, bgY, bgX + bgWidth, bgY + bgHeight);
      gradient.addColorStop(0, config.gradientColors[0]);
      gradient.addColorStop(1, config.gradientColors[1]);
      ctx.fillStyle = gradient;
    } else {
      // Solid background
      ctx.fillStyle = config.backgroundColor;
    }
    
    // Draw rounded rectangle with scaled border radius
    if (ctx.roundRect && scaledBorderRadius > 0) {
      ctx.beginPath();
      ctx.roundRect(bgX, bgY, bgWidth, bgHeight, scaledBorderRadius);
      ctx.fill();
    } else {
      // Fallback for browsers without roundRect or no border radius
      ctx.fillRect(bgX, bgY, bgWidth, bgHeight);
    }
    
    // Draw text with outline if needed
    if (config.hasOutline) {
      ctx.strokeStyle = config.outlineColor;
      ctx.lineWidth = config.outlineWidth * 2;
      ctx.lineJoin = 'round';
      ctx.strokeText(text, x, y);
    }
    
    // Draw text fill
    ctx.fillStyle = config.textColor;
    ctx.fillText(text, x, y);
  };

  const drawTextShadowText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Split text into words for currentColor logic
    const words = text.split(' ');
    
    // Calculate total text width for centering
    const totalWidth = ctx.measureText(text).width;
    let currentX = x - totalWidth / 2;
    
    words.forEach((word, index) => {
      // Determine if this word should be highlighted (simulate word highlighting)
      // For demo purposes, highlight every 3rd word to show the effect
      const isHighlighted = index % 3 === 1;
      const wordColor = isHighlighted ? config.highlightedTextColor : config.textColor;
      
      // Measure this word
      const wordMetrics = ctx.measureText(word);
      const wordWidth = wordMetrics.width;
      const wordX = currentX + wordWidth / 2;
      
      // Save context for shadows
      ctx.save();
      
      // Draw shadow layer 2 (outer, larger blur)
      ctx.shadowColor = wordColor;
      ctx.shadowBlur = config.shadowBlur2;
      ctx.fillStyle = wordColor;
      ctx.globalAlpha = config.shadowOpacity2;
      ctx.fillText(word, wordX, y);
      
      // Draw shadow layer 1 (inner, smaller blur)
      ctx.shadowBlur = config.shadowBlur1;
      ctx.globalAlpha = config.shadowOpacity1;
      ctx.fillText(word, wordX, y);
      
      // Reset for crisp text
      ctx.restore();
      ctx.shadowBlur = 0;
      ctx.fillStyle = wordColor;
      ctx.globalAlpha = 1.0;
      ctx.fillText(word, wordX, y);
      
      // Move to next word position
      currentX += wordWidth;
      
      // Add space width if not the last word
      if (index < words.length - 1) {
        currentX += ctx.measureText(' ').width;
      }
    });
  };

  const drawDualGlowText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Split text into words for dual color logic
    const words = text.split(' ');
    
    // Calculate total text width for centering
    const totalWidth = ctx.measureText(text).width;
    let currentX = x - totalWidth / 2;
    
    words.forEach((word, index) => {
      // Determine if this word should be highlighted (simulate karaoke highlighting)
      const isHighlighted = index % 3 === 1;
      const wordColor = isHighlighted ? config.highlightedTextColor : config.textColor;
      const glowColor = isHighlighted ? config.highlightedGlowColor : config.glowColor;
      
      // Measure this word
      const wordMetrics = ctx.measureText(word);
      const wordWidth = wordMetrics.width;
      const wordX = currentX + wordWidth / 2;
      
      // Only draw glow if glowRadius > 0 and not disabled
      if (config.glowRadius > 0 && !config.noGlowEffects) {
        // Save context for glow
        ctx.save();
        
        // Draw glow layers
        const glowSteps = 8;
        for (let i = glowSteps; i > 0; i--) {
          const alpha = (i / glowSteps) * 0.6;
          ctx.shadowColor = glowColor;
          ctx.shadowBlur = config.glowRadius * (i / glowSteps);
          ctx.fillStyle = glowColor;
          ctx.globalAlpha = alpha;
          ctx.fillText(word, wordX, y);
        }
        
        // Reset for main text
        ctx.restore();
      }
      
      // Draw crisp main text (no shadow effects)
      ctx.shadowBlur = 0;
      ctx.fillStyle = wordColor;
      ctx.globalAlpha = 1.0;
      ctx.fillText(word, wordX, y);
      
      // Move to next word position
      currentX += wordWidth;
      
      // Add space width if not the last word
      if (index < words.length - 1) {
        currentX += ctx.measureText(' ').width;
      }
    });
  };

  const drawKaraokeOutlineText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Split text into words for karaoke coloring
    const words = text.split(' ');
    
    // Calculate total text width for centering
    const totalWidth = ctx.measureText(text).width;
    let currentX = x - totalWidth / 2;
    
    words.forEach((word, index) => {
      // Karaoke highlighting: simulate word being spoken (every 3rd word)
      const isHighlighted = index % 3 === 1;
      const wordColor = isHighlighted ? config.highlightedTextColor : config.textColor;
      
      // Measure this word
      const wordMetrics = ctx.measureText(word);
      const wordWidth = wordMetrics.width;
      const wordX = currentX + wordWidth / 2;
      
      // Draw outline first
      ctx.strokeStyle = config.outlineColor;
      ctx.lineWidth = config.outlineWidth * 2;
      ctx.lineJoin = 'round';
      ctx.strokeText(word, wordX, y);
      
      // Draw fill text on top
      ctx.fillStyle = wordColor;
      ctx.fillText(word, wordX, y);
      
      // Move to next word position
      currentX += wordWidth;
      
      // Add space width if not the last word
      if (index < words.length - 1) {
        currentX += ctx.measureText(' ').width;
      }
    });
  };

  const renderStyle = (ctx, canvas, styleId, text) => {
    const config = styleConfigs[styleId];
    if (!config) return;
    
    clearCanvas(ctx, canvas);
    
    // Transform text
    if (config.textTransform === 'uppercase') {
      text = text.toUpperCase();
    }
    
    const centerX = canvas.width / 2;
    // Position text in the lower third for Instagram stories
    const centerY = canvas.height * 0.8;
    
    // Apply rotation if needed
    if (config.rotation) {
      ctx.save();
      ctx.translate(centerX, centerY);
      ctx.rotate(config.rotation * Math.PI / 180);
      ctx.translate(-centerX, -centerY);
    }
    
    // Render based on effect type
    if (config.effectType === 'Outline') {
      drawOutlineText(ctx, text, centerX, centerY, config);
    } else if (config.effectType === 'Glow') {
      drawGlowText(ctx, text, centerX, centerY, config);
    } else if (config.effectType === 'TextShadow') {
      drawTextShadowText(ctx, text, centerX, centerY, config);
    } else if (config.effectType === 'DualGlow') {
      drawDualGlowText(ctx, text, centerX, centerY, config);
    } else if (config.effectType === 'KaraokeOutline') {
      drawKaraokeOutlineText(ctx, text, centerX, centerY, config);
    } else if (config.effectType === 'Background' || config.effectType === 'Gradient Background') {
      drawBackgroundText(ctx, text, centerX, centerY, config);
    } else if (config.effectType === 'Outline + Glow') {
      // Draw glow first
      drawGlowText(ctx, text, centerX, centerY, config);
      // Then outline
      drawOutlineText(ctx, text, centerX, centerY, config);
    }
    
    // Restore rotation
    if (config.rotation) {
      ctx.restore();
    }
  };

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    // Ensure canvas has no default background
    canvas.style.backgroundColor = 'transparent';
    
    const styleToRender = hoveredStyleId || styleId;
    const textToRender = text || 'THIS IS A SAMPLE SUBTITLE';
    
    renderStyle(ctx, canvas, styleToRender, textToRender);
  }, [text, styleId, hoveredStyleId]);

  return (
    <canvas 
      ref={canvasRef} 
      width={1080} 
      height={1920}
      style={{ 
        width: '100%',
        maxWidth: '400px',
        height: 'auto',
        backgroundColor: 'transparent'
      }}
    />
  );
}

export default CanvasPreview;
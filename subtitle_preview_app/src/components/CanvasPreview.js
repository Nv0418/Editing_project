import React, { useEffect, useRef } from 'react';

// Style configurations matching the Python implementation
const styleConfigs = {
  simple_caption: {
    name: 'Simple Caption',
    effectType: 'Outline',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFFFF',
    outlineColor: '#000000',
    outlineWidth: 3,
    textTransform: 'uppercase'
  },
  glow_caption: {
    name: 'Glow Caption',
    effectType: 'TextShadow',
    font: 'Arial Black',
    fontSize: 72,
    textColor: '#FFFFFF',
    highlightedTextColor: '#FF5050',
    shadowBlur1: 18,
    shadowOpacity1: 0.8,
    shadowBlur2: 27,
    shadowOpacity2: 0.6,
    textTransform: 'uppercase',
    currentColorGlow: true
  },
  karaoke_style: {
    name: 'Karaoke Style',
    effectType: 'DualGlow',
    font: '"Tide Sans 900 Dude", "Arial Black", Impact, sans-serif',
    fontSize: 72,
    fontWeight: '800',
    textColor: '#FFFFFF',
    highlightedTextColor: '#FFFF00',
    glowColor: '#FFFFFF',
    highlightedGlowColor: '#FFFF00',
    glowRadius: 0,
    textTransform: 'uppercase',
    noGlowEffects: true
  },
  background_caption: {
    name: 'Background Caption',
    effectType: 'Background',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFFFF',
    backgroundColor: '#00FFFF',
    padding: { x: 30, y: 15 },
    borderRadius: 8,
    textTransform: 'uppercase'
  },
  highlight_caption: {
    name: 'Highlight Caption',
    effectType: 'Gradient Background',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFFFF',
    gradientColors: ['#9B59B6', '#8E44AD'],
    padding: { x: 30, y: 15 },
    borderRadius: 8,
    textTransform: 'uppercase'
  },
  dashing_caption: {
    name: 'Dashing Caption',
    effectType: 'Glow',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFFFF',
    glowColor: '#FFA500',
    glowRadius: 20,
    textTransform: 'uppercase'
  },
  newscore: {
    name: 'Newscore',
    effectType: 'Outline',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFF00',
    outlineColor: '#000000',
    outlineWidth: 3,
    textTransform: 'uppercase'
  },
  popling_caption: {
    name: 'Popling Caption',
    effectType: 'Outline',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FF69B4',
    outlineColor: '#FF1493',
    outlineWidth: 3,
    textTransform: 'uppercase'
  },
  whistle_caption: {
    name: 'Whistle Caption',
    effectType: 'Gradient Background',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFFFF',
    gradientColors: ['#20B2AA', '#008B8B'],
    padding: { x: 30, y: 15 },
    borderRadius: 8,
    textTransform: 'uppercase'
  },
  karaoke_caption: {
    name: 'Karaoke Caption',
    effectType: 'Outline + Glow',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFFFFF',
    outlineColor: '#00FF00',
    outlineWidth: 3,
    glowColor: '#00FF00',
    glowRadius: 15,
    textTransform: 'uppercase'
  },
  tilted_caption: {
    name: 'Tilted Caption',
    effectType: 'Outline',
    font: 'Arial Black',
    fontSize: 60,
    textColor: '#FFA500',
    outlineColor: '#FF8C00',
    outlineWidth: 3,
    rotation: -3,
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
    ctx.font = `bold ${config.fontSize}px ${config.font}`;
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
    ctx.font = `bold ${config.fontSize}px ${config.font}`;
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
    ctx.font = `bold ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Measure text
    const metrics = ctx.measureText(text);
    const textWidth = metrics.width;
    const textHeight = config.fontSize;
    
    // Draw background
    const bgX = x - textWidth/2 - config.padding.x;
    const bgY = y - textHeight/2 - config.padding.y;
    const bgWidth = textWidth + config.padding.x * 2;
    const bgHeight = textHeight + config.padding.y * 2;
    
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
    
    // Draw rounded rectangle
    if (ctx.roundRect) {
      ctx.beginPath();
      ctx.roundRect(bgX, bgY, bgWidth, bgHeight, config.borderRadius);
      ctx.fill();
    } else {
      // Fallback for browsers without roundRect
      ctx.fillRect(bgX, bgY, bgWidth, bgHeight);
    }
    
    // Draw text
    ctx.fillStyle = config.textColor;
    ctx.fillText(text, x, y);
  };

  const drawTextShadowText = (ctx, text, x, y, config) => {
    ctx.font = `bold ${config.fontSize}px ${config.font}`;
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
    ctx.font = `${fontWeight} ${config.fontSize}px ${config.font}`;
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
    ctx.font = `bold ${config.fontSize}px ${config.font}`;
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
        maxWidth: '240px',
        height: 'auto',
        backgroundColor: 'transparent'
      }}
    />
  );
}

export default CanvasPreview;
import React, { useRef, useEffect, useState } from 'react';

// Font configurations matching the JSON config exactly - ACCURATE COLORS AND SIZES
const styleConfigs = {
  simple_caption: { 
    font: '"Oswald Heavy", "Oswald", Impact, sans-serif', 
    fontWeight: 'heavy',
    fontSize: 72,
    fontSizeHighlighted: 80,
    textTransform: 'uppercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255]
    outlineColor: 'rgb(0, 0, 0)', // [0, 0, 0]
    outlineWidth: 4,
    effectType: 'outline'
  },
  background_caption: { 
    font: '"Bicyclette Black", Impact, sans-serif', 
    fontWeight: '900',
    fontSize: 140,
    fontSizeHighlighted: 140,
    textTransform: 'uppercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255]
    backgroundColor: 'rgb(0, 51, 102)', // [0, 51, 102]
    outlineColor: 'rgb(0, 0, 0)', // [0, 0, 0]
    outlineWidth: 6,
    padding: { x: 120, y: 50 },
    borderRadius: 30,
    effectType: 'background'
  },
  glow_caption: { 
    font: '"Impact", "Arial Black", sans-serif', 
    fontWeight: 'bold',
    fontSize: 72,
    fontSizeHighlighted: 72,
    textTransform: 'uppercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255] normal
    highlightColor: 'rgb(57, 255, 20)', // [57, 255, 20] highlighted
    shadowBlur1: 18,
    shadowBlur2: 27,
    shadowOpacity1: 0.8,
    shadowOpacity2: 0.6,
    shadowOpacity1Highlighted: 0.96,
    shadowOpacity2Highlighted: 0.72,
    effectType: 'text_shadow'
  },
  karaoke_style: { 
    font: '"Alverata Bold Italic", serif', 
    fontWeight: '800',
    fontStyle: 'italic',
    fontSize: 108,
    fontSizeHighlighted: 108,
    textTransform: 'uppercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255] normal
    highlightColor: 'rgb(255, 255, 0)', // [255, 255, 0] highlighted
    effectType: 'dual_glow'
  },
  highlight_caption: { 
    font: '"Mazzard M Bold", Impact, sans-serif', 
    fontWeight: 'bold',
    fontSize: 80,
    fontSizeHighlighted: 80,
    textTransform: 'none',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255]
    highlightBgColor: 'rgb(126, 87, 194)', // [126, 87, 194]
    padding: { x: 15, y: 10 },
    borderRadius: 20,
    effectType: 'word_highlight'
  },
  deep_diver: { 
    font: '"Publica Sans Round Bold", "Nunito", sans-serif', 
    fontWeight: 'bold',
    fontSize: 70,
    fontSizeHighlighted: 70,
    textTransform: 'lowercase',
    activeTextColor: 'rgb(0, 0, 0)', // [0, 0, 0]
    inactiveTextColor: 'rgb(80, 80, 80)', // [80, 80, 80]
    backgroundColor: 'rgb(140, 140, 140)', // [140, 140, 140]
    padding: { x: 15, y: 8 },
    borderRadius: 25,
    effectType: 'deep_diver'
  },
  popling_caption: { 
    font: '"Bicyclette Black", Impact, sans-serif', 
    fontWeight: 'bold',
    fontSize: 100,
    fontSizeHighlighted: 100,
    textTransform: 'lowercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255]
    outlineColor: 'rgb(0, 0, 0)', // [0, 0, 0]
    outlineWidth: 5,
    underlineColor: 'rgb(147, 51, 234)', // [147, 51, 234]
    underlineHeight: 8, // FIX 2: Reduce underline boldness by 50% (16 -> 8)
    underlineOffset: 10,
    effectType: 'underline'
  },
  greengoblin: { 
    font: '"Manrope ExtraBold", Impact, sans-serif', 
    fontWeight: '800',
    fontSize: 108,
    fontSizeHighlighted: 108,
    textTransform: 'uppercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255] normal
    highlightColor: 'rgb(57, 255, 20)', // [57, 255, 20] highlighted
    outlineColor: 'rgb(0, 0, 0)', // [0, 0, 0]
    outlineWidth: 3,
    scaleFactor: 1.1,
    effectType: 'dual_glow'
  },
  sgone_caption: { 
    font: '"The Sgone", Impact, sans-serif', 
    fontWeight: 'normal',
    fontSize: 65,
    fontSizeHighlighted: 75,
    textTransform: 'lowercase',
    textColor: 'rgb(255, 255, 255)', // [255, 255, 255]
    outlineColor: 'rgb(0, 0, 0)', // [0, 0, 0]
    outlineWidth: 4,
    effectType: 'outline'
  }
};

function CanvasPreview({ text, styleId, hoveredStyleId }) {
  const canvasRef = useRef(null);
  const [highlightedWordIndex, setHighlightedWordIndex] = useState(0);
  const [animationId, setAnimationId] = useState(null);

  // Use hovered style if available, otherwise use active style
  const currentStyleId = hoveredStyleId || styleId;
  const config = styleConfigs[currentStyleId] || styleConfigs.simple_caption;

  useEffect(() => {
    // Clear any existing animation
    if (animationId) {
      clearInterval(animationId);
    }

    // Start word highlighting animation for ALL styles EXCEPT SGONE and Simple Caption
    if (currentStyleId !== 'sgone_caption' && currentStyleId !== 'simple_caption') {
      const words = text.split(' ');
      if (words.length > 1) {
        const id = setInterval(() => {
          setHighlightedWordIndex(prev => (prev + 1) % words.length);
        }, 800);
        setAnimationId(id);
      }
    }

    return () => {
      if (animationId) {
        clearInterval(animationId);
      }
    };
  }, [text, currentStyleId]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    
    // Set canvas to fill the entire preview container (9:16 aspect ratio)
    const container = canvas.parentElement;
    const containerWidth = container.clientWidth;
    const containerHeight = container.clientHeight;
    
    // Calculate dimensions to maintain 9:16 aspect ratio
    let width, height;
    if (containerWidth / containerHeight > 9 / 16) {
      // Container is wider than 9:16, fit to height
      height = containerHeight;
      width = height * (9 / 16);
    } else {
      // Container is taller than 9:16, fit to width
      width = containerWidth;
      height = width * (16 / 9);
    }
    
    canvas.width = width * dpr;
    canvas.height = height * dpr;
    canvas.style.width = width + 'px';
    canvas.style.height = height + 'px';
    
    ctx.scale(dpr, dpr);
    
    // Clear canvas with black background
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, width, height);
    
    // Configure text rendering with auto-scaling for longer text
    const baseVideoWidth = 1080; // Video pipeline uses 1080x1920
    const scaleFactor = width / baseVideoWidth; // Scale based on actual video resolution
    let baseFontSize = config.fontSize;
    let fontSize = Math.round(baseFontSize * scaleFactor);
    
    // AUTO-SCALING: Reduce font size for longer text to fit canvas width (do this BEFORE Simple Caption multiplier)
    ctx.font = `${config.fontStyle || 'normal'} ${config.fontWeight} ${fontSize}px ${config.font}`;
    const maxWidth = width * 0.85; // Use 85% of canvas width as max
    const textWidth = ctx.measureText(text).width;
    
    if (textWidth > maxWidth) {
      // Calculate scaling factor to fit text
      const textScaleFactor = maxWidth / textWidth;
      fontSize = Math.round(fontSize * textScaleFactor);
    }
    
    // FIX 1: Apply Simple Caption multiplier AFTER auto-scaling to prevent it from being cancelled out
    if (currentStyleId === 'simple_caption') {
      fontSize = Math.round(fontSize * 3.5); // Increase to match glow caption size
    }
    
    // Apply final font size
    ctx.font = `${config.fontStyle || 'normal'} ${config.fontWeight} ${fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    const words = text.split(' ');
    const centerX = width / 2;
    const centerY = height * 0.75; // Bottom positioning like Instagram
    
    // Calculate total text width for positioning
    const spacing = 8;
    let totalWidth = 0;
    const wordWidths = words.map(word => {
      const width = ctx.measureText(word).width;
      totalWidth += width;
      return width;
    });
    totalWidth += (words.length - 1) * spacing;
    
    // Special handling for Simple Caption - render as unified text with correct font size
    if (currentStyleId === 'simple_caption') {
      // Re-set font to ensure correct size for full text rendering
      ctx.font = `${config.fontStyle || 'normal'} ${config.fontWeight} ${fontSize}px ${config.font}`;
      
      // Outline
      ctx.strokeStyle = config.outlineColor;
      ctx.lineWidth = config.outlineWidth * scaleFactor;
      ctx.strokeText(text, centerX, centerY);
      
      // Text fill
      ctx.fillStyle = config.textColor;
      ctx.fillText(text, centerX, centerY);
      
      return; // Skip the word-by-word rendering
    }
    
    let currentX = centerX - totalWidth / 2;
    
    // Handle styles that need full-text rendering first (background_caption, deep_diver, simple_caption)
    if (currentStyleId === 'background_caption') {
      renderBackgroundCaptionStyle(ctx, words, highlightedWordIndex, centerX, centerY, config, scaleFactor, fontSize);
    } else if (currentStyleId === 'deep_diver') {
      renderDeepDiverStyle(ctx, words, highlightedWordIndex, centerX, centerY, config, scaleFactor, fontSize);
    } else {
      // Handle word-by-word styles
      words.forEach((word, index) => {
        // FIX 3: SGONE Caption should be completely static (no highlighting)
        const isHighlighted = currentStyleId === 'sgone_caption' ? false : index === highlightedWordIndex;
        const wordWidth = wordWidths[index];
        const wordCenterX = currentX + wordWidth / 2;
        
        switch (currentStyleId) {
          case 'glow_caption':
            renderGlowCaptionStyle(ctx, word, wordCenterX, centerY, isHighlighted, config, fontSize);
            break;
          case 'karaoke_style':
            renderKaraokeStyle(ctx, word, wordCenterX, centerY, isHighlighted, config, fontSize);
            break;
          case 'highlight_caption':
            renderHighlightCaptionStyle(ctx, word, wordCenterX, centerY, isHighlighted, config, scaleFactor, fontSize);
            break;
          case 'popling_caption':
            renderPoplingCaptionStyle(ctx, word, wordCenterX, centerY, isHighlighted, config, fontSize);
            break;
          case 'greengoblin':
            renderGreenGoblinStyle(ctx, word, wordCenterX, centerY, isHighlighted, config, scaleFactor, fontSize);
            break;
          case 'sgone_caption':
          default:
            renderOutlineStyle(ctx, word, wordCenterX, centerY, isHighlighted, config, scaleFactor, fontSize);
        }
        
        currentX += wordWidth + spacing;
      });
    }
    
  }, [text, currentStyleId, highlightedWordIndex]);

  // Style-specific rendering functions matching video pipeline exactly
  
  function renderOutlineStyle(ctx, word, x, y, isHighlighted, config, scaleFactor, fontSize) {
    // Apply size scaling for highlighted words (simple_caption and sgone_caption)
    if (isHighlighted && config.fontSizeHighlighted !== config.fontSize) {
      ctx.save();
      const scale = config.fontSizeHighlighted / config.fontSize;
      ctx.translate(x, y);
      ctx.scale(scale, scale);
      ctx.translate(-x, -y);
    }
    
    // Outline (stroke)
    ctx.strokeStyle = config.outlineColor;
    ctx.lineWidth = config.outlineWidth * scaleFactor;
    ctx.strokeText(word, x, y);
    
    // Text fill
    ctx.fillStyle = config.textColor;
    ctx.fillText(word, x, y);
    
    if (isHighlighted && config.fontSizeHighlighted !== config.fontSize) {
      ctx.restore();
    }
  }

  function renderBackgroundCaptionStyle(ctx, words, highlightedIndex, centerX, centerY, config, scaleFactor, fontSize) {
    // Background Caption renders all words together with single background
    const fullText = words.join(' ');
    const metrics = ctx.measureText(fullText);
    
    // Use very small padding to match actual video output (like "IRON KINGDOMS RISE")
    const paddingX = 8 * scaleFactor;  // Much smaller to match video output
    const paddingY = 4 * scaleFactor;  // Much smaller to match video output
    
    // Background rectangle - tight fit around text (using dynamic fontSize)
    const bgWidth = metrics.width + (paddingX * 2);
    const bgHeight = fontSize * 0.8 + (paddingY * 2);
    const bgX = centerX - bgWidth / 2;
    const bgY = centerY - bgHeight / 2;
    
    ctx.fillStyle = config.backgroundColor;
    ctx.beginPath();
    ctx.roundRect(bgX, bgY, bgWidth, bgHeight, config.borderRadius * scaleFactor * 0.3);
    ctx.fill();
    
    // Text with outline
    ctx.strokeStyle = config.outlineColor;
    ctx.lineWidth = config.outlineWidth * scaleFactor;
    ctx.strokeText(fullText, centerX, centerY);
    
    ctx.fillStyle = config.textColor;
    ctx.fillText(fullText, centerX, centerY);
  }

  function renderGlowCaptionStyle(ctx, word, x, y, isHighlighted, config) {
    // Two-layer shadow system from text_shadow config
    const currentColor = isHighlighted ? config.highlightColor : config.textColor;
    
    // Layer 1 shadow (inner glow)
    const opacity1 = isHighlighted ? config.shadowOpacity1Highlighted : config.shadowOpacity1;
    ctx.shadowColor = currentColor.replace('rgb', 'rgba').replace(')', `, ${opacity1})`);
    ctx.shadowBlur = config.shadowBlur1;
    ctx.shadowOffsetX = 0;
    ctx.shadowOffsetY = 0;
    ctx.fillStyle = currentColor;
    ctx.fillText(word, x, y);
    
    // Layer 2 shadow (outer glow)
    const opacity2 = isHighlighted ? config.shadowOpacity2Highlighted : config.shadowOpacity2;
    ctx.shadowColor = currentColor.replace('rgb', 'rgba').replace(')', `, ${opacity2})`);
    ctx.shadowBlur = config.shadowBlur2;
    ctx.fillText(word, x, y);
    
    // Clean text on top
    ctx.shadowBlur = 0;
    ctx.fillStyle = currentColor;
    ctx.fillText(word, x, y);
  }

  function renderKaraokeStyle(ctx, word, x, y, isHighlighted, config) {
    // Two-tone text effect (no glow as specified in JSON)
    ctx.fillStyle = isHighlighted ? config.highlightColor : config.textColor;
    ctx.fillText(word, x, y);
  }

  function renderHighlightCaptionStyle(ctx, word, x, y, isHighlighted, config, scaleFactor) {
    // Background highlight for highlighted word only
    if (isHighlighted) {
      const metrics = ctx.measureText(word);
      const padding = config.padding;
      const paddingX = padding.x * scaleFactor;
      const paddingY = padding.y * scaleFactor;
      
      ctx.fillStyle = config.highlightBgColor;
      ctx.beginPath();
      ctx.roundRect(
        x - metrics.width / 2 - paddingX,
        y - config.fontSize * scaleFactor * 0.4 - paddingY,
        metrics.width + paddingX * 2,
        config.fontSize * scaleFactor * 0.8 + paddingY * 2,
        config.borderRadius * scaleFactor
      );
      ctx.fill();
    }
    
    // Text (always white as per JSON)
    ctx.fillStyle = config.textColor;
    ctx.fillText(word, x, y);
  }

  function renderDeepDiverStyle(ctx, words, highlightedIndex, centerX, centerY, config, scaleFactor) {
    // Deep Diver renders all words together with single gray background
    const fullText = words.join(' ');
    const metrics = ctx.measureText(fullText);
    const padding = config.padding;
    
    // Scale padding
    const paddingX = padding.x * scaleFactor;
    const paddingY = padding.y * scaleFactor;
    
    // Single background for all words
    const bgWidth = metrics.width + (paddingX * 2);
    const bgHeight = config.fontSize * scaleFactor + (paddingY * 2);
    const bgX = centerX - bgWidth / 2;
    const bgY = centerY - bgHeight / 2;
    
    ctx.fillStyle = config.backgroundColor;
    ctx.beginPath();
    ctx.roundRect(bgX, bgY, bgWidth, bgHeight, config.borderRadius * scaleFactor);
    ctx.fill();
    
    // Render words individually with different colors
    const spacing = 8;
    let totalWidth = 0;
    const wordWidths = words.map(word => {
      const width = ctx.measureText(word).width;
      totalWidth += width;
      return width;
    });
    totalWidth += (words.length - 1) * spacing;
    
    let currentX = centerX - totalWidth / 2;
    words.forEach((word, index) => {
      const isHighlighted = index === highlightedIndex;
      const wordWidth = wordWidths[index];
      const wordCenterX = currentX + wordWidth / 2;
      
      // Text color based on highlight state
      ctx.fillStyle = isHighlighted ? config.activeTextColor : config.inactiveTextColor;
      ctx.fillText(word, wordCenterX, centerY);
      
      currentX += wordWidth + spacing;
    });
  }

  function renderPoplingCaptionStyle(ctx, word, x, y, isHighlighted, config) {
    // Outline
    ctx.strokeStyle = config.outlineColor;
    ctx.lineWidth = config.outlineWidth;
    ctx.strokeText(word, x, y);
    
    // Text
    ctx.fillStyle = config.textColor;
    ctx.fillText(word, x, y);
    
    // Underline for highlighted word
    if (isHighlighted) {
      const metrics = ctx.measureText(word);
      ctx.fillStyle = config.underlineColor;
      
      // Check if word has descenders (y, g, j, p, q) and adjust underline position
      const hasDescenders = /[ygpqj]/i.test(word);
      const baseOffset = config.underlineOffset;
      const underlineY = hasDescenders ? y + baseOffset + 8 : y + baseOffset; // Extra space for descenders
      
      ctx.fillRect(
        x - metrics.width / 2,
        underlineY,
        metrics.width,
        config.underlineHeight
      );
    }
  }

  function renderGreenGoblinStyle(ctx, word, x, y, isHighlighted, config, scaleFactor) {
    // Outline (same for all words)
    ctx.strokeStyle = config.outlineColor;
    ctx.lineWidth = config.outlineWidth * scaleFactor;
    ctx.strokeText(word, x, y);
    
    // Text with color change ONLY (no size scaling)
    ctx.fillStyle = isHighlighted ? config.highlightColor : config.textColor;
    ctx.fillText(word, x, y);
  }

  return (
    <canvas 
      ref={canvasRef}
      className="subtitle-canvas"
      style={{
        width: '100%',
        height: '100%',
        backgroundColor: '#000',
        borderRadius: '8px'
      }}
    />
  );
}

export default CanvasPreview;
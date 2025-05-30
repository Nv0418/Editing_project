import React, { useEffect, useRef, useState } from 'react';

// 🎨 STYLE CONFIGURATIONS - This is where the magic happens!
// These configs define how each subtitle style should look in the React preview
// ⚠️ IMPORTANT: These should match subtitle_styles/config/subtitle_styles_v3.json exactly!
const styleConfigs = {
  // 📖 SIMPLE CAPTION - Clean educational style
  // Used for: Tutorials, how-to content, clear messaging
  simple_caption: {
    name: 'SIMPLE CAPTION',
    effectType: 'Outline', // Just text with a border around it
    font: '"Oswald", "Arial Black", Impact, sans-serif', // Font fallback chain
    fontWeight: '700', // Bold text
    fontSize: 98, // STANDARDIZED: Matching background_caption size
    textColor: '#FFFFFF', // White text
    outlineColor: '#000000', // Black border around text
    outlineWidth: 4, // Border thickness
    textTransform: 'uppercase' // MAKES TEXT ALL CAPS
  },
  // ✨ GLOW CAPTION - Gaming/tech style with neon vibes
  // Used for: Gaming content, tech tutorials, cyberpunk aesthetic
  glow_caption: {
    name: 'GLOW CAPTION',
    effectType: 'TextShadow', // Text with glowing shadow effects
    font: '"Impact", "Arial Black", sans-serif', // Chunky, bold fonts
    fontWeight: '700',
    fontSize: 98, // STANDARDIZED: Matching background_caption size
    textColor: '#FFFFFF', // Base text is white
    highlightedTextColor: '#39FF14', // When word is "spoken", turns this neon green color
    shadowBlur1: 18, // Inner glow radius (smaller)
    shadowOpacity1: 0.8, // Inner glow strength (normal state)
    shadowOpacity1Highlighted: 0.96, // Inner glow strength (highlighted state)
    shadowBlur2: 27, // Outer glow radius (bigger)
    shadowOpacity2: 0.6, // Outer glow strength (normal state)
    shadowOpacity2Highlighted: 0.72, // Outer glow strength (highlighted state)
    textTransform: 'uppercase',
    currentColorGlow: true // Glow color changes with text color (magic!)
  },
  // 🎤 KARAOKE STYLE - Y2K nostalgia vibes
  // Used for: Music content, sing-alongs, entertainment, retro aesthetic
  karaoke_style: {
  name: 'KARAOKE STYLE',
    effectType: 'DualGlow', // Changed to DualGlow to use word coloring without glow
    font: '"Alverata Bold Italic"', // Custom italic font for elegant karaoke style
    fontWeight: '700',
    fontStyle: 'italic',
    fontSize: 98, // STANDARDIZED: Matching background_caption size
    textColor: '#FFFFFF', // Base text is white
    highlightedTextColor: '#FFFF00', // When word is "spoken", turns bright yellow
    glowColor: '#FFFFFF', // Glow color for normal words (won't be used)
    highlightedGlowColor: '#FFFF00', // Glow color for highlighted words (won't be used)
    glowRadius: 0, // No glow radius - completely disabled
    textTransform: 'uppercase',
    noGlowEffects: true // Disable all glow effects
  },
  // 📺 BACKGROUND CAPTION - Professional news/sports ticker style
  // Used for: Breaking news, sports updates, professional announcements
  // 🎯 EXACT MATCH to JSON config: subtitle_styles_v3.json
  // 
  // ✅ UPDATED SPECIFICATIONS:
  // - Font: Bicyclette-Black.ttf (matches video output)
  // - Background: RGB(0,51,102) dark blue (was cyan)
  // - Auto-scaling: 5% reduction until text fits (JSON logic)
  // - Max width: 836px usable area (calculated from JSON margins)
  // - All other specs match the "IRON KINGDOMS RISE" video exactly
  background_caption: {
    name: 'BACKGROUND CAPTION',
    effectType: 'Background',
    font: '"Bicyclette Black"', // EXACT MATCH: Only use Bicyclette Black, no fallbacks
    fontWeight: '900', // Extra bold to match TTF weight
    fontSize: 98, // DECREASED by 30% from 140px
    textColor: '#FFFFFF',
    outlineColor: '#000000',
    outlineWidth: 6,
    backgroundColor: 'rgb(0, 51, 102)', // EXACT: RGB(0,51,102) from JSON config
    backgroundOpacity: 1.0,
    padding: { x: 70, y: 35 }, // DECREASED by 30% to match font size reduction
    borderRadius: 21, // DECREASED by 30% from 30px
    textTransform: 'uppercase',
    hasOutline: true,
    lineHeight: 1.1,
    autoScale: true,
    maxTextWidth: 836,
    minFontSize: 20
  },
  highlight_caption: {
    name: 'highlight caption',
    effectType: 'Gradient Background',
    font: '"Montserrat", "Arial Black", sans-serif',
    fontWeight: '600',
    fontSize: 98, // STANDARDIZED: Matching background_caption size
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
    fontSize: 98, // STANDARDIZED: Matching background_caption size
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
    fontSize: 98, // STANDARDIZED: Matching background_caption size
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
    fontSize: 98, // STANDARDIZED: Matching background_caption size
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
    fontSize: 98, // STANDARDIZED: Matching background_caption size
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
    fontSize: 98, // STANDARDIZED: Matching background_caption size
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
    fontSize: 98, // STANDARDIZED: Matching background_caption size
    textColor: '#FFA500',
    highlightedTextColor: '#FFD700',
    glowColor: '#FF8C00',
    glowRadius: 16,
    rotation: -5,
    textTransform: 'uppercase'
  }
};

// 🖼️ MAIN CANVAS COMPONENT - This is what you see in the preview!
// Props:
// - text: The subtitle text to display
// - styleId: Which style is currently selected
// - hoveredStyleId: Which style is being hovered over (for preview)
function CanvasPreview({ text, styleId, hoveredStyleId }) {
  const canvasRef = useRef(null); // Reference to the HTML5 canvas element
  const [fontReady, setFontReady] = useState(false); // Track if Bicyclette Black is ready

  // 🔤 ENSURE BICYCLETTE BLACK LOADS PROPERLY
  useEffect(() => {
    // Wait for document fonts to be ready first
    document.fonts.ready.then(() => {
      // Check if Bicyclette Black is available
      if (document.fonts.check('900 100px "Bicyclette Black"')) {
        console.log('✅ Bicyclette Black already available');
        setFontReady(true);
      } else {
        console.log('⏳ Loading Bicyclette Black font...');
        // Force a re-render after a delay to let CSS @font-face load
        setTimeout(() => {
          setFontReady(true);
          console.log('✅ Font loading timeout complete, rendering now');
        }, 1000);
      }
    });
  }, []);

  // 🧽 CLEAR CANVAS - Wipe the slate clean and make it black
  // This creates the black Instagram-style background
  const clearCanvas = (ctx, canvas) => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // Erase everything
    ctx.fillStyle = '#000000'; // Set brush to black
    ctx.fillRect(0, 0, canvas.width, canvas.height); // Paint entire canvas black
  };

  // ✏️ DRAW OUTLINE TEXT - For styles like Simple Caption
  // This draws text with a border around it (like outlined letters)
  const drawOutlineText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`; // Set the font
    ctx.textAlign = 'center'; // Center the text horizontally
    ctx.textBaseline = 'middle'; // Center the text vertically
    
    // First, draw the outline (border around text)
    ctx.strokeStyle = config.outlineColor; // Set outline color
    ctx.lineWidth = config.outlineWidth * 2; // Make outline thick
    ctx.lineJoin = 'round'; // Smooth corners on outline
    ctx.strokeText(text, x, y); // Draw the outline
    
    // Then, draw the text fill (the inside color)
    ctx.fillStyle = config.textColor; // Set text color
    ctx.fillText(text, x, y); // Draw the filled text on top
  };

  // ✨ DRAW GLOW TEXT - For styles like Dashing Caption
  // This creates that cool neon/cyberpunk glowing effect
  const drawGlowText = (ctx, text, x, y, config) => {
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    ctx.font = `${fontStyle} ${fontWeight} ${config.fontSize}px ${config.font}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Save the current canvas state (so we can restore it later)
    ctx.save();
    
    // Draw multiple glow layers (like onion layers - creates the glow effect)
    const glowSteps = 10; // How many glow layers to draw
    for (let i = glowSteps; i > 0; i--) {
      const alpha = (i / glowSteps) * 0.5; // Each layer gets more transparent
      ctx.shadowColor = config.glowColor; // Color of the glow
      ctx.shadowBlur = config.glowRadius * (i / glowSteps); // Blur size decreases
      ctx.fillStyle = config.glowColor;
      ctx.globalAlpha = alpha; // Make this layer semi-transparent
      ctx.fillText(text, x, y); // Draw the glow layer
    }
    
    // Reset to normal and draw the main crisp text on top
    ctx.restore(); // Bring back original canvas state
    ctx.shadowBlur = 0; // No shadow for main text
    ctx.fillStyle = config.textColor; // Main text color
    ctx.fillText(text, x, y); // Draw the sharp text on top
  };

  // 📦 DRAW BACKGROUND TEXT - For styles like Background Caption
  // This puts a colored box behind the text (like a news ticker)
  const drawBackgroundText = (ctx, text, x, y, config) => {
    // Store the original font size (we might need to shrink it if text is too long)
    const originalFontSize = config.fontSize;
    let currentFontSize = originalFontSize;
    const fontWeight = config.fontWeight || 'bold';
    const fontStyle = config.fontStyle || 'normal';
    
    // Set font to measure text
    const fontString = `${fontStyle} ${fontWeight} ${currentFontSize}px ${config.font}`;
    ctx.font = fontString;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    // Debug: Log what font is actually being used
    console.log('🎨 Background Caption Font String:', fontString);
    
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
      // Solid background with proper opacity handling
      if (config.backgroundOpacity !== undefined && config.backgroundOpacity < 1.0) {
        // Extract RGB values and apply opacity
        const bgColor = config.backgroundColor;
        if (bgColor.startsWith('rgb(')) {
          // Handle rgb(r,g,b) format - convert to rgba
          const rgbValues = bgColor.match(/\d+/g);
          ctx.fillStyle = `rgba(${rgbValues[0]}, ${rgbValues[1]}, ${rgbValues[2]}, ${config.backgroundOpacity})`;
        } else {
          // Handle hex colors
          ctx.fillStyle = config.backgroundColor;
        }
      } else {
        // Full opacity
        ctx.fillStyle = config.backgroundColor;
      }
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

  // 🎬 MAIN RENDER FUNCTION - This is the director!
  // It takes a style and makes the magic happen on the canvas
  const renderStyle = (ctx, canvas, styleId, text) => {
    const config = styleConfigs[styleId]; // Get the style configuration
    if (!config) return; // If style doesn't exist, bail out
    
    clearCanvas(ctx, canvas); // Start with a clean black canvas
    
    // Transform text based on style (uppercase/lowercase)
    if (config.textTransform === 'uppercase') {
      text = text.toUpperCase(); // MAKE IT SHOUT!
    }
    
    const centerX = canvas.width / 2; // Middle of canvas horizontally
    // Position text in the lower third for Instagram stories (like real subtitles!)
    const centerY = canvas.height * 0.8; // 80% down from top
    
    // Apply rotation if needed (like for Tilted Caption)
    if (config.rotation) {
      ctx.save(); // Save current state
      ctx.translate(centerX, centerY); // Move to text center
      ctx.rotate(config.rotation * Math.PI / 180); // Rotate by degrees
      ctx.translate(-centerX, -centerY); // Move back
    }
    
    // 🎨 THE BIG SWITCH - Choose how to draw based on effect type
    if (config.effectType === 'Outline') {
      drawOutlineText(ctx, text, centerX, centerY, config); // Simple outline style
    } else if (config.effectType === 'Glow') {
      drawGlowText(ctx, text, centerX, centerY, config); // Glowing neon style
    } else if (config.effectType === 'TextShadow') {
      drawTextShadowText(ctx, text, centerX, centerY, config); // Shadow/glow that changes color
    } else if (config.effectType === 'DualGlow') {
      drawDualGlowText(ctx, text, centerX, centerY, config); // Karaoke-style word coloring
    } else if (config.effectType === 'KaraokeOutline') {
      drawKaraokeOutlineText(ctx, text, centerX, centerY, config); // Outline with word coloring
    } else if (config.effectType === 'Background' || config.effectType === 'Gradient Background') {
      drawBackgroundText(ctx, text, centerX, centerY, config); // Text with colored background box
    } else if (config.effectType === 'Outline + Glow') {
      // Combo style: glow + outline
      drawGlowText(ctx, text, centerX, centerY, config); // Draw glow first (behind)
      drawOutlineText(ctx, text, centerX, centerY, config); // Then outline on top
    }
    
    // Restore rotation state if we rotated
    if (config.rotation) {
      ctx.restore(); // Go back to normal orientation
    }
  };

  // 🔄 REACT EFFECT - This runs whenever something changes
  // It watches for changes in text, selected style, or hovered style
  useEffect(() => {
    const canvas = canvasRef.current; // Get the canvas element
    if (!canvas) return; // If no canvas, do nothing
    
    const ctx = canvas.getContext('2d'); // Get the drawing context (like a paintbrush)
    
    // Make sure canvas background is transparent (we handle the black background ourselves)
    canvas.style.backgroundColor = 'transparent';
    
    // Decide which style to show: hovered style takes priority over selected style
    const styleToRender = hoveredStyleId || styleId;
    // Use custom text if provided, otherwise show default demo text
    const textToRender = text || 'THIS IS A SAMPLE SUBTITLE';
    
    // 🎬 ACTION! Render the subtitle with the chosen style
    renderStyle(ctx, canvas, styleToRender, textToRender);
  }, [text, styleId, hoveredStyleId, fontReady]); // Re-run when any of these values change

  // 📱 RETURN THE CANVAS - This is what shows up on your screen!
  return (
    <canvas 
      ref={canvasRef} // Connect this to our canvas reference
      width={1080}  // Instagram Stories width (actual pixels)
      height={1920} // Instagram Stories height (actual pixels) 
      style={{ 
        width: '100%',        // Scale to fit container
        maxWidth: '400px',    // Don't get too big
        height: 'auto',       // Keep aspect ratio
        backgroundColor: 'transparent' // Let our black background show through
      }}
    />
  );
}

// 🚀 EXPORT THE COMPONENT - Make it available to other files
// This component is used in the main App.js to show subtitle previews
export default CanvasPreview;
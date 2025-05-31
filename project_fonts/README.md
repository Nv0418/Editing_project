# VinVideo Project Fonts

This directory contains all the custom fonts required for the 9 professional subtitle styles in the VinVideo project. These fonts ensure consistency across different development environments and laptops.

## Font List and Usage

### 1. **Oswald-Heavy.ttf**
- **Used in**: Simple Caption
- **Style**: Educational, tutorial content
- **License**: SIL Open Font License

### 2. **Bicyclette-Black.ttf**
- **Used in**: Background Caption, Popling Caption
- **Style**: News-style, professional announcements, playful content
- **License**: Commercial license required

### 3. **Impact.ttf**
- **Used in**: Glow Caption
- **Style**: Gaming, tech content with neon effects
- **License**: System font (included with most OS)

### 4. **alverata-bold-italic.ttf**
- **Used in**: Karaoke Style
- **Style**: Y2K nostalgic karaoke for music and entertainment
- **License**: Commercial license required

### 5. **Manrope-ExtraBold.ttf**
- **Used in**: Green Goblin
- **Style**: Clean dynamic highlighting without glow effects
- **License**: SIL Open Font License

### 6. **mazzard-m-bold.otf**
- **Used in**: Highlight Caption (Hormozi Style)
- **Style**: Motivational, business content
- **License**: Commercial license required

### 7. **PublicaSansRound-Bd.otf**
- **Used in**: Deep Diver
- **Style**: Philosophical, contemplative content
- **License**: SIL Open Font License

### 8. **The Sgone.otf**
- **Used in**: Sgone Caption
- **Style**: Artistic content with distinctive typography
- **License**: Custom font

### 9. **Nunito-Regular.ttf**
- **Used in**: Whistle Caption
- **Style**: Calming wellness & ASMR content
- **License**: SIL Open Font License

### 10. **BebasNeue-Regular.ttf**
- **Used in**: Karaoke Caption (Live Caption)
- **Style**: Dynamic live streaming & sports content
- **License**: SIL Open Font License

### 11. **LobsterTwo-Italic.ttf**
- **Used in**: Tilted Caption
- **Style**: Comedy & meme content with quirky tilt
- **License**: SIL Open Font License

### 12. **Quicksand-Bold.ttf**
- **Used in**: Dashing Caption
- **Style**: Fashion & lifestyle content
- **License**: SIL Open Font License

## Installation Instructions

### For Development Setup:
1. Copy all fonts from this directory to your system fonts folder:
   - **macOS**: `/Users/[username]/Library/Fonts/` or `/Library/Fonts/`
   - **Windows**: `C:\Windows\Fonts\`
   - **Linux**: `/usr/share/fonts/` or `~/.local/share/fonts/`

2. Restart your development environment after font installation

### For Automated Setup:
The subtitle styles system automatically references these fonts from the project directory, so manual installation is optional for development.

## Font Paths in Configuration

All font paths in `subtitle_styles_v3.json` have been updated to use relative paths from the project root:
```
/Users/naman/Desktop/movie_py/project_fonts/[font-name]
```

## License Compliance

Please ensure you have appropriate licenses for commercial fonts:
- **Bicyclette-Black.ttf**: Requires commercial license
- **mazzard-m-bold.otf**: Requires commercial license
- **The Sgone.otf**: Custom font - verify usage rights

All other fonts use SIL Open Font License or are system fonts.

## Troubleshooting

If fonts don't load:
1. Verify font files exist in this directory
2. Check file permissions (fonts should be readable)
3. Clear font cache and restart application
4. For system installation issues, try copying fonts to user fonts directory first

## Version Information

- **Created**: May 30, 2025
- **VinVideo Version**: v4
- **Total Styles Supported**: 9 professional subtitle styles
- **Total Font Files**: 12 font files
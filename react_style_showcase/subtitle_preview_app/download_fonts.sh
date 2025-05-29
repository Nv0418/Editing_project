#!/bin/bash

# Google Fonts Downloader Script
# Downloads specific fonts needed for subtitle styles

echo "Downloading Google Fonts for subtitle styles..."

# Create fonts directory if it doesn't exist
mkdir -p fonts

# Download Montserrat Black (for HORMOZI CAPTION)
echo "Downloading Montserrat Black..."
curl -o fonts/Montserrat-Black.ttf "https://fonts.gstatic.com/s/montserrat/v29/JTUHjIg1_i6t8kCHKm4532VJOt5-QNFgpCvC70w-.ttf"

# Download Bebas Neue Regular (for LIVE CAPTION)
echo "Downloading Bebas Neue Regular..."
curl -o fonts/BebasNeue-Regular.ttf "https://fonts.gstatic.com/s/bebasneue/v14/JTUSjIg69CK48gW7PXooxW4.ttf"

# Download Quicksand Bold (for DASHING CAPTION)
echo "Downloading Quicksand Bold..."
curl -o fonts/Quicksand-Bold.ttf "https://fonts.gstatic.com/s/quicksand/v36/6xK-dSZaM9iE8KbpRA_LJ3z8mH9BOJvgkBgv18E.ttf"

# Download Nunito Regular (for WHISTLE CAPTION)
echo "Downloading Nunito Regular..."
curl -o fonts/Nunito-Regular.ttf "https://fonts.gstatic.com/s/nunito/v26/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshRTM.ttf"

# Download Fredoka Bold (for POPLING CAPTION)
echo "Downloading Fredoka Bold..."
curl -o fonts/Fredoka-Bold.ttf "https://fonts.gstatic.com/s/fredoka/v16/X7nP4b87HvSqjb_WIi2yDCRwoQ_k7367_B-i2yQag0-mac3OFiXMFg.ttf"

# Download Lobster Two Italic (for TILTED CAPTION)
echo "Downloading Lobster Two Italic..."
curl -o fonts/LobsterTwo-Italic.ttf "https://fonts.gstatic.com/s/lobstertwo/v20/BngOUXZGTXPUvIoyV6yN5-fI5qA.ttf"

# Download Shrikhand Regular (for KARAOKE STYLE)
echo "Downloading Shrikhand Regular..."
curl -o fonts/Shrikhand-Regular.ttf "https://fonts.gstatic.com/s/shrikhand/v16/a8IbNovtLWfR7T7bMJwbBA.ttf"

echo "All fonts downloaded successfully to ./fonts/ directory"
echo ""
echo "Downloaded fonts:"
ls -la fonts/
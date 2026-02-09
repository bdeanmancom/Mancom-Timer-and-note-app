# Mancom, Inc Branding Guide

## Logo Setup

The Mancom Timer application supports a custom logo/icon in the system tray and window.

### Adding the Mancom Logo

1. **Prepare Your Logo**
   - Save your Mancom, Inc logo as `icon.ico` (Windows icon format)
   - Or create one from `logo.png` using an online converter:
     - https://convertio.co/png-ico/
     - https://icoconvert.com/

2. **Place in Application Folder**
   - Copy `icon.ico` to the application root directory
   - It should be at the same level as `main.py`

3. **Rebuild the Executable (Optional)**
   - If you've built a standalone executable with `python build.py`
   - The icon will automatically be included in the `.exe` file

### Creating an Icon from Scratch

If you don't have a logo yet, you can:

1. **Use an Online Tool**
   - Visit: https://www.favicon-generator.org/
   - Upload your image or design a new one
   - Download as `.ico` format

2. **Use Python Script** (included as `create_icon.py`)
   ```bash
   python create_icon.py
   ```

### Current Branding

**Company**: Mancom, Inc
**Colors**: 
- Primary: #2c3e50 (Dark Blue-Gray)
- Accent: #27ae60 (Green)
- Warning: #e67e22 (Orange)

**Application Title**: Mancom Timer & Notes

### Logo Specifications

For best results:
- **Format**: `.ico` (Windows Icon) or `.png`
- **Size**: 256x256 pixels or larger
- **Style**: Professional, clean design
- **Background**: Transparent preferred

### Customization

To change branding in the application:

1. **Window Title**
   - Edit in `main.py` line: `self.setWindowTitle("Mancom Timer & Notes")`

2. **Label Text**
   - Edit in `main.py` line: `tasks_label.setText("MANCOM, INC - TASK TIMER")`

3. **Colors**
   - Edit in `config.py` under `COLORS` dictionary

### Where the Logo Appears

- ✅ System tray icon
- ✅ Executable icon (Windows Task Bar)
- ✅ Desktop shortcut icon
- ✅ File explorer icon

---

**To use your Mancom logo:**
1. Save as `icon.ico` in the application folder
2. Optionally rebuild the executable with `python build.py`
3. The logo will appear automatically!

# How to Export Your Presentation to PowerPoint

Complete step-by-step guide to convert the Markdown presentation to PPTX using Marp.

---

## Option A: VS Code with Marp Extension (EASIEST - Recommended)

### Step 1: Install VS Code (if you don't have it)
1. Download from: https://code.visualstudio.com/
2. Install (takes 2 minutes)

### Step 2: Install Marp Extension
1. Open VS Code
2. Click Extensions icon (left sidebar) or press `Ctrl+Shift+X`
3. Search for: **"Marp for VS Code"**
4. Click **Install** on the extension by **Marp Team**
5. Wait 10 seconds for installation

### Step 3: Open the Presentation
1. In VS Code: **File** → **Open Folder**
2. Navigate to: `C:\Users\aq668e\Projects\medical-ner-lora`
3. Open the file: **PRESENTATION.md**

### Step 4: Preview the Presentation
1. With PRESENTATION.md open, click the **Marp icon** in top-right corner
   (Looks like a slide icon)
2. Or press `Ctrl+K` then `V`
3. Preview window opens → You'll see your slides!

### Step 5: Export to PowerPoint
1. Press `Ctrl+Shift+P` (opens Command Palette)
2. Type: **"Marp: Export Slide Deck"**
3. Select: **"PowerPoint (.pptx)"**
4. Choose save location (same folder is fine)
5. Click **Save**
6. ✅ Done! Your PPTX file is created!

**File location:** `medical-ner-lora/PRESENTATION.pptx`

---

## Option B: Marp CLI (For Command-Line Folks)

### Step 1: Install Marp CLI

**Windows (using npm):**
```bash
npm install -g @marp-team/marp-cli
```

**Mac/Linux:**
```bash
npm install -g @marp-team/marp-cli
# or
brew install marp-cli
```

### Step 2: Export to PPTX
```bash
cd C:/Users/aq668e/Projects/medical-ner-lora
marp PRESENTATION.md --pptx -o PRESENTATION.pptx
```

**Alternative formats:**
```bash
# Export to PDF
marp PRESENTATION.md --pdf -o PRESENTATION.pdf

# Export to HTML
marp PRESENTATION.md --html -o PRESENTATION.html
```

---

## Option C: Pandoc (Alternative Tool)

### Step 1: Install Pandoc
Download from: https://pandoc.org/installing.html

### Step 2: Convert
```bash
cd C:/Users/aq668e/Projects/medical-ner-lora
pandoc PRESENTATION.md -o PRESENTATION.pptx
```

**Note:** Pandoc won't render Mermaid diagrams or Marp-specific styling. Use Marp for best results.

---

## After Export: Add Charts in PowerPoint

Once you have the PPTX file:

1. **Open** PRESENTATION.pptx in PowerPoint
2. **Find slides** with "[CHART PLACEHOLDER]" text
3. **Delete** the placeholder text
4. **Insert charts** following the guide in `CHART_CREATION_GUIDE.md`
5. **Save** your final presentation

**3 charts to add:**
- Slide 11: Training Loss Curve
- Slide 13: Performance Comparison Bar Chart
- Slide 18: Cost Comparison Chart

---

## Troubleshooting

### Problem: "Marp command not found"
**Solution:** Marp CLI not installed. Use VS Code method (Option A) instead - it's easier!

### Problem: "Mermaid diagrams not showing"
**Solution:**
- In VS Code Marp: They should render automatically
- If not, check Marp extension settings → Enable Mermaid

### Problem: "Export button grayed out"
**Solution:**
- Make sure PRESENTATION.md has the frontmatter (lines 1-8 starting with `---`)
- The file must have `marp: true` in the frontmatter

### Problem: "Slides look different in PowerPoint"
**Solution:** This is normal. Marp → PPTX conversion isn't perfect. You can:
- Adjust fonts/spacing in PowerPoint after export
- Use PDF export for pixel-perfect slides (but can't edit)

### Problem: "Tables are messy in PPTX"
**Solution:** After export, manually adjust table column widths in PowerPoint

---

## Tips for Best Results

### Before Exporting:
- ✅ Check all slides in Marp preview look good
- ✅ Verify no typos or formatting errors
- ✅ Ensure Mermaid diagrams render correctly

### After Exporting:
- ✅ Open in PowerPoint and review every slide
- ✅ Fix any formatting issues (spacing, alignment)
- ✅ Add the 3 charts (see CHART_CREATION_GUIDE.md)
- ✅ Add speaker notes if needed
- ✅ Check slide numbers are visible
- ✅ Test on presentation computer/projector

### Final Polish:
- ✅ Add custom footer with your contact info
- ✅ Adjust header if needed
- ✅ Consider adding GE Healthcare logo (if appropriate)
- ✅ Save a backup copy before presenting!

---

## Presentation Delivery Tips

### File Management:
1. **Create 3 versions:**
   - PRESENTATION.pptx (main editable)
   - PRESENTATION_FINAL.pptx (after adding charts)
   - PRESENTATION.pdf (backup if PPTX fails)

2. **Test on actual presentation setup:**
   - Open on the laptop you'll use
   - Test projector connection
   - Ensure all visuals render correctly

### During Presentation:
- **Presenter View:** Use PowerPoint's Presenter View to see notes
- **Slide Timing:** Aim for 1-2 minutes per slide (45 slides = 45-60 min)
- **Backup Plan:** Have PDF version on USB drive

---

## Time Estimate

| Task | Time |
|------|------|
| Install VS Code + Marp | 5 minutes |
| Export to PPTX | 30 seconds |
| Review slides in PowerPoint | 10 minutes |
| Add 3 charts | 15 minutes |
| Final polish | 10 minutes |
| **Total** | **~40 minutes** |

---

## Quick Start (TL;DR)

```bash
# Install Marp extension in VS Code
# Open PRESENTATION.md
# Press Ctrl+Shift+P
# Type "Marp: Export Slide Deck"
# Choose PowerPoint (.pptx)
# Add 3 charts using CHART_CREATION_GUIDE.md
# Done!
```

---

## Need Help?

- **Marp Documentation:** https://marp.app/
- **VS Code Marp Extension:** https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode
- **Video Tutorial:** Search YouTube for "Marp VS Code tutorial"

Good luck with your presentation! 🚀

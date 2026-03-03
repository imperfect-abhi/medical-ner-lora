# Chart Creation Guide for PowerPoint

After exporting the presentation from Marp to PPTX, you need to add **3 charts** manually. This guide tells you exactly what to create.

---

## Chart 1: Training Loss Curve (Slide 11)

### Chart Type: Line Chart

### Data to Plot:

```
Epoch    Training Loss
1        0.1217
2        0.0917
3        0.0612
4        0.0387
5        0.0273
6        0.0190
7        0.0132
8        0.0141
9        0.0117
10       0.0097
```

### How to Create in PowerPoint:

1. Go to Slide 11 (titled "Training Performance")
2. Click **Insert** → **Chart** → **Line Chart**
3. Delete the placeholder text that says "[CHART PLACEHOLDER 1: Training Loss Curve]"
4. Enter the data above in Excel sheet that pops up
5. **Format the chart:**
   - Chart Title: "Training Loss Convergence"
   - X-axis Label: "Epoch"
   - Y-axis Label: "Loss"
   - Line Color: Blue or Green
   - Add data labels if you want
   - Gridlines: Light gray

### Visual Tips:
- The line should show a clear downward trend
- Loss drops rapidly in first 5 epochs, then plateaus
- Make the line thick (3pt) for visibility

---

## Chart 2: Model Performance Comparison (Slide 13)

### Chart Type: Clustered Bar Chart (Horizontal)

### Data to Plot:

```
Model                     F1 Score
Industry Baseline         80%
BioBERT                   87%
ClinicalBERT             87%
Our LoRA Model           96.9%
```

### How to Create in PowerPoint:

1. Go to Slide 13 (after the results table)
2. Click **Insert** → **Chart** → **Bar Chart** (Clustered Bar)
3. Delete the placeholder text
4. Enter the data above
5. **Format the chart:**
   - Chart Title: "F1 Score Comparison: Industry Benchmarks"
   - X-axis: 0% to 100% (F1 Score)
   - Y-axis: Model names
   - Colors:
     - Industry Baseline: Light gray
     - BioBERT: Gray
     - ClinicalBERT: Gray
     - **Our LoRA Model: Green** (highlight)
   - Add data labels showing exact percentages
   - Add annotation: "+9.9 pts improvement" with arrow pointing to your bar

### Visual Tips:
- Make your bar (96.9%) stand out with bright green
- Add a vertical reference line at 85% (average benchmark)
- Your bar should clearly exceed others

---

## Chart 3: Cost Comparison (Slide 18)

### Chart Type: Stacked Bar Chart (Horizontal)

### Data to Plot:

```
Category          Traditional    LoRA
Training Cost     $100          $0.50
Storage Cost      $50           $0.50
Deployment Cost   $200          $10
```

### How to Create in PowerPoint:

1. Go to Slide 18 (titled "Business Value Analysis")
2. Click **Insert** → **Chart** → **Stacked Bar Chart**
3. Delete the placeholder text
4. Enter the data above with 3 categories stacked
5. **Format the chart:**
   - Chart Title: "Cost Breakdown: Traditional vs LoRA"
   - X-axis: Cost in $ (0 to 400)
   - Y-axis: Approach (Traditional, LoRA)
   - Colors:
     - Training: Blue
     - Storage: Orange
     - Deployment: Green
   - Show total at end of each bar:
     - Traditional: $350
     - LoRA: $11
   - Add annotation: "97% cost reduction"

### Alternative (Simpler):
If stacked bars are confusing, just do a simple clustered bar chart:
```
Approach       Total Cost
Traditional    $350
LoRA          $11
```

### Visual Tips:
- Make the cost difference dramatic (LoRA bar should be tiny)
- Add dollar signs to all labels
- Consider using a logarithmic scale if the difference is too extreme to show

---

## Quick PowerPoint Tips

### Inserting Charts:
1. **Insert** → **Chart** → Choose type
2. Excel window opens → Enter your data
3. Close Excel → Chart appears in slide
4. Right-click chart → **Edit Data** to modify later

### Making Charts Look Professional:
- **Remove chart border**: Click chart → Format → Shape Outline → No Outline
- **Clean background**: Chart Area → Fill → No Fill (or white)
- **Font consistency**: Change chart fonts to match presentation (Calibri or Arial, 14-16pt)
- **Color scheme**: Use corporate colors or stick to blue/green/gray
- **Data labels**: Add them! People like seeing exact numbers

### Common Mistakes to Avoid:
- ❌ 3D charts (look dated, avoid them)
- ❌ Too many colors (stick to 2-3)
- ❌ Missing axis labels
- ❌ Illegible small text
- ✅ Simple, clean, readable from back of room

---

## If You're Short on Time

**Minimum viable approach:**
1. Export presentation from Marp
2. Add just Chart #2 (Performance Comparison) - most important
3. For Charts 1 and 3, you can talk through the numbers without visual if needed

But ideally, add all 3 charts - they're quick to create and add big visual impact!

---

## Sample Color Schemes

### Option 1: Professional Blue/Green
- Primary: #2E86AB (Blue)
- Success: #06A77D (Green)
- Neutral: #6C757D (Gray)

### Option 2: Healthcare
- Primary: #0066CC (Medical blue)
- Accent: #00CC66 (Health green)
- Warning: #FF9900 (Orange)

### Option 3: GE Healthcare Brand (if you have access)
- Use official GE brand colors
- Maintains visual consistency

---

## Need Help?

If you get stuck:
1. Google "how to create [chart type] in PowerPoint"
2. YouTube has great tutorials: "PowerPoint bar chart tutorial"
3. Or just use PowerPoint's default styling - it's good enough!

**Remember:** Content > Design. Even basic charts are better than no charts.

# Time-to-Move: Project Website

Complete project page for the paper "Time-to-Move: Training-Free Motion Controlled Video Generation via Dual-Clock Denoising"

## 📁 File Structure

```
website/
├── index_new.html          # Main project page
├── supplementary.html      # Supplementary materials page
├── style_new.css          # Modern CSS styling for both pages
├── assets/                # Placeholder assets directory
│   ├── README.md
│   ├── method_placeholder.svg
│   └── dual_clock_placeholder.svg
├── UserObjectControl/     # Object control video results
├── UserCameraControl/     # Camera control video results
├── DL3DV/                 # DL3DV dataset comparisons
└── MC-Bench/              # MC-Bench dataset comparisons
```

## 🎨 Main Page Sections

The main page (`index_new.html`) includes:

1. **Header**
   - Paper title
   - Authors with affiliations
   - Institution names
   - Conference/Journal
   - Links (Paper, Code, Supplementary, YouTube)

2. **Teaser Video**
   - Placeholder for teaser video
   - Add your video to `assets/teaser_placeholder.mp4`

3. **Abstract**
   - Overview of the method
   - Key contributions
   - Results summary

4. **Method Overview**
   - Method figure placeholder
   - Description of the approach
   - Three main components explained

5. **Dual-Clock Denoising**
   - Dual-clock mechanism figure
   - Detailed explanation

6. **User-Specified Object Control**
   - Example videos (6 shown on main page)
   - Warped vs. Ours comparisons

7. **User-Specified Camera Control**
   - Example videos (6 shown on main page)
   - Warped vs. Ours comparisons

8. **Qualitative Comparisons**
   - Object Control comparisons
   - Camera Control comparisons

9. **Citation**
   - BibTeX entry

## 📄 Supplementary Page Sections

The supplementary page (`supplementary.html`) includes:

1. **Header**
   - Title and navigation
   - Quick links back to main page

2. **MC-Bench Comparisons**
   - All 13 MC-Bench examples
   - 5-way comparisons: Warped | Ours | DragAnything | SGI2V | MotionPro

3. **DL3DV Comparisons**
   - All 10 DL3DV examples
   - 4-way comparisons: Warped | Ours | GWTF | Ground Truth

4. **More Object Control Results**
   - Additional examples not shown on main page

5. **More Camera Control Results**
   - Additional examples not shown on main page

## 🎯 What You Need to Do

### 1. Update Author Information

Edit `index_new.html`:
```html
<!-- Replace these placeholders -->
<span class="author">Author Name<sup>1</sup></span>
<span class="affiliation"><sup>1</sup>Institution Name</span>
<div class="conference">Conference/Journal Name 2025</div>
```

### 2. Add Links

Update the href attributes in both HTML files:
```html
<a href="#" class="paper-btn">Paper (arXiv)</a>  <!-- Add arXiv link -->
<a href="#" class="paper-btn">Code</a>           <!-- Add GitHub link -->
<a href="#" class="paper-btn">YouTube</a>        <!-- Add YouTube link -->
```

### 3. Write Abstract and Descriptions

In `index_new.html`, replace the placeholder text:
- Abstract section: Expand with your full abstract
- Method description: Detail your approach
- Dual-clock description: Explain the mechanism

### 4. Add Figures

Replace the placeholder SVG files with your actual figures:
- `assets/method_placeholder.svg` → Your method overview figure
- `assets/dual_clock_placeholder.svg` → Your dual-clock mechanism figure

Supported formats: PNG, JPG, SVG
Recommended width: 1200px

### 5. Add Teaser Video

Add your teaser video:
- Path: `assets/teaser_placeholder.mp4`
- Recommended: 1920x1080 or 1280x720 (16:9 aspect ratio)
- Format: MP4 (H.264)

### 6. Update BibTeX

Edit the citation in `index_new.html`:
```bibtex
@article{yourname2025timetomove,
  title={Time-to-Move: Training-Free Motion Controlled Video Generation via Dual-Clock Denoising},
  author={Author Names},
  journal={Conference/Journal Name},
  year={2025}
}
```

## 🎨 Customization

### Colors

Edit CSS variables in `style_new.css`:
```css
:root {
  --primary-color: #4a90e2;      /* Main accent color */
  --secondary-color: #667eea;    /* Gradient start */
  --accent-color: #764ba2;       /* Gradient end */
  --text-color: #333;            /* Main text */
  --text-light: #666;            /* Secondary text */
}
```

### Layout

The design is fully responsive:
- Desktop: 1200px max width
- Tablet: Adapts to smaller screens
- Mobile: Single column layout

## 🚀 Deployment

### Option 1: GitHub Pages

1. Rename `index_new.html` to `index.html`
2. Rename `style_new.css` to `style.css`
3. Update references in HTML files
4. Push to GitHub
5. Enable GitHub Pages in repository settings

### Option 2: Custom Server

1. Upload all files to your web server
2. Ensure video files are accessible
3. Set proper MIME types for videos

### Option 3: Local Preview

Open `index_new.html` directly in a browser to preview.

## 📝 Notes

- All video files use autoplay, loop, and muted attributes for best UX
- Videos are lazy-loaded for performance
- The design follows modern academic project page standards
- Fully responsive and mobile-friendly
- Print-friendly styles included

## 🔗 Original Files

Your original files are preserved:
- `index.html` - Original supplementary page
- `style.css` - Original styles

The new files are:
- `index_new.html` - New main project page
- `supplementary.html` - New supplementary page
- `style_new.css` - New modern styles

## 📧 Support

If you need to adjust any section or styling, refer to the CSS file for class names and modify accordingly.

---

**Last Updated:** October 19, 2025

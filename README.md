# 🌱 AgriSmart AI

> **Multimodal Plant Health & Irrigation Assessment** — upload a leaf image, enter your sensor readings, and get a combined visual + environmental health report.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=flat&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=flat&logo=plotly&logoColor=white)
![Status](https://img.shields.io/badge/status-active%20development-16804c?style=flat)

---

## ⚠️ A Note on Accuracy — Please Read First

I want to be upfront about this: **AgriSmart's predictions are not always accurate.** The main reason is dataset availability — the CNN was trained on publicly available leaf-image data that isn't as large or field-diverse as a real agricultural system needs, and the irrigation models were trained on limited sensor samples. The app is a **working end-to-end product** — image in, sensor data in, fused report out — but it should be treated as a demonstration of the approach, not a diagnostic tool.

I could have left this out of the README. I'd rather you know exactly what you're looking at.

---

## 📖 Overview

AgriSmart AI is a Streamlit web app that combines two independent pipelines into a single report:

1. **Visual analysis** — a CNN classifies an uploaded plant leaf image into one of **15 plant-condition classes**, returning the top-3 predictions with confidence scores.
2. **Sensor analysis** — two Random Forest models use six environmental and soil readings to predict whether irrigation is needed, and how much water (in litres) to apply.

The two are combined at the **decision/output level** (see `utils/fusion.py`), and the app presents the result as a clean, readable health assessment report — not a wall of numbers.

---

## ✨ Features

- **🌿 Multimodal input** — one leaf image plus six sensor readings, in a single form
- **📊 CNN top-3 breakdown** — see not just the top prediction, but how confident the model is across the next two candidates
- **💧 Irrigation gauge** — probability gauge with clear visual zones (low / moderate / high)
- **🩺 Overall risk level** — Low / Moderate / High, derived from the visual result and confidence
- **📋 Structured report** — visual analysis, irrigation analysis, environmental context, and combined interpretation in one place
- **💡 Actionable next steps** — recommendations generated from the actual model outputs, not static text
- **🎨 Custom UI** — light agricultural theme, custom cards, hidden Streamlit chrome for a product-like feel
- **ℹ️ Transparency** — a Model Information expander explains exactly what each model is, plus a visible disclaimer

---

## 🧠 How It Works

```
┌─────────────────┐     ┌──────────────────────────┐
│  Leaf Image     │────▶│  CNN (MobileNetV2-based)  │──┐
└─────────────────┘     │  15-class classification  │  │
                        └──────────────────────────┘  │
                                                        ├──▶  Fusion  ──▶  Report
                        ┌──────────────────────────┐  │     (utils/fusion.py)
┌─────────────────┐     │  Irrigation Classifier    │  │
│  Sensor Inputs  │────▶│  (Random Forest)          │──┤
│  (6 readings)   │     ├──────────────────────────┤  │
└─────────────────┘     │  Irrigation Regressor     │  │
                        │  (Random Forest)          │──┘
                        └──────────────────────────┘
```

### 1. Visual Pipeline
The uploaded image is preprocessed and passed to a **MobileNetV2-based CNN** trained on 15 plant-condition classes (disease and healthy variants). The model returns a top-3 prediction list with probabilities. A class is treated as healthy if its label contains `"healthy"`.

### 2. Sensor Pipeline
Six readings are collected:

| Input | Unit | Typical Range |
|---|---|---|
| Soil Moisture | % | 0 – 100 |
| Soil Temperature | °C | — |
| Soil pH | pH | 0 – 14 |
| Humidity | % | 0 – 100 |
| Air Temperature | °C | — |
| Solar Radiation | W/m² | — |

These feed:
- A **Random Forest classifier** → is irrigation needed? (binary) + probability
- A **Random Forest regressor** → recommended irrigation volume in litres

### 3. Fusion
`utils/fusion.py` combines both pipelines into a single result object: the disease prediction, the irrigation decision, the recommended litres, and the raw sensor readings (echoed back in the report for context). Fusion is at the **output level** — the sensor model supports irrigation decisions and environmental context; it does **not** claim to explain the cause of a visually detected disease.

---

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| App framework | Streamlit |
| Image model | TensorFlow / Keras — MobileNetV2-based CNN |
| Sensor models | scikit-learn — Random Forest (classifier + regressor) |
| Visualization | Plotly Express, Plotly Graph Objects |
| Image handling | Pillow (PIL) |
| Fusion logic | Custom Python (`utils/fusion.py`) |

---

## 📁 Project Structure

```
AgriSmart/
├── app.py                     # Streamlit app — UI, layout, report rendering
├── utils/
│   └── fusion.py              # Combines image + sensor model outputs
├── models/                    # Trained model files
│   ├── plant_disease_model.h5
│   ├── irrigation_classifier.pkl
│   └── irrigation_regressor.pkl
├── assets/                    # Screenshots, demo images
├── requirements.txt
└── README.md
```

> Structure is indicative — adjust the `models/` filenames to match your repo.

---

## ⚙️ Installation

```bash
# 1. Clone the repo
git clone https://github.com/PritySingha/AgriSmart.git
cd AgriSmart

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

**`requirements.txt`** (core dependencies):

```
streamlit
plotly
pillow
tensorflow
scikit-learn
numpy
pandas
```

---

## ▶️ Usage

```bash
streamlit run app.py
```

Then in the browser:

1. **Upload** a clear plant leaf image (JPG / JPEG / PNG)
2. **Enter** your six sensor readings in the Environmental & Soil Data panel
3. Click **🌿 Analyze Plant**
4. Review the generated report:
   - Summary cards (visual analysis, CNN confidence, irrigation amount, overall risk)
   - Live sensor reading cards
   - Leaf image + irrigation probability gauge
   - CNN top-3 prediction chart
   - Written analysis summary
   - Recommended next steps
   - Model information + disclaimer

The app will warn you if you try to analyze without uploading an image.

---

## 📊 Reading the Output

| Output | Meaning |
|---|---|
| **Visual Analysis** | Top CNN class, underscores replaced with spaces for readability |
| **CNN Confidence** | Probability of the top class (0–100%) |
| **Irrigation Assessment** | Litres recommended + "Needed / Not Needed" badge |
| **Overall Risk** | `Low` if healthy · `High` if disease confidence ≥ 70% · `Moderate` otherwise |
| **Irrigation Gauge** | Model probability of irrigation being needed, with visual zones |
| **CNN Breakdown** | Top-3 classes by probability, as a horizontal bar chart |
| **Recommendations** | Generated from the actual outputs — e.g. water amount, monitoring advice |

---

## 🚧 Known Limitations

Being honest about what this project is *not*:

- **Accuracy** — the CNN and sensor models were trained on limited, publicly available datasets. Real-field performance is not guaranteed. This is the single biggest limitation.
- **Dataset diversity** — training images and sensor samples don't cover the full range of crops, lighting conditions, growth stages, or soil types found in the field.
- **Disease classes are fixed** — the CNN can only predict the 15 classes it was trained on; unknown conditions will still be forced into one of them.
- **Sensor model is not causal** — irrigation prediction uses environmental readings; it cannot tell you *why* a disease appeared.
- **Output-level fusion** — the pipelines are combined after prediction, not jointly trained.

---

## 🔭 Future Improvements

- Train on a larger, field-verified, multi-crop dataset
- Add class-confidence thresholds / "unknown" handling instead of forcing a prediction
- Expand sensor coverage (NPK, leaf wetness, light spectrum)
- Move from output-level to feature-level fusion
- Add per-crop model variants
- Persist analysis history for tracking plant health over time

---

## ⚠️ Disclaimer

AgriSmart AI provides **AI-based supporting information** from image and sensor analysis. Results should **not** be treated as a definitive agricultural diagnosis. For real crop decisions, consult an agricultural expert or extension service.

---

## 📬 Contact

**Prity Singha**
Computer Science Student · Aspiring Software Engineer / Data Analyst

- GitHub: [@PritySingha](https://github.com/PritySingha)
- LinkedIn: [prity-singha](https://www.linkedin.com/in/prity-singha/)
- Email: pritysingha001@gmail.com
- Portfolio: [pritysingha.github.io](https://pritysingha.github.io/Portfolio-Prity_singha/)

---

<p align="center">
  <em>Built to finish, not just to tick a box.</em>
</p>

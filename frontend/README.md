# House Price Prediction Dashboard

A sleek, modern web interface for predicting house prices using machine learning models.

## Features

- **Minimalistic Design**: Clean, modern interface with gradient backgrounds and smooth animations
- **Smart Form**: Automatically loads available features from the API and highlights the most important ones
- **Feature Importance**: Essential features are marked with stars and badges to guide users
- **Intelligent Defaults**: Users can leave fields empty - the system will use intelligent defaults
- **Real-time Predictions**: Fast predictions with detailed confidence metrics
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Detailed Breakdown**: View which features were provided vs. defaulted

## Quick Start

### Option 1: Use the start script (Windows)
```bash
start_dashboard.bat
```

### Option 2: Manual start
1. Start the API server:
```bash
python src/api.py
```

2. Start the frontend server:
```bash
python frontend/server.py
```

3. Open your browser to: http://localhost:3000

## How It Works

1. **Feature Loading**: The frontend calls `/features` endpoint to get all available features, their defaults, and importance rankings
2. **Smart Form Generation**: Creates a form with two sections:
   - **Essential Features**: Top 10 most important features (marked with stars)
   - **Additional Features**: Other features (optional)
3. **Prediction**: Sends provided features to `/predict` endpoint
4. **Results Display**: Shows price estimate with confidence metrics and feature breakdown

## Architecture

```
frontend/
├── index.html          # Main HTML file
├── static/
│   ├── style.css      # Styles (gradients, animations, responsive)
│   └── script.js      # JavaScript (API calls, form handling)
├── server.py          # FastAPI server for frontend
└── README.md          # This file
```

## API Endpoints Used

- `GET /features` - Get feature list, defaults, and importance
- `POST /predict` - Make price predictions

## Styling

The interface uses:
- **Inter** font family for modern typography
- **Gradient backgrounds** for visual appeal
- **Card-based layout** for content organization
- **Smooth animations** for interactions
- **Responsive grid** for form layout
- **Modal dialogs** for detailed information

## Browser Support

Modern browsers supporting:
- CSS Grid
- Flexbox
- CSS Custom Properties
- Fetch API
- ES6+ JavaScript

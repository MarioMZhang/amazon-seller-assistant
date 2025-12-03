# Amazon Content Generator - Frontend

A React-based web interface for the Amazon Content Generator. Upload XLSX files and generate optimized Amazon product listings using AI.

## Features

- **File Upload**: Upload seller_elf.xlsx and sif.xlsx files
- **Customizable Parameters**: Configure brand name, product type, keyword count, and AI model
- **Real-time Results**: View generated content immediately with comprehensive display
- **Download Results**: Export generated content as JSON
- **Responsive Design**: Beautiful gradient UI that works on all screen sizes

## Getting Started

### Prerequisites

- Node.js 16+ (though Node 20+ is recommended)
- npm or yarn

### Installation

```bash
# Install dependencies
npm install
```

### Running the Development Server

```bash
# Start the Vite dev server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Building for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Usage

1. **Start the Backend API**: Make sure the FastAPI backend is running on `http://localhost:8000`
   ```bash
   # From the project root
   python3 api_server.py
   ```

2. **Open the Frontend**: Navigate to `http://localhost:5173` in your browser

3. **Upload Files**:
   - Select your `seller_elf.xlsx` file
   - Select your `sif.xlsx` file

4. **Configure Parameters**:
   - Brand Name (default: "Amazing Cosy")
   - Product Type (default: "Women's Slippers")
   - Top N Keywords (default: 50)
   - AI Model (default: "gemini-2.5-flash-lite")

5. **Generate Content**: Click "Generate Content" and wait for the AI to process

6. **View Results**: Browse through the generated:
   - Market Research
   - Product Titles (3 variations)
   - Bullet Points (2 versions, 5 bullets each)
   - Product Description
   - Search Keywords
   - Quality Check Results
   - SEO Rationale and Recommendations

7. **Download**: Click "Download JSON" to save the results

## API Integration

The frontend connects to the FastAPI backend at `http://localhost:8000/generate`

CORS is configured to allow requests from:
- `http://localhost:5173` (Vite default)
- `http://localhost:3000` (Create React App default)

## Project Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main application component
│   ├── App.css          # Application styles
│   ├── index.css        # Global styles
│   └── main.jsx         # Application entry point
├── index.html           # HTML template
├── package.json         # Dependencies and scripts
└── vite.config.js       # Vite configuration
```

## Technologies Used

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **CSS3**: Styling with gradients and animations
- **Fetch API**: HTTP requests to backend

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## License

MIT

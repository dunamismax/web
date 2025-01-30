# DunamisMax Main Site

Central hub for the DunamisMax web application suite, serving as the primary entry point and service directory for all DunamisMax services.

## Features

- **Service Directory:** Quick access to all DunamisMax services
- **Responsive Design:** Optimized for all device sizes
- **Nord Theme:** Clean, modern aesthetic using the Nord color palette
- **Fast Loading:** Minimal dependencies for optimal performance
- **SEO Optimized:** Meta tags and semantic HTML structure
- **Accessible:** Follows web accessibility guidelines

## Technology Stack

### Backend

- FastAPI - Web framework
- Uvicorn - ASGI server
- Python 3.x - Core language
- Jinja2 - Template engine

### Frontend

- HTML5 - Semantic markup
- CSS3
  - CSS Variables
  - Nord color theme
  - Flexbox/Grid layouts
  - Responsive design
- Vanilla JavaScript - Minimal, no frameworks
- Feather Icons - UI icons
- Fira Code - Monospace font

### Infrastructure

- Caddy - Reverse proxy
- Cloudflare - DNS and CDN

## Project Structure

```bash
dunamismax/
├── app/
│   ├── static/
│   │   ├── favicon.ico    # Site favicon
│   │   ├── logo.svg       # Site logo
│   │   └── styles.css     # Main stylesheet
│   ├── templates/
│   │   ├── base.html      # Base template
│   │   └── index.html     # Homepage
│   ├── __init__.py
│   └── main.py           # FastAPI application
├── README.md
└── requirements.txt
```

## Installation

1. **Set Up Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the Site**
   - Local development: `http://localhost:8000`
   - Production: `https://dunamismax.com`

## Page Components

### Homepage Elements

- Site header with logo
- Service navigation cards
- Quick links to subdomains
- Footer with contact information

### Service Cards

- AI Agents link and description
- Messenger link and description
- Additional service previews

### Navigation

- Clean, intuitive interface
- Visual feedback on interaction
- Mobile-responsive menu
- Icon-based navigation

## Styling

### Nord Theme Implementation

```css
:root {
    /* Nord Color Palette */
    --nord0: #2E3440;  /* Dark Background */
    --nord1: #3B4252;  /* Lighter Background */
    --nord4: #D8DEE9;  /* Main Text */
    --nord8: #88C0D0;  /* Accent Color */
}
```

### Responsive Breakpoints

```css
/* Mobile devices */
@media (max-width: 768px) {
    /* Mobile-specific styles */
}

/* Tablets */
@media (min-width: 769px) and (max-width: 1024px) {
    /* Tablet-specific styles */
}

/* Desktops */
@media (min-width: 1025px) {
    /* Desktop-specific styles */
}
```

## Development

### Running Locally

```bash
# With auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Template Modification

1. Base template (`base.html`) contains:
   - Common HTML structure
   - Meta tags
   - CSS/JS includes
   - Header/Footer

2. Index template (`index.html`) contains:
   - Service cards
   - Main content
   - Navigation elements

### Static Files

- Place new static files in `app/static/`
- Access via `{{ url_for('static', path='filename') }}`
- Automatically served by FastAPI

## Production Setup

### Server Configuration

1. Configure Caddy reverse proxy:

   ```caddy
   dunamismax.com {
       reverse_proxy localhost:8000
       encode gzip
       header {
           Strict-Transport-Security "max-age=31536000;"
       }
   }
   ```

2. Set up Cloudflare:
   - Enable SSL/TLS
   - Configure DNS records
   - Enable caching
   - Set up firewall rules

### Deployment

1. Clone repository
2. Install production dependencies
3. Configure environment
4. Start application with production server
5. Set up monitoring

## Performance Optimization

- Minified CSS
- Optimized SVG icons
- Cached static files
- Compressed responses
- Lazy loading images
- Preloaded critical assets

## Security Features

- HTTPS enforcement
- Security headers
- Rate limiting
- XSS protection
- CSRF protection
- Content Security Policy

## Contributing

1. Fork the repository
2. Create your feature branch

   ```bash
   git checkout -b feature/new-feature
   ```

3. Commit your changes

   ```bash
   git commit -am 'Add new feature'
   ```

4. Push to the branch

   ```bash
   git push origin feature/new-feature
   ```

5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

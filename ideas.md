# Web app ideas

1. **File Tools (files.dunamismax.com)**

```python
{
    "name": "File Tools",
    "description": "Suite of file conversion and manipulation tools",
    "url": "https://files.dunamismax.com",
    "icon": "file-text",
    "port": 8200
}
```

- PDF generation and manipulation
- Image format conversion
- File compression tools
- CSV/Excel converters
- Markdown to HTML converter

2. **API Playground (api.dunamismax.com)**

```python
{
    "name": "API Tools",
    "description": "HTTP request testing and API documentation",
    "url": "https://api.dunamismax.com",
    "icon": "code",
    "port": 8201
}
```

- HTTP request tester (like Postman)
- JSON formatter and validator
- JWT decoder
- Base64 encoder/decoder

3. **Code Utilities (code.dunamismax.com)**

```python
{
    "name": "Code Utils",
    "description": "Developer utilities and formatters",
    "url": "https://code.dunamismax.com",
    "icon": "terminal",
    "port": 8202
}
```

- Code formatters (Python, JavaScript, SQL)
- Regex tester
- Color picker with Nord theme integration
- UUID generator
- Hash generator

4. **Math Tools (math.dunamismax.com)**

```python
{
    "name": "Math Tools",
    "description": "Mathematical calculations and visualizations",
    "url": "https://math.dunamismax.com",
    "icon": "pie-chart",
    "port": 8203
}
```

- Statistical calculator
- Graph plotter
- Matrix calculator
- Unit converter
- Financial calculators

5. **Text Tools (text.dunamismax.com)**

```python
{
    "name": "Text Tools",
    "description": "Text manipulation and analysis utilities",
    "url": "https://text.dunamismax.com",
    "icon": "type",
    "port": 8204
}
```

- Text difference comparator
- Word counter with analytics
- String manipulation tools
- Lorem ipsum generator
- Character encoder/decoder

6. **Share Tools (share.dunamismax.com)**

```python
{
    "name": "Quick Share",
    "description": "Temporary file and text sharing",
    "url": "https://share.dunamismax.com",
    "icon": "share-2",
    "port": 8205
}
```

- Temporary file sharing
- Code snippet sharing
- Text snippet sharing
- Link shortener
- QR code generator

7. **Data Tools (data.dunamismax.com)**

```python
{
    "name": "Data Tools",
    "description": "Data analysis and visualization",
    "url": "https://data.dunamismax.com",
    "icon": "database",
    "port": 8206
}
```

- CSV data viewer/editor
- SQL query builder
- JSON explorer
- Basic data visualization
- Data format converter

8. **Time Tools (time.dunamismax.com)**

```python
{
    "name": "Time Tools",
    "description": "Time zones and date calculations",
    "url": "https://time.dunamismax.com",
    "icon": "clock",
    "port": 8207
}
```

- Time zone converter
- Date calculator
- Countdown timer
- Meeting scheduler
- Calendar tools

9. **Note Tools (notes.dunamismax.com)**

```python
{
    "name": "Quick Notes",
    "description": "Temporary note taking and sharing",
    "url": "https://notes.dunamismax.com",
    "icon": "edit-3",
    "port": 8208
}
```

- Markdown editor
- Code note editor
- Drawing pad
- Todo list
- Voice notes

10. **Network Tools (net.dunamismax.com)**

```python
{
    "name": "Network Tools",
    "description": "Network diagnostics and utilities",
    "url": "https://net.dunamismax.com",
    "icon": "wifi",
    "port": 8209
}
```

- IP lookup
- DNS tools
- Port scanner
- SSL checker
- Ping tools

Each of these could be built as a standalone FastAPI application maintaining your minimalist design principles and Nord theme. They could share authentication if desired, and each would serve a specific purpose while being part of your larger ecosystem.

The beauty of this approach is:

1. Each service is independent
2. Easy to maintain and update
3. Can be developed incrementally
4. Shares common design language
5. Uses your existing infrastructure
6. Provides genuinely useful tools

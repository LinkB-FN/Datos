# Plagiarism Detector System

A Python-based plagiarism detection system using hash tables and sorting algorithms to analyze document similarities.

## Features
- Document similarity analysis
- Multiple comparison algorithms
- Visualization of results (graphs, heatmaps)
- Export capabilities (CSV, images)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/detector-plagio.git
cd detector-plagio
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Place documents to analyze in `documentos/` folder (supports .txt files)
2. Run the main script:
```bash
python main.py
```

3. View results in `resultados/` folder:
- CSV files with similarity scores
- Visualization graphs (PNG format)

## Project Structure

```
detector-plagio/
├── src/                  # Source code
│   ├── bloom_filter.py   # Bloom filter implementation
│   ├── exportar.py       # Export functionality  
│   ├── graficos.py       # Visualization tools
│   ├── hash_table.py     # Hash table implementation
│   ├── preprocesamiento.py # Text preprocessing
│   ├── similitud.py      # Similarity algorithms
│   └── sorting.py        # Sorting algorithms
├── test/                 # Unit tests
├── documentos/           # Input documents
├── resultados/           # Analysis results
│   ├── csv/              # CSV output
│   └── graficos/         # Visualization output
├── main.py               # Main entry point
└── requirements.txt      # Dependencies
```

## Testing

Run all tests:
```bash
python -m pytest
```

Or run specific test files:
```bash
python -m pytest test/test_bloom_filter.py
python -m pytest test/test_hash_table.py  
python -m pytest test/test_sorting.py
python -m pytest test/test_similitud.py
python -m pytest test/test_preprocesamiento.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first.

## License
[MIT](https://choosealicense.com/licenses/mit/)

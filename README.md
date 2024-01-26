# BSE Stock Viewer (Python & MongoDB)

## Version Details

- Python 3.11.7
- MongoDB 7.0.2
- cURL 8.4.0

## Setup & Run

### 1. Clone the repository

```bash
git clone https://github.com/<username>/stock-price-view.git
```

### 2. Initialize Python Virtual Environment

```bash
python -m venv env
```

### 3. Activate the virtual environment

```bash
source env/bin/activate
```

### 4. Install the dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python app.py
```

## API Endpoints

### 1. Get Top <i>k</i> Stocks

```bash
curl -X GET http://localhost:8000/get_top_k/<k>
```

### 2. Search Stock by Name

```bash
curl -X GET http://localhost:8000/search/<name>
```

### 3. Get Favorite Stocks

```bash
curl -X GET http://localhost:8000/get_favorites
```

### 4. Add Stock to Favorites

```bash
curl -X POST http://localhost:8000/add_favorite/<stock_code>
```

### 5. Remove Stock from Favorites

```bash
curl -X DELETE http://localhost:8000/remove_favorite/<stock_code>
```

### 6. Get Stock Price History

```bash
curl -X GET http://localhost:8000/get_price_history/<stock_code>
```

## Other Details

- 
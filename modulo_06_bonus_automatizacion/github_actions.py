import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import subprocess
import os
import json

def run():
    """Módulo Bonus - Automatización con GitHub Actions y CI/CD."""
    
    with st.container():
        st.title("🤖 Clase 1: Automatización con GitHub Actions")
        st.markdown("""
        Aprende a automatizar el testing, deployment y mantenimiento de tus aplicaciones
        Streamlit usando GitHub Actions y herramientas de CI/CD.
        """)
        
        # Pestañas del módulo
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔄 GitHub Actions",
            "🧪 Testing Automatizado",
            "📦 Build & Deploy",
            "📊 Monitoring & Alerts"
        ])
        
        with tab1:
            render_github_actions()
        
        with tab2:
            render_testing_automatizado()
        
        with tab3:
            render_build_deploy()
        
        with tab4:
            render_monitoring_alerts()

def render_github_actions():
    """Renderiza la configuración de GitHub Actions."""
    st.subheader("🔄 Configuración de GitHub Actions")
    
    st.markdown("""
    GitHub Actions te permite automatizar workflows directamente desde tu repositorio.
    """)
    
    # Introducción a GitHub Actions
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**¿Qué es GitHub Actions?**")
        st.markdown("""
        - 🤖 Automatización de workflows
        - 🧪 Testing automático
        - 🚀 Deployment continuo
        - 📊 Monitoreo de código
        - 🔐 Security scanning
        """)
        
        st.markdown("**Beneficios:**")
        st.markdown("""
        - ✅ Testing automático en cada push
        - ✅ Deploy automático a producción
        - ✅ Notificaciones de errores
        - ✅ Code quality checks
        - ✅ Dependency updates
        """)
    
    with col2:
        st.markdown("**Estructura básica:**")
        st.code("""
📁 .github/
  └── 📁 workflows/
      ├── 📄 test.yml          # Testing
      ├── 📄 deploy.yml        # Deployment
      ├── 📄 code-quality.yml  # Code quality
      └── 📄 security.yml      # Security checks
        """, language="text")
    
    # Ejemplos de workflows
    st.markdown("---")
    st.markdown("### 📝 Workflows Esenciales")
    
    workflow_tabs = st.tabs([
        "🧪 Testing Workflow",
        "🚀 Deploy Workflow", 
        "🔍 Code Quality",
        "🔐 Security Scan"
    ])
    
    with workflow_tabs[0]:
        st.markdown("**Archivo: `.github/workflows/test.yml`**")
        st.code("""
name: 🧪 Test Streamlit App

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🐍 Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: 📦 Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-streamlit

    - name: 🧪 Run tests
      run: |
        pytest tests/ -v
        
    - name: 🔍 Test app startup
      run: |
        timeout 30 streamlit run app.py --server.headless true --server.port 8501 &
        sleep 10
        curl -f http://localhost:8501 || exit 1

    - name: 📊 Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.python-version == '3.10'
        """, language="yaml")
    
    with workflow_tabs[1]:
        st.markdown("**Archivo: `.github/workflows/deploy.yml`**")
        st.code("""
name: 🚀 Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]
  workflow_run:
    workflows: ["🧪 Test Streamlit App"]
    types:
      - completed

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🔔 Notify deployment start
      uses: 8398a7/action-slack@v3
      with:
        status: custom
        custom_payload: |
          {
            "text": "🚀 Starting deployment to Streamlit Cloud",
            "color": "warning"
          }
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

    - name: 🎯 Trigger Streamlit Cloud deployment
      run: |
        # Streamlit Cloud auto-deploys on push to main
        echo "✅ Deployment triggered automatically"

    - name: 🔔 Notify deployment success
      uses: 8398a7/action-slack@v3
      with:
        status: success
        text: "✅ Deployment to Streamlit Cloud successful!"
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}

    - name: 🔔 Notify deployment failure
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: failure
        text: "❌ Deployment to Streamlit Cloud failed!"
      env:
        SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
        """, language="yaml")
    
    with workflow_tabs[2]:
        st.markdown("**Archivo: `.github/workflows/code-quality.yml`**")
        st.code("""
name: 🔍 Code Quality

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🐍 Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: 📦 Install quality tools
      run: |
        pip install black flake8 isort mypy bandit
        pip install -r requirements.txt

    - name: 🖤 Check code formatting (Black)
      run: black --check --diff .

    - name: 📏 Check code style (Flake8)
      run: flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

    - name: 🔀 Check import sorting (isort)
      run: isort --check-only --diff .

    - name: 🏷️ Type checking (MyPy)
      run: mypy . --ignore-missing-imports

    - name: 🔐 Security analysis (Bandit)
      run: bandit -r . -f json -o bandit-report.json

    - name: 📊 Upload reports
      uses: actions/upload-artifact@v3
      with:
        name: quality-reports
        path: |
          bandit-report.json
        """, language="yaml")
    
    with workflow_tabs[3]:
        st.markdown("**Archivo: `.github/workflows/security.yml`**")
        st.code("""
name: 🔐 Security Scan

on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * 1'  # Weekly on Monday at 2 AM

jobs:
  security:
    runs-on: ubuntu-latest

    steps:
    - name: 📥 Checkout code
      uses: actions/checkout@v4

    - name: 🔍 Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'

    - name: 📊 Upload Trivy scan results
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

    - name: 🐍 Security audit for Python
      run: |
        pip install safety
        safety check --json --output safety-report.json

    - name: 🔍 Dependency review
      uses: actions/dependency-review-action@v3
      if: github.event_name == 'pull_request'
        """, language="yaml")
    
    # Configuración de secretos
    st.markdown("---")
    st.markdown("### 🔐 Configuración de Secretos para Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Secretos comunes:**")
        secretos_actions = [
            "SLACK_WEBHOOK_URL",
            "DISCORD_WEBHOOK",
            "TELEGRAM_BOT_TOKEN",
            "CODECOV_TOKEN",
            "SONAR_TOKEN",
            "DOCKER_USERNAME",
            "DOCKER_PASSWORD"
        ]
        
        for secreto in secretos_actions:
            st.code(f"${{{{ secrets.{secreto} }}}}")
    
    with col2:
        st.markdown("**Cómo configurar:**")
        st.markdown("""
        1. Ve a tu repositorio en GitHub
        2. Settings → Secrets and variables → Actions
        3. Click "New repository secret"
        4. Agrega nombre y valor
        5. Save secret
        """)
        
        st.info("💡 Los secretos están encriptados y solo son visibles en los workflows")

def render_testing_automatizado():
    """Renderiza testing automatizado."""
    st.subheader("🧪 Testing Automatizado para Streamlit")
    
    st.markdown("""
    Implementa testing robusto para asegurar la calidad de tu aplicación.
    """)
    
    # Tipos de testing
    test_types = st.tabs([
        "🔧 Unit Tests",
        "🔗 Integration Tests",
        "🎭 UI Tests",
        "⚡ Performance Tests"
    ])
    
    with test_types[0]:
        st.markdown("### 🔧 Unit Tests")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Estructura de tests:**")
            st.code("""
📁 tests/
├── 📄 __init__.py
├── 📄 test_data_processing.py
├── 📄 test_calculations.py
├── 📄 test_utils.py
├── 📄 conftest.py
└── 📁 fixtures/
    ├── 📄 sample_data.csv
    └── 📄 expected_results.json
            """, language="text")
        
        with col2:
            st.markdown("**conftest.py:**")
            st.code("""
import pytest
import pandas as pd
import streamlit as st

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=100),
        'value': range(100),
        'category': ['A', 'B'] * 50
    })

@pytest.fixture
def mock_streamlit_session():
    # Mock session state
    if 'mock_session' not in st.session_state:
        st.session_state.mock_session = {}
    return st.session_state.mock_session
            """, language="python")
        
        st.markdown("**Ejemplo de test:**")
        st.code("""
# test_data_processing.py
import pytest
import pandas as pd
from your_app import process_data, calculate_metrics

class TestDataProcessing:
    
    def test_process_data_empty_input(self):
        \"\"\"Test with empty DataFrame\"\"\"
        empty_df = pd.DataFrame()
        result = process_data(empty_df)
        assert result is None or result.empty
    
    def test_process_data_valid_input(self, sample_dataframe):
        \"\"\"Test with valid input\"\"\"
        result = process_data(sample_dataframe)
        assert not result.empty
        assert 'processed_value' in result.columns
    
    def test_calculate_metrics(self, sample_dataframe):
        \"\"\"Test metric calculations\"\"\"
        metrics = calculate_metrics(sample_dataframe)
        
        assert 'mean' in metrics
        assert 'std' in metrics
        assert metrics['mean'] > 0
        assert metrics['std'] >= 0
    
    def test_invalid_data_handling(self):
        \"\"\"Test error handling\"\"\"
        invalid_df = pd.DataFrame({'wrong_column': [1, 2, 3]})
        
        with pytest.raises(KeyError):
            process_data(invalid_df)

# Ejecutar: pytest tests/test_data_processing.py -v
        """, language="python")
    
    with test_types[1]:
        st.markdown("### 🔗 Integration Tests")
        
        st.code("""
# test_integration.py
import pytest
import streamlit as st
from streamlit.testing.v1 import AppTest

class TestStreamlitIntegration:
    
    def test_app_loads_without_error(self):
        \"\"\"Test that the app loads successfully\"\"\"
        at = AppTest.from_file("app.py")
        at.run()
        
        # Check no exceptions occurred
        assert not at.exception
        
        # Check main title exists
        assert len(at.title) > 0
    
    def test_user_input_flow(self):
        \"\"\"Test complete user interaction flow\"\"\"
        at = AppTest.from_file("app.py")
        at.run()
        
        # Simulate user input
        at.text_input("user_name").input("Test User")
        at.selectbox("category").select("Option A")
        at.button("submit").click()
        
        at.run()
        
        # Verify expected outputs
        assert "Test User" in str(at.markdown)
        assert not at.exception
    
    def test_file_upload_functionality(self):
        \"\"\"Test file upload feature\"\"\"
        at = AppTest.from_file("app.py")
        at.run()
        
        # Simulate file upload
        test_data = b"name,value\\ntest,123"
        at.file_uploader("data_file").upload(
            ("test.csv", test_data)
        )
        
        at.run()
        
        # Check file was processed
        assert "File uploaded successfully" in str(at.success)

# Ejecutar: pytest tests/test_integration.py -v
        """, language="python")
    
    with test_types[2]:
        st.markdown("### 🎭 UI Tests con Selenium")
        
        st.code("""
# test_ui.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestStreamlitUI:
    
    @pytest.fixture
    def driver(self):
        # Configurar Chrome en modo headless
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        driver = webdriver.Chrome(options=options)
        yield driver
        driver.quit()
    
    def test_page_loads(self, driver):
        \"\"\"Test that page loads correctly\"\"\"
        driver.get("http://localhost:8501")
        
        # Wait for Streamlit to load
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        assert "Streamlit" in driver.title
    
    def test_widget_interaction(self, driver):
        \"\"\"Test widget interactions\"\"\"
        driver.get("http://localhost:8501")
        
        # Wait for app to load
        time.sleep(3)
        
        # Find and interact with slider
        slider = driver.find_element(By.CSS_SELECTOR, "[data-testid='stSlider'] input")
        driver.execute_script("arguments[0].value = 50", slider)
        
        # Trigger change event
        driver.execute_script("arguments[0].dispatchEvent(new Event('change'))", slider)
        
        # Wait for update
        time.sleep(2)
        
        # Verify result updated
        metrics = driver.find_elements(By.CSS_SELECTOR, "[data-testid='metric-container']")
        assert len(metrics) > 0

# requirements-test.txt adicional:
# selenium==4.15.0
# chromedriver-autoinstaller==0.6.2
        """, language="python")
    
    with test_types[3]:
        st.markdown("### ⚡ Performance Tests")
        
        st.code("""
# test_performance.py
import pytest
import time
import psutil
import pandas as pd
from memory_profiler import profile
from your_app import load_large_dataset, process_heavy_computation

class TestPerformance:
    
    def test_load_time_benchmark(self):
        \"\"\"Test that app loads within acceptable time\"\"\"
        start_time = time.time()
        
        # Simulate app loading
        result = load_large_dataset()
        
        load_time = time.time() - start_time
        
        # Should load within 5 seconds
        assert load_time < 5.0, f"Load time {load_time:.2f}s exceeds 5s limit"
    
    def test_memory_usage(self):
        \"\"\"Test memory consumption\"\"\"
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Perform memory-intensive operation
        large_df = pd.DataFrame(np.random.randn(100000, 50))
        processed = process_heavy_computation(large_df)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Should not use more than 500MB additional
        assert memory_increase < 500, f"Memory increase {memory_increase:.1f}MB too high"
    
    @profile  # Decorator from memory_profiler
    def test_function_memory_profile(self):
        \"\"\"Profile memory usage of specific function\"\"\"
        data = pd.DataFrame(np.random.randn(10000, 10))
        result = process_heavy_computation(data)
        return result
    
    def test_concurrent_users_simulation(self):
        \"\"\"Simulate multiple concurrent users\"\"\"
        import concurrent.futures
        import requests
        
        def make_request():
            try:
                response = requests.get("http://localhost:8501", timeout=5)
                return response.status_code == 200
            except:
                return False
        
        # Simulate 10 concurrent users
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # At least 80% should succeed
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.8, f"Success rate {success_rate:.1%} too low"

# requirements-test.txt adicional:
# memory-profiler==0.61.0
# psutil==5.9.0
        """, language="python")
    
    # Configuración de pytest
    st.markdown("---")
    st.markdown("### ⚙️ Configuración de pytest")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**pytest.ini:**")
        st.code("""
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    ui: marks tests as UI tests
        """, language="ini")
    
    with col2:
        st.markdown("**tox.ini (opcional):**")
        st.code("""
[tox]
envlist = py38,py39,py310,py311

[testenv]
deps = 
    pytest
    pytest-cov
    pytest-streamlit
    -r requirements.txt
    -r requirements-test.txt
commands = 
    pytest {posargs}

[testenv:lint]
deps = 
    flake8
    black
    isort
commands = 
    flake8 .
    black --check .
    isort --check-only .
        """, language="ini")

def render_build_deploy():
    """Renderiza automatización de build y deploy."""
    st.subheader("📦 Automatización de Build & Deploy")
    
    st.markdown("""
    Configura pipelines completos de CI/CD para tu aplicación Streamlit.
    """)
    
    # Pipeline stages
    pipeline_tabs = st.tabs([
        "🏗️ Build Pipeline",
        "🐳 Docker Integration",
        "🚀 Multi-Environment Deploy",
        "📋 Release Management"
    ])
    
    with pipeline_tabs[0]:
        st.markdown("### 🏗️ Build Pipeline Completo")
        
        st.code("""
# .github/workflows/ci-cd.yml
name: 🏗️ Complete CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
    tags: [ 'v*' ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.10'
  NODE_VERSION: '18'

jobs:
  # =====================================
  # 🧪 TESTING STAGE
  # =====================================
  test:
    name: 🧪 Test Suite
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']
    
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
        cache: 'pip'
        
    - name: 📦 Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
        
    - name: 🧪 Run tests
      run: |
        pytest --cov=. --cov-report=xml
        
    - name: 📊 Upload coverage
      uses: codecov/codecov-action@v3
      if: matrix.python-version == env.PYTHON_VERSION

  # =====================================
  # 🔍 CODE QUALITY STAGE  
  # =====================================
  quality:
    name: 🔍 Code Quality
    runs-on: ubuntu-latest
    needs: test
    
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        
    - name: 📦 Install tools
      run: |
        pip install black flake8 isort mypy bandit safety
        pip install -r requirements.txt
        
    - name: 🖤 Format check
      run: black --check --diff .
      
    - name: 📏 Lint check
      run: flake8 .
      
    - name: 🔀 Import sort check
      run: isort --check-only --diff .
      
    - name: 🏷️ Type check
      run: mypy . --ignore-missing-imports
      
    - name: 🔐 Security check
      run: |
        bandit -r . -f json -o bandit-report.json
        safety check --json --output safety-report.json
        
    - name: 📊 Upload artifacts
      uses: actions/upload-artifact@v3
      with:
        name: quality-reports
        path: |
          bandit-report.json
          safety-report.json

  # =====================================
  # 🏗️ BUILD STAGE
  # =====================================
  build:
    name: 🏗️ Build Application
    runs-on: ubuntu-latest
    needs: [test, quality]
    
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: 🐍 Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
        
    - name: 📦 Build package
      run: |
        pip install build
        python -m build
        
    - name: 📊 Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: dist
        path: dist/

  # =====================================
  # 🚀 DEPLOY STAGE
  # =====================================
  deploy:
    name: 🚀 Deploy Application
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    
    environment:
      name: production
      url: https://your-app.streamlit.app
      
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: 🔔 Notify deployment start
      run: |
        curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"🚀 Starting deployment of ${{ github.sha }}"}' \
        ${{ secrets.SLACK_WEBHOOK_URL }}
        
    - name: 🎯 Deploy to Streamlit Cloud
      run: |
        # Streamlit Cloud auto-deploys on push to main
        echo "✅ Deployment triggered"
        
    - name: 🔍 Health check
      run: |
        sleep 30  # Wait for deployment
        curl -f https://your-app.streamlit.app || exit 1
        
    - name: 🔔 Notify success
      run: |
        curl -X POST -H 'Content-type: application/json' \
        --data '{"text":"✅ Deployment successful! https://your-app.streamlit.app"}' \
        ${{ secrets.SLACK_WEBHOOK_URL }}
        """, language="yaml")
    
    with pipeline_tabs[1]:
        st.markdown("### 🐳 Integración con Docker")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dockerfile:**")
            st.code("""
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
            """, language="dockerfile")
        
        with col2:
            st.markdown("**docker-compose.yml:**")
            st.code("""
version: '3.8'

services:
  streamlit-app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data:ro
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Optional: Add Redis for caching
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  # Optional: Add database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: streamlit_db
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
            """, language="yaml")
        
        st.markdown("**GitHub Action para Docker:**")
        st.code("""
# .github/workflows/docker.yml
name: 🐳 Docker Build & Push

on:
  push:
    tags: [ 'v*' ]

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: 🔑 Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
        
    - name: 🏷️ Extract metadata
      id: meta
      uses: docker/metadata-action@v4
      with:
        images: your-username/streamlit-app
        tags: |
          type=ref,event=tag
          type=raw,value=latest
          
    - name: 🏗️ Build and push
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: ${{ steps.meta.outputs.tags }}
        labels: ${{ steps.meta.outputs.labels }}
        """, language="yaml")
    
    with pipeline_tabs[2]:
        st.markdown("### 🚀 Deploy Multi-Ambiente")
        
        st.markdown("**Configuración de ambientes:**")
        st.code("""
# .github/workflows/multi-env-deploy.yml
name: 🌍 Multi-Environment Deploy

on:
  push:
    branches: [ main, develop, staging ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        include:
          - branch: develop
            environment: development
            url: https://dev-your-app.streamlit.app
          - branch: staging  
            environment: staging
            url: https://staging-your-app.streamlit.app
          - branch: main
            environment: production
            url: https://your-app.streamlit.app
    
    if: github.ref == format('refs/heads/{0}', matrix.branch)
    
    environment:
      name: ${{ matrix.environment }}
      url: ${{ matrix.url }}
      
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      
    - name: ⚙️ Setup environment config
      run: |
        echo "Deploying to ${{ matrix.environment }}"
        
        # Copy environment-specific config
        cp .streamlit/config-${{ matrix.environment }}.toml .streamlit/config.toml
        
    - name: 🚀 Deploy to ${{ matrix.environment }}
      run: |
        echo "Deploying to ${{ matrix.url }}"
        # Add your deployment logic here
        
    - name: 🧪 Run smoke tests
      run: |
        sleep 30
        curl -f ${{ matrix.url }}/_stcore/health
        """, language="yaml")
        
        st.markdown("**Configuraciones por ambiente:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Development:**")
            st.code("""
# .streamlit/config-development.toml
[global]
developmentMode = true
logLevel = "debug"

[server]
runOnSave = true
allowRunOnSave = true

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
            """, language="toml")
        
        with col2:
            st.markdown("**Staging:**")
            st.code("""
# .streamlit/config-staging.toml
[global]
developmentMode = false
logLevel = "info"

[server]
runOnSave = false

[theme]
primaryColor = "#FFA500"
backgroundColor = "#FFFFFF"
            """, language="toml")
        
        with col3:
            st.markdown("**Production:**")
            st.code("""
# .streamlit/config-production.toml
[global]
developmentMode = false
logLevel = "warning"

[server]
runOnSave = false
enableCORS = false

[theme]
primaryColor = "#4CAF50"
backgroundColor = "#FFFFFF"
            """, language="toml")
    
    with pipeline_tabs[3]:
        st.markdown("### 📋 Release Management")
        
        st.markdown("**Automated Release Workflow:**")
        st.code("""
# .github/workflows/release.yml
name: 📦 Release Management

on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
    - name: 📥 Checkout
      uses: actions/checkout@v4
      with:
        fetch-depth: 0
        
    - name: 📝 Generate changelog
      id: changelog
      uses: metcalfc/changelog-generator@v4.0.1
      with:
        myToken: ${{ secrets.GITHUB_TOKEN }}
        
    - name: 📦 Create release
      uses: actions/create-release@v1
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      with:
        tag_name: ${{ github.ref }}
        release_name: Release ${{ github.ref }}
        body: |
          ## Changes in this Release
          ${{ steps.changelog.outputs.changelog }}
          
          ## Deployment
          - 🚀 Production: https://your-app.streamlit.app
          - 📊 Staging: https://staging-your-app.streamlit.app
          
        draft: false
        prerelease: false
        
    - name: 🔔 Notify team
      run: |
        curl -X POST -H 'Content-type: application/json' \\
        --data '{
          "text": "🎉 New release ${{ github.ref }} is live!",
          "attachments": [{
            "color": "good",
            "fields": [{
              "title": "Release Notes",
              "value": "${{ steps.changelog.outputs.changelog }}",
              "short": false
            }]
          }]
        }' \\
        ${{ secrets.SLACK_WEBHOOK_URL }}
        """, language="yaml")
        
        st.markdown("**Semantic Versioning:**")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Convenciones de versioning:**")
            st.markdown("""
            - `v1.0.0` - Major release (breaking changes)
            - `v1.1.0` - Minor release (new features)  
            - `v1.1.1` - Patch release (bug fixes)
            - `v1.1.1-beta.1` - Pre-release
            """)
        
        with col2:
            st.markdown("**Automatic versioning:**")
            st.code("""
# package.json (for semantic-release)
{
  "name": "streamlit-app",
  "version": "0.0.0-development",
  "scripts": {
    "semantic-release": "semantic-release"
  },
  "devDependencies": {
    "@semantic-release/changelog": "^6.0.0",
    "@semantic-release/git": "^10.0.0",
    "semantic-release": "^21.0.0"
  }
}
            """, language="json")

def render_monitoring_alerts():
    """Renderiza monitoreo y alertas."""
    st.subheader("📊 Monitoreo y Alertas Automatizadas")
    
    st.markdown("""
    Configura monitoreo proactivo y alertas para mantener tu aplicación saludable.
    """)
    
    # Tipos de monitoreo
    monitoring_tabs = st.tabs([
        "🔍 Health Monitoring",
        "📈 Performance Tracking", 
        "🚨 Error Alerting",
        "📊 Analytics Dashboard"
    ])
    
    with monitoring_tabs[0]:
        st.markdown("### 🔍 Health Monitoring")
        
        st.code("""
# .github/workflows/health-check.yml
name: 🔍 Health Monitoring

on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        environment:
          - name: "Production"
            url: "https://your-app.streamlit.app"
          - name: "Staging"  
            url: "https://staging-your-app.streamlit.app"
    
    steps:
    - name: 🔍 Health Check - ${{ matrix.environment.name }}
      run: |
        response=$(curl -s -o /dev/null -w "%{http_code}" ${{ matrix.environment.url }}/_stcore/health)
        
        if [ $response -eq 200 ]; then
          echo "✅ ${{ matrix.environment.name }} is healthy"
        else
          echo "❌ ${{ matrix.environment.name }} is unhealthy (HTTP $response)"
          exit 1
        fi
        
    - name: 🚨 Alert on failure
      if: failure()
      run: |
        curl -X POST -H 'Content-type: application/json' \\
        --data '{
          "text": "🚨 ALERT: ${{ matrix.environment.name }} health check failed!",
          "attachments": [{
            "color": "danger",
            "fields": [{
              "title": "Environment",
              "value": "${{ matrix.environment.name }}",
              "short": true
            }, {
              "title": "URL", 
              "value": "${{ matrix.environment.url }}",
              "short": true
            }, {
              "title": "Time",
              "value": "$(date)",
              "short": true
            }]
          }]
        }' \\
        ${{ secrets.SLACK_WEBHOOK_URL }}
        """, language="yaml")
        
        st.markdown("**Script de monitoreo avanzado:**")
        st.code("""
# health_monitor.py
import requests
import time
import json
from datetime import datetime

class HealthMonitor:
    def __init__(self, app_url, webhook_url):
        self.app_url = app_url
        self.webhook_url = webhook_url
        self.metrics = []
    
    def check_health(self):
        try:
            start_time = time.time()
            response = requests.get(f"{self.app_url}/_stcore/health", timeout=10)
            response_time = time.time() - start_time
            
            metric = {
                "timestamp": datetime.now().isoformat(),
                "status_code": response.status_code,
                "response_time": response_time,
                "status": "healthy" if response.status_code == 200 else "unhealthy"
            }
            
            self.metrics.append(metric)
            return metric
            
        except requests.exceptions.RequestException as e:
            metric = {
                "timestamp": datetime.now().isoformat(),
                "status_code": 0,
                "response_time": 0,
                "status": "error",
                "error": str(e)
            }
            self.metrics.append(metric)
            return metric
    
    def check_page_load(self):
        try:
            start_time = time.time()
            response = requests.get(self.app_url, timeout=30)
            load_time = time.time() - start_time
            
            # Check if it contains Streamlit content
            is_streamlit = "streamlit" in response.text.lower()
            
            return {
                "load_time": load_time,
                "status_code": response.status_code,
                "is_streamlit": is_streamlit,
                "size": len(response.content)
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def send_alert(self, message, color="warning"):
        payload = {
            "text": message,
            "attachments": [{
                "color": color,
                "timestamp": int(time.time())
            }]
        }
        
        try:
            requests.post(self.webhook_url, json=payload)
        except Exception as e:
            print(f"Failed to send alert: {e}")

# Usage
if __name__ == "__main__":
    monitor = HealthMonitor(
        app_url="https://your-app.streamlit.app",
        webhook_url=os.getenv("SLACK_WEBHOOK_URL")
    )
    
    health = monitor.check_health()
    page_load = monitor.check_page_load()
    
    if health["status"] != "healthy":
        monitor.send_alert(f"🚨 App is {health['status']}", "danger")
    elif page_load.get("load_time", 0) > 10:
        monitor.send_alert(f"⚠️ Slow page load: {page_load['load_time']:.2f}s", "warning")
        """, language="python")
    
    with monitoring_tabs[1]:
        st.markdown("### 📈 Performance Tracking")
        
        st.code("""
# performance_tracker.py
import streamlit as st
import time
import psutil
import requests
from datetime import datetime, timedelta

class PerformanceTracker:
    def __init__(self):
        if 'performance_metrics' not in st.session_state:
            st.session_state.performance_metrics = []
    
    def track_page_load(self, page_name):
        start_time = time.time()
        
        def end_tracking():
            load_time = time.time() - start_time
            metric = {
                "timestamp": datetime.now(),
                "page": page_name,
                "load_time": load_time,
                "memory_usage": self.get_memory_usage()
            }
            st.session_state.performance_metrics.append(metric)
            
            # Alert if slow
            if load_time > 5:
                self.send_performance_alert(page_name, load_time)
        
        return end_tracking
    
    def get_memory_usage(self):
        try:
            process = psutil.Process()
            return process.memory_info().rss / 1024 / 1024  # MB
        except:
            return 0
    
    def send_performance_alert(self, page, load_time):
        message = f"⚠️ Slow performance detected on {page}: {load_time:.2f}s"
        # Send to monitoring service
        
    def get_metrics_summary(self, hours=24):
        cutoff = datetime.now() - timedelta(hours=hours)
        recent_metrics = [
            m for m in st.session_state.performance_metrics 
            if m["timestamp"] > cutoff
        ]
        
        if not recent_metrics:
            return {}
        
        load_times = [m["load_time"] for m in recent_metrics]
        memory_usage = [m["memory_usage"] for m in recent_metrics]
        
        return {
            "avg_load_time": sum(load_times) / len(load_times),
            "max_load_time": max(load_times),
            "avg_memory": sum(memory_usage) / len(memory_usage),
            "max_memory": max(memory_usage),
            "total_page_views": len(recent_metrics)
        }

# Usage in your Streamlit app
tracker = PerformanceTracker()

def main():
    # Track page load
    end_tracking = tracker.track_page_load("main_page")
    
    # Your app content here
    st.title("My App")
    
    # Show performance metrics to admins
    if st.sidebar.checkbox("Show Performance Metrics", False):
        metrics = tracker.get_metrics_summary()
        if metrics:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Avg Load Time", f"{metrics['avg_load_time']:.2f}s")
            with col2:
                st.metric("Avg Memory", f"{metrics['avg_memory']:.1f} MB")
            with col3:
                st.metric("Page Views (24h)", metrics['total_page_views'])
    
    # End tracking
    end_tracking()
        """, language="python")
    
    with monitoring_tabs[2]:
        st.markdown("### 🚨 Error Alerting")
        
        st.code("""
# error_handler.py
import streamlit as st
import traceback
import logging
import requests
from datetime import datetime
import hashlib

class ErrorHandler:
    def __init__(self, webhook_url=None, environment="production"):
        self.webhook_url = webhook_url
        self.environment = environment
        self.setup_logging()
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('errors.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error, context=None):
        error_info = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "environment": self.environment,
            "user_agent": self.get_user_agent(),
            "session_id": self.get_session_id()
        }
        
        # Create error hash for deduplication
        error_hash = self.create_error_hash(error_info)
        error_info["error_hash"] = error_hash
        
        # Log error
        self.logger.error(f"Error {error_hash}: {error_info}")
        
        # Send alert (with rate limiting)
        if self.should_send_alert(error_hash):
            self.send_error_alert(error_info)
        
        return error_info
    
    def create_error_hash(self, error_info):
        content = f"{error_info['error_type']}:{error_info['error_message']}"
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def should_send_alert(self, error_hash):
        # Simple rate limiting - store in session state
        if 'error_alerts_sent' not in st.session_state:
            st.session_state.error_alerts_sent = {}
        
        last_sent = st.session_state.error_alerts_sent.get(error_hash)
        if last_sent:
            # Don't send same error more than once per hour
            time_diff = datetime.now() - last_sent
            if time_diff.total_seconds() < 3600:
                return False
        
        st.session_state.error_alerts_sent[error_hash] = datetime.now()
        return True
    
    def send_error_alert(self, error_info):
        if not self.webhook_url:
            return
        
        payload = {
            "text": f"🚨 Error in {self.environment}",
            "attachments": [{
                "color": "danger",
                "fields": [
                    {"title": "Error Type", "value": error_info["error_type"], "short": True},
                    {"title": "Error Hash", "value": error_info["error_hash"], "short": True},
                    {"title": "Message", "value": error_info["error_message"][:500], "short": False},
                    {"title": "Time", "value": error_info["timestamp"], "short": True},
                    {"title": "Environment", "value": error_info["environment"], "short": True}
                ]
            }]
        }
        
        try:
            requests.post(self.webhook_url, json=payload, timeout=5)
        except Exception as e:
            self.logger.error(f"Failed to send error alert: {e}")
    
    def get_user_agent(self):
        try:
            return st.context.headers.get("user-agent", "Unknown")
        except:
            return "Unknown"
    
    def get_session_id(self):
        return getattr(st.session_state, '_session_id', 'Unknown')

# Error boundary decorator
def error_boundary(error_handler):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_info = error_handler.handle_error(e, {
                    "function": func.__name__,
                    "args": str(args)[:200],
                    "kwargs": str(kwargs)[:200]
                })
                
                # Show user-friendly error
                st.error("🚨 Something went wrong. The error has been logged.")
                
                # Show details in development
                if error_handler.environment == "development":
                    with st.expander("Error Details"):
                        st.code(error_info["traceback"])
                
                return None
        return wrapper
    return decorator

# Usage
error_handler = ErrorHandler(
    webhook_url=st.secrets.get("SLACK_WEBHOOK_URL"),
    environment=st.secrets.get("ENVIRONMENT", "production")
)

@error_boundary(error_handler)
def risky_function():
    # Your code that might fail
    return some_operation()
        """, language="python")
    
    with monitoring_tabs[3]:
        st.markdown("### 📊 Analytics Dashboard")
        
        # Create a simple analytics dashboard
        st.markdown("**Vista previa del Dashboard de Analytics:**")
        
        # Mock data for demonstration
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Uptime", "99.9%", delta="0.1%")
        with col2:
            st.metric("Avg Response Time", "234ms", delta="-15ms")
        with col3:
            st.metric("Daily Users", "1,247", delta="127")
        with col4:
            st.metric("Error Rate", "0.02%", delta="-0.01%")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:            # Response time chart
            response_times = pd.DataFrame({
                'Time': pd.date_range('2024-01-01', periods=24, freq='h'),
                'Response Time (ms)': np.random.normal(250, 50, 24)
            })
            
            fig = px.line(response_times, x='Time', y='Response Time (ms)', 
                         title="Response Time Over 24h")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Error distribution
            error_types = pd.DataFrame({
                'Error Type': ['ConnectionError', 'ValueError', 'KeyError', 'TimeoutError'],
                'Count': [45, 23, 12, 8]
            })
            
            fig = px.pie(error_types, values='Count', names='Error Type',
                        title="Error Distribution")
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Código para Analytics:**")
        st.code("""
# analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

class AnalyticsDashboard:
    def __init__(self):
        self.init_session_state()
    
    def init_session_state(self):
        if 'analytics_data' not in st.session_state:
            st.session_state.analytics_data = {
                'page_views': [],
                'user_sessions': [],
                'errors': [],
                'performance_metrics': []
            }
    
    def track_page_view(self, page_name):
        st.session_state.analytics_data['page_views'].append({
            'timestamp': datetime.now(),
            'page': page_name,
            'user_id': self.get_user_id(),
            'session_id': self.get_session_id()
        })
    
    def track_user_action(self, action, details=None):
        st.session_state.analytics_data['user_sessions'].append({
            'timestamp': datetime.now(),
            'action': action,
            'details': details,
            'user_id': self.get_user_id(),
            'session_id': self.get_session_id()
        })
    
    def render_dashboard(self):
        st.title("📊 Analytics Dashboard")
        
        # Time range selector
        time_range = st.selectbox(
            "Time Range",
            ["Last 24 hours", "Last 7 days", "Last 30 days"]
        )
        
        hours_map = {
            "Last 24 hours": 24,
            "Last 7 days": 168,
            "Last 30 days": 720
        }
        
        hours = hours_map[time_range]
        cutoff = datetime.now() - timedelta(hours=hours)
        
        # Filter data
        page_views = [
            pv for pv in st.session_state.analytics_data['page_views']
            if pv['timestamp'] > cutoff
        ]
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Page Views", len(page_views))
        
        with col2:
            unique_users = len(set(pv['user_id'] for pv in page_views))
            st.metric("Unique Users", unique_users)
        
        with col3:
            unique_sessions = len(set(pv['session_id'] for pv in page_views))
            st.metric("Sessions", unique_sessions)
        
        with col4:
            if page_views:
                avg_session_length = len(page_views) / unique_sessions
                st.metric("Avg Session Length", f"{avg_session_length:.1f} pages")
        
        # Charts
        if page_views:
            # Page views over time
            df_views = pd.DataFrame(page_views)
            df_views['hour'] = df_views['timestamp'].dt.floor('H')
            hourly_views = df_views.groupby('hour').size().reset_index(name='views')
            
            fig = px.line(hourly_views, x='hour', y='views', 
                         title="Page Views Over Time")
            st.plotly_chart(fig, use_container_width=True)
            
            # Most popular pages
            page_counts = df_views['page'].value_counts()
            fig = px.bar(x=page_counts.index, y=page_counts.values,
                        title="Most Popular Pages")
            st.plotly_chart(fig, use_container_width=True)
    
    def get_user_id(self):
        # Simple user tracking
        if 'user_id' not in st.session_state:
            st.session_state.user_id = f"user_{hash(str(datetime.now()))}"
        return st.session_state.user_id
    
    def get_session_id(self):
        # Session tracking
        return getattr(st.session_state, '_session_id', 'unknown')

# Usage in your main app
analytics = AnalyticsDashboard()

def main():
    analytics.track_page_view("main_page")
    
    # Your app content
    st.title("My App")
    
    # Admin panel
    if st.sidebar.checkbox("Show Analytics", False):
        analytics.render_dashboard()
        """, language="python")

if __name__ == "__main__":
    run()

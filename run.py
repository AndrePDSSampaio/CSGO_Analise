#!/usr/bin/env python3
"""
CS:GO Analysis Dashboard Runner

Simple script to launch the Streamlit application.
This script provides an easy way to run the dashboard with proper configuration.
"""

import sys
import subprocess
import os

def check_requirements():
    """Check if required files exist."""
    required_files = ['streamlit_app.py', 'csgo_dados.csv', 'requirements.txt']
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Arquivos necessários não encontrados:")
        for file in missing_files:
            print(f"   - {file}")
        print("\nPor favor, certifique-se de que todos os arquivos estão presentes.")
        return False
    
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências.")
        return False

def run_streamlit():
    """Run the Streamlit application."""
    print("🚀 Iniciando CS:GO Analysis Dashboard...")
    print("📊 A aplicação será aberta em: http://localhost:8501")
    print("🔄 Pressione Ctrl+C para parar a aplicação")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação encerrada.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar a aplicação: {e}")

def main():
    """Main function to coordinate the application launch."""
    print("🎮 CS:GO Player Analysis Dashboard")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Run application
    run_streamlit()

if __name__ == "__main__":
    main()
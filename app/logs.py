import logging
import os

# Obter o diretório atual do script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Criar diretório de logs se não existir
log_dir = os.path.join(current_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

# Caminho absoluto para o arquivo de log
log_file = os.path.join(log_dir, "app.log")

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file),  # Caminho absoluto para o arquivo de log
        logging.StreamHandler()
    ]
)

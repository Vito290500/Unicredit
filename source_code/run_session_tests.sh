#!/bin/bash

# Script per eseguire i test di sessione in Docker
# Uso: ./run_session_tests.sh

echo "🐳 ESECUZIONE TEST SESSIONE IN DOCKER"
echo "====================================="

# Verifica se Docker è in esecuzione
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker non è in esecuzione!"
    exit 1
fi

# Trova il container dell'applicazione
CONTAINER_NAME=$(docker ps --format "table {{.Names}}" | grep -E "(web|app|django)" | head -1)

if [ -z "$CONTAINER_NAME" ]; then
    echo "❌ Container dell'applicazione non trovato!"
    echo "Containers disponibili:"
    docker ps --format "table {{.Names}}\t{{.Image}}"
    exit 1
fi

echo "📦 Usando container: $CONTAINER_NAME"

# Esegui i test nel container
echo "🧪 Esecuzione test..."
docker exec -it $CONTAINER_NAME python manage.py test tests.test_session_management -v 2

# Oppure esegui il test direttamente
echo ""
echo "🔄 Esecuzione test alternativa..."
docker exec -it $CONTAINER_NAME python tests/test_session_management.py

echo ""
echo "✅ Test completati!"
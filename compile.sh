#!/bin/bash

echo "Iniciando compilación de LaTeX a PDF vía Docker..."
docker compose up

echo "✅ Compilación finalizada. Revisa el PDF en output/TFM_Final.pdf"
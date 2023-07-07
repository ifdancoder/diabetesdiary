#!/usr/bin/env python
from config import DevelopmentConfig, ProductionConfig

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()

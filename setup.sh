#!/bin/bash
# Setup script for UniLand Bot

set -e

echo "🚀 Setting up UniLand Bot..."

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.cargo/bin:$PATH"
fi

# Create virtual environment
echo "🐍 Creating virtual environment..."
uv venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
uv pip install -r requirements.txt

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your credentials!"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs media staticfiles bot_sessions

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python manage.py collectstatic --noinput

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Telegram bot credentials"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. Run the bot: python manage.py runbot"
echo "4. Run Django server: python manage.py runserver"
echo "5. Run Celery worker: celery -A config worker -l info"
echo "6. Run Celery beat: celery -A config beat -l info"

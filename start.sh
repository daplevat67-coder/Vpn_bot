#!/bin/bash
# Telegram Bot Builder — start/stop script

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$PROJECT_DIR/data/bot.pid"
LOGFILE="$PROJECT_DIR/bot/logs/bot.log"

mkdir -p "$PROJECT_DIR/data" "$PROJECT_DIR/bot/logs"

start() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "Bot is already running (PID $(cat "$PIDFILE"))"
        return 1
    fi
    echo "Starting Telegram Bot Builder..."
    cd "$PROJECT_DIR"
    nohup python3 -m bot.main > "$LOGFILE" 2>&1 &
    echo $! > "$PIDFILE"
    echo "Bot started (PID $(cat "$PIDFILE")). Log: $LOGFILE"
}

stop() {
    if [ ! -f "$PIDFILE" ]; then
        echo "Bot is not running."
        return 1
    fi
    PID=$(cat "$PIDFILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping bot (PID $PID)..."
        kill "$PID"
        sleep 2
        if kill -0 "$PID" 2>/dev/null; then
            kill -9 "$PID"
        fi
        rm -f "$PIDFILE"
        echo "Bot stopped."
    else
        echo "Bot process not found. Cleaning up."
        rm -f "$PIDFILE"
    fi
}

status() {
    if [ -f "$PIDFILE" ] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
        echo "Bot is running (PID $(cat "$PIDFILE"))"
    else
        echo "Bot is not running."
    fi
}

restart() {
    stop
    sleep 1
    start
}

case "${1:-}" in
    start)   start ;;
    stop)    stop ;;
    restart) restart ;;
    status)  status ;;
    *)
        echo "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

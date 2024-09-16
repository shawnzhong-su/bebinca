#!/bin/bash

# 设置 FastAPI 应用程序的文件路径和名称
APP_MODULE="viper:app"
# 临时目录
TMP_PATH="/var/run/myapp"
# 日志文件路径
LOG_FILE="/var/log/myapp.log"

# 可以写本地具体路径 如:/usr/bin/uvicorn
UVICORN_BIN="uvicorn"

# 默认参数
UVICORN_OPTS="--host 0.0.0.0 --port 8848"

# 创建必要的目录
mkdir -p $TMP_PATH
touch $LOG_FILE

# 日志记录函数
log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') $1" | tee -a $LOG_FILE
}

# 检查依赖
check_dependencies() {
    command -v $UVICORN_BIN >/dev/null 2>&1 || { log "Uvicorn not found. Aborting."; exit 1; }
}

# 启动 FastAPI 应用程序
start() {
    log "准备启动应用程序..."
    log "运行脚本: $UVICORN_BIN $APP_MODULE $UVICORN_OPTS $@"
    $UVICORN_BIN $APP_MODULE $UVICORN_OPTS "$@" &
    echo $! > $TMP_PATH/app.pid
    log "应用程序已启动，PID: $(cat $TMP_PATH/app.pid)"
}

# 重启 FastAPI 应用程序
restart() {
    log "准备重启应用程序..."
    stop
    start "$@"
}

# 关闭 FastAPI 应用程序
stop() {
    log "准备关闭应用程序..."
    if [ -f $TMP_PATH/app.pid ]; then
        pid=$(cat $TMP_PATH/app.pid)
        log "执行删除进程: kill $pid"
        kill $pid
        if [ $? -eq 0 ]; then
            log "进程 $pid 已成功终止"
            rm $TMP_PATH/app.pid
        else
            log "无法终止进程 $pid"
        fi
    else
        log "PID 文件未找到，服务可能未运行."
    fi
}

# 解析命令行参数
case "$1" in
    start)
        shift
        check_dependencies
        start "$@"
        ;;
    restart)
        shift
        check_dependencies
        restart "$@"
        ;;
    stop)
        check_dependencies
        stop
        ;;
    *)
        echo "Usage: $0 {start|restart|stop}"
        exit 1
        ;;
esac
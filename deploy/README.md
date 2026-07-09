# 生产部署（Lighthouse）

nginx 已将 `/api*` 反代到 `http://localhost:8000`。本仓库只负责通过 **gunicorn + systemd** 管理监听 8000 端口的 Django 进程。

## 服务器一次性初始化

用具备 `sudo` 权限的账号 SSH 登录后执行：

```bash
cd /home/lighthouse/proj/next-server
git fetch origin main
git checkout -f origin/main

# 在现有虚拟环境中安装 gunicorn 等依赖
env/bin/pip install -r requirements.txt

# 确认 .env 为生产配置（DEBUG=False、ALLOWED_HOSTS、DB_* 等）
# 所需键名可参考 .env_backup

mkdir -p staticfiles

# 安装 systemd 单元
sudo cp deploy/next-server.service /etc/systemd/system/next-server.service
sudo systemctl daemon-reload
sudo systemctl enable next-server

# 允许部署用户无密码重启服务
sudo cp deploy/sudoers-next-server /etc/sudoers.d/next-server
sudo chmod 440 /etc/sudoers.d/next-server
sudo visudo -cf /etc/sudoers.d/next-server

# 从 runserver 切到 gunicorn
pkill -f "manage.py runserver" || true
sudo systemctl start next-server
sudo systemctl status next-server
curl -fsS http://127.0.0.1:8000/healthz/
```

**不要**改现有 nginx 的 `/api` location，除非还需要把 `/admin/`、`/upload/`、`/mailinglist/` 暴露到公网。

## 日常部署

由 `.github/workflows/deploy.yml` 在 push 到 `main` 时自动执行：

1. `git fetch` + checkout `origin/main`
2. `pip install -r requirements.txt`
3. `migrate` + `collectstatic`
4. `systemctl restart next-server`
5. 探活 `http://127.0.0.1:8000/healthz/`

## 日志

```bash
sudo journalctl -u next-server -f
sudo journalctl -u next-server -n 200 --no-pager
```

## 回滚

选取一个已知可用的 commit SHA（Actions 日志里会打印 `Deployed commit:`）：

```bash
cd /home/lighthouse/proj/next-server
git fetch origin
git checkout -f <previous_sha>
env/bin/pip install -r requirements.txt
# 除非确认安全，否则不要 reverse migrations
env/bin/python manage.py collectstatic --noinput
sudo systemctl restart next-server
curl -fsS http://127.0.0.1:8000/healthz/
```

## 手动重启 / 查看状态

```bash
sudo systemctl restart next-server
sudo systemctl status next-server
sudo systemctl is-active next-server
```

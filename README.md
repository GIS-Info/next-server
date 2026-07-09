# next-server

“GIS海外院校和项目信息”下一代网站的后端部分（Django）。

## 本地开发

```bash
python manage.py runserver
```

## 生产部署

生产环境由 **nginx（已有）→ gunicorn:8000（systemd 托管）** 组成。

- 一次性上机、切流、回滚、日志：见 [deploy/README.md](deploy/README.md)
- CI 自动部署：push `main` 触发 [.github/workflows/deploy.yml](.github/workflows/deploy.yml)

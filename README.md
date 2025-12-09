# Auto Task Project

一个基于 OCR + ADB 的手机自动化任务系统，功能包括：

- 自动看新闻
- 自动看视频
- 自动看直播
- 自动听新闻
- OCR 截图文字识别
- AI 自动生成评论

## 运行方式

```bash
pip install -r requirements.txt
python main.py
```

需要配置环境变量：

```bash
export DEEPSEEK_API_KEY=你的key
```

截图 & 模板文件放在：

```bash
templates/screenshots/
templates/buttons/
```

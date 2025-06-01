# GuardianAI

**GuardianAI** is an open-source content moderation toolkit designed to detect and filter nudity, explicit language, and other offensive content across multiple media types. It works with videos, blogs, apps, and is deployable on Android TV, mobile, and web platforms.

## Features

- 🎞️ **Video Moderation** — Detect and blur nudity or explicit scenes using computer vision.
- 📝 **Text Moderation** — Filter profanity and offensive language in blogs, comments, and captions.
- 📱 **Cross-Platform** — Android TV, mobile, and web-ready.
- ⚡ **Real-Time Processing** — Stream-safe moderation with low-latency options.
- 🔌 **Modular Design** — Use only what you need: video, text, or both.
- 🔍 **AI-Powered** — Leverages modern ML/NLP models for content analysis.

## Use Cases

- Family-safe content streaming  
- Moderated video sharing platforms  
- Comment & blog filtering  
- Educational platforms  
- Smart TV apps  

## Usage

- ensure that you have docker installed
- run the following command in your terminal
```bash
docker run --name guardianai --rm -p 8000:8000 -v $(pwd):/app guardianai-app
```

- then open http://0.0.0.0:8000/ in your browser.
- upload a video, wait for it to process
- download the video 
- enjoy clean content

## Contributing
PRs welcome! Please follow the contribution guide in CONTRIBUTING.md.

## License
MIT License


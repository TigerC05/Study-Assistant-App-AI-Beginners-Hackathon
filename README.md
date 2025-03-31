# Study Assistant Cue Card Application

**Version Date:** March 31, 2025  
**Authors:** Teige Cordiner & Curtis Lawrence  

## Introduction

Ever caught yourself flipping over a flashcard too early and thinking, *"Eh, close enough"*? We’ve all been there. That’s why we created **Cue Card Assistant**—your personal AI-powered study buddy that keeps you honest and makes learning more engaging.

Whether you're preparing for exams, mastering a new language, or reinforcing concepts, **Cue Card Assistant** uses AI to provide an interactive, hands-free way to study.

## Inspiration

Traditional flashcard systems often rely on self-assessment, which can lead to overestimating knowledge. We wanted to create a tool that actively quizzes users and prevents self-deception when recalling answers. Our goal was to combine the efficiency of spaced repetition with the interactivity of AI-powered study techniques.

## How We Use AI

Cue Card Assistant incorporates AI to:
- **Use Speech-to-Text**: Users can speak their answers aloud, and the assistant will transcribe and evaluate them.
- **Enable Text-to-Speech**: The assistant can read cue cards out loud, making hands-free studying possible.
- **Enhance Learning with Spaced Repetition**: Using the [SuperMemo 2](https://www.supermemo.com/en/blog/application-of-a-computer-to-improve-the-results-obtained-in-working-with-the-supermemo-method) algorithm, the app intelligently schedules review sessions for optimal retention.

## Dependencies

To run the project, ensure you have Python installed and install the required dependencies:

```sh
pip install flask flask-login flask-sqlalchemy
```

## Getting Started
1. Navigate into your preferred directory
```sh
cd /Users/yourname/preferred/dir
```
2. Clone this repository:
```sh
git clone https://github.com/TigerC05/Study-Assistant-App-AI-Beginners-Hackathon.git
```
3. Navigate to the project folder:
```sh
cd Study-Assistant-App-AI-Beginners-Hackathon
```
3. Install dependencies (see above).
4. Run the main.py:
```sh
python3 main.py
```
5. Open http://127.0.0.1:5000/
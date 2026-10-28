# Phishing Awareness Training

A beginner-friendly, responsive cybersecurity awareness course built with plain HTML, CSS, and JavaScript. Learn to recognize phishing emails, deceptive websites, and social engineering, then check your understanding with a ten-question interactive quiz.

## Problem statement

Phishing messages can use familiar names, convincing designs, and pressure to persuade people to click links, open files, disclose information, or send money. People need practical, accessible guidance for spotting warning signs and choosing a safe next step.

## Objectives

- Explain common phishing channels and social engineering tactics in simple language.
- Show safe, fictional examples of suspicious messages and lookalike addresses.
- Teach repeatable habits for verifying requests and reporting suspicious messages.
- Provide immediate quiz feedback, explanations, a score, and review recommendations.

## Features

- Responsive single-page course with working in-page navigation and a reading progress indicator.
- Clear sections for phishing basics, email clues, fake websites, social engineering, case studies, and protective habits.
- Fictional educational examples only; no credential collection, real malicious URLs, or user accounts.
- Ten multiple-choice questions, each with four options and one correct answer.
- Immediate answer feedback and explanation, score and percentage, review topics, and a retake control.
- Final assessment with correct/incorrect totals, performance summary, recommended review topics, and restart control.
- Accessible landmarks, labels, keyboard focus styling, skip link, and reduced-motion support.
- No framework, backend, paid service, or build step required.

## Technologies

- HTML5
- CSS3
- Vanilla JavaScript
- Visual Studio Code
- Any modern desktop or mobile browser

## Folder structure

```text
Phishing-Awareness-Training/
├── index.html
├── css/
│   └── style.css
├── js/
│   ├── main.js
│   └── quiz.js
├── assets/
│   └── README.md
└── README.md
```

## Installation and setup

1. Create a folder named `Phishing-Awareness-Training`.
2. Inside it, create `index.html`, `README.md`, and the `css`, `js`, and `assets` folders.
3. Create `css/style.css`, `js/main.js`, `js/quiz.js`, and `assets/README.md`.
4. Paste the corresponding project source into each file and save.
5. Open the project folder in VS Code using **File → Open Folder**.

These files are also ready to run directly; no package installation or server is necessary.

## Run locally in VS Code

1. Open `index.html` in VS Code.
2. Use **File → Open Folder** if you have not opened the project folder already.
3. To preview, either open the file in your browser from File Explorer or use a local-preview extension such as Live Server if it is already installed.
4. With Live Server, right-click `index.html` and select **Open with Live Server**. The browser will open the local page.
5. The training and quiz run locally. The optional Google Fonts import may need internet access; system-font fallbacks are included.

## How to use the module

1. Select **Start training** or choose a topic from the navigation.
2. Read each section and review the safe, fictional examples.
3. In the quiz, select one option and press **Submit answer**.
4. Read the immediate explanation, then press **Next question**.
5. After question ten, review your score, percentage, and any recommended topics.
6. Visit **Training summary** for correct and incorrect totals and the performance summary.
7. Use **Retake quiz** to retry, or **Restart training** in the assessment to reset and return home.

## Quiz functionality

The questions and answer explanations are defined in `js/quiz.js`. `js/main.js` renders the current question, checks one selected answer, displays feedback, calculates the score, records missed topics, and updates the final assessment. Results exist only in the current page session; no answers or personal information are transmitted or stored.

## Expected output

- A responsive training website with eight topic areas, sample scenarios, and a scroll progress indicator.
- A ten-question quiz with four answers per question, immediate explanations, and sequential navigation.
- A results summary showing score out of ten, percentage, correct/incorrect totals, and suggested review topics.
- A final assessment with a performance summary and controls to retake or restart.

## Test checklist

- Select each main-navigation item and confirm it scrolls to the matching section.
- Resize the browser or use its mobile device preview; open and close the navigation menu.
- Submit without selecting an answer and confirm the quiz asks you to choose one.
- Complete the quiz with both correct and incorrect answers; check score, percentage, totals, and recommendations.
- Retake the quiz and confirm the score and missed topics reset.
- Finish again and use **Restart training**; confirm the quiz and assessment reset and the page returns to Home.
- Confirm fictional sample links are presentation-only and do not navigate to external sites.

## Screenshots for submission

1. Run the website in a browser and maximize the window for a desktop screenshot.
2. Capture the Home page and one or more content sections with **Windows + Shift + S** (Snipping Tool).
3. Capture the completed quiz results and final assessment after answering all ten questions.
4. Save screenshots in a separate submission folder, not in the source folders unless requested.
5. Avoid including private email, account, or personal information in screenshots.

## Upload to GitHub

1. Sign in to GitHub and create a new repository, for example `Phishing-Awareness-Training`. Do not add a README there if you already have this one locally.
2. In VS Code, open **Terminal → New Terminal** with this project as the current folder.
3. If Git is initialized and configured, run:

   ```powershell
   git init
   git add index.html css js assets README.md
   git commit -m "Create phishing awareness training project"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/Phishing-Awareness-Training.git
   git push -u origin main
   ```

4. Replace `YOUR-USERNAME` with your GitHub username. GitHub may ask you to authenticate using its normal sign-in flow.
5. Refresh the repository page and confirm the files are present. Never commit passwords, tokens, private messages, or screenshots containing personal information.

If Git is already initialized, skip `git init`. If an `origin` remote already exists, inspect it with `git remote -v` and update it only if appropriate.

## Future enhancements

- Add optional localization and more accessible-language versions.
- Add printable learning notes or downloadable, non-sensitive completion summaries.
- Add more question sets and scenario variations while preserving the offline, no-data-collection design.

This training supports awareness practice only; completing the quiz does not certify professional cybersecurity competence.

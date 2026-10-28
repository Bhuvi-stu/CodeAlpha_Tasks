(() => {
  const nav = document.querySelector(".primary-navigation");
  const menuToggle = document.querySelector(".menu-toggle");
  const progressTrack = document.querySelector(".progress-track");
  const progressFill = document.querySelector(".progress-fill");
  const answerForm = document.querySelector("#answer-form");
  const optionsContainer = document.querySelector("#answer-options");
  const questionText = document.querySelector("#question-text");
  const questionCount = document.querySelector("#quiz-count");
  const scoreText = document.querySelector("#quiz-score");
  const quizProgress = document.querySelector("#quiz-progress");
  const feedback = document.querySelector("#answer-feedback");
  const submitButton = document.querySelector("#submit-answer");
  const nextButton = document.querySelector("#next-question");
  const quizContent = document.querySelector("#quiz-content");
  const quizResults = document.querySelector("#quiz-results");
  const assessmentContent = document.querySelector("#assessment-content");

  let questionIndex = 0;
  let score = 0;
  let answered = false;
  const missedTopics = new Set();

  function updatePageProgress() {
    const scrollable = document.documentElement.scrollHeight - window.innerHeight;
    const percentage = scrollable > 0 ? Math.round((window.scrollY / scrollable) * 100) : 0;
    progressFill.style.width = `${percentage}%`;
    progressTrack.setAttribute("aria-valuenow", String(percentage));
  }

  window.addEventListener("scroll", updatePageProgress, { passive: true });
  window.addEventListener("resize", updatePageProgress);
  updatePageProgress();

  menuToggle.addEventListener("click", () => {
    const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
    menuToggle.setAttribute("aria-expanded", String(!isOpen));
    nav.classList.toggle("open", !isOpen);
  });

  nav.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      nav.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
    }
  });

  function renderQuestion() {
    const question = quizQuestions[questionIndex];
    answered = false;
    questionCount.textContent = `Question ${questionIndex + 1} of ${quizQuestions.length}`;
    scoreText.textContent = `Score: ${score}`;
    quizProgress.style.width = `${(questionIndex / quizQuestions.length) * 100}%`;
    questionText.textContent = question.question;
    optionsContainer.replaceChildren();
    feedback.hidden = true;
    feedback.className = "answer-feedback";
    nextButton.hidden = true;
    submitButton.hidden = false;

    question.options.forEach((option, index) => {
      const label = document.createElement("label");
      label.className = "answer-option";
      const input = document.createElement("input");
      input.type = "radio";
      input.name = "quiz-answer";
      input.value = String(index);
      input.required = true;
      const text = document.createElement("span");
      text.textContent = option;
      label.append(input, text);
      optionsContainer.append(label);
    });
  }

  answerForm.addEventListener("submit", (event) => {
    event.preventDefault();
    if (answered) return;

    const selected = answerForm.querySelector('input[name="quiz-answer"]:checked');
    if (!selected) {
      feedback.hidden = false;
      feedback.className = "answer-feedback incorrect";
      feedback.textContent = "Choose an answer before submitting.";
      return;
    }

    answered = true;
    const question = quizQuestions[questionIndex];
    const isCorrect = Number(selected.value) === question.answer;
    if (isCorrect) {
      score += 1;
    } else {
      missedTopics.add(question.topic);
    }
    scoreText.textContent = `Score: ${score}`;
    feedback.hidden = false;
    feedback.className = `answer-feedback ${isCorrect ? "correct" : "incorrect"}`;
    feedback.replaceChildren();
    const result = document.createElement("strong");
    result.textContent = isCorrect ? "Correct!" : "Not quite.";
    const explanation = document.createElement("p");
    explanation.textContent = question.explanation;
    feedback.append(result, explanation);
    answerForm.querySelectorAll('input[name="quiz-answer"]').forEach((input) => {
      input.disabled = true;
    });
    submitButton.hidden = true;
    nextButton.textContent = questionIndex === quizQuestions.length - 1 ? "View results →" : "Next question →";
    nextButton.hidden = false;
    quizProgress.style.width = `${((questionIndex + 1) / quizQuestions.length) * 100}%`;
  });

  function recommendationsMarkup() {
    if (missedTopics.size === 0) {
      return "<p>You answered every question correctly. Keep using the pause, check, and verify habits.</p>";
    }
    const list = document.createElement("ul");
    list.className = "recommendation-list";
    missedTopics.forEach((topic) => {
      const item = document.createElement("li");
      item.textContent = `Review: ${topic}`;
      list.append(item);
    });
    return list;
  }

  function showResults() {
    const incorrect = quizQuestions.length - score;
    const percentage = Math.round((score / quizQuestions.length) * 100);
    const summary = percentage >= 80
      ? "Strong awareness: you’re applying useful verification habits."
      : percentage >= 60
        ? "Good start: review the topics below to strengthen your habits."
        : "Keep practicing: revisit the recommended topics and try again.";

    quizContent.hidden = true;
    quizResults.hidden = false;
    quizProgress.style.width = "100%";
    quizResults.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = "Quiz complete";
    const scoreElement = document.createElement("p");
    scoreElement.className = "quiz-result-score";
    scoreElement.textContent = `${score} / ${quizQuestions.length}`;
    const resultSummary = document.createElement("p");
    resultSummary.className = "quiz-result-summary";
    resultSummary.textContent = `${percentage}% · ${score} correct · ${incorrect} incorrect. ${summary}`;
    const recommendationTitle = document.createElement("strong");
    recommendationTitle.textContent = "Suggested review";
    const recommendations = recommendationsMarkup();
    const retake = document.createElement("button");
    retake.className = "button button-primary";
    retake.id = "retake-quiz";
    retake.type = "button";
    retake.textContent = "Retake quiz";
    retake.addEventListener("click", resetQuiz);

    quizResults.append(heading, scoreElement, resultSummary, recommendationTitle);
    if (typeof recommendations === "string") {
      const recommendationText = document.createElement("div");
      recommendationText.className = "recommendation-list";
      recommendationText.innerHTML = recommendations;
      quizResults.append(recommendationText);
    } else {
      quizResults.append(recommendations);
    }
    quizResults.append(retake);
    renderAssessment(score, incorrect, percentage, summary);
  }

  function renderAssessment(correct, incorrect, percentage, summary) {
    assessmentContent.replaceChildren();
    const layout = document.createElement("div");
    layout.className = "assessment-ready";
    const circle = document.createElement("div");
    circle.className = "score-circle";
    const scoreValue = document.createElement("strong");
    scoreValue.textContent = `${percentage}%`;
    const scoreLabel = document.createElement("span");
    scoreLabel.textContent = `${correct} of ${quizQuestions.length} correct`;
    circle.append(scoreValue, scoreLabel);

    const details = document.createElement("div");
    details.className = "assessment-details";
    const heading = document.createElement("h3");
    heading.textContent = "Your learning assessment";
    const result = document.createElement("p");
    result.textContent = `${correct} correct · ${incorrect} incorrect. ${summary}`;
    const recommendationHeading = document.createElement("p");
    recommendationHeading.innerHTML = "<strong>Topics to review:</strong>";
    const recommendations = recommendationsMarkup();
    details.append(heading, result, recommendationHeading);
    if (typeof recommendations === "string") {
      const recommendationText = document.createElement("p");
      recommendationText.textContent = "None needed—keep practicing your safe habits.";
      details.append(recommendationText);
    } else {
      details.append(recommendations.cloneNode(true));
    }
    const restart = document.createElement("button");
    restart.className = "button button-secondary";
    restart.type = "button";
    restart.textContent = "Restart training";
    restart.addEventListener("click", () => {
      resetQuiz();
      window.location.hash = "home";
    });
    details.append(restart);
    layout.append(circle, details);
    assessmentContent.append(layout);
  }

  function resetQuiz() {
    questionIndex = 0;
    score = 0;
    answered = false;
    missedTopics.clear();
    quizContent.hidden = false;
    quizResults.hidden = true;
    assessmentContent.innerHTML = '<div class="assessment-pending"><span class="assessment-icon" aria-hidden="true">◎</span><h3>Your results will appear here</h3><p>Complete all 10 quiz questions to unlock your final assessment.</p><a class="button button-secondary" href="#quiz">Go to the quiz</a></div>';
    renderQuestion();
    updatePageProgress();
  }

  nextButton.addEventListener("click", () => {
    if (questionIndex === quizQuestions.length - 1) {
      showResults();
      return;
    }
    questionIndex += 1;
    renderQuestion();
  });

  renderQuestion();
})();

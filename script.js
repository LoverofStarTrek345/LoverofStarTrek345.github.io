const questions = [
  {
    category: "Mystery message",
    icon: "✉",
    title: "A delivery text says your package is stuck. It wants you to tap a link and pay a small fee.",
    detail: "You weren't expecting the message, but it looks pretty convincing.",
    choices: [
      "Tap the link quickly so your package isn't returned.",
      "Don't tap. Check delivery details using the carrier's official app or website.",
      "Reply and ask the sender to prove they're real."
    ],
    answer: 1,
    explanation: "Good call to pause. Unexpected messages that create urgency can be scams. Use a website or app you already trust instead of the message link."
  },
  {
    category: "App permissions",
    icon: "📍",
    title: "A flashlight app asks to use your location, contacts, and microphone.",
    detail: "The app needs to work, but those permissions don't seem related.",
    choices: [
      "Allow everything. The app probably knows what it needs.",
      "Deny unrelated permissions, and look for another app if it won't work without them.",
      "Allow it now and remember to check again someday."
    ],
    answer: 1,
    explanation: "Exactly. Apps should only get access they need for the features you use. You can review or change permissions in your device settings."
  },
  {
    category: "Account security",
    icon: "🔑",
    title: "You make a new account and want a password you'll remember.",
    detail: "You already use your pet's name plus your birth year on a few sites.",
    choices: [
      "Reuse that password. Familiar is easier to remember.",
      "Use a unique, longer password or passphrase; a password manager can help.",
      "Use the same password but add an exclamation point."
    ],
    answer: 1,
    explanation: "Nice move. If one site is breached, a unique password helps protect your other accounts. A password manager can generate and remember them for you."
  },
  {
    category: "Public Wi-Fi",
    icon: "☕",
    title: "At a cafe, two networks have almost the same name. One asks you to sign in to connect.",
    detail: "You're about to check your account balance.",
    choices: [
      "Pick whichever network has the strongest signal.",
      "Ask staff which network is theirs, and avoid sensitive activity on a network you can't verify.",
      "Use either one—public Wi-Fi is always safe if it has a password."
    ],
    answer: 1,
    explanation: "Smart thinking. Check the network name with staff before joining. For sensitive tasks, your mobile data or a trusted connection is a safer choice."
  },
  {
    category: "Sharing online",
    icon: "📸",
    title: "You want to post a photo from a fun day out. It shows your house number and that you're away from home.",
    detail: "You love the photo, but didn't notice those details at first.",
    choices: [
      "Post it right away—only friends can see your profile.",
      "Crop or edit out identifying details, and think about who can see the post.",
      "Add your location so everyone knows where the fun happened."
    ],
    answer: 1,
    explanation: "Great catch. Before posting, check for details you didn't mean to share and review your audience. You can enjoy sharing while choosing what stays private."
  }
];

const content = document.querySelector("#game-content");
const scoreLabel = document.querySelector("#score-label");
const roundLabel = document.querySelector("#round-label");
const progressFill = document.querySelector("#progress-fill");
const progressLabel = document.querySelector("#progress-label");
let currentQuestion = 0;
let score = 0;
let answered = false;
let gameStarted = false;

function updateProgress() {
  const position = gameStarted ? currentQuestion + 1 : 0;
  progressFill.style.width = `${(position / questions.length) * 100}%`;
  progressLabel.textContent = `${position} / ${questions.length}`;
  scoreLabel.textContent = `${score} ${score === 1 ? "point" : "points"}`;
  roundLabel.textContent = gameStarted ? `SCENARIO ${position} OF ${questions.length}` : "READY WHEN YOU ARE";
}

function startGame() {
  currentQuestion = 0;
  score = 0;
  answered = false;
  gameStarted = true;
  showQuestion();
}

function showQuestion() {
  answered = false;
  updateProgress();
  const question = questions[currentQuestion];
  content.innerHTML = `
    <div class="scenario">
      <div class="scenario-category"><span aria-hidden="true">${question.icon}</span> ${question.category}</div>
      <h3>${question.title}</h3>
      <p>${question.detail}</p>
      <div class="answers" role="group" aria-label="Choose your response">
        ${question.choices.map((choice, index) => `<button class="answer-button" type="button" data-choice="${index}">${choice}</button>`).join("")}
      </div>
      <div id="feedback-slot"></div>
    </div>`;
  content.querySelectorAll(".answer-button").forEach(button => {
    button.addEventListener("click", () => chooseAnswer(Number(button.dataset.choice)));
  });
  content.querySelector(".answer-button").focus({ preventScroll: true });
}

function chooseAnswer(choice) {
  if (answered) return;
  answered = true;
  const question = questions[currentQuestion];
  const correct = choice === question.answer;
  if (correct) score += 1;
  scoreLabel.textContent = `${score} ${score === 1 ? "point" : "points"}`;

  content.querySelectorAll(".answer-button").forEach((button, index) => {
    button.disabled = true;
    if (index === question.answer) button.classList.add("is-correct", ...(correct ? [] : ["is-answer"]));
    else if (index === choice) button.classList.add("is-incorrect");
  });

  const feedback = correct
    ? `<strong>That's the safer move!</strong> ${question.explanation}`
    : `<strong>Not quite—and that's okay.</strong> ${question.explanation}`;
  const nextLabel = currentQuestion === questions.length - 1 ? "See my results" : "Next scenario";
  document.querySelector("#feedback-slot").innerHTML = `
    <div class="feedback">
      <p>${feedback}</p>
      <button class="next-button" type="button">${nextLabel} <span aria-hidden="true">→</span></button>
    </div>`;
  content.querySelector(".next-button").addEventListener("click", nextQuestion);
  content.querySelector(".next-button").focus({ preventScroll: true });
}

function nextQuestion() {
  currentQuestion += 1;
  if (currentQuestion === questions.length) {
    showResults();
    return;
  }
  showQuestion();
}

function showResults() {
  progressFill.style.width = "100%";
  progressLabel.textContent = `${questions.length} / ${questions.length}`;
  roundLabel.textContent = "QUEST COMPLETE";
  scoreLabel.textContent = `${score} ${score === 1 ? "point" : "points"}`;
  let title = "A thoughtful start!";
  let message = "You know the basics—and now you have a few more moves to protect your privacy. Keep pausing, checking, and choosing what feels right.";
  if (score >= 4) {
    title = "Privacy pro moves!";
    message = "You made some seriously thoughtful choices. Keep that curious, careful mindset as you explore your digital world.";
  } else if (score >= 2) {
    title = "Look at you, leveling up!";
    message = "You're building strong digital instincts. Remember: pause, check, and choose what you share.";
  }
  content.innerHTML = `
    <div class="result">
      <div class="result-badge" aria-hidden="true">${score >= 4 ? "★" : "✦"}</div>
      <h3>${title}</h3>
      <p>You earned <strong>${score} out of ${questions.length} points</strong>. ${message}</p>
      <button class="primary-button" id="restart-button" type="button">Play again <span aria-hidden="true">↻</span></button>
    </div>`;
  content.querySelector("#restart-button").addEventListener("click", startGame);
  content.querySelector("#restart-button").focus({ preventScroll: true });
}

document.querySelector("#start-button").addEventListener("click", startGame);
updateProgress();

const courtCases = [
  {
    topic: "The data docket",
    icon: "📄",
    title: "A company has collected information about your account. You want to know what it holds.",
    detail: "Your client asks: “Can I demand a copy of every piece of data right now?”",
    choices: [
      "Yes. Every person everywhere has an absolute right to every record.",
      "Privacy laws in some places let people request access to personal data, with limits and exceptions.",
      "No. Companies never have to explain how they use personal data."
    ],
    answer: 1,
    ruling: "The court finds: it depends on where you live and the data involved. Some privacy laws give people rights to access, correct, or sometimes delete personal data, but there can be exceptions. Check the organization’s privacy notice and your local privacy regulator for the rules that apply."
  },
  {
    topic: "Permission hearing",
    icon: "📱",
    title: "A game app wants your precise location even when you're not playing.",
    detail: "Your client asks: “Do I have to hand it over to keep using my phone?”",
    choices: [
      "Yes. Installing an app means agreeing to every permission forever.",
      "You can often deny or change a device permission; some features may stop working.",
      "No app can ever collect location data, so there is nothing to check."
    ],
    answer: 1,
    ruling: "The court finds: you can usually review app permissions in your device settings and turn off access you don’t want. Available controls and legal protections differ by device and location. If an app’s request seems unrelated to its purpose, consider another app."
  },
  {
    topic: "Online safety case",
    icon: "🛡️",
    title: "Someone is posting your private details and sending threatening messages.",
    detail: "Your client wants it to stop, but isn't sure what to do first.",
    choices: [
      "Post their private details too, so they learn a lesson.",
      "Save evidence safely, report and block the account, and tell a trusted person; seek urgent local help if in immediate danger.",
      "Ignore every threat—online behavior can never affect real-world safety."
    ],
    answer: 1,
    ruling: "The court finds: prioritize safety, don’t retaliate, and use the platform’s reporting and blocking tools. Keep evidence if it’s safe to do so and ask a trusted adult or support service for help. If someone is in immediate danger, contact local emergency services. Platform processes and legal options vary."
  }
];

const courtContent = document.querySelector("#court-content");
const courtScoreLabel = document.querySelector("#court-score-label");
const courtRoundLabel = document.querySelector("#court-round-label");
const courtProgressFill = document.querySelector("#court-progress-fill");
const courtProgressLabel = document.querySelector("#court-progress-label");
let currentCourtCase = 0;
let courtScore = 0;
let courtCaseAnswered = false;
let courtGameStarted = false;

function updateCourtProgress() {
  const progress = courtGameStarted ? Math.min(currentCourtCase + 1, courtCases.length) : 0;
  courtProgressFill.style.width = `${(progress / courtCases.length) * 100}%`;
  courtProgressLabel.textContent = `${progress} / ${courtCases.length}`;
  courtScoreLabel.textContent = `${courtScore} / ${courtCases.length} calls`;
  courtRoundLabel.textContent = courtGameStarted ? `CASE ${progress} OF ${courtCases.length}` : "COURT IS IN SESSION";
}

function startCourtGame() {
  currentCourtCase = 0;
  courtScore = 0;
  courtCaseAnswered = false;
  courtGameStarted = true;
  showCourtCase();
}

function showCourtCase() {
  courtCaseAnswered = false;
  updateCourtProgress();
  const courtCase = courtCases[currentCourtCase];
  courtContent.innerHTML = `
    <div class="court-scenario">
      <div class="court-topic"><span aria-hidden="true">${courtCase.icon}</span> ${courtCase.topic}</div>
      <h3>${courtCase.title}</h3>
      <p>${courtCase.detail}</p>
      <div class="court-choices" role="group" aria-label="Choose your legal argument">
        ${courtCase.choices.map((choice, index) => `<button class="court-choice" type="button" data-court-choice="${index}">${choice}</button>`).join("")}
      </div>
      <div id="court-ruling-slot"></div>
    </div>`;
  courtContent.querySelectorAll(".court-choice").forEach(button => {
    button.addEventListener("click", () => chooseCourtAnswer(Number(button.dataset.courtChoice)));
  });
  courtContent.querySelector(".court-choice").focus({ preventScroll: true });
}

function chooseCourtAnswer(choice) {
  if (courtCaseAnswered) return;
  courtCaseAnswered = true;
  const courtCase = courtCases[currentCourtCase];
  const correct = choice === courtCase.answer;
  if (correct) courtScore += 1;
  courtScoreLabel.textContent = `${courtScore} / ${courtCases.length} calls`;

  courtContent.querySelectorAll(".court-choice").forEach((button, index) => {
    button.disabled = true;
    if (index === courtCase.answer) button.classList.add("is-correct", ...(correct ? [] : ["is-answer"]));
    else if (index === choice) button.classList.add("is-incorrect");
  });

  const verdict = correct ? "A sound argument!" : "The judge has a note for you.";
  const nextLabel = currentCourtCase === courtCases.length - 1 ? "Hear the verdict" : "Next case";
  document.querySelector("#court-ruling-slot").innerHTML = `
    <div class="court-ruling">
      <p><strong>${verdict}</strong> ${courtCase.ruling}</p>
      <button class="court-next" type="button">${nextLabel} <span aria-hidden="true">→</span></button>
    </div>`;
  courtContent.querySelector(".court-next").addEventListener("click", nextCourtCase);
  courtContent.querySelector(".court-next").focus({ preventScroll: true });
}

function nextCourtCase() {
  currentCourtCase += 1;
  if (currentCourtCase === courtCases.length) {
    showCourtVerdict();
    return;
  }
  showCourtCase();
}

function showCourtVerdict() {
  courtProgressFill.style.width = "100%";
  courtProgressLabel.textContent = `${courtCases.length} / ${courtCases.length}`;
  courtRoundLabel.textContent = "VERDICT DELIVERED";
  courtScoreLabel.textContent = `${courtScore} / ${courtCases.length} calls`;
  const headline = courtScore === courtCases.length ? "The jury is on a roll!" : "Court adjourned—keep learning!";
  courtContent.innerHTML = `
    <div class="court-result">
      <div class="court-result-badge" aria-hidden="true">⚖</div>
      <h3>${headline}</h3>
      <p>You made ${courtScore} out of ${courtCases.length} strong calls. Remember: privacy rights depend on local laws, and this mini-game is a starting point—not legal advice.</p>
      <button class="primary-button" id="court-restart-button" type="button">Hear the cases again <span aria-hidden="true">↻</span></button>
    </div>`;
  courtContent.querySelector("#court-restart-button").addEventListener("click", startCourtGame);
  courtContent.querySelector("#court-restart-button").focus({ preventScroll: true });
}

document.querySelector("#court-start-button").addEventListener("click", startCourtGame);
updateCourtProgress();

const dispatchSection = document.querySelector("#privacy-dispatch");
document.querySelector(".tips-section").after(dispatchSection);

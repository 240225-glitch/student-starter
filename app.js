// LESSON 2 STARTER: JavaScript connects the form to the page.
const INTERESTS = [
  "technology", "engineering", "problem-solving", "games", "art", "design",
  "photography", "music", "performance", "culture", "storytelling",
  "sports", "fitness", "teamwork", "nature", "service", "science",
  "leadership", "debate", "languages"
];

const form = document.querySelector("#matcherForm");
const grid = document.querySelector("#interestGrid");
const message = document.querySelector("#formMessage");
const results = document.querySelector("#results");
const resultTitle = document.querySelector("#resultTitle");
const resultSummary = document.querySelector("#resultSummary");
const resultCards = document.querySelector("#resultCards");
const grade = document.querySelector("#grade");
const gradeGroup = document.querySelector("#gradeGroup");

// 1) Build interest checkboxes from the list above.
for (const interest of INTERESTS) {
  const label = document.createElement("label");
  label.className = "interest";
  label.innerHTML = `<input type="checkbox" name="interests" value="${interest}"> ${interest}`;
  grid.append(label);
}

// 2) Keep the grade group sensible when the grade changes.
grade.addEventListener("change", () => {
  gradeGroup.value = Number(grade.value) <= 8 ? "Middle School" : "High School";
});

// 3) When students click submit, collect the form data.
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  message.textContent = "";

  const data = new FormData(form);
  const interests = data.getAll("interests");

  if (interests.length < 2) {
    message.textContent = "Choose at least two interests.";
    return;
  }

  const profile = {
    name: String(data.get("name")).trim(),
    grade: Number(data.get("grade")),
    grade_group: String(data.get("gradeGroup")),
    house: String(data.get("house")),
    day: String(data.get("day")),
    style: String(data.get("style")),
    interests: interests
  };

  console.log(profile);

  // Send the profile to matcher.py and wait for Python's answer.
  const response = await fetch("/api/match", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile)
  });

  const result = await response.json();
  showResults(result);
});

function showResults(result) {
  resultTitle.textContent = `${result.profile.name}, here are your top matches`;
  resultSummary.textContent = `Python checked ${result.checked_clubs} clubs and returned the best three.`;

  resultCards.replaceChildren();

  if (!result.matches || result.matches.length === 0) {
    resultCards.append(buildCard("No matches found.", "Try choosing different interests or a different club day."));
    results.hidden = false;
    return;
  }

  for (const club of result.matches) {
    const title = club.symbol ? `${club.symbol} ${club.name}` : club.name;
    resultCards.append(buildCard(title, club.description, `${club.score} match points`, club.reasons));
  }

  results.hidden = false;
}

function buildCard(name, description, score, reasons) {
  const card = document.createElement("article");
  card.className = "result-card";

  const scoreEl = document.createElement("p");
  scoreEl.className = "score";
  scoreEl.textContent = score;
  card.append(scoreEl);

  const nameEl = document.createElement("h3");
  nameEl.textContent = name;
  card.append(nameEl);

  const descEl = document.createElement("p");
  descEl.textContent = description;
  card.append(descEl);

  if (reasons && reasons.length) {
    const list = document.createElement("ul");
    for (const reason of reasons) {
      const item = document.createElement("li");
      item.textContent = reason;
      list.append(item);
    }
    card.append(list);
  }

  return card;
}

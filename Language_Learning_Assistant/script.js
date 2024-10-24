// script.js
const words = [
    { word: "Bonjour", translation: "Hello" },
    { word: "Merci", translation: "Thank you" },
    { word: "S'il vous plaît", translation: "Please" },
    { word: "Excusez-moi", translation: "Excuse me" },
    { word: "Oui", translation: "Yes" },
    { word: "Non", translation: "No" }
];

let currentWordIndex = 0;

function showWord() {
    const wordElement = document.getElementById("word");
    const translationElement = document.getElementById("translation");
    const word = words[currentWordIndex];

    wordElement.textContent = word.word;
    translationElement.textContent = word.translation;
}

function showQuiz() {
    const quizSection = document.getElementById("quiz-section");
    const quizQuestion = document.getElementById("quiz-question");
    const word = words[currentWordIndex];

    quizSection.style.display = "block";
    quizQuestion.textContent = `What is the translation of "${word.word}"?`;
}

document.getElementById("next-word").addEventListener("click", () => {
    currentWordIndex = (currentWordIndex + 1) % words.length;
    showWord();
    document.getElementById("quiz-section").style.display = "none";
});

document.getElementById("submit-answer").addEventListener("click", () => {
    const quizAnswer = document.getElementById("quiz-answer").value;
    const feedback = document.getElementById("quiz-feedback");
    const word = words[currentWordIndex];

    if (quizAnswer.trim().toLowerCase() === word.translation.toLowerCase()) {
        feedback.textContent = "Correct! Well done.";
    } else {
        feedback.textContent = `Incorrect. The correct answer is "${word.translation}".`;
    }

    document.getElementById("quiz-answer").value = ""; // Clear input
});

document.addEventListener("DOMContentLoaded", showWord);

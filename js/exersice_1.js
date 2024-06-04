// Declaring variables
const agent = ['jett','reyna','braimstone']
let students = ["het", "harsh", "anish", "rutvik", "swarup"];
let scores = [85, 92, 78, 90, 88];

// ------------ for each loop--------------
agent.forEach((item,index)=>{
    console.log(`${index} : ${item}`)
})

// --------------for loop-----------------
for (let i = 0; i < students.length; i++) {
    console.log(`Student: ${students[i]}, Score: ${scores[i]}`);
}

// ----------- while loop-----------------------
let totalScore = 0;
let index = 0;
while (index < scores.length) {
    totalScore += scores[index];
    index++;
}
let averageScore = totalScore / scores.length;
console.log(`Average Score: ${averageScore}`);

// ------------finding total with the help of reduce method-----------
totalScore = scores.reduce((total, score) => total + score, 0);
console.log(`Total Score: ${totalScore}`);

// ------------finding highest score---------------------
let highestScore = scores.reduce((max, score) => (score > max ? score : max), scores[0]);
console.log(`Highest Score: ${highestScore}`);

// -------------sorting scores in descending order------------------
let sortedScoresDescending = [...scores].sort((a, b) => b - a);
console.log(`Sorted Scores (Descending): ${sortedScoresDescending}`);

// -------------sorting scores in ascending order------------------
let sortedScoresAscending = [...scores].sort((a, b) => a - b);
console.log(`Sorted Scores (Ascending) order : ${sortedScoresAscending}`);

// ------------finding above average student with the help of filter method--------------
let aboveAverageStudents = students.filter((student, index) => scores[index] > averageScore);
console.log(`Students who scored above average: ${aboveAverageStudents.join(", ")}`);

// ------------finding below average student with the help of filter method------------
let belowAverageStudents = students.filter((student, index) => scores[index] < averageScore);
console.log(`Students who scored below average: ${belowAverageStudents.join(", ")}`);

// ----------------map method example--------------------
let studentObjects = students.map((student, index) => ({
    name: student,
    score: scores[index]
}));
console.log('Student Objects:', studentObjects);

// -----------------splice method example--------------------
let removedStudent = students.splice(2, 1); // Removing anish
let removedScore = scores.splice(2, 1);     // Removing anish's score
console.log(`Removed Student: ${removedStudent}, Removed Score: ${removedScore}`);
console.log('Updated Students:', students);
console.log('Updated Scores:', scores);

// -------------------indexof method example------------------
let indexOfBob = students.indexOf("Bob");
console.log(`Index of Bob: ${indexOfBob}`);

// --------------------slice method example---------------------
let firstThreeScores = scores.slice(0, 3);
console.log('First Three Scores:', firstThreeScores);

// ---------------------concat method example-----------------------
let newStudents = ["abdul", "baburao"];
let newScores = [93, 81];
students = students.concat(newStudents);
scores = scores.concat(newScores);
console.log('All Students:', students);
console.log('All Scores:', scores);

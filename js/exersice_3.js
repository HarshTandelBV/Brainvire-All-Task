//--------we can define date object in 5 ways-----------


//------1st way---------
let todayDate = new Date()
console.log(todayDate)

//------2nd way----------
let todayDate1 = new Date('2003-05-09T11:12:13Z');
console.log(todayDate1);

//------3rd way----------
let todayDate2 = new Date(2003, 4, 9, 11, 12, 13, 0);
console.log(todayDate2);

//------4th way----------
let todayDate3 = new Date(1052438400000);
console.log(todayDate3);

//------5th way---------
let todayDate4 = new Date(Date.UTC(2003, 4, 9, 11, 12, 13));
console.log(todayDate4);



//--------Getter methods----------
console.log("Date: ", todayDate1.getDate()); 
console.log("Day: ", todayDate1.getDay()); 
console.log("Month: ", todayDate1.getMonth()); 
console.log("Year: ", todayDate1.getFullYear()); 
console.log("Hours: ", todayDate1.getHours()); 
console.log("Minutes: ", todayDate1.getMinutes()); 
console.log("Seconds: ", todayDate1.getSeconds()); 
console.log("Milliseconds: ", todayDate1.getMilliseconds()); 

//--------Setter methods------------
todayDate1.setDate(9); 
todayDate1.setFullYear(2025); 
todayDate1.setMonth(5); 
todayDate1.setHours(12); 
todayDate1.setMinutes(13); 
todayDate1.setSeconds(14); 
todayDate1.setMilliseconds(500);


console.log("Date: ", todayDate1.getDate()); 
console.log("Day: ", todayDate1.getDay()); 
console.log("Month: ", todayDate1.getMonth()); 
console.log("Year: ", todayDate1.getFullYear()); 
console.log("Hours: ", todayDate1.getHours()); 
console.log("Minutes: ", todayDate1.getMinutes()); 
console.log("Seconds: ", todayDate1.getSeconds()); 
console.log("Milliseconds: ", todayDate1.getMilliseconds()); 

// implemented error handling concept in hr_expense_button.js file in patch code

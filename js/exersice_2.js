// ----Make a JavaScript Class "A", along with this,------- 
// ----inherit this into a new class called Class "B"------

class sageAgent {
    constructor() {
        this.name = 'Sage';
        this.country = 'Mexico';
    }

    ability() {
        return `Sage is better than Reyna`;
    }
}
console.log(typeof sageAgent)
class reynaAgent extends sageAgent {
    constructor() {
        super(); // Call the parent constructor first
        this.name = 'Reyna';
    }

    ability2() {
        return `${super.ability()} but ${this.name} has better abilities`;
    }
}

const obj = new reynaAgent();
console.log(obj.ability2());

// --------prototype concept------------

function Agent(name){
    this.name = name;
}

Agent.prototype.welcome = function(){
    return `Hello ${this.name}, Welcome to riot games`
}

let agent1 = new Agent('harsh')

console.log(agent1.welcome())

//----------2nd example------------

let a = {
    run:() => {
        alert("you're better")
    }
}

let b = {
    run:() => {
        alert("you're more better")
    },

    exp:() => {
        alert('here is the example of _proto_')
    }
}

a.__proto__ = b
a.run()
a.exp()


// dynamic nature of object

function Rectangle(len,bre) {
    this.length = len;
    this.breath = bre;

    this.draw = function(){
        console.log('-----Draw------');
    }
};

let obj1 = new Rectangle(10,20);

obj1.color = 'red';
console.log(obj1);

delete obj1.color;
console.log(obj1);

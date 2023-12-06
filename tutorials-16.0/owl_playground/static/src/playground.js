/** @odoo-module **/ //Don't forget in all .js files.s
 
// import { Component, useState } from "@odoo/owl"; // Here we are adding the useState hook (React.js). //Also this line we are importing from Counter.js file. 
import { Counter } from "./counter/counter"; // Here we are importing the Counter.js file to here. 
// import { Todo } from "./todo/todo"; // Here we are importing the Todo.js file to here to be able to use it.
import { TodoList } from "./todo_list/todo_list" //Here we are importing everything from the todolist file, so we do not need the todo. 
import { Component } from "@odoo/owl"; 

export class Playground extends Component {
    static template = "owl_playground.playground";

    static components = { Counter, TodoList }; // Here we are calling the counter.js file (that contains all the code below. ) and the TodoList (which will make the code of TodoList run).

    // setup(){
    //     this.state = useState({ value: 1 }); //Here we are defining the state value to begin = 1.
    // }

    // increment(){
    //     this.state.value++; // Here we are making the increment declaration where we will activate it through XML file. 
    //     // Another way to do it:
    //         //this.state.value = this.state.value + 1; Where it takes the value and add always one. 
    // }

    //Because we are importing the whole functionality from the TodoList we do not need these code anymore.
    // setup() {
    //     this.todo = { id: 3, description: "buy milk", done: false };
    // }

}

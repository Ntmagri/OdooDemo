/** @odoo-module **/

import { Todo } from "../todo/todo"; //Here we are calling the todo, where there is the props validation for the list.
import { Component, useState } from "@odoo/owl"; // Imported the useState so we are able to do the todo list dynamically.
import { useAutofocus } from "../utils";

export class TodoList extends Component {
    setup(){
        // this.todoList = [ //Here is where we defined the foreach in the .xml file.
        //     {id:3, description: "buy milk", done: false},
        //     {id:4, description: "buy eggs", done: true},
        //     {id:5, description: "buy avocado", done: true},
        // ];
        this.nextId = 0;
        this.todoList = useState([]);
        useAutofocus("todoListInput"); //Here is calling the utils.js useAutoFocus function.
    }

    // Now we will modify it for adding a todo, where it will be dinamically modified the list, where the user will be able to add a todo.
    // With that we wont need to have the hard-coded above.
    addTodo(ev){
        if (ev.keyCode === 13 && ev.target.value != ""){
            this.todoList.push({id: this.nextId++, description: ev.target.value, done: false}); //The nextId++ it's to have an unique id. 
            ev.target.value = "";
        }
    }

}



TodoList.components = { Todo }; // Here is to connect the list to be declared in the xml file. 
TodoList.template = "owl_playground.TodoList"; // Here is to use as the template in the xml file, to connect this .js file to that .xml file.


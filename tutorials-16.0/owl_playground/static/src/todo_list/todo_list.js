/** @odoo-module **/

import { Todo } from "../todo/todo"; //Here we are calling the todo, where there is the props validation for the list.
import { Component } from "@odoo/owl";

export class TodoList extends Component {
    setup(){
        this.todoList = [ //Here is where we defined the foreach in the .xml file.
            {id:3, description: "buy milk", done: false},
            {id:4, description: "buy eggs", done: true},
            {id:5, description: "buy avocado", done: true},
        ];
    }
}

TodoList.components = { Todo }; // Here is to connect the list to be declared in the xml file. 
TodoList.template = "owl_playground.TodoList"; // Here is to use as the template in the xml file, to connect this .js file to that .xml file.

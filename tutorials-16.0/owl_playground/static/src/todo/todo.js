/** @odoo-module **/

import { Component } from "@odoo/owl"; 

export class Todo extends Component {
    onClick(ev) {
        this.props.toggleState(this.props.id);
    }

    onRemove() {
        this.props.removeTodo(this.props.id);
    }

}

Todo.template = "owl_playground.Todo"; // This is how we will connect with the playground.js file.

// Here we are preveting errors, so an invalid data will not make impact to our application or functionality.
Todo.props = {
    id: {type: Number},
    description: {type: String},
    done: {type: Boolean},
    toggleState: {type: Function},
    removeTodo: {type: Function}
};

    
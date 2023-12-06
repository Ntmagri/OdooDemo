/** @odoo-module **/ //Don't forget in all .js files.

import { Component, useState } from "@odoo/owl"; // Here we are adding the useState hook (React.js).

export class Counter extends Component {
    setup(){
        this.state = useState({ value: 1 });
    }

    increment(){
        this.state.value = this.state.value + 1;
    }
}


Counter.template = "owl_playground.Counter"; // This is what we are going to use to import to playground.js file.
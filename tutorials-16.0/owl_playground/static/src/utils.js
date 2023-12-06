/** @odoo-module **/

import { onMounted, useRef } from "@odoo/owl"

export function useAutofocus(name){
    const ref = useRef(name); // Here is if the component is mounted, refs are active
    onMounted(() => ref.el && ref.el.focus()); // Here we are using the ref above and Ref.el is the input HTMLElement
    //The actual HTMLElement is accessed with the el key. 
}


//MAKE SURE TO CHECK HOW IS DECLARED THE NAMES AND ETC HERE, IN THE TODO_LIST.JS AND .XML, TO UNDERSTAND BETTER THE RELATION BETWEEN THEM.


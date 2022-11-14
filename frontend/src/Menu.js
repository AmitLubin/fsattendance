import { Component } from "react";
import "./css/Menu.css"
import Searches from "./Searches";
import Category from "./Category";

class Menu extends Component {
    state = { Categories: "*" }

    constructor(){
        super();
    }

    render(){
        return(
            <div className="topnav">
                <div className="menu-item leftmost">
                    <Category />
                </div>
                <div className="menu-item left-push">
                    <Searches />
                </div>
            </div> 
        );
    }
}

export default Menu;
import { Component } from "react";
import "./css/Menu.css"

class Menu extends Component {
    
    render(){
        return(
            <div class="topnav">
            <a href="#home">Home</a>
            <a href="#news">News</a>
            <a href="#contact">Contact</a>
            <a href="#about">About</a>
            </div> 
        );
    } 
}

export default Menu;
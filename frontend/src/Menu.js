import { Component } from "react";
import "./css/Menu.css"
import Category from "./Category";
import Searches from "./Searches";
import SearchType from "./SearchType"

const Menu = () => {
    return(
        <div className="topnav">
            <div className="menu-item leftmost">
                <Category />
            </div>
            <div className="menu-item left-push padding-top">
                <input type="checkbox" className="checkbox-dynamic"/>
            </div>
            <div className="menu-item left-push" >
                <p className="dynamic-search-label">Dynamic Search</p>
            </div>
            <div className="menu-item left-push">
                <SearchType />
            </div>
            <div className="menu-item left-push">
                <Searches />
            </div>
        </div> 
    );
}

export default Menu;
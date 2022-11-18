import React from "react";
import "./css/Menu.css";
import Category from "./Category";
import SearchType from "./SearchType";
import Searches from "./Searches";
import SpecificSearches from "./SpecificSearches";



class Menu extends React.Component { 
    state = { searchBy: "Search by:" };

    constructor(props) {
        super(props);
    }

    stateUpdater = (e) => {
        this.setState({ searchBy: "Search by: " + e.currentTarget.innerHTML });
    }

    render(){
        return(
            <div className="topnav">
                <div className="menu-item leftmost">
                    <Category />
                </div>
                <div className="menu-item left-push">
                    <Searches changeState={this.props.changeState}/>
                </div>
                <div className="menu-item left-push-bigger padding-top">
                    <input type="checkbox" id="dynamic-checkbox" className="checkbox-dynamic"/>
                </div>
                <div className="menu-item left-push" >
                    <p className="dynamic-search-label">Dynamic Search</p>
                </div>
                <div className="menu-item left-push">
                    <SearchType searchByUpdater={this.stateUpdater} searchByState={this.state.searchBy}/>
                </div>
                <div className="menu-item left-push">
                    <SpecificSearches changeState={this.props.changeState} searchByState={this.state.searchBy}/>
                </div>
                <div className="rightmost">

                </div>
            </div> 
        );
    }
}

export default Menu;
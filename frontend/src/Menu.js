import React from "react";
import "./css/Menu.css";
import Category from "./Category";
import SearchType from "./SearchType";
import Searches from "./Searches";
import SpecificSearches from "./SpecificSearches";
import Average from "./Average";
import Update from "./Update";
import Delete from "./Delete";


class Menu extends React.Component { 
    state = { searchBy: "Search by:", action: false };

    constructor(props) {
        super(props);
    }

    stateUpdater = (e) => {
        this.setState({ searchBy: "Search by: " + e.currentTarget.innerHTML });
    }

    actionOnUpdater = () => {
        this.setState({ action: true });
    }

    actionOffUpdater = () => {
        this.setState({ action: false });
    }

    render(){
        return(
            <div className="topnav">
                <div className="menu-item leftmost left-push">
                    <Category />
                </div>
                <div className="menu-item left-push">
                    <Searches changeState={this.props.changeState} action={this.state.action} />
                </div>
                <div className="menu-item left-push">
                    <div className="checkbox-dynamic">
                        <input type="checkbox" id="dynamic-checkbox" className="checkbox-dynamic"/>
                    </div>
                    <div className="dynamic-search" >
                        <p className="dynamic-search-label">Dynamic Search</p>
                    </div>
                </div>
                
                <div className="menu-item left-push">
                    <SearchType searchByUpdater={this.stateUpdater} searchByState={this.state.searchBy}/>
                </div>
                <div className="menu-item left-push-massive">
                    <SpecificSearches changeState={this.props.changeState} searchByState={this.state.searchBy} action={this.state.action}/>
                </div>
                <div className="menu-item">
                    <Average changeAvgState={this.props.changeAvgState} action={this.state.action} />
                </div>


                <div className="right-menu-item right-push">
                    <Update action={this.state.action} actionOn={this.actionOnUpdater} actionOff={this.actionOffUpdater}/>
                </div>
                <div className="right-menu-item">
                    <Delete action={this.state.action} actionOn={this.actionOnUpdater} actionOff={this.actionOffUpdater}/>
                </div>
            </div> 
        );
    }
}

export default Menu;
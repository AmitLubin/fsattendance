import { Component } from "react";
import "./css/SearchType.css"

function dropDownEventLoader(e) {
    const p = e.currentTarget.parentNode;
    if (p.classList.contains('visible'))
        p.classList.remove('visible');
    else
        p.classList.add('visible');      
};

class SearchType extends Component {
    stateUpdater = (e) => {
        this.setState({ searchBy: "Search by: " + e.currentTarget.innerHTML })
    }
    
    state = { searchBy: "Search by:" }

    constructor() {
        super();
    }

    render(){
        return(
            <div id="dropdown-type">
                <span className="anchor" onClick={dropDownEventLoader} >{this.state.searchBy}</span>
                <ul className="items">
                    <li><label id="type-email" onClick={this.stateUpdater}>Student email</label></li>
                    <li><label id="type-email" onClick={this.stateUpdater}>Student name</label></li>
                </ul>
            </div>
        );
    }
}

export default SearchType;
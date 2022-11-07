import { Component } from "react";
import './css/App.css'
import Table from "./Table"

class App extends Component {
    state = { data: [] };
    
    constructor(){
        super();
    }

    async componentDidMount(){
        let tempArray = [];
        await fetch('http://localhost:5000/')
            .then(res => res.json())
            .then(newData => {
                tempArray = tempArray.concat(newData);
            });
        this.setState({ data: tempArray });
    }
    
        
    
    render() {
        return(
            <div className="background">
                <div className="menu">
                    <h1>Menu</h1>
                </div>
                <div className="list">
                    <div className="table">
                        <table id="table">
                            <thead id="thead">
                                <tr>
                                    <th className="cell">Room name</th>
                                    <th className="cell">Room start time</th>
                                    <th className="cell">Room end time</th>
                                    <th className="nameCell">Student name</th>
                                    <th className="mailCell">Student mail</th>
                                    <th className="cell">Student attendance time stamps</th>
                                    <th className="cell">Student overall attendance time (mins)</th>
                                    <th className="cell">Student platform</th>
                                </tr>
                            </thead>
                            <tbody id="tbody">
                                <Table queries={this.state.data}/>
                            </tbody>
                        </table>  
                    </div>
                </div>
            </div>
        );
    }
    
}

export default App;
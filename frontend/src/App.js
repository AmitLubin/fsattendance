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
                    
                </div>
                <div className="list">
                    <div className="table">
                        <Table queries={this.state.data}/>
                    </div>
                </div>
            </div>
        );
    }
    
}

export default App;
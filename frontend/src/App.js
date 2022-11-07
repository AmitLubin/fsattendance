import { Component } from "react";
import './css/App.css'

class App extends Component {
    constructor(){
        super();
    }

    componentDidMount(){
        fetch('http://localhost:5000/')
            .then(res => res.json())
            .then(newData => console.log(newData));
    }
    
        
    
    render() {
        return(
            <div className="background">
                <div className="menu">
                    
                </div>
                <div className="list">
                    
                </div>
            </div>
        );
    }
    
}

export default App;
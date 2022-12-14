import { Component } from "react";
import "./css/UpdateAndDelete.css";

const sleep = ms => new Promise((resolve, reject) => {
    setTimeout(resolve, ms);
})

class Delete extends Component {
    state = { icon: "Press to delete" }

    constructor(){
        super();
    }

    deleteDatabase = async e => {
        this.setState({ icon: "waiting" });

        const requestOptions = { method: 'DELETE' };
        await fetch(process.env.REACT_APP_PUBLIC_IP, requestOptions)
            .then(response => response.json())
            .then(data => this.setState({ icon: data.results }));
        
        await sleep(1400);

        this.setState({ icon: "Click to delete database" });
    }
    
    render(){
        return(
            <button className="post-button" onClick={this.deleteDatabase}>{this.state.icon}</button>
        );
    }
}
    
export default Delete;
import React from "react";
import './css/App.css'

const App = () => {
    let data = {};
    fetch('http://localhost:5000/')
        .then(res => res.json())
        .then(newData => console.log(newData));
        
    //console.log(data);
    
    return(
        <div className="background">
            <div className="menu">
                
            </div>
            <div className="list">
                
            </div>
        </div>
    );
}

export default App;
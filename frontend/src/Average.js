import React from "react";
import "./css/Searches.css";

const Average = props => {
    async function getAverage(e) {
        await fetch(process.env.REACT_APP_PUBLIC_IP)
                .then(res => res.json())
                .then(newData => {
                    props.changeAvgState(newData);
        });
    }

    return(
        <div>
            <button type="submit" className="search-avg-button" onClick={getAverage}>Search Avg % <i className="fa fa-search"></i></button>
        </div>
    );
}

export default Average;
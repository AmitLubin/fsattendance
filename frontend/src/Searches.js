import React from "react";
import "./css/Searches.css"

const Searches = () => {
    return (
        <div className="search">
            <form method="get">
                <input type="text" name="search-bar" placeholder="Search by mail or name" className="input-height" />
                <button type="submit" className="button"><i className="fa fa-search"></i></button>
            </form>
        </div>
    );
}

export default Searches;
import React from "react";
import "./css/Searches.css"

function getAllCategories(){
    const categories = {
        
    }
}

function searchSpecific(e){

}

const Searches = () => {
    return (
        <div className="search-specific">
            <form method="get">
                <input type="text" name="search-bar" placeholder="Search by specific category" className="specific-bar input-height" />
                <button type="submit" className="button"><i className="fa fa-search"></i></button>
            </form>
        </div>
    );
}

export default Searches;
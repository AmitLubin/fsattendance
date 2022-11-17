import React from "react";
import "./css/Searches.css"

function getAllCategories(){
    const categories = {
        all: document.getElementById('check-all').checked,
        specific: {
            roomName: document.getElementById('check-room-name').checked,
            roomStart: document.getElementById('check-room-start').checked,
            roomFinish: document.getElementById('check-room-end').checked,
            studentName: document.getElementById('check-student-name').checked,
            studentMail: document.getElementById('check-student-mail').checked,
            studentTime: document.getElementById('check-student-time').checked,
            studentOverall: document.getElementById('check-student-overall').checked,
            studentPlatform: document.getElementById('check-student-platform').checked
        }
    };

    return categories;
}

const Searches = props => {
    function search(e){
        const categories = getAllCategories();
        if (categories.all == true) {

        } else {
            
        }
    }

    return (
        <div className="search-specific">
            <input type="text" name="search-bar" placeholder="Search by specific category" className="specific-bar input-height" />
            <button type="submit" className="button" onClick={search}><i className="fa fa-search"></i></button>
        </div>
    );
}

export default Searches;
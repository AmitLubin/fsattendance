import React from "react";
import "./css/Category.css"

const Category = () => {
    
    return (
        <div id="ddcbl" className="dropdown-check-list">
            <span className="anchor">Select categories:</span>
            <ul className="items">
                <li><input type="checkbox" id="check-all" />All</li>
                <li><input type="checkbox" id="check-room-name" />Room name</li>
                <li><input type="checkbox" id="check-room-start" />Room start time</li>
                <li><input type="checkbox" id="check-room-end" />Room end time</li>
                <li><input type="checkbox" id="check-student-name" />Student name</li>
                <li><input type="checkbox" id="check-student-mail" />Student mail</li>
                <li><input type="checkbox" id="check-student-time" />Student attendnace time stamps</li>
                <li><input type="checkbox" id="check-student-overall" />Student overall attendance time</li>
                <li><input type="checkbox" id="check-student-platform" />Student platform</li>
            </ul>
        </div>
    );
    
}

export default Category;
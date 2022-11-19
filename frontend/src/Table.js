import React from "react";
import TableHeader from "./TableHeader";
import TableBody from "./TableBody";
import "./css/Table.css";

function checkCategories(categoriesChecker){
    let categories = [];
    
    if (categoriesChecker.roomName)
        categories.push("Room name");
    if (categoriesChecker.roomStart)
        categories.push("Room start time");
    if (categoriesChecker.roomFinish)
        categories.push("Room end time");
    if (categoriesChecker.studentName)
        categories.push("Student name");
    if (categoriesChecker.studentMail)
        categories.push("Student mail");
    if (categoriesChecker.studentTimeIntervals)
        categories.push("Student attendance time");
    if (categoriesChecker.studentOverallTime)
        categories.push("Student overall attendance");
    if (categoriesChecker.studentPlatform)
        categories.push("Student platform");
    
    return categories;
}

function setTableWidth(categories){
    let width = 40;
    categories.map(category => {
        if (category == "Student mail")
            width += 400;
        else
            width += 160;
    });

    console.log(width.toString() + "px");

    document.getElementById('d-table').style.width = (width+2).toString() + "px";
    document.getElementById('table-header-row').style.width = width.toString() + "px";
    document.getElementById('table-body').style.width = (width+2).toString() + "px";
}

const Table = props => {
    if (props.data.length === 0) return;

    const categories = checkCategories(props.categories);
    if (categories.length === 0) return;

    setTableWidth(categories);

    return (
        <div id="table">
            <table id="d-table">
                <thead id="table-header-row">
                    <tr >
                        <TableHeader categories={categories} />
                    </tr>
                </thead>
                <tbody id="table-body">
                    <TableBody categories={categories} data={props.data} />
                </tbody>
            </table>
        </div>
        
    );
}

export default Table;
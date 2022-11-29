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
    if (categoriesChecker.average)
        categories.push("Average");
    
    return categories;
}

/*function setTableWidth(categories, header){
    let width = 0;
    categories.map(category => {
        if (category === "Student mail")
            width += 30;
        else
            width += 10;
    });

    if (header) return {
        width: (width).toString() + "%"
    };
    return {
        width: (width+2).toString() + "%"
    };
}*/

const Table = props => {
    if (props.error == true) {
        console.log(props.data)
        return;
    }
    if (props.data.length === 0) return;

    const categories = checkCategories(props.categories);
    if (categories.length === 0) return;

    return (
        <table id="d-table">
            <thead id="table-header-row" >
                <tr>
                    <TableHeader categories={categories} data={props.data} changeSortedState={props.changeSortedState}/>
                </tr>
            </thead>
            <tbody id="table-body" >
                <TableBody categories={categories} data={props.data} />
            </tbody>
        </table>
    );
}


//style={setTableWidth(categories, true)}
export default Table;
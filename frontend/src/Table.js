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

function setTableWidth(categories, header){
    let width = 0;
    categories.map(category => {
        if (category === "Student mail")
            width += 25;
        else
            width += 10;
    });

    if (header) return {
        width: (width).toString() + "vw"
    };
    return {
        width: (width+0.9).toString() + "vw"
    };
}

const Table = props => {
    if (typeof props.data === 'string') {
        console.log(props.data);
        return;
    }
    if (props.data.length === 0) return;

    const categories = checkCategories(props.categories);
    if (categories.length === 0) return;

    return (
        <div id="table">
            <table id="d-table" tyle={setTableWidth(categories, true)}>
                <thead id="table-header-row" style={setTableWidth(categories, true)}>
                    <tr>
                        <TableHeader categories={categories} data={props.data} changeSortedState={props.changeSortedState}/>
                    </tr>
                </thead>
                <tbody id="table-body" style={setTableWidth(categories, false)}>
                    <TableBody categories={categories} data={props.data} />
                </tbody>
            </table>
        </div>
        
    );
}

export default Table;
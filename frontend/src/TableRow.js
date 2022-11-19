import React from "react";
import "./css/TableCell.css";

const TableRow = props => {
    return props.data.map((data, index) => {
        if (props.categories[index] === "Student mail"){
            return(
                <td className="table-cell table-regular mail-cell">{data}</td>
            );
        } else {
            return(
                <td className="table-cell table-regular reg-cell">{data}</td>
            );
        }
    });
}

export default TableRow;
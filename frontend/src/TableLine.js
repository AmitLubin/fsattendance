import React from "react";
import './css/App.css'

const TableLine = props => {
    return(
        <tr>
            <td className="cell">{props.data[0]}</td>
            <td className="cell">{props.data[1]}</td>
            <td className="cell">{props.data[2]}</td>
            <td className="cell">{props.data[3]}</td>
            <td className="mailCell">{props.data[4]}</td>
            <td className="cell">{props.data[5]}</td>
            <td className="cell">{props.data[6]} mins</td>
            <td className="cell">{props.data[7]}</td>
        </tr>
    );
}

export default TableLine;
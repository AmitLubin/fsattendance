import React from "react";
import TableLine from './TableLine';

const Table = props => {
    return props.queries.map((line, index) => {
        return (
            <TableLine data={line} key={index}/>
        );
    });
}

export default Table;
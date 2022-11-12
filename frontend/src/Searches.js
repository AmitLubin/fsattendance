import React from "react";

const Searches = () => {
    return (
        <div>
            <form method="get">
                <input type="text" name="nameOrMail" placeholder="Search by mail or name"/>
                <button type="submit"><i className="fa fa-search"></i></button>
            </form>
        </div>
    );
}

export default Searches;